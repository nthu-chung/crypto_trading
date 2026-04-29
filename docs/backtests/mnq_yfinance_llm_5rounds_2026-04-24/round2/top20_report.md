# Round 2 Top 20 Report

- Population size: `50`
- Family cap: `4`

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r2_c01` | `price_moving_average` | 6.1799 | 13.3346% | 3.3198% | 58 | `{"entry_threshold": 0.001, "period": 55}` |
| 2 | `r2_c22` | `moving_average_cross` | 4.8277 | 9.2712% | 5.1654% | 147 | `{"entry_threshold": 0.0, "fast_window": 37, "slow_window": 99}` |
| 3 | `r2_c41` | `price_moving_average` | 4.7859 | 12.1620% | 3.4801% | 168 | `{"entry_threshold": 0.0005, "period": 54}` |
| 4 | `r2_c02` | `moving_average_cross` | 4.5838 | 9.2014% | 4.7197% | 124 | `{"entry_threshold": 0.0005, "fast_window": 34, "slow_window": 89}` |
| 5 | `r2_c03` | `moving_average_cross` | 4.3748 | 10.8043% | 3.1442% | 198 | `{"entry_threshold": 0.0005, "fast_window": 20, "slow_window": 50}` |
| 6 | `r2_c23` | `moving_average_cross` | 4.3509 | 9.3658% | 6.8969% | 96 | `{"entry_threshold": 0.0015, "fast_window": 19, "slow_window": 60}` |
| 7 | `r2_c21` | `price_moving_average` | 4.0797 | 6.8483% | 2.9178% | 61 | `{"entry_threshold": 0.001, "period": 50}` |
| 8 | `r2_c29` | `price_moving_average` | 3.6029 | 7.9871% | 7.4059% | 110 | `{"entry_threshold": 0.001, "period": 18}` |
| 9 | `r2_c32` | `bollinger_mean_reversion` | 3.0472 | 10.0954% | 8.2017% | 728 | `{"period": 12, "stddev_multiplier": 1.5}` |
| 10 | `r2_c06` | `atr_breakout` | 2.6213 | 7.5867% | 6.9631% | 110 | `{"atr_multiplier": 3.0, "atr_period": 21, "ma_period": 80}` |
| 11 | `r2_c39` | `rsi_reversion` | 2.6001 | 5.8336% | 3.9109% | 650 | `{"overbought": 60.0, "oversold": 30.0, "period": 10}` |
| 12 | `r2_c26` | `atr_breakout` | 2.5840 | 7.0670% | 6.1299% | 126 | `{"atr_multiplier": 2.5, "atr_period": 19, "ma_period": 90}` |
| 13 | `r2_c28` | `rsi_reversion` | 2.5225 | 5.3794% | 3.8880% | 412 | `{"overbought": 70.0, "oversold": 20.0, "period": 9}` |
| 14 | `r2_c07` | `rsi_reversion` | 2.4999 | 6.1767% | 4.9242% | 600 | `{"overbought": 70.0, "oversold": 30.0, "period": 9}` |
| 15 | `r2_c08` | `rsi_reversion` | 2.2004 | 5.2302% | 4.4997% | 683 | `{"overbought": 75.0, "oversold": 25.0, "period": 7}` |
| 16 | `r2_c11` | `atr_breakout` | 1.6766 | 4.7762% | 8.4746% | 155 | `{"atr_multiplier": 2.5, "atr_period": 21, "ma_period": 50}` |
| 17 | `r2_c31` | `atr_breakout` | 1.5663 | 4.3084% | 7.3015% | 154 | `{"atr_multiplier": 2.5, "atr_period": 17, "ma_period": 52}` |
| 18 | `r2_c12` | `bollinger_mean_reversion` | 1.5214 | 4.6881% | 7.7073% | 835 | `{"period": 10, "stddev_multiplier": 1.5}` |
| 19 | `r2_c14` | `multi_timeframe_ma_spread` | 0.9833 | 2.3622% | 6.9323% | 113 | `{"primary_ma_period": 20, "reference_ma_period": 34, "spread_threshold_bps": 10.0}` |
| 20 | `r2_c15` | `bollinger_mean_reversion` | 0.7098 | 1.9740% | 8.2394% | 149 | `{"period": 30, "stddev_multiplier": 2.5}` |
