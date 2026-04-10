# BTCUSDT 5m MA vs 1h MA Cross Backtest

## Strategy

- Strategy ID: `multi_timeframe_ma_spread`
- Market: `Binance Futures`
- Instrument: `BTCUSDT`
- Primary timeframe: `5m`
- Reference timeframe: `1h`
- Primary MA period: `20`
- Reference MA period: `20`
- Spread threshold: `0 bps`
- Decision rule:
  - If `MA_5m > MA_1h`, target position = `long`
  - If `MA_5m < MA_1h`, target position = `short`
- Execution model: signal at `5m` bar close, fill at next `5m` bar open
- Fee model: taker fee `10 bps`
- Funding: `0`
- Liquidity cap: `10%` of next bar volume

## Window

- Start: `2026-01-10 00:00:00 UTC`
- End: `2026-04-10 00:00:00 UTC`
- Source storage: local historical parquet, downloaded as `1m`, then resampled locally to `5m` and `1h`

## Result

- Total return: `-30.35%`
- Max drawdown: `-32.73%`
- Sharpe ratio: `-2.46`
- Win rate: `19.09%`
- Trade count: `242`
- Completed round trips used for win-rate calculation: `241`
- Final equity: `6964.98`

## Notes

- Sharpe is computed from `5m` equity returns and annualized with a `24/7 crypto` assumption: `sqrt(365 * 24 * 12)`.
- Win rate is computed from completed round trips, net of fees.
- This strategy currently performs poorly on the tested 90-day window and should not be used for live trading without further filtering or parameter work.
