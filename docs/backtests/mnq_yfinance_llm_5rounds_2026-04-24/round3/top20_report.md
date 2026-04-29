# Round 3 Top 20 Report

- Population size: `50`
- Family cap: `4`

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r3_c01` | `price_moving_average` | 6.1799 | 13.3346% | 3.3198% | 58 | `{"entry_threshold": 0.001, "period": 55}` |
| 2 | `r3_c47` | `price_moving_average` | 5.5424 | 10.4998% | 2.9984% | 63 | `{"entry_threshold": 0.001, "period": 49}` |
| 3 | `r3_c42` | `moving_average_cross` | 4.9812 | 9.6089% | 4.6987% | 142 | `{"entry_threshold": 0.0, "fast_window": 34, "slow_window": 104}` |
| 4 | `r3_c44` | `moving_average_cross` | 4.9098 | 9.6682% | 4.9127% | 120 | `{"entry_threshold": 0.0005, "fast_window": 32, "slow_window": 94}` |
| 5 | `r3_c02` | `moving_average_cross` | 4.8277 | 9.2712% | 5.1654% | 147 | `{"entry_threshold": 0.0, "fast_window": 37, "slow_window": 99}` |
| 6 | `r3_c03` | `price_moving_average` | 4.7859 | 12.1620% | 3.4801% | 168 | `{"entry_threshold": 0.0005, "period": 54}` |
| 7 | `r3_c23` | `price_moving_average` | 4.6271 | 9.1107% | 3.4051% | 62 | `{"entry_threshold": 0.001, "period": 51}` |
| 8 | `r3_c04` | `moving_average_cross` | 4.5838 | 9.2014% | 4.7197% | 124 | `{"entry_threshold": 0.0005, "fast_window": 34, "slow_window": 89}` |
| 9 | `r3_c09` | `bollinger_mean_reversion` | 3.0472 | 10.0954% | 8.2017% | 728 | `{"period": 12, "stddev_multiplier": 1.5}` |
| 10 | `r3_c10` | `atr_breakout` | 2.6213 | 7.5867% | 6.9631% | 110 | `{"atr_multiplier": 3.0, "atr_period": 21, "ma_period": 80}` |
| 11 | `r3_c11` | `rsi_reversion` | 2.6001 | 5.8336% | 3.9109% | 650 | `{"overbought": 60.0, "oversold": 30.0, "period": 10}` |
| 12 | `r3_c12` | `atr_breakout` | 2.5840 | 7.0670% | 6.1299% | 126 | `{"atr_multiplier": 2.5, "atr_period": 19, "ma_period": 90}` |
| 13 | `r3_c13` | `rsi_reversion` | 2.5225 | 5.3794% | 3.8880% | 412 | `{"overbought": 70.0, "oversold": 20.0, "period": 9}` |
| 14 | `r3_c32` | `atr_breakout` | 2.5126 | 7.1018% | 6.3530% | 141 | `{"atr_multiplier": 2.25, "atr_period": 15, "ma_period": 88}` |
| 15 | `r3_c14` | `rsi_reversion` | 2.4999 | 6.1767% | 4.9242% | 600 | `{"overbought": 70.0, "oversold": 30.0, "period": 9}` |
| 16 | `r3_c15` | `rsi_reversion` | 2.2004 | 5.2302% | 4.4997% | 683 | `{"overbought": 75.0, "oversold": 25.0, "period": 7}` |
| 17 | `r3_c50` | `atr_breakout` | 1.9531 | 5.0396% | 8.3889% | 88 | `{"atr_multiplier": 3.5, "atr_period": 25, "ma_period": 85}` |
| 18 | `r3_c18` | `bollinger_mean_reversion` | 1.5214 | 4.6881% | 7.7073% | 835 | `{"period": 10, "stddev_multiplier": 1.5}` |
| 19 | `r3_c39` | `multi_timeframe_ma_spread` | 0.9899 | 2.7120% | 7.5740% | 85 | `{"primary_ma_period": 17, "reference_ma_period": 24, "spread_threshold_bps": 20.0}` |
| 20 | `r3_c19` | `multi_timeframe_ma_spread` | 0.9833 | 2.3622% | 6.9323% | 113 | `{"primary_ma_period": 20, "reference_ma_period": 34, "spread_threshold_bps": 10.0}` |
