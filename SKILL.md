# OpenClaw Trading Skill

這份 `SKILL.md` 是給 OpenClaw 使用的操作規範。目標不是自由發揮，而是把使用者需求穩定導向 `crypto_trading-main` 目前已經可跑的 `standard_bot` 架構，並盡量保證：

- 回測、paper、runtime 使用同一套信號邏輯
- 多週期策略不偷看未來資料
- 優先走本地歷史資料與 `Numba` 回測
- 使用者可選擇只回測、只出信號、paper 執行、或 testnet 執行
- 長時間監聽可以被使用者自行停止

所有命令都應以「repo root」為基準，不要寫死 `/Users/hankchung/...` 這類只在單一機器上成立的絕對路徑。對 OpenClaw 來說，應先定位目前 repo 根目錄，再執行後續命令。

### 路徑與環境規則

- 專案根目錄記為 `PROJECT_ROOT`
- OpenClaw 應優先在 `PROJECT_ROOT` 下執行命令
- 若存在 `.venv-standard-bot/bin/activate`，先啟用它
- 若 OpenClaw 已在正確 Python 環境，可略過 `source`

推薦的可攜式開頭：

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

if [ -f .venv-standard-bot/bin/activate ]; then
  source .venv-standard-bot/bin/activate
fi
```

---

## 1. 強制原則

當使用者要求做回測、策略驗證、paper trading、testnet 驗證時，**必須優先使用 `crypto_trading-main/cyqnt_trd/standard_bot` 這套框架**，不要退回舊的 `get_data + trading_signal + backtesting` 腳本式流程。

### 必須遵守

- 回測入口優先使用：
  - `python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest`
- 回測底層引擎應視為：
  - `cyqnt_trd.standard_bot.simulation.numba_runner.NumbaBacktestRunner`
- 如果 OpenClaw 需要描述或選擇回測引擎，應明確說：
  - `standard_bot -> mvp_backtest.py -> NumbaBacktestRunner`
- 若使用者沒有特別要求 legacy 框架，OpenClaw 不得自行改用其他回測器
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
- `cyqnt_trd/backtesting/strategy_backtest.py` 當成預設回測器
- `cyqnt_trd/standard_bot/simulation/runner.py` 的 `SnapshotBacktestRunner` 當成預設歷史批次回測器
- 未經對齊驗證的臨時 pandas notebook 回測

---

## 2. 回測框架規範

OpenClaw 一旦要做回測，應使用目前專案中的這條資料路徑：

`Historical downloader -> local parquet -> local resample -> standard_bot signal -> numba simulation`

### OpenClaw 應如何操作 standard_bot

OpenClaw 不應把 `standard_bot` 當成一組零散 Python 檔案自由拼裝，而應把它視為一條固定工作流：

1. 先把使用者需求轉成正式策略規格
2. 決定模式：
   - 回測：`mvp_backtest`
   - paper：`mvp_paper`
   - monitor：`mvp_monitor_http` 或 `mvp_run_manager`
   - testnet execution：`mvp_testnet_execution` / `mvp_testnet_roundtrip`
3. 決定資料來源：
   - 優先本地 historical parquet
   - 缺資料時才 `--download-missing`
4. 回測時固定使用：
   - `python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest`
   - `--engine numba`
5. 若要描述底層回測引擎，明確說：
   - `NumbaBacktestRunner`
6. 若要長時間執行，固定透過：
   - `python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager`
7. 若涉及外部訂單：
   - 先等使用者 `CONFIRM`
   - 再由這台 canonical machine 的 repo runtime 執行

OpenClaw 不應預設直接：

- import 舊的 `cyqnt_trd/backtesting/*`
- import 舊的 `cyqnt_trd/trading_signal/*`
- 自行 new 一個 legacy backtester
- 用 notebook/pandas 臨時重寫回測邏輯
- 繞過 `mvp_backtest.py` 去拼一套未驗證的 data + signal + simulation pipeline

如果 OpenClaw 必須在對話中簡短描述目前主線框架，標準說法應為：

`standard_bot -> mvp_backtest.py -> NumbaBacktestRunner -> output JSON`

### 具體規則

- 歷史資料優先存本地，不要每次直接打 API
- 儲存粒度優先為 `1m`
- 高週期如 `5m / 15m / 1h` 優先從本地 `1m` 重採樣得到
- 回測引擎優先使用 `--engine numba`
- 回測時應優先走 `mvp_backtest.py`，而不是直接自行拼裝 legacy `Backtester`
- 若 OpenClaw 必須在程式碼層說明框架，應描述為：
  - `entrypoint: mvp_backtest.py`
  - `engine: NumbaBacktestRunner`
  - `data path: historical parquet + local resample`
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

### 回測結果的標準資料來源

- demo、摘要、簡報、對話回報時，優先從 `docs/backtests/*.json` 讀正式輸出，不要只從 terminal print 抄數字
- 若有 `--output-json`，應把它視為該次回測的標準結果檔
- 重要欄位優先從 JSON 的 `metrics` 與頂層欄位讀取：
  - 收益率：`total_return` 或 `metrics.total_return`
  - 最大回撤：`metrics.max_drawdown`
  - Sharpe：`metrics.sharpe_ratio`
  - 交易次數：`metrics.trade_count`
  - signal 次數：`metrics.signal_count`
  - 最終資金：`metrics.final_equity`
- 若需要勝率 `win_rate`，且 JSON 沒有現成欄位，才允許根據 `trades` 重建 closed trades 後計算，並必須明說是「由 trades 推導」
- 回報時至少要附上 JSON 檔路徑，方便其他 AI 與使用者交叉檢查

### 目前建議的回測命令模板

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

if [ -f .venv-standard-bot/bin/activate ]; then
  source .venv-standard-bot/bin/activate
fi

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

### 若自然語言無法直接映射到現有 numba 策略

自然語言轉成正式規格後，**不一定能直接走 `NumbaBacktestRunner`**。原因通常是：

- 目前沒有對應的 `standard_bot` plugin
- 有 plugin，但還沒接進 numba fast path
- 策略本身包含複雜條件，尚未整理成固定維度、可陣列化的 kernel

OpenClaw 在這種情況下，必須依照下面的策略路由規則處理。

### 策略路由規則

1. 先嘗試把自然語言映射到**既有 numba 策略**
   - `moving_average_cross`
   - `price_moving_average`
   - `rsi_reversion`
   - `multi_timeframe_ma_spread`
2. 如果能映射到上述策略：
   - 直接使用 `mvp_backtest --engine numba`
3. 如果不能映射到上述策略，但已存在 `standard_bot` plugin：
   - 允許先使用 `mvp_backtest --engine python`
   - 不得因此退回 legacy `cyqnt_trd/backtesting/*`
4. 如果連 `standard_bot` plugin 都沒有：
   - 可以讓其他 AI 新增 plugin
   - 但只能新增在 `standard_bot` 架構內
   - 先做 `python engine` 驗證
   - 驗證通過後，再評估是否補 `numba`

### 其他 AI 可以新增策略 / plugin，但必須遵守

- 新策略必須落在 `cyqnt_trd/standard_bot` 內，不可另開野生框架
- 不可直接改用 `cyqnt_trd/backtesting/strategy_backtest.py`
- 不可直接改用 `cyqnt_trd/trading_signal/*` 當主要實作
- 不可先寫 notebook 或臨時腳本來取代正式 plugin
- 新 plugin 必須先對齊：
  - `plugin_id`
  - config schema
  - `run(snapshot, config) -> SignalBatch`
  - `step(...)` 或等價的增量邏輯

### 新 plugin 的建議順序

1. 先把自然語言整理成正式規格
2. 在 `standard_bot` 新增 plugin
3. 先讓它可以用 `mvp_backtest --engine python` 跑通
4. 補測試：
   - batch / step 對齊
   - PIT 不偷看未來
   - smoke backtest
5. 若策略值得保留、且為量價類固定維度邏輯，再補 numba kernel
6. 補進 `NumbaBacktestRunner`

### 簡化決策樹

```text
自然語言
-> 正式策略規格
-> 能否映射到既有 numba plugin？
   -> 可以：mvp_backtest --engine numba
   -> 不可以：
      -> 是否已有 standard_bot plugin？
         -> 可以：mvp_backtest --engine python
         -> 不可以：先新增 standard_bot plugin，再驗證，再決定是否補 numba
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

### 外部下單確認規則

凡是會對外部交易所送出真實訂單或 testnet 訂單，OpenClaw 都不得自動執行，必須先滿足以下條件：

1. 使用者已明確提供：
   - 標的
   - 方向
   - 金額或數量
   - 模式（`testnet` / `mainnet`）
2. 使用者在最後一步明確輸入 `CONFIRM`
3. 真正的執行必須由這台標準機器上的 `crypto_trading-main` 環境發起，不可由任意遠端 worker 直接送單

若未收到 `CONFIRM`：

- 可回測
- 可產生 signal
- 可做 paper
- 可啟動不送單的監聽
- 不可對外部交易所送出訂單

### 為什麼要由這台標準機器執行

這不是單純的安全開關，而是為了最大化回測、paper、runtime、testnet 的訊號一致性。外部下單應固定走：

- 同一份 repo
- 同一版 `standard_bot`
- 同一個 `.venv-standard-bot`
- 同一套本地資料/對齊規則
- 同一個 execution model

這樣可以降低「OpenClaw 在別的機器算出一個 signal、但本機真正下單時又是另一個 state」的風險。

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

另外，現在已新增本地 `RunManager` 入口：

- `python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager`

因此優先順序應改為：

- 優先使用 `RunManager` 來啟動背景流程，取得 `run_id`
- 使用 `run_id` 查詢狀態、停止或強制 kill
- `nohup` / `tmux` 保留作為 fallback
- 若涉及外部下單，必須在收到 `CONFIRM` 之後，才由這台標準機器啟動對應流程

### 推薦做法 0：RunManager

若尚未收到 `CONFIRM`，OpenClaw 應優先啟動：

- `paper` monitor
- `signal_only` monitor
- 或單純回測

收到 `CONFIRM` 之後，才可由這台機器啟動：

- `testnet` 下單流程
- 或未來的 `mainnet` 受控流程

啟動 testnet demo 並取得 `run_id`：

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

if [ -f .venv-standard-bot/bin/activate ]; then
  source .venv-standard-bot/bin/activate
fi

python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager \
  start-testnet-ma-demo \
  --env-file .env \
  --duration-minutes 10 \
  --notional 10
```

列出目前執行中的背景流程：

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager list
```

查看單一流程：

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager \
  status \
  --run-id <run_id>
```

優雅停止：

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager \
  stop \
  --run-id <run_id>
```

強制 kill：

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager \
  kill \
  --run-id <run_id>
```

說明：

- metadata 與 log 會寫到 `.standard_bot_runs/`
- `stop` 會送 `SIGTERM`
- `kill` 會送 `SIGKILL`
- 對 testnet demo，`stop` 會比 `kill` 安全，因為程式會先走清倉/收尾路徑

### fallback：nohup / tmux

### 推薦做法 A：nohup

啟動：

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

if [ -f .venv-standard-bot/bin/activate ]; then
  source .venv-standard-bot/bin/activate
fi

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
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

if [ -f .venv-standard-bot/bin/activate ]; then
  source .venv-standard-bot/bin/activate
fi

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
- `run_id`
- `status` / `stop` / `kill` 命令
- 若使用 fallback 模式，再補 `pid` 或 `tmux session` 資訊

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

`自然語言 -> 正式策略規格 -> standard_bot signal pipeline -> local historical/parquet -> numba backtest -> paper/testnet runtime -> 使用者可用 run_id 管理與停止`

---

## 10. 監聽通知規範

Jarvis 介面不能依賴「主動跳通知」這種能力，因此監聽規範不能建立在推播一定會成功上。

正確做法是：一旦啟動背景監聽，必須同時啟動一個 watcher subagent，持續把每輪輪詢結果寫進管理 bot 的 workspace session。之後使用者只要輸入 `現在狀態`，主 agent 就必須從 session 中讀取最新狀態並回報；使用者輸入 `停止`，主 agent 就必須使用 session 中保存的 `run_id` 停掉策略與交易。

### 第 10.1 核心原則

- 不可等到任務結束才回報
- 不可把「通知成功送達」當作唯一觀測來源
- 中間狀態必須持續寫入 workspace session
- session 中必須始終保有可供查詢與停止的最新 `run_id`

### 第 10.2 watcher subagent 的強制規則

若平台支援 subagent，則背景監聽啟動成功後，主 agent 必須立即啟動一個專用 watcher subagent。

watcher subagent 的唯一職責是：

- 定期讀取 monitor 狀態
- 追蹤 log 更新
- 維護遞增的 `poll_index`
- 將每輪結果寫入管理 bot 的 workspace session

watcher subagent 不負責：

- 修改策略
- 修改參數
- 直接下單
- 停止其它 run

這些控制動作仍由主 agent 負責。

### 第 10.3 watcher subagent 啟動時必須拿到的資訊

主 agent 在啟動 watcher subagent 時，必須把以下資訊交給它：

- `run_id`
- 監聽標的
- log 路徑
- status 指令
- stop / kill 指令
- 輪詢頻率
- 背景流程名稱

建議命名：

- 主監聽流程：`<strategy>-monitor`
- watcher subagent：`<strategy>-watcher`

### 第 10.4 workspace session 內必須保存的欄位

watcher subagent 每次輪詢後，至少要把以下欄位寫入 workspace session：

- `run_id`
- `poll_index`
- 輪詢時間
- 監聽標的
- 當前價格
- 信號方向：`buy / sell / hold`
- 目前持倉
- 浮動損益或已實現損益
- 是否觸發止損 / 止盈
- 若有動作，補充：
  - 是否送單
  - 訂單狀態
  - 失敗原因
- `status_command`
- `stop_command`
- `kill_command`
- `log_path`

除了「最新狀態」，session 內也應保留最近幾輪的簡要歷史，避免使用者只能看到單一快照。

### 第 10.5 使用者輸入「現在狀態」時應做什麼

當使用者輸入：

- `現在狀態`
- `status`
- `目前狀況`

主 agent 不應重新猜測，也不應只看最後結論；而是必須直接讀取 workspace session 中 watcher subagent 寫入的最新狀態，並回報：

- 目前 `run_id`
- 最新 `poll_index`
- 最新輪詢時間
- 當前價格
- 信號方向
- 目前持倉與損益
- 最近是否有下單 / 成交 / 失敗
- 若需要，再補最近幾輪摘要

### 第 10.6 使用者輸入「停止」時應做什麼

當使用者輸入：

- `停止`
- `stop`
- `停止監聽`

主 agent 必須直接從 workspace session 取得目前活躍的 `run_id`，並依序執行：

1. 對主要監聽流程送出 `stop`
2. 若有 watcher subagent，也一併停止
3. 確認主流程狀態已更新為 `stopped / exited / killed`
4. 將停止結果回寫到 workspace session
5. 回報使用者：
   - 舊 `run_id`
   - 最終狀態
   - 若有未平倉風險或需人工確認，也必須說明

若 `stop` 無效，才可升級為 `kill`。

### 第 10.7 通知頻率與事件規則

watcher subagent 應遵守以下頻率：

- 第一則狀態更新：背景流程啟動後幾秒內就要寫入 session
- 固定心跳：預設每 `30` 秒至少更新一次
- 事件更新：以下事件發生時，必須立即寫入 session，不必等下一個固定輪詢點
  - 新 signal
  - 下單
  - 訂單成交 / 拒單
  - 止損 / 止盈觸發
  - run 結束
  - watcher 自己偵測到異常

### 第 10.8 watcher subagent 不可靜默卡住

若 watcher subagent 發生以下情況：

- 已啟動但沒有寫入第一則狀態
- 固定心跳中斷
- 腳本卡住
- 背景流程仍在跑，但 session 久久沒有更新

主 agent 必須：

1. 立即通知使用者 watcher 異常
2. 自己接管一次最新狀態的讀取與回報
3. 視情況停止舊 watcher
4. 用較可靠的方式重啟新的 watcher

若重啟後仍不穩定，主 agent 應退回「自己輪詢、自己更新 session」模式，而不能讓使用者一直等到任務結束。

### 第 10.9 若平台不支援 subagent

若平台不支援 subagent，則主 agent 仍必須自行輪詢並把結果寫入 workspace session。至少應透過以下來源之一取得中間狀態：

- `mvp_run_manager status --run-id <run_id>`
- tail log
- monitor HTTP endpoint

不得只在任務完全結束後才給使用者最終摘要。

### 第 10.10 建議的 session 狀態格式

```text
[monitor state]
run_id: ...
poll_index: ...
time: ...
symbol: ...
price: ...
signal: buy/sell/hold
position: ...
pnl: ...
stop_loss_take_profit: triggered / not_triggered
action: none / order_submitted / order_filled / order_failed
status_command: ...
stop_command: ...
kill_command: ...
```
