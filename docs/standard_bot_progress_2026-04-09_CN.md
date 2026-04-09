# Standard Bot 進度整理 - 2026-04-09

## 參考 Roadmap

- 主要對照文件：`/Users/hankchung/Dev/Orderbook-research/docs/standard_trading_bot_pdf.md`
- 實作專案：`/Users/hankchung/Dev/crypto_trading-main`

## 今日總結

今天我們把 `crypto_trading-main` 從偏研究工具的型態，往協議優先的 `standard_bot` MVP 推進。  
目前這個新架構已經可以：

- 抓取市場資料並組裝 PIT 對齊快照
- 用 plugin 形式跑 signal，且同時支援 backtest 與 step/runtime
- 執行歷史回測
- 執行 paper trading
- 連上 Binance USD-M Futures Testnet
- 驗證並執行隔離的 testnet 測試單
- 暴露最小可用的 HTTP monitor 入口
- 套用第一版 execution risk rules
- 支援決定性的 execution 幂等鍵

## 今天完成的內容

### 1. 協議優先的 sidecar 架構

新增不破壞舊模組的 `cyqnt_trd.standard_bot` 套件，先把核心契約與分層邊界搭起來，讓新功能可以逐步遷移，而不是直接推翻 legacy 結構。

主要位置：

- `cyqnt_trd/standard_bot/core/contracts.py`
- `cyqnt_trd/standard_bot/data/*`
- `cyqnt_trd/standard_bot/signal/*`
- `cyqnt_trd/standard_bot/simulation/*`
- `cyqnt_trd/standard_bot/runtime/*`
- `cyqnt_trd/standard_bot/execution/*`

### 2. Market-only 的資料層 MVP

已完成市場資料 adapter 與 PIT 快照組裝：

- Binance spot/futures REST market adapter
- 歷史 JSON adapter
- 帶 `decision_as_of` 的 historical snapshot assembler
- alignment policy 串接

主要位置：

- `cyqnt_trd/standard_bot/data/adapters.py`
- `cyqnt_trd/standard_bot/data/snapshot.py`
- `cyqnt_trd/standard_bot/data/alignment.py`

### 3. Signal plugin 系統

已實作並註冊內建 signal plugin：

- `moving_average_cross`
- `price_moving_average`
- `rsi_reversion`

三者目前都支援：

- batch 型態的 `run(...)`
- incremental 型態的 `step(...)`
- 可序列化的 `SignalState`
- 一致的 `SignalEnvelope`

主要位置：

- `cyqnt_trd/standard_bot/signal/plugins.py`
- `cyqnt_trd/standard_bot/signal/registry.py`
- `cyqnt_trd/standard_bot/entrypoints/common.py`

### 4. Simulation / backtest MVP

已完成 snapshot-driven historical backtest：

- 在 PIT snapshots 上重放 signal pipeline
- 簡化版 long/flat 交易流程
- commission 與 slippage 參數
- 權益曲線與交易輸出

主要位置：

- `cyqnt_trd/standard_bot/simulation/runner.py`
- `cyqnt_trd/standard_bot/entrypoints/mvp_backtest.py`

### 5. Runtime + paper execution MVP

已完成 step-based runtime runner 與 paper broker：

- runtime 重用同一套 signal pipeline
- 把 account snapshot 注入 signal context
- 預留 risk rule 掛點
- paper execution 可產生 fills、balances、positions

主要位置：

- `cyqnt_trd/standard_bot/runtime/runner.py`
- `cyqnt_trd/standard_bot/execution/paper.py`
- `cyqnt_trd/standard_bot/entrypoints/mvp_paper.py`

### 6. 第一版 execution risk rules

新增兩個可重用的 `RiskRule`：

- `MaxPositionFractionRule`
- `LongOnlySinglePositionRule`

主要位置：

- `cyqnt_trd/standard_bot/execution/rules.py`

### 7. HTTP Monitor API

已完成最小 monitor server：

- `GET /health`
- `POST /run`
- 從 HTTP payload 建立 `RunContext`
- 支援 dry-run / signal-only
- 對 invalid JSON 與 runtime failure 給出穩定錯誤回應

主要位置：

- `cyqnt_trd/standard_bot/entrypoints/mvp_monitor_http.py`

### 8. Binance Futures Testnet execution

已完成 Binance USD-M Futures Testnet 串接：

- 支援 `.env`，且能讀 `export KEY=...` 格式
- 帳戶同步
- 下單驗證
- 真正送單
- duplicate `client_order_id` 的回查恢復

主要位置：

- `cyqnt_trd/standard_bot/config.py`
- `cyqnt_trd/standard_bot/execution/binance_futures_testnet.py`
- `cyqnt_trd/standard_bot/entrypoints/mvp_testnet_execution.py`
- `cyqnt_trd/standard_bot/entrypoints/mvp_testnet_roundtrip.py`

