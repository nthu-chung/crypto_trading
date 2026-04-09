# Standard Bot Progress - 2026-04-09

## Source Roadmap

- Primary reference: `/Users/hankchung/Dev/Orderbook-research/docs/standard_trading_bot_pdf.md`
- Implementation repo: `/Users/hankchung/Dev/crypto_trading-main`

## Summary

Today we moved `crypto_trading-main` from an early research-style toolkit toward a protocol-first `standard_bot` MVP that can now:

- fetch market data and assemble PIT-aligned snapshots
- run plugin-based signals in both backtest and step/runtime mode
- run historical backtests
- run paper execution
- connect to Binance USD-M Futures Testnet
- validate and execute isolated testnet orders
- expose a minimal HTTP monitor entrypoint
- enforce initial execution risk rules
- support deterministic execution idempotency keys

## What Was Completed

### 1. Protocol-first sidecar architecture

Added a non-breaking `cyqnt_trd.standard_bot` package with core contracts and layer boundaries so new work can evolve without rewriting legacy modules first.

Key areas:

- `cyqnt_trd/standard_bot/core/contracts.py`
- `cyqnt_trd/standard_bot/data/*`
- `cyqnt_trd/standard_bot/signal/*`
- `cyqnt_trd/standard_bot/simulation/*`
- `cyqnt_trd/standard_bot/runtime/*`
- `cyqnt_trd/standard_bot/execution/*`

### 2. Market-only Data MVP

Implemented market adapters and PIT snapshot assembly:

- Binance spot/futures REST market adapter
- historical JSON adapter
- historical snapshot assembler with `decision_as_of`
- alignment policy wiring

Key files:

- `cyqnt_trd/standard_bot/data/adapters.py`
- `cyqnt_trd/standard_bot/data/snapshot.py`
- `cyqnt_trd/standard_bot/data/alignment.py`

### 3. Signal plugin system

Implemented and registered built-in signal plugins:

- `moving_average_cross`
- `price_moving_average`
- `rsi_reversion`

All three now support:

- batch-style `run(...)`
- incremental `step(...)`
- serializable `SignalState`
- consistent `SignalEnvelope`

Key files:

- `cyqnt_trd/standard_bot/signal/plugins.py`
- `cyqnt_trd/standard_bot/signal/registry.py`
- `cyqnt_trd/standard_bot/entrypoints/common.py`

### 4. Simulation / backtest MVP

Implemented snapshot-driven historical backtesting:

- signal pipeline replay on PIT snapshots
- simple long/flat trade loop
- commission and slippage configuration
- equity curve and trade output

Key files:

- `cyqnt_trd/standard_bot/simulation/runner.py`
- `cyqnt_trd/standard_bot/entrypoints/mvp_backtest.py`

### 5. Runtime + paper execution MVP

Implemented a step-based runtime runner and paper broker:

- same signal pipeline reused for runtime
- account snapshot injection into signal context
- risk rule hook points
- paper execution with fills, balances, and positions

Key files:

- `cyqnt_trd/standard_bot/runtime/runner.py`
- `cyqnt_trd/standard_bot/execution/paper.py`
- `cyqnt_trd/standard_bot/entrypoints/mvp_paper.py`

### 6. Initial execution risk rules

Added the first two reusable `RiskRule` implementations:

- `MaxPositionFractionRule`
- `LongOnlySinglePositionRule`

Key file:

- `cyqnt_trd/standard_bot/execution/rules.py`

### 7. HTTP Monitor API

Implemented a minimal monitor server with:

- `GET /health`
- `POST /run`
- `RunContext` creation from HTTP payload
- configurable dry-run / signal-only mode
- stable error responses for invalid JSON and runtime failures

Key file:

- `cyqnt_trd/standard_bot/entrypoints/mvp_monitor_http.py`

### 8. Binance Futures Testnet execution

Implemented Binance USD-M Futures Testnet support:

- `.env` loader that supports `export KEY=...`
- account sync
- order validation
- order placement
- duplicate `client_order_id` recovery

Key files:

- `cyqnt_trd/standard_bot/config.py`
- `cyqnt_trd/standard_bot/execution/binance_futures_testnet.py`
- `cyqnt_trd/standard_bot/entrypoints/mvp_testnet_execution.py`
- `cyqnt_trd/standard_bot/entrypoints/mvp_testnet_roundtrip.py`

