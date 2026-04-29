# MNQ yfinance 5m/15m LLM Strategy Search Notes

## Experiment

- Data: yfinance `MNQ=F`
- Bars: `5m` primary and `15m` secondary
- Coverage used by full best replay: `2026-02-11 05:09:59 UTC` to `2026-04-23 16:44:59 UTC`
- Engine: `standard_bot -> NumbaBacktestRunner`
- Execution: signal on confirmed 5m close, fill on next 5m open
- Contract model: MNQ multiplier `2.0`, integer quantity step `1`
- Cost model: `0.25 bps` per side + `0.60` fixed fee per contract per side + `0.10 bps` slippage

## Best Candidate

- Strategy: `price_moving_average`
- Period: `55`
- Entry threshold: `0.001`, equal to `0.10%`
- Full replay return: `13.3346%`
- Full replay final equity: `113334.55`
- Full replay max drawdown: `3.3198%`
- Full replay trades: `58`
- Full replay win rate: `55.17%`
- Recent 30% replay return: `6.5477%`
- Recent 30% replay max drawdown: `1.9244%`
- Recent 30% replay trades: `10`

## Manual Signal Rule

Use only confirmed 5m candles.

At each 5m close:

1. Compute `SMA55_previous`, the average of the prior 55 completed 5m closes, excluding the current close.
2. Compute the prior bar's same style moving average, `SMA55_prior_previous`.
3. Buy signal:
   - previous 5m close was `<= SMA55_prior_previous`
   - current 5m close is `> SMA55_previous`
   - `(current_close - SMA55_previous) / SMA55_previous > 0.001`
4. Exit long signal:
   - previous 5m close was `>= SMA55_prior_previous`
   - current 5m close is `< SMA55_previous`
   - `(SMA55_previous - current_close) / SMA55_previous > 0.001`
5. Execution assumption:
   - enter or exit at the next 5m candle open.

This best candidate is long/flat, not short. A sell signal means close the long position, not open a short.

## Latest State In Data

- Last yfinance 5m bar in local data: `2026-04-23 16:44:59 UTC`
- Last close: `27100.25`
- Last `SMA55_previous`: `27057.1091`
- Last spread: `0.1594%`
- Latest bar did not create a fresh buy or exit cross.
- Last actual signal in the replay was an exit-long signal at `2026-04-23 00:09:59 UTC`, executed at the next 5m open.
- Ending replay position: flat.

## Risk Notes

- yfinance/Yahoo is suitable for research and recent-data smoke tests, not production live trading.
- This experiment optimized over one recent sample. Treat the result as a candidate rule, not a finished trading system.
- The backtest does not include exchange session rules, macro-news filters, manual hesitation, rejected orders, or live-data latency.
- If paper trading this manually, start with `1` MNQ contract and track slippage, missed fills, and whether signals remain clear in real time.
