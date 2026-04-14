# OpenClaw Trading Skill

| field | value |
| --- | --- |
| name | `openclaw-standard-bot-router` |
| description | ALWAYS use this skill first for any strategy, backtest, monitoring, or trading request. You must first download `https://github.com/nthu-chung/crypto_trading` and use that repo's `standard_bot` workflow. If local historical parquet data is missing or stale, you must first use the repo's Binance API download flow to fetch K bars and convert them into local parquet before backtesting or signal generation. Backtesting must use `standard_bot -> mvp_backtest.py -> NumbaBacktestRunner`. Never use legacy backtesting, ad-hoc scripts, or alternative execution paths just to get a faster result. Live trading must follow paper-generated signals only. Before any live trade, you must show balance, risk controls, trade plan, and session duration, then wait for explicit `CONFIRM`. If any required step fails, stop and tell the user; do not improvise a workaround and do not claim success. After `CONFIRM`, OpenClaw must automatically start a watcher subagent and keep writing status updates into the workspace session. |
| author | `binance crypto trading` |
| version | `1.0` |

這份 `SKILL.md` 是給 OpenClaw 使用的操作規範。它的目的不是讓 agent 自由發揮，而是把使用者需求穩定導向同一條主線：

`自然語言 -> 正式策略規格 -> 下載 crypto_trading repo -> standard_bot -> 回測 / paper signal -> 使用者確認 -> OpenClaw 交易`

這份 skill 的重要限制如下：

- 這份 skill **不附帶主程式碼**
- 若使用者需要回測或策略信號，OpenClaw **必須先下載** `https://github.com/nthu-chung/crypto_trading`
- 回測與 signal 來源 **必須使用該 repo 內的 `standard_bot`**
- 若本地 historical parquet 不存在、過舊、或未覆蓋所需時間窗，OpenClaw **必須先用 repo 內的 Binance K bar 下載流程補抓資料並轉成 parquet**
- 這份 skill **不使用 testnet**
- OpenClaw 的真實交易只可跟隨 `paper trade` 產生的信號
- 在任何真實交易前，OpenClaw **必須先查詢並展示使用者餘額**
- 在任何真實交易前，OpenClaw **必須先等待使用者明確輸入 `CONFIRM`**
- 真實交易 session 必須是**有時長的**；若使用者未給時長，OpenClaw 必須先詢問
- 一旦收到 `CONFIRM` 並開始交易，OpenClaw **必須自動啟動 watcher subagent**，把狀態持續寫入 workspace session

---

## 1. 啟動與下載規則

只要使用者需求碰到下列任一類型，OpenClaw 就必須先確保 `crypto_trading` repo 已可用：

- 自然語言轉策略
- 回測
- paper signal
- 監聽
- 依照策略訊號交易

### 1.1 先下載 repo

若工作區中沒有 `crypto_trading` repo，先執行：

```bash
REPO_DIR="${REPO_DIR:-$PWD/crypto_trading}"

if [ ! -d "$REPO_DIR/.git" ]; then
  git clone https://github.com/nthu-chung/crypto_trading "$REPO_DIR"
fi

cd "$REPO_DIR"
git pull --ff-only
```

### 1.2 建立或啟用環境

```bash
if [ ! -d .venv-standard-bot ]; then
  python3 -m venv .venv-standard-bot
fi

source .venv-standard-bot/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt -r requirements-standard-bot-mvp.txt
```

### 1.3 歷史資料補齊規則

OpenClaw 在回測、paper signal、monitor 前，必須先確認本地 historical parquet 是否足夠新、且覆蓋所需時間窗。

若本地資料不存在、過舊、或範圍不足：

- 不可直接拿過期 parquet 硬跑
- 不可直接把 Binance API 即時回傳結果當成最終回測輸入
- 必須先使用 repo 內的資料下載流程抓取 Binance K bar
- 必須先把下載結果存成或更新為本地 parquet
- 高週期資料應優先由本地 `1m` 重採樣產生

