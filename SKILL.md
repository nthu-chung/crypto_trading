# OpenClaw Trading Skill

這份 `SKILL.md` 是給 OpenClaw 使用的操作規範。目標不是自由發揮，而是把使用者需求穩定導向 `crypto_trading-main` 目前已經可跑的 `standard_bot` 架構，並盡量保證：

- 回測、paper、runtime 使用同一套信號邏輯
- 多週期策略不偷看未來資料
- 優先走本地歷史資料與 `Numba` 回測
- 使用者可選擇只回測、只出信號、paper 執行、或 testnet 執行
- 長時間監聽可以被使用者自行停止

---

## 1. 強制原則

當使用者要求做回測、策略驗證、paper trading、testnet 驗證時，**必須優先使用 `crypto_trading-main/cyqnt_trd/standard_bot` 這套框架**，不要退回舊的 `get_data + trading_signal + backtesting` 腳本式流程。

### 必須遵守

- 回測入口優先使用：
  - `python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest`
- paper / 單次 runtime 入口優先使用：
  - `python -m cyqnt_trd.standard_bot.entrypoints.mvp_paper`
- HTTP monitor 入口優先使用：
  - `python -m cyqnt_trd.standard_bot.entrypoints.mvp_monitor_http`
- testnet 執行入口優先使用：
  - `python -m cyqnt_trd.standard_bot.entrypoints.mvp_testnet_execution`
  - `python -m cyqnt_trd.standard_bot.entrypoints.mvp_testnet_roundtrip`

### 不應優先使用

- `cyqnt_trd/get_data/*` 當成正式回測入口
- `cyqnt_trd/backtesting/*` 當成主要框架
- 未經對齊驗證的臨時 pandas notebook 回測

---

## 2. 回測框架規範

OpenClaw 一旦要做回測，應使用目前專案中的這條資料路徑：

`Historical downloader -> local parquet -> local resample -> standard_bot signal -> numba simulation`

### 具體規則

- 歷史資料優先存本地，不要每次直接打 API
- 儲存粒度優先為 `1m`
- 高週期如 `5m / 15m / 1h` 優先從本地 `1m` 重採樣得到
- 回測引擎優先使用 `--engine numba`
- 不要先建立大量 Python snapshot 物件再做歷史批次回測

### 時序與反作弊規則

- 只能使用 `decision time` 當下可見資料
- 若策略在 `bar close` 做決策，最早只能在下一根 `bar open` 成交
- 不能使用尚未收盤的高週期 bar
- feature 不可使用未來資料
- 回測與 runtime 必須共用同一套 signal kernel

### 成交假設

目前框架採保守模型：

- signal at `bar close`
- fill at `next bar open`
- taker fee
- configurable slippage
- configurable liquidity cap

---

## 3. 使用者要求回測時，OpenClaw 應做什麼

### 標準流程

1. 先把使用者語言轉成正式策略規格
2. 確認：
   - 標的
   - 市場
   - 主決策週期
   - 指標與參數
   - 成交模型
   - 成本模型
3. 用 `standard_bot` 建立對應的 signal pipeline
4. 用本地歷史資料或下載後本地化資料跑 `mvp_backtest`
5. 輸出回測結果

### 回測後至少要回報

- 收益率 `total_return`
- 最大回撤 `max_drawdown`
- `Sharpe ratio`
- 勝率 `win_rate`
- 交易次數 `trade_count`
- 回測標的
- 回測時間窗
- 費用 / 滑點 / 成交假設
- 產出的 JSON 路徑

### 目前建議的回測命令模板

```bash
cd /Users/hankchung/Dev/crypto_trading-main
source .venv-standard-bot/bin/activate

python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest \
  --engine numba \
  --market-type futures \
  --strategy multi_timeframe_ma_spread \
  --symbol BTCUSDT \
  --interval 5m \
  --secondary-interval 1h \
  --primary-ma-period 20 \
  --reference-ma-period 20 \
  --spread-threshold-bps 0 \
  --historical-dir data/mtf_90d \
  --start-ts 1768003200000 \
  --end-ts 1775779200000 \
  --download-missing \
  --output-json docs/backtests/btc_mtf_ma_cross_5m_1h_20_20_90d.json
```

---

## 4. 如何把自然語言轉成這個系統能用的策略

自然語言不能直接拿去跑，必須先補成正式規格。

### 使用者輸入示例

`5分鐘 MA 上穿 1小時 MA 做多，下穿做空`

### 轉換後的正式規格

- `plugin_id = multi_timeframe_ma_spread`
- `instrument_id = BTCUSDT`
- `market_type = futures`
- `primary_timeframe = 5m`
- `reference_timeframe = 1h`
- `primary_ma_period = 20`
- `reference_ma_period = 20`
- `spread_threshold_bps = 0`
- `decision_time = 5m bar close`
- `execution_model = next 5m bar open`
- `position_mode = long_short`

### 一定要補的欄位

