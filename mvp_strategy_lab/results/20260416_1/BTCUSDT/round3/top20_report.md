# Round 3 Top 20 Report

- Population size: `50`
- Family cap: `5`

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r3_c01` | `donchian_breakout` | 3.6157 | 58.1413% | 19.1910% | 95 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 2 | `r3_c41` | `donchian_breakout` | 2.5582 | 36.7902% | 22.9539% | 99 | `{"breakout_buffer_bps": 40.0, "lookback_window": 58}` |
| 3 | `r3_c46` | `donchian_breakout` | 2.1396 | 29.1521% | 27.2363% | 101 | `{"breakout_buffer_bps": 40.0, "lookback_window": 55}` |
| 4 | `r3_c02` | `donchian_breakout` | 1.6962 | 21.5874% | 27.4253% | 148 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 5 | `r3_c23` | `multi_timeframe_ma_spread` | 1.2244 | 13.2600% | 26.4470% | 83 | `{"primary_ma_period": 23, "reference_ma_period": 65, "spread_threshold_bps": 70.0}` |
| 6 | `r3_c03` | `multi_timeframe_ma_spread` | 0.8113 | 7.3561% | 30.5089% | 74 | `{"primary_ma_period": 22, "reference_ma_period": 70, "spread_threshold_bps": 50.0}` |
| 7 | `r3_c24` | `multi_timeframe_ma_spread` | 0.5605 | 3.9286% | 24.6558% | 79 | `{"primary_ma_period": 24, "reference_ma_period": 62, "spread_threshold_bps": 60.0}` |
| 8 | `r3_c50` | `multi_timeframe_ma_spread` | 0.4289 | 2.1591% | 20.1719% | 227 | `{"primary_ma_period": 10, "reference_ma_period": 27, "spread_threshold_bps": 30.0}` |
| 9 | `r3_c04` | `multi_timeframe_ma_spread` | 0.3008 | 0.4902% | 23.8181% | 79 | `{"primary_ma_period": 25, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 10 | `r3_c05` | `donchian_breakout` | 0.2473 | -0.4669% | 27.5863% | 338 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 11 | `r3_c35` | `rsi_reversion` | -1.0403 | -13.4128% | 35.1398% | 333 | `{"overbought": 77.5, "oversold": 25.0, "period": 19}` |
| 12 | `r3_c31` | `moving_average_cross` | -1.2215 | -11.8356% | 17.8382% | 335 | `{"entry_threshold": 0.0035, "fast_window": 20, "slow_window": 115}` |
| 13 | `r3_c32` | `moving_average_cross` | -1.4310 | -13.5543% | 20.2304% | 369 | `{"entry_threshold": 0.003, "fast_window": 22, "slow_window": 105}` |
| 14 | `r3_c33` | `moving_average_cross` | -1.6575 | -15.1465% | 20.7508% | 413 | `{"entry_threshold": 0.0025, "fast_window": 20, "slow_window": 110}` |
| 15 | `r3_c11` | `moving_average_cross` | -1.7108 | -15.6087% | 19.5592% | 417 | `{"entry_threshold": 0.0025, "fast_window": 23, "slow_window": 100}` |
| 16 | `r3_c34` | `rsi_reversion` | -2.0816 | -26.4070% | 36.8319% | 278 | `{"overbought": 77.5, "oversold": 37.5, "period": 23}` |
| 17 | `r3_c12` | `moving_average_cross` | -2.2933 | -20.0511% | 25.1260% | 411 | `{"entry_threshold": 0.003, "fast_window": 23, "slow_window": 90}` |
| 18 | `r3_c14` | `rsi_reversion` | -3.2614 | -33.1825% | 40.9330% | 914 | `{"overbought": 72.5, "oversold": 35.0, "period": 19}` |
| 19 | `r3_c39` | `rsi_reversion` | -3.3755 | -28.0852% | 33.0385% | 597 | `{"overbought": 70.0, "oversold": 25.0, "period": 18}` |
| 20 | `r3_c15` | `rsi_reversion` | -3.6577 | -35.4586% | 39.8875% | 732 | `{"overbought": 75.0, "oversold": 30.0, "period": 17}` |
