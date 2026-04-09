# Standard Bot MVP

This MVP chooses the smallest architecture slice that still matches the
`standard_trading_bot_pdf.md` design direction:

- Data: market-only adapter plus PIT-aligned historical snapshots
- Signal: plugin-based moving-average-cross strategy
- Simulation: snapshot-driven backtest runner
- Runtime/Execution: step-based paper runner sharing the same signal plugin

## Virtual environment

The dedicated environment for this MVP is:

```bash
.venv-standard-bot
```

Activate it with:

```bash
source .venv-standard-bot/bin/activate
```

## Run the MVP

Fetch public Binance spot klines and run a moving-average-cross backtest:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest \
  --symbol BTCUSDT \
  --interval 1h \
  --limit 300 \
  --fast-window 5 \
  --slow-window 20 \
  --commission-bps 10
```

Switch strategy with `--strategy`:

- `moving_average_cross`
- `price_moving_average`
- `rsi_reversion`

Example:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest \
  --strategy rsi_reversion \
  --symbol BTCUSDT \
  --interval 1h \
  --limit 300 \
  --rsi-period 14 \
  --oversold 30 \
  --overbought 70
```

Run from an existing JSON export:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest \
  --input-json path/to/BTCUSDT_data.json \
  --symbol BTCUSDT \
  --interval 1h
```

Run one paper-execution cycle with the same signal plugin:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_paper \
  --symbol BTCUSDT \
  --interval 1h \
  --limit 120 \
  --strategy price_moving_average \
  --ma-period 5 \
  --max-position-pct 0.5
```

Validate Binance futures testnet connectivity from `.env`:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_testnet_execution \
  --env-file /Users/hankchung/Dev/crypto_trading-main/.env \
  --sync-account
```

Validate an order without placing it:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_testnet_execution \
  --env-file /Users/hankchung/Dev/crypto_trading-main/.env \
  --validate-order \
  --symbol BTCUSDT \
  --side buy \
  --notional 110
```

Run an isolated round-trip testnet trade on a clean symbol:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_testnet_roundtrip \
  --env-file /Users/hankchung/Dev/crypto_trading-main/.env \
  --symbol XRPUSDT \
  --side buy \
  --notional 10
```

## Files added for the MVP

- `cyqnt_trd/standard_bot/data/adapters.py`
- `cyqnt_trd/standard_bot/data/snapshot.py`
- `cyqnt_trd/standard_bot/signal/plugins.py`
- `cyqnt_trd/standard_bot/signal/registry.py`
- `cyqnt_trd/standard_bot/simulation/runner.py`
- `cyqnt_trd/standard_bot/entrypoints/mvp_backtest.py`
- `cyqnt_trd/standard_bot/execution/paper.py`
- `cyqnt_trd/standard_bot/runtime/runner.py`
- `cyqnt_trd/standard_bot/entrypoints/mvp_paper.py`
