# Standard Bot Migration Plan

This repository now contains an initial scaffold for the protocol-first bot
architecture under `cyqnt_trd.standard_bot`.

## Why this sidecar package exists

The current codebase already has useful functionality:

- market data fetchers in `cyqnt_trd.get_data`
- signal logic in `cyqnt_trd.trading_signal`
- backtesting in `cyqnt_trd.backtesting`
- live tracking and order helpers in `cyqnt_trd.online_trading` and `cyqnt_trd.test_script`

What it does not have yet is the standardized contract layer described in
`standard_trading_bot_pdf.md`:

- `DataSnapshot`
- `SignalBatch`
- `ExecutionIntent`
- PIT alignment via `decision_as_of`
- separate data / signal / simulation / runtime / execution boundaries

The new package gives us a safe place to build that architecture without
breaking legacy entrypoints.

## New package layout

```text
cyqnt_trd/standard_bot/
├── core/contracts.py
├── data/alignment.py
├── data/interfaces.py
├── signal/interfaces.py
├── simulation/interfaces.py
├── runtime/interfaces.py
└── execution/interfaces.py
```

## How existing modules should migrate

### Data layer

- Current source:
  - `cyqnt_trd/get_data/get_trending_data.py`
  - `cyqnt_trd/get_data/get_futures_data.py`
  - `cyqnt_trd/get_data/get_web3_trending_data.py`
- Target:
  - wrap these as `MarketDataAdapter` implementations
  - stop calculating factors in the data layer
  - move all snapshot assembly through `AlignmentPolicy` and `DataSnapshot`

### Signal layer

- Current source:
  - `cyqnt_trd/trading_signal/factor/*`
  - `cyqnt_trd/trading_signal/signal/*`
  - `cyqnt_trd/trading_signal/selected_alpha/*`
- Target:
  - expose plugin entrypoints returning `SignalBatch`
  - move toward shared batch / step kernels
  - keep pandas wrappers only as a thin compatibility layer

### Simulation layer

- Current source:
  - `cyqnt_trd/backtesting/framework.py`
  - `cyqnt_trd/backtesting/factor_test.py`
  - `cyqnt_trd/backtesting/strategy_backtest.py`
- Target:
  - replay `DataSnapshot` streams
  - consume the same signal plugins used by runtime
  - plug fee / slippage / fill models behind the new interfaces

### Runtime layer

- Current source:
  - `test/real_time_trade.py`
  - `cyqnt_trd/online_trading/realtime_price_tracker.py`
- Target:
  - turn `real_time_trade.py` logic into a `Runner`
  - keep websocket and live data code as feed adapters
  - make each run carry a `RunContext` and `decision_as_of`

### Execution layer

- Current source:
  - `cyqnt_trd/test_script/test_order.py`
- Target:
  - split Binance order placement into `BrokerAdapter`
  - add `RiskRule` chain before placing orders
  - emit `ExecutionReport` consistently for paper and live trading

## Recommended next implementation order

1. Build a `BinanceMarketDataAdapter` that returns `MarketBundle`.
2. Add a `HistoricalSnapshotAssembler` and `LiveSnapshotAssembler` using the same alignment code.
3. Port one simple strategy, ideally MA, into a `SignalPlugin`.
4. Implement a minimal `PaperBrokerAdapter`.
5. Rebuild backtesting on top of `DataSnapshot -> SignalBatch -> ExecutionReport`.
6. Replace `test/real_time_trade.py` with a runtime entrypoint that uses the new layers.

## Important cleanup still pending

- Remove hard-coded API credentials from live-trading related files.
- Add unit tests for PIT alignment.
- Add batch vs step signal consistency tests.
- Add JSON schema or protobuf serialization once the v1 fields stabilize.
