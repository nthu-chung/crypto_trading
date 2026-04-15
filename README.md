# cyqnt-trd

`cyqnt-trd` is a cryptocurrency trading toolkit centered on the `standard_bot` workflow for:

- historical data download to local parquet
- local resample from `1m` into higher timeframes
- Numba-accelerated backtesting
- paper signal generation
- monitor / run-manager driven execution flows

The current recommended path is:

`historical parquet -> local resample -> standard_bot signal -> NumbaBacktestRunner`

## Install

### From PyPI

```bash
pip install cyqnt-trd
```

### For development

```bash
git clone https://github.com/nthu-chung/crypto_trading
cd crypto_trading
python3 -m venv .venv-standard-bot
source .venv-standard-bot/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt -r requirements-standard-bot-mvp.txt
```

## Recommended Standard Bot Entry Points

### Backtest

```bash
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

### Paper Signal

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_paper \
  --market-type futures \
  --strategy multi_timeframe_ma_spread \
  --symbol BTCUSDT \
  --interval 5m \
  --secondary-interval 1h \
  --primary-ma-period 20 \
  --reference-ma-period 20 \
  --spread-threshold-bps 0 \
  --historical-dir data/mtf_90d \
  --dry-run
```

### Monitor / Background Session

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_monitor_http \
  --broker paper \
  --host 127.0.0.1 \
  --port 8787
```

## Data Workflow

The preferred data workflow is:

1. Download Binance K bars into local parquet
2. Store the finest useful granularity, usually `1m`
3. Resample locally into `5m`, `15m`, `1h`, etc.
4. Run `standard_bot` on local parquet instead of using raw API responses as final backtest input

This keeps:

- point-in-time alignment clearer
- local backtests repeatable
- paper signal and backtest logic consistent

## Current Strategy Families On The Mainline

The `standard_bot` mainline currently includes Numba-backed support for:

- `moving_average_cross`
- `price_moving_average`
- `rsi_reversion`
- `multi_timeframe_ma_spread`
- `donchian_breakout`

## Package Notes

- The preferred historical backtest engine is `NumbaBacktestRunner`
- The preferred CLI entrypoint is `cyqnt_trd.standard_bot.entrypoints.mvp_backtest`
- Legacy `cyqnt_trd/backtesting/*` still exists for compatibility, but is not the recommended path for new work

## Requirements

Key dependencies include:

- `pandas>=2.2.0`
- `polars>=1.0,<2.0`
- `numba>=0.60,<0.62`
- `pyarrow>=16.1.0`
- `requests>=2.32.0`

Binance SDK dependencies:

- `binance-sdk-spot`
- `binance-sdk-derivatives-trading-usds-futures`
- `binance-sdk-algo`
- `binance-common`

## License

MIT License
