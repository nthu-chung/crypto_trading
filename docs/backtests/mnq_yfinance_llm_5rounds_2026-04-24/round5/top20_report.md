# Round 5 Top 20 Report

- Population size: `50`
- Family cap: `4`

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r5_c01` | `price_moving_average` | 6.1799 | 13.3346% | 3.3198% | 58 | `{"entry_threshold": 0.001, "period": 55}` |
| 2 | `r5_c02` | `price_moving_average` | 5.7141 | 12.5340% | 3.8392% | 23 | `{"entry_threshold": 0.0015, "period": 52}` |
| 3 | `r5_c03` | `price_moving_average` | 5.6514 | 11.9016% | 3.3853% | 51 | `{"entry_threshold": 0.001, "period": 54}` |
| 4 | `r5_c04` | `price_moving_average` | 5.5424 | 10.4998% | 2.9984% | 63 | `{"entry_threshold": 0.001, "period": 49}` |
| 5 | `r5_c45` | `moving_average_cross` | 5.4773 | 9.8945% | 4.4843% | 136 | `{"entry_threshold": 0.0005, "fast_window": 40, "slow_window": 69}` |
| 6 | `r5_c05` | `moving_average_cross` | 5.1393 | 9.8855% | 5.9975% | 180 | `{"entry_threshold": 0.0, "fast_window": 37, "slow_window": 79}` |
| 7 | `r5_c06` | `moving_average_cross` | 4.9812 | 9.6089% | 4.6987% | 142 | `{"entry_threshold": 0.0, "fast_window": 34, "slow_window": 104}` |
| 8 | `r5_c07` | `moving_average_cross` | 4.9536 | 9.6422% | 4.9152% | 155 | `{"entry_threshold": 0.0, "fast_window": 38, "slow_window": 94}` |
| 9 | `r5_c09` | `rsi_reversion` | 3.5135 | 9.4131% | 5.1043% | 426 | `{"overbought": 75.0, "oversold": 27.5, "period": 10}` |
| 10 | `r5_c30` | `atr_breakout` | 3.4897 | 10.8193% | 7.3457% | 110 | `{"atr_multiplier": 2.75, "atr_period": 18, "ma_period": 73}` |
| 11 | `r5_c10` | `atr_breakout` | 3.1326 | 9.0252% | 6.5676% | 128 | `{"atr_multiplier": 2.5, "atr_period": 22, "ma_period": 78}` |
| 12 | `r5_c11` | `bollinger_mean_reversion` | 3.0472 | 10.0954% | 8.2017% | 728 | `{"period": 12, "stddev_multiplier": 1.5}` |
| 13 | `r5_c12` | `atr_breakout` | 2.6213 | 7.5867% | 6.9631% | 110 | `{"atr_multiplier": 3.0, "atr_period": 21, "ma_period": 80}` |
| 14 | `r5_c13` | `rsi_reversion` | 2.6001 | 5.8336% | 3.9109% | 650 | `{"overbought": 60.0, "oversold": 30.0, "period": 10}` |
| 15 | `r5_c14` | `atr_breakout` | 2.5840 | 7.0670% | 6.1299% | 126 | `{"atr_multiplier": 2.5, "atr_period": 19, "ma_period": 90}` |
| 16 | `r5_c15` | `rsi_reversion` | 2.5225 | 5.3794% | 3.8880% | 412 | `{"overbought": 70.0, "oversold": 20.0, "period": 9}` |
| 17 | `r5_c40` | `multi_timeframe_ma_spread` | 2.5195 | 6.9442% | 6.3773% | 113 | `{"primary_ma_period": 18, "reference_ma_period": 34, "spread_threshold_bps": 10.0}` |
| 18 | `r5_c17` | `rsi_reversion` | 2.4999 | 6.1767% | 4.9242% | 600 | `{"overbought": 70.0, "oversold": 30.0, "period": 9}` |
| 19 | `r5_c39` | `multi_timeframe_ma_spread` | 2.2652 | 6.1120% | 9.2817% | 106 | `{"primary_ma_period": 11, "reference_ma_period": 17, "spread_threshold_bps": 20.0}` |
| 20 | `r5_c18` | `bollinger_mean_reversion` | 1.5214 | 4.6881% | 7.7073% | 835 | `{"period": 10, "stddev_multiplier": 1.5}` |