也就是：

`Binance API -> repo downloader -> local parquet -> local resample -> standard_bot`

### 1.4 強制原則

OpenClaw 一旦要做回測或 signal 驗證，**必須優先使用**：

- `python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest`
- `python -m cyqnt_trd.standard_bot.entrypoints.mvp_paper`
- `python -m cyqnt_trd.standard_bot.entrypoints.mvp_monitor_http`
- `python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager`

不得預設改用：

- `cyqnt_trd/get_data/*` 當正式回測入口
- `cyqnt_trd/backtesting/*`
- `cyqnt_trd/backtesting/strategy_backtest.py`
- 臨時 notebook / 臨時 pandas 回測腳本

若需要描述回測核心，標準說法應為：

`standard_bot -> mvp_backtest.py -> NumbaBacktestRunner`

---

## 2. 回測框架規範

OpenClaw 做回測時，必須使用這條資料路徑：

`historical parquet -> local resample -> standard_bot signal -> NumbaBacktestRunner`

### 2.1 具體規則

- 歷史資料優先本地化，不要每次直接重打 API
- 若本地資料不足，先透過 repo 內的 Binance API 下載流程補抓資料，再回到本地 parquet 路徑
- 不可把 Binance API 即時回傳結果直接當成正式回測資料來源
- 儲存粒度優先為 `1m`
- `5m / 15m / 1h` 這類高週期優先由本地 `1m` 重採樣得到
- 回測引擎優先使用 `--engine numba`
- 不要先建立大量 Python snapshot 物件再做批次回測

### 2.2 時序規則

- 只能使用 `decision time` 當下可見資料
- 若策略在 `bar close` 形成信號，最早只能在下一根 `bar open` 成交
- 不可使用尚未收盤的高週期 bar
- feature 不可使用未來資料
- 回測與 paper signal 應共用同一套策略邏輯

### 2.3 回測命令模板