### 9. Execution 幂等基礎

已補上第一版幂等能力：

- 由 `(run_id, intent_id)` 產生穩定的 `client_tag`
- monitor 可接受外部傳入 `run_id`
- runtime 在缺少 `client_tag` 時自動補 deterministic tag
- testnet broker 碰到 duplicate submission 時可回查既有訂單

主要位置：

- `cyqnt_trd/standard_bot/execution/idempotency.py`

## 今日實際驗證

### 自動化測試

最終本地測試結果：

- `pytest /Users/hankchung/Dev/crypto_trading-main/tests/standard_bot -q`
- 結果：`19 passed`

目前測試已涵蓋：

- backtest flow
- paper runtime flow
- signal plugin 行為
- monitor HTTP 行為
- config 載入
- testnet execution helper 邏輯
- 內建 plugins 的 batch vs step 對齊
- idempotency 行為

### Binance Testnet 驗證

已使用 `.env` 中的 Binance USD-M Futures Testnet 金鑰實際測試：

- 帳戶同步成功
- order validation 成功
- `XRPUSDT` 的隔離 roundtrip 測試成功
- 開倉單成交
- `reduce_only` 平倉單成交
- 最終該 symbol 倉位回到空倉

測試過程中觀察到的交易所限制：

- `BTCUSDT` testnet 的 `min_notional = 100`
- 數量會被交易所 `step_size` 向下取整
- 名義金額即使剛好等於門檻，也可能因為取整後掉到門檻以下而被拒

## 與 `standard_trading_bot_pdf.md` 的對應

| 已完成項目 | 對應章節 | 狀態 |
| --- | --- | --- |
| 核心 contracts 與 sidecar 分層架構 | `1.2 设计原则`、`2 总体架构`、`4 跨层公共类型` | MVP 基礎已落地 |
| PIT 對齊的 market snapshots | `3.1 数据层`、`4.6 DataSnapshot`、`4.6.1 多源时间与 K 线锚定` | 已完成 market-only 路徑 |
| Plugin-based signal system | `3.2 信号层` | 已完成 |
| Batch + step signal execution | `3.2.1 回测与实盘：同一逻辑、双执行形态` | 已完成於目前內建 plugin |
| Batch vs step alignment 測試 | `3.2.1 一致性验证（必做）` | 已完成 |
| Snapshot-driven backtest | `3.3 仿真层`、`4.11 BacktestRequest / BacktestResult` | MVP 已完成 |
| Paper execution runner | `3.4 Runtime & Execution`、`3.4.2 执行` | MVP 已完成 |
| HTTP monitor 入口 | `3.4.1 监控 / 调度（Monitor）` | 最小 HTTP 版本已完成 |
| Risk rule chain | `3.4.2 执行` | 第一版已完成 |
| Binance testnet broker adapter | `3.4.2 执行`、`4.9 ExecutionIntent`、`4.10 ExecutionReport` | MVP 已完成 |
| 幂等 client order id 流程 | `3.4.1 定制扩展` 中的幂等要求 | 第一版已完成 |
| Execution-only CLI 與隔離 roundtrip | `3.4.2 可独立使用` | 已完成且已驗證 |

## 目前相對於 Roadmap 的狀態

### 已經有 MVP 基礎的部分

- Market-only 的 `Data -> Signal -> Simulation`
- Market-only 的 `Data -> Signal -> Runtime -> Execution`
- Signal plugin 註冊與共用 contracts
- 第一版 risk rules
- HTTP 觸發 monitor 入口
- Testnet 交易所串接
- 內建 signal 的 batch/step 一致性驗證

### 仍然只做了一部分或尚未開始的部分

- `SocialDataAdapter` 與 `OnChainDataAdapter`
- 多資料源下的 `partial_ok` 編排
- 更完整的 fee / fill / slippage simulation model
- attribution 與績效拆解
- queue / cron trigger adapters
- retry policies、持久化 state store、durable run logs
- 與 historical assembler 對應的 `LiveSnapshotAssembler`
- Numba-based shared kernels
- 更進階的 execution 能力，例如 cancel/replace、倉位同步校正、多 broker abstraction

## 建議下一步

1. 補 `LiveSnapshotAssembler`，讓 runtime 與 replay 真正共用同一套 clipping 邏輯，而不只是沿用 historical pattern。
2. 補一個 durable state backend，保存 `SignalState` 與 idempotency records，讓 monitor 重試在程序重啟後仍能延續。
3. 補一個真正的端到端 monitor smoke test，直接驗證 `HTTP /run -> Signal -> Testnet Execution`。
4. 補第二個資料域，建議先做一個最小 `SocialDataAdapter`，開始讓 `DataSnapshot` 不再只是 market-only。

## Repo 內相關文件

- `docs/standard_bot_migration.md`
- `docs/standard_bot_mvp.md`
- `docs/standard_bot_progress_2026-04-09.md`
