# Standard Bot MVP

This MVP chooses the smallest architecture slice that still matches the
`standard_trading_bot_pdf.md` design direction:

- Data: market-only adapter plus PIT-aligned historical snapshots
- Signal: plugin-based strategy layer with Python encoders and shared Numba kernels
- Simulation: snapshot runner plus a Numba-backed conservative execution kernel
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

Use local historical parquet storage first, and allow remote API as an explicit fallback:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest \
  --engine numba \
  --symbol BTCUSDT \
  --interval 1h \
  --limit 300 \
  --allow-remote-api \
  --fast-window 5 \
  --slow-window 20 \
  --taker-fee-bps 10 \
  --slippage-bps 5 \
  --impact-slippage-bps 15 \
  --funding-bps-per-bar 1 \
  --max-bar-volume-fraction 0.05
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
  --allow-remote-api \
  --rsi-period 14 \
  --oversold 30 \
  --overbought 70
```

Run from an existing JSON export:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest \
  --engine numba \
  --input-json path/to/BTCUSDT_data.json \
  --symbol BTCUSDT \
  --interval 1h
```

Use `--engine python` if you need the older snapshot-driven runner for comparison.

## Local historical storage

For OpenClaw-style environments, the backtest CLI now supports a local-first history flow:

1. download historical bars in chunks
2. stream them into parquet
3. load parquet locally for backtests
4. resample `1m -> 5m / 1h` when needed

Seed local historical parquet and backtest from it:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest \
  --engine numba \
  --market-type futures \
  --strategy multi_timeframe_ma_spread \
  --symbol BTCUSDT \
  --interval 5m \
  --secondary-interval 1h \
  --primary-ma-period 3 \
  --reference-ma-period 3 \
  --spread-threshold-bps 0 \
  --historical-dir data/historical \
  --start-ts 1775520000000 \
  --end-ts 1775692800000 \
  --download-missing
```

Notes:

- `--historical-dir` is preferred over direct API fetches.
- If local parquet is missing, use `--download-missing` together with `--start-ts` and `--end-ts`.
- If you want the old ad hoc remote mode, add `--allow-remote-api`.
- The `numba` path now works directly from `MarketBundle` and does not eagerly build large snapshot lists.
- The parquet loader reads by time-filtered row groups and tail slices, so small OpenClaw-style machines do not need to load the full historical file into RAM for short-window runs.
- Resampled `5m / 1h` bars are built from raw `1m` `open_time / close_time`, and only full higher-timeframe buckets are emitted.

## Numba backtest assumptions

The `numba` engine is intentionally conservative:

- Decision time uses confirmed historical bars only.
- Signals generated on bar-close execute at the next bar open.
- Features only use historical windows. No future-return fields are used as inputs.
- Market-order fills use taker fees, configurable base slippage, and participation-based impact slippage.
- Liquidity is capped by `--max-bar-volume-fraction`, using both bar volume and quote volume when available.
- Funding can be charged per held bar with `--funding-bps-per-bar`.

This means the default `numba` path is a better fit for realistic strategy validation than the older same-bar-close fill model.

## Signal / Simulation Numba split

The current fast path follows the roadmap's "thin Python IO + single numerical kernel" pattern:

- Signal encoder: `DataSnapshot -> ndarray`
- Signal kernel: shared Numba kernels for MA / Price-MA / RSI
- Simulation kernel: Numba execution kernel for next-open fills, fees, slippage, and liquidity caps
- Plugin / Runner layer: Python only, responsible for config parsing and result packaging

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

Run `mvp_paper` from local historical parquet with the same `1m -> 5m / 1h` path:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_paper \
  --market-type futures \
  --strategy multi_timeframe_ma_spread \
  --symbol BTCUSDT \
  --interval 5m \
  --secondary-interval 1h \
  --primary-ma-period 3 \
  --reference-ma-period 3 \
  --spread-threshold-bps 0 \
  --historical-dir data/historical \
  --limit 96 \
  --dry-run
```

If local parquet is missing and you explicitly want live fallback, add `--allow-remote-api`.

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

## Managed background runs

For demos or long-running monitor processes, prefer the local run manager so each
background process gets a stable `run_id` and can later be stopped or killed by id.

Start a managed testnet MA demo:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager \
  start-testnet-ma-demo \
  --env-file .env \
  --duration-minutes 10 \
  --notional 10
```

List active managed runs:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager list
```

Inspect one run:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager \
  status \
  --run-id <run_id>
```

Gracefully stop one run by id:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager \
  stop \
  --run-id <run_id>
```

Force kill one run by id:

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_run_manager \
  kill \
  --run-id <run_id>
```

Notes:

- Managed metadata and logs are written under `.standard_bot_runs/`.
- `stop` sends `SIGTERM`; the testnet demo handles this gracefully and still runs its final close path.
- `kill` sends `SIGKILL`; use it only if graceful stop fails.

## Files added for the MVP

- `cyqnt_trd/standard_bot/data/adapters.py`
- `cyqnt_trd/standard_bot/data/downloader.py`
- `cyqnt_trd/standard_bot/data/historical.py`
- `cyqnt_trd/standard_bot/data/snapshot.py`
- `cyqnt_trd/standard_bot/signal/encoders.py`
- `cyqnt_trd/standard_bot/signal/plugins.py`
- `cyqnt_trd/standard_bot/signal/numba_kernels.py`
- `cyqnt_trd/standard_bot/signal/registry.py`
- `cyqnt_trd/standard_bot/simulation/execution_kernels.py`
- `cyqnt_trd/standard_bot/simulation/runner.py`
- `cyqnt_trd/standard_bot/simulation/numba_runner.py`
- `cyqnt_trd/standard_bot/entrypoints/mvp_backtest.py`
- `cyqnt_trd/standard_bot/execution/paper.py`
- `cyqnt_trd/standard_bot/runtime/runner.py`
- `cyqnt_trd/standard_bot/entrypoints/mvp_paper.py`