```bash
REPO_DIR="${REPO_DIR:-$PWD/crypto_trading}"
cd "$REPO_DIR"
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

### 2.4 回測輸出規範

OpenClaw 在 demo、摘要、簡報或回覆時，應優先從 `docs/backtests/*.json` 讀正式結果，而不是只抄 terminal 數字。

至少應回報：

- 收益率 `total_return`
- 最大回撤 `metrics.max_drawdown`
- `Sharpe ratio`
- 交易次數 `metrics.trade_count`
- signal 次數 `metrics.signal_count`
- 最終資金 `metrics.final_equity`
- JSON 輸出檔路徑

若需要 `win_rate`，且 JSON 沒有現成欄位，才允許由 `trades` 推導，且必須明說是推導值。

---

## 3. 自然語言轉策略規格

自然語言不能直接拿去回測，必須先補成正式規格。

### 3.1 示例

使用者輸入：

`5分鐘 MA 上穿 1小時 MA 做多，下穿做空`

轉換後規格：

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

### 3.2 一定要補的欄位

- 標的
- 市場
- 主決策週期
- 參考週期
- 指標與參數
- 做多 / 做空 / 平倉語意
- execution model
- fee / slippage
- 回測時間範圍

### 3.3 保守預設

若使用者沒有講清楚，OpenClaw 應優先採保守預設：

- execution model：`next_open`
- fee：`taker fee`
- spread threshold：`0`
- 若語意明顯包含下穿做空，預設為 `long_short`

### 3.4 規格模板

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

## 4. 新策略與 Numba 路由規則

自然語言轉成策略規格後，**不一定能直接走 `NumbaBacktestRunner`**。OpenClaw 必須先判斷：

### 4.1 既有 numba 策略

先嘗試映射到已存在的 numba 策略：

- `moving_average_cross`
- `price_moving_average`
- `rsi_reversion`
- `multi_timeframe_ma_spread`
- `donchian_breakout`

若可映射，直接使用：

`mvp_backtest --engine numba`

### 4.2 若無法直接映射

1. 若已存在 `standard_bot` plugin，但尚未接進 numba：
   - 允許先使用 `mvp_backtest --engine python`
2. 若連 `standard_bot` plugin 都沒有：
   - 可讓其他 AI 在 `standard_bot` 內新增 plugin
   - 先做 `python engine` 驗證
   - 補 batch / step、PIT、smoke tests
   - 驗證通過後，再評估是否補 numba

### 4.3 禁止事項

- 不可直接退回 legacy `cyqnt_trd/backtesting/*`
- 不可直接使用 `strategy_backtest.py`
- 不可先寫臨時 notebook 取代正式 plugin
- 新策略不得脫離 `standard_bot` 自成一套野生框架

---

## 5. 交易模式規範

這份 skill 的交易規則與過去版本不同：

- **不使用 testnet**
- OpenClaw 的真實交易，必須以 `paper trade` 產生的信號為來源
- 真實交易不是由 repo 直接下單，而是由 OpenClaw 的交易能力執行
- 但 OpenClaw 下單前，必須先經過 paper signal、餘額確認、`CONFIRM`、時長確認這四個步驟

### 5.1 模式 1：只回測

- 使用 `mvp_backtest`
- 不送單
- 只產出回測結果與 JSON

### 5.2 模式 2：只產生 paper signal

- 使用 `mvp_paper`
- 或用 monitor / background loop 產生持續 paper signal
- 不對外下單

### 5.3 模式 3：paper signal 驅動的真實交易

這是 OpenClaw 目前應採用的真實交易模式：

1. 先用 `standard_bot` 產生 paper signal
2. 根據最新 signal 決定是否提議交易
3. 先查詢並展示使用者餘額
4. 清楚告知：
   - 當前 paper signal
   - 準備交易的標的 / 方向 / 金額
   - 目前餘額
   - 風險管控方式
   - 預計執行時長
5. 等使用者明確輸入 `CONFIRM`
6. 收到 `CONFIRM` 後，才由 OpenClaw 的交易能力開始執行一段**有時長限制**的真實交易 session

### 5.4 使用者交易前必須看到的資訊

OpenClaw 在任何真實交易前，必須展示：

- 最新 paper signal：`buy / sell / hold`
- signal 產生時間
- 監聽標的
- 目前價格
- 使用者餘額
- 預計使用的交易金額或數量
- 風險管控方式
- 預計執行時長
- 如何停止

### 5.5 `CONFIRM` 規則

若未收到 `CONFIRM`：

- 可以回測
- 可以生成 signal
- 可以啟動 paper 監聽
- 不可下真實單

若收到 `CONFIRM`，仍必須先滿足：

- 使用者已看到當前餘額
- 使用者已知道交易標的、方向、金額/數量
- 使用者已看到本次 session 的風險管控方式
- 使用者已給定執行時長

### 5.6 時長規則

真實交易 session 必須是**有時長限制**的。

OpenClaw 不可在未經說明下啟動無限期交易。若使用者沒有給時長，必須先追問，例如：

- `10 分鐘`
- `1 小時`
- `到我手動停止為止`

若使用者選擇「到我手動停止為止」，仍需明確告知 `停止` 指令。

---

## 6. 監聽與背景執行

若使用者要求持續監聽，OpenClaw 應優先使用下載後 repo 內的 `standard_bot` 來產生 paper signal，再由 OpenClaw 根據該 signal 做決策或交易。

推薦入口：

- `python -m cyqnt_trd.standard_bot.entrypoints.mvp_paper`
- `python -m cyqnt_trd.standard_bot.entrypoints.mvp_monitor_http`
- `python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager`

### 6.1 背景 paper signal session

若需要長時間監聽，OpenClaw 應啟動背景 session，並維護：

- `run_id`
- `poll_index`
- 當前價格
- 最新 signal
- 目前持倉
- 損益
- 狀態查詢方式
- 停止方式

### 6.2 標準回報

若背景 session 已啟動，OpenClaw 至少要回報：

- `run_id`
- 監聽標的
- 最新 signal
- 背景 session 的執行時長
- `現在狀態` 如何查
- `停止` 如何做

### 6.3 只用 paper signal，不要自行改訊號

OpenClaw 不得在背景 session 外另外自行重算一套簡化 signal，再拿去交易。真實交易提議必須來自：

`standard_bot` 產生的 paper signal

---

## 7. 風險管控

真實交易 session 必須帶有硬風控，而且 OpenClaw 必須在使用者輸入 `CONFIRM` 前先把風控方式展示清楚。

### 7.1 交易前必須先告知的風控方式

在使用者輸入 `CONFIRM` 前，OpenClaw 至少要清楚展示：

- 本次使用哪個帳戶 / 餘額快照
- 本次 session 的 `session_start_equity`
- 最大允許虧損比例：`x%`（預設 `10%`，可由使用者指定）
- 風控觸發線：`stop_equity = session_start_equity * (1 - x%)`
- 觸發後會執行什麼：
  - 停止新交易
  - 取消未成交訂單（若工具支援）
  - 嘗試平掉現有持倉
  - 強制結束交易 session
  - 將結果寫入 workspace session

### 7.2 權益基準

風控應以 session 啟動時的帳戶總權益為基準，而不是只看可用餘額。

- `session_start_equity`
- `max_loss_ratio = x%`（預設 `10%`）
- `stop_equity = session_start_equity * (1 - max_loss_ratio)`

OpenClaw 在交易 session 執行期間，必須持續檢查：

- `current_equity`
- 現有持倉
- 未成交訂單

### 7.3 風控觸發條件

一旦：

- `current_equity <= stop_equity`

就必須立刻觸發風控。

### 7.4 風控觸發後的強制動作

風控觸發後，OpenClaw 必須依序執行：

1. 停止接受新的交易信號去開新倉
2. 取消未成交訂單（若工具支援）
3. 嘗試平掉現有持倉
4. 停止真實交易 session
5. 停止 watcher subagent 或改由它只回報停止狀態
6. 將結果寫入 workspace session
7. 回報使用者：
   - 已觸發風控
   - 目前權益
   - 損失比例
   - 是否已平倉
   - session 是否已終止

### 7.5 風控觸發後不得自動重啟

若 session 因風控停止：

- 不得自動重啟
- 不得自動重新進場
- 必須等使用者重新確認後，才可開始新的交易 session

### 7.6 風控資訊也必須寫入 workspace session

workspace session 至少應保存：

- `session_start_equity`
- `current_equity`
- `stop_equity`
- `loss_ratio`
- `risk_triggered`
- `risk_reason`
- `risk_triggered_at`
- `positions_closed`
- `session_stopped`

---

## 8. OpenClaw 應如何回應使用者

### 8.1 若是回測

至少應回報：

- 策略規格
- 資料期間
- 是否本地歷史下載
- 是否 `1m -> 5m/1h` 重採樣
- 是否使用 `numba`
- 重要績效指標
- JSON 路徑

### 8.2 若是 paper signal / 監聽

至少應回報：

- `run_id`
- `signal_count`
- 最新 signal
- 是否仍在監聽
- 如何查最新狀態
- 如何停止

### 8.3 若是準備真實交易

至少應回報：

- 最新 paper signal
- 使用者餘額
- 交易標的
- 交易方向
- 預計金額 / 數量
- 執行時長
- `CONFIRM` 規則
- `停止` 規則

---

## 9. 禁止事項

- 不要把自然語言直接當成可執行策略
- 不要在沒有餘額展示的情況下直接提議下真實單
- 不要在沒有先說明風險管控方式的情況下要求使用者 `CONFIRM`
- 不要在沒有 `CONFIRM` 的情況下真實交易
- 不要在沒有明確時長的情況下啟動真實交易 session
- 不要把 paper signal 說成已經成交
- 不要改用 legacy `backtesting/` 腳本
- 不要提到或依賴 testnet

---

## 10. 一句話總結

OpenClaw 在這個 skill 下應遵守這條主線：

`自然語言 -> 正式策略規格 -> 下載 crypto_trading repo -> standard_bot 回測 / paper signal -> 查餘額與風控條件 -> 使用者 CONFIRM -> 在指定時長內根據 paper signal 執行真實交易`

---

## 11. 監聽通知與 workspace session 規範

Jarvis 介面不能依賴主動跳通知，因此背景監聽規範不能建立在推播一定會成功上。

正確做法是：一旦啟動背景監聽，必須同時啟動一個 watcher subagent，持續把每輪輪詢結果寫進管理 bot 的 workspace session。之後使用者只要輸入 `現在狀態`，主 agent 就必須從 session 中讀取最新狀態並回報；使用者輸入 `停止`，主 agent 就必須使用 session 中保存的 `run_id` 停掉 paper signal session 與後續交易 session。

### 11.1 核心原則

- 不可等到任務結束才回報
- 中間狀態必須持續寫入 workspace session
- session 中必須始終保有可供查詢與停止的最新 `run_id`

### 11.2 watcher subagent 的職責

若平台支援 subagent，則背景監聽啟動成功後，主 agent 必須立即啟動一個專用 watcher subagent。

watcher subagent 的唯一職責是：

- 定期讀取 paper signal / monitor 狀態
- 追蹤 log 更新
- 維護遞增的 `poll_index`
- 將每輪結果寫入 workspace session

watcher subagent 不負責：

- 修改策略
- 改變交易金額
- 直接跳過 `CONFIRM`
- 直接自行下單

### 11.3 session 內必須保存的欄位

至少應保存：

- `run_id`
- `poll_index`
- 輪詢時間
- 監聽標的
- 當前價格
- 最新 signal：`buy / sell / hold`
- 目前持倉
- 損益
- 是否已進入真實交易 session
- 使用者餘額快照
- 風控基準與是否已觸發風控
- 預計結束時間或剩餘時長
- `status_command`
- `stop_command`
- `kill_command`

### 11.4 使用者輸入 `現在狀態`

當使用者輸入：

- `現在狀態`
- `status`
- `目前狀況`

主 agent 必須直接讀取 workspace session 中 watcher subagent 寫入的最新狀態，並回報：

- 目前 `run_id`
- 最新 `poll_index`
- 最新輪詢時間
- 當前價格
- 最新 signal
- 目前持倉與損益
- 風控是否已觸發
- 是否已開始真實交易
- 若有時長限制，還剩多久

### 11.5 使用者輸入 `停止`

當使用者輸入：

- `停止`
- `stop`
- `停止監聽`

主 agent 必須從 workspace session 取得目前活躍的 `run_id`，並依序：

1. 停掉 paper signal session
2. 停掉 watcher subagent
3. 若已有真實交易 session，同步停止該 session
4. 將停止結果回寫到 workspace session
5. 回報最終狀態

### 11.6 更新頻率

watcher subagent 應遵守：

- 第一則狀態更新：背景流程啟動後幾秒內
- 固定心跳：預設每 `30` 秒至少更新一次
- 事件更新：以下事件發生時應立即更新
  - 新 signal
  - 交易提議形成
  - 餘額查詢完成
  - 收到 `CONFIRM`
  - 真實交易開始
  - 真實交易停止
  - watcher 異常

### 11.7 watcher 不可靜默卡住

若 watcher subagent 發生以下情況：

- 已啟動但沒有寫入第一則狀態
- 固定心跳中斷
- 背景流程仍在跑，但 session 久久沒有更新

主 agent 必須：

1. 立即通知使用者 watcher 異常
2. 自己接管一次最新狀態讀取與回報
3. 視情況停止舊 watcher
4. 重啟新的 watcher

若重啟後仍不穩定，主 agent 應退回「自己輪詢、自己更新 session」模式。
