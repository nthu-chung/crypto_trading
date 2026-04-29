# Round 1 Top 20 Report

- Population size: `50`
- Family cap: `4`

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r1_c13` | `price_moving_average` | 6.1799 | 13.3346% | 3.3198% | 58 | `{"entry_threshold": 0.001, "period": 55}` |
| 2 | `r1_c07` | `moving_average_cross` | 4.5838 | 9.2014% | 4.7197% | 124 | `{"entry_threshold": 0.0005, "fast_window": 34, "slow_window": 89}` |
| 3 | `r1_c06` | `moving_average_cross` | 4.3748 | 10.8043% | 3.1442% | 198 | `{"entry_threshold": 0.0005, "fast_window": 20, "slow_window": 50}` |
| 4 | `r1_c10` | `price_moving_average` | 2.9486 | 5.3178% | 5.8540% | 609 | `{"entry_threshold": 0.0003, "period": 13}` |
| 5 | `r1_c12` | `price_moving_average` | 2.8010 | 6.8544% | 4.6911% | 217 | `{"entry_threshold": 0.0005, "period": 34}` |
| 6 | `r1_c43` | `atr_breakout` | 2.6213 | 7.5867% | 6.9631% | 110 | `{"atr_multiplier": 3.0, "atr_period": 21, "ma_period": 80}` |
| 7 | `r1_c16` | `rsi_reversion` | 2.4999 | 6.1767% | 4.9242% | 600 | `{"overbought": 70.0, "oversold": 30.0, "period": 9}` |
| 8 | `r1_c15` | `rsi_reversion` | 2.2004 | 5.2302% | 4.4997% | 683 | `{"overbought": 75.0, "oversold": 25.0, "period": 7}` |
| 9 | `r1_c11` | `price_moving_average` | 1.9690 | 4.6370% | 5.3515% | 294 | `{"entry_threshold": 0.0005, "period": 21}` |
| 10 | `r1_c03` | `moving_average_cross` | 1.8919 | 3.2787% | 5.7756% | 725 | `{"entry_threshold": 0.0, "fast_window": 8, "slow_window": 21}` |
| 11 | `r1_c42` | `atr_breakout` | 1.6766 | 4.7762% | 8.4746% | 155 | `{"atr_multiplier": 2.5, "atr_period": 21, "ma_period": 50}` |
| 12 | `r1_c44` | `bollinger_mean_reversion` | 1.5214 | 4.6881% | 7.7073% | 835 | `{"period": 10, "stddev_multiplier": 1.5}` |
| 13 | `r1_c05` | `moving_average_cross` | 1.1612 | 2.0316% | 5.8849% | 342 | `{"entry_threshold": 0.0003, "fast_window": 13, "slow_window": 34}` |
| 14 | `r1_c27` | `multi_timeframe_ma_spread` | 0.9833 | 2.3622% | 6.9323% | 113 | `{"primary_ma_period": 20, "reference_ma_period": 34, "spread_threshold_bps": 10.0}` |
| 15 | `r1_c46` | `bollinger_mean_reversion` | 0.7098 | 1.9740% | 8.2394% | 149 | `{"period": 30, "stddev_multiplier": 2.5}` |
| 16 | `r1_c14` | `rsi_reversion` | 0.5261 | 1.0560% | 7.0926% | 894 | `{"overbought": 80.0, "oversold": 20.0, "period": 5}` |
| 17 | `r1_c47` | `bollinger_mean_reversion` | 0.5046 | 1.2582% | 9.0287% | 62 | `{"period": 50, "stddev_multiplier": 3.0}` |
| 18 | `r1_c24` | `multi_timeframe_ma_spread` | 0.2326 | 0.3415% | 6.8465% | 141 | `{"primary_ma_period": 20, "reference_ma_period": 20, "spread_threshold_bps": 10.0}` |
| 19 | `r1_c18` | `rsi_reversion` | 0.0307 | -0.1376% | 6.3438% | 427 | `{"overbought": 65.0, "oversold": 35.0, "period": 14}` |
| 20 | `r1_c26` | `multi_timeframe_ma_spread` | -0.4170 | -1.3565% | 8.4537% | 277 | `{"primary_ma_period": 8, "reference_ma_period": 21, "spread_threshold_bps": 2.0}` |