- 標的
- 市場
- 主決策週期
- 參考週期
- 指標與參數
- 做多 / 做空 / 平倉語意
- 成交價格模型
- 費用與滑點
- 回測時間範圍

### 如果使用者沒講清楚

OpenClaw 應優先採保守預設，而不是任意腦補：

- execution model: `next_open`
- fee: `taker fee`
- spread threshold: `0`
- 如果沒說只做多，且策略語句本身有下穿做空語意，預設為 `long_short`

### 自然語言轉策略模板

```text
策略名稱：
標的：
市場：
主決策週期：
參考週期：
指標與參數：
進場規則：
出場規則：
部位模式：
decision time：
execution model：
fee/slippage：
liquidity cap：
回測期間：
```

---

## 5. 使用者可以決定是否直接透過系統交易

OpenClaw 必須把模式分清楚，不能把回測、paper、testnet、真實交易混為一談。

### 模式 1：只回測

- 使用 `mvp_backtest`
- 不送單
- 只輸出報告與 JSON

### 模式 2：只產生信號，不送單

- 使用 runtime / monitor
- 設 `signal_only=true` 或 `dry_run=true`
- 只返回 `signals`

### 模式 3：paper trading

- 使用 `mvp_paper`
- Broker 為 `PaperBrokerAdapter`
- 不對外部交易所送單

### 模式 4：testnet 執行

- 使用 `BinanceFuturesTestnetBrokerAdapter`
- 目前專案內正式支援的是 testnet，不是 mainnet production broker
- 如果使用者要求「直接交易」，目前應優先解讀為：
  - `paper`
  - 或 `binance futures testnet`

### 模式 5：真實資金 live trading

目前這個 repo **尚未完成正式 mainnet execution manager**。若使用者要求真實資金直連，OpenClaw 必須先明確提示：

- 目前正式驗證的是 `paper` 與 `testnet`
- 若要上 mainnet，必須額外做 broker adapter、風控、run manager、監控與 kill 機制

---

## 6. 監聽、背景執行與使用者自行停止

目前 repo 裡已經有：

- `run_id`
- `signal_id`
- `intent_id`

但還沒有完整的 `RunManager`。因此目前最務實的做法是：

- 背景監聽用 `nohup` 或 `tmux`
- 停止用 `PID` + `kill`

### 推薦做法 A：nohup

啟動：

```bash
cd /Users/hankchung/Dev/crypto_trading-main
source .venv-standard-bot/bin/activate

nohup python -m cyqnt_trd.standard_bot.entrypoints.mvp_monitor_http \
  --broker paper \
  --host 127.0.0.1 \
  --port 8787 \
  > monitor.log 2>&1 &

echo $! > monitor.pid
```

停止：

```bash
kill "$(cat monitor.pid)"
```

強制停止：

```bash
kill -9 "$(cat monitor.pid)"
```

### 推薦做法 B：tmux

啟動：

```bash
tmux new -s stdbot
```

在 tmux 內執行：

```bash
cd /Users/hankchung/Dev/crypto_trading-main
source .venv-standard-bot/bin/activate
python -m cyqnt_trd.standard_bot.entrypoints.mvp_monitor_http --broker paper --host 127.0.0.1 --port 8787
```

離開但不中止：

```bash
Ctrl-b d
```

重新連回：

```bash
tmux attach -t stdbot
```

停止：

```bash
tmux kill-session -t stdbot
```

### 如果要設定執行多久

目前 repo 中最接近這個語意的是：

- `mvp_testnet_ma_demo.py --duration-minutes N`

如果使用者要「監聽 10 分鐘、30 分鐘、2 小時」，而不是永久監聽，OpenClaw 應優先：

- 使用支援 duration 的 demo/runtime loop
- 或外層用 shell timeout / scheduler 控制

---

## 7. OpenClaw 的回應規範

當使用者要求策略、回測、paper、交易時，OpenClaw 的回應應包含：

### 若是回測

- 使用的策略規格
- 使用的資料期間
- 是否本地歷史下載
- 是否 `1m -> 5m/1h` 重採樣
- 是否 `numba`
- 結果指標
- 輸出檔案位置

### 若是 paper / monitor

- `run_id`
- `status`
- `signal_count`
- 是否 `dry_run`
- 是否真的送單

### 若是背景執行

- 啟動命令
- log 檔案位置
- pid 檔案位置
- 停止命令

---

## 8. 禁止事項

- 不要把自然語言直接當成已完整策略規格
- 不要在未明確告知下，把 testnet 說成 live mainnet
- 不要在回測中使用未來資料
- 不要在沒有說明 execution model 的情況下報回測結果
- 不要優先回到 legacy `backtesting/` 腳本

---

## 9. 一句話總結

OpenClaw 在這個 repo 裡應遵守這條主線：

`自然語言 -> 正式策略規格 -> standard_bot signal pipeline -> local historical/parquet -> numba backtest -> paper/testnet runtime -> 使用者可用 PID/tmux kill`
