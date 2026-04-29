# Round 4 Top 20 Report

- Population size: `50`
- Family cap: `4`

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r4_c01` | `price_moving_average` | 6.1799 | 13.3346% | 3.3198% | 58 | `{"entry_threshold": 0.001, "period": 55}` |
| 2 | `r4_c22` | `price_moving_average` | 5.7141 | 12.5340% | 3.8392% | 23 | `{"entry_threshold": 0.0015, "period": 52}` |
| 3 | `r4_c47` | `price_moving_average` | 5.6514 | 11.9016% | 3.3853% | 51 | `{"entry_threshold": 0.001, "period": 54}` |
| 4 | `r4_c02` | `price_moving_average` | 5.5424 | 10.4998% | 2.9984% | 63 | `{"entry_threshold": 0.001, "period": 49}` |
| 5 | `r4_c48` | `moving_average_cross` | 5.1393 | 9.8855% | 5.9975% | 180 | `{"entry_threshold": 0.0, "fast_window": 37, "slow_window": 79}` |
| 6 | `r4_c03` | `moving_average_cross` | 4.9812 | 9.6089% | 4.6987% | 142 | `{"entry_threshold": 0.0, "fast_window": 34, "slow_window": 104}` |
| 7 | `r4_c45` | `moving_average_cross` | 4.9536 | 9.6422% | 4.9152% | 155 | `{"entry_threshold": 0.0, "fast_window": 38, "slow_window": 94}` |
| 8 | `r4_c04` | `moving_average_cross` | 4.9098 | 9.6682% | 4.9127% | 120 | `{"entry_threshold": 0.0005, "fast_window": 32, "slow_window": 94}` |
| 9 | `r4_c35` | `rsi_reversion` | 3.5135 | 9.4131% | 5.1043% | 426 | `{"overbought": 75.0, "oversold": 27.5, "period": 10}` |
| 10 | `r4_c50` | `atr_breakout` | 3.1326 | 9.0252% | 6.5676% | 128 | `{"atr_multiplier": 2.5, "atr_period": 22, "ma_period": 78}` |
| 11 | `r4_c09` | `bollinger_mean_reversion` | 3.0472 | 10.0954% | 8.2017% | 728 | `{"period": 12, "stddev_multiplier": 1.5}` |
| 12 | `r4_c10` | `atr_breakout` | 2.6213 | 7.5867% | 6.9631% | 110 | `{"atr_multiplier": 3.0, "atr_period": 21, "ma_period": 80}` |
| 13 | `r4_c11` | `rsi_reversion` | 2.6001 | 5.8336% | 3.9109% | 650 | `{"overbought": 60.0, "oversold": 30.0, "period": 10}` |
| 14 | `r4_c12` | `atr_breakout` | 2.5840 | 7.0670% | 6.1299% | 126 | `{"atr_multiplier": 2.5, "atr_period": 19, "ma_period": 90}` |
| 15 | `r4_c13` | `rsi_reversion` | 2.5225 | 5.3794% | 3.8880% | 412 | `{"overbought": 70.0, "oversold": 20.0, "period": 9}` |
| 16 | `r4_c32` | `atr_breakout` | 2.5133 | 7.1954% | 6.7232% | 133 | `{"atr_multiplier": 2.25, "atr_period": 15, "ma_period": 92}` |
| 17 | `r4_c15` | `rsi_reversion` | 2.4999 | 6.1767% | 4.9242% | 600 | `{"overbought": 70.0, "oversold": 30.0, "period": 9}` |
| 18 | `r4_c18` | `bollinger_mean_reversion` | 1.5214 | 4.6881% | 7.7073% | 835 | `{"period": 10, "stddev_multiplier": 1.5}` |
| 19 | `r4_c39` | `multi_timeframe_ma_spread` | 1.2321 | 3.1957% | 8.4216% | 97 | `{"primary_ma_period": 16, "reference_ma_period": 22, "spread_threshold_bps": 20.0}` |
| 20 | `r4_c19` | `multi_timeframe_ma_spread` | 0.9899 | 2.7120% | 7.5740% | 85 | `{"primary_ma_period": 17, "reference_ma_period": 24, "spread_threshold_bps": 20.0}` |