### 9. Execution idempotency foundation

Added deterministic execution idempotency helpers:

- stable `client_tag` derived from `(run_id, intent_id)`
- monitor accepts external `run_id`
- runtime injects deterministic `client_tag` when missing
- testnet broker can recover existing order state after duplicate submission

Key file:

- `cyqnt_trd/standard_bot/execution/idempotency.py`

## Validation Performed

### Automated tests

Final local test result:

- `pytest /Users/hankchung/Dev/crypto_trading-main/tests/standard_bot -q`
- result: `19 passed`

Coverage now includes:

- backtest flow
- paper runtime flow
- signal plugin behavior
- monitor HTTP behavior
- config loading
- testnet execution helper logic
- batch vs step alignment for built-in plugins
- idempotency behavior

### Binance Testnet checks

Executed against the Binance USD-M Futures Testnet using credentials from `.env`:

- account sync succeeded
- order validation succeeded
- isolated roundtrip trade on `XRPUSDT` succeeded
- open order filled
- reduce-only close order filled
- final position returned to flat for that symbol

Observed exchange constraints during testing:

- `BTCUSDT` testnet `min_notional = 100`
- quantity is truncated to exchange `step_size`
- a nominal order exactly at the threshold can still fail after truncation

## Mapping To `standard_trading_bot_pdf.md`

| Completed work | Roadmap section(s) | Status |
| --- | --- | --- |
| Core contracts and sidecar layered architecture | `1.2 设计原则`, `2 总体架构`, `4 跨层公共类型` | Implemented MVP foundation |
| PIT-aligned market snapshots | `3.1 数据层`, `4.6 DataSnapshot`, `4.6.1 多源时间与 K 线锚定` | Market-only path implemented |
| Plugin-based signal system | `3.2 信号层` | Implemented |
| Batch + step signal execution | `3.2.1 回测与实盘：同一逻辑、双执行形态` | Implemented for current built-in plugins |
| Batch vs step alignment tests | `3.2.1 一致性验证（必做）` | Implemented |
| Snapshot-driven backtest | `3.3 仿真层`, `4.11 BacktestRequest / BacktestResult` | Implemented MVP |
| Paper execution runner | `3.4 Runtime & Execution`, `3.4.2 执行` | Implemented MVP |
| HTTP monitor entrypoint | `3.4.1 监控 / 调度（Monitor）` | Implemented minimal HTTP version |
| Risk rule chain | `3.4.2 执行` | Implemented first rules |
| Binance testnet broker adapter | `3.4.2 执行`, `4.9 ExecutionIntent`, `4.10 ExecutionReport` | Implemented MVP |
| Idempotent client order id path | `3.4.1 定制扩展`, idempotency requirement | Implemented first foundation |
| Execution-only CLI and isolated roundtrip test | `3.4.2 可独立使用` | Implemented and verified |

## Current Status Against The Roadmap

### Already covered well enough for MVP

- Market-only `Data -> Signal -> Simulation`
- Market-only `Data -> Signal -> Runtime -> Execution`
- Signal plugin registration and reusable contracts
- Initial risk rules
- HTTP-triggered monitor entrypoint
- Testnet exchange connectivity
- Batch/step consistency checks for built-in signals

### Still partial or not yet implemented

- `SocialDataAdapter` and `OnChainDataAdapter`
- `partial_ok` orchestration across multiple source domains
- richer fee / fill / slippage simulation models
- attribution and performance decomposition
- queue / cron trigger adapters
- retry policies, persistent state store, and durable run logs
- live snapshot assembler separate from historical assembler
- Numba-based shared kernels
- advanced execution features such as cancel/replace orchestration, position sync reconciliation, and broker abstraction beyond testnet + paper

## Recommended Next Steps

1. Add `LiveSnapshotAssembler` so runtime and replay share the same clipping logic instead of relying only on historical assembly patterns.
2. Add one durable state backend for `SignalState` and run idempotency records so monitor retries survive process restart.
3. Add a real end-to-end monitor smoke test that drives `HTTP /run -> Signal -> Testnet Execution` in a controlled dry-run and optional live-test mode.
4. Introduce a second data domain, preferably a minimal `SocialDataAdapter`, to start exercising `DataSnapshot` beyond market-only inputs.

## Related Docs In Repo

- `docs/standard_bot_migration.md`
- `docs/standard_bot_mvp.md`
