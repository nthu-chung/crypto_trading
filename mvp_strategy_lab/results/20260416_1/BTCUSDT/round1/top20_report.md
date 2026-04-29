# Round 1 Top 20 Report

- Population size: `50`
- Family cap: `5`

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r1_c49` | `donchian_breakout` | 1.6962 | 21.5874% | 27.4253% | 148 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 2 | `r1_c40` | `donchian_breakout` | 0.2473 | -0.4669% | 27.5863% | 338 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 3 | `r1_c08` | `multi_timeframe_ma_spread` | -0.1297 | -4.9402% | 30.9595% | 119 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 4 | `r1_c17` | `multi_timeframe_ma_spread` | -0.6201 | -11.0834% | 32.2154% | 367 | `{"primary_ma_period": 5, "reference_ma_period": 22, "spread_threshold_bps": 20.0}` |
| 5 | `r1_c47` | `multi_timeframe_ma_spread` | -0.7282 | -12.0953% | 35.1636% | 104 | `{"primary_ma_period": 19, "reference_ma_period": 52, "spread_threshold_bps": 40.0}` |
| 6 | `r1_c38` | `multi_timeframe_ma_spread` | -0.8714 | -13.6337% | 36.3283% | 105 | `{"primary_ma_period": 23, "reference_ma_period": 55, "spread_threshold_bps": 20.0}` |
| 7 | `r1_c28` | `multi_timeframe_ma_spread` | -0.8853 | -13.8147% | 36.4572% | 90 | `{"primary_ma_period": 21, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 8 | `r1_c20` | `donchian_breakout` | -0.9965 | -16.2469% | 32.3411% | 403 | `{"breakout_buffer_bps": 10.0, "lookback_window": 65}` |
| 9 | `r1_c10` | `donchian_breakout` | -1.9221 | -26.3494% | 40.4562% | 446 | `{"breakout_buffer_bps": 10.0, "lookback_window": 55}` |
| 10 | `r1_c13` | `moving_average_cross` | -2.6816 | -22.5187% | 28.1404% | 509 | `{"entry_threshold": 0.002, "fast_window": 22, "slow_window": 95}` |
| 11 | `r1_c30` | `donchian_breakout` | -3.6580 | -42.2029% | 43.5453% | 707 | `{"breakout_buffer_bps": 0.0, "lookback_window": 65}` |
| 12 | `r1_c15` | `rsi_reversion` | -3.8160 | -30.3388% | 33.5824% | 783 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 13 | `r1_c03` | `moving_average_cross` | -4.3204 | -33.4226% | 34.6653% | 768 | `{"entry_threshold": 0.001, "fast_window": 20, "slow_window": 80}` |
| 14 | `r1_c33` | `moving_average_cross` | -4.8654 | -36.8236% | 38.1461% | 802 | `{"entry_threshold": 0.001, "fast_window": 21, "slow_window": 75}` |
| 15 | `r1_c05` | `rsi_reversion` | -5.5360 | -44.3946% | 45.1756% | 1373 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
| 16 | `r1_c35` | `rsi_reversion` | -5.8727 | -48.6186% | 49.5008% | 1529 | `{"overbought": 70.0, "oversold": 35.0, "period": 15}` |
| 17 | `r1_c12` | `moving_average_cross` | -6.2837 | -44.5821% | 45.6250% | 1183 | `{"entry_threshold": 0.001, "fast_window": 8, "slow_window": 55}` |
| 18 | `r1_c25` | `rsi_reversion` | -6.5085 | -50.9000% | 51.8592% | 1378 | `{"overbought": 70.0, "oversold": 32.5, "period": 15}` |
| 19 | `r1_c23` | `moving_average_cross` | -6.5181 | -45.1253% | 46.4828% | 962 | `{"entry_threshold": 0.0005, "fast_window": 19, "slow_window": 70}` |
| 20 | `r1_c36` | `price_moving_average` | -7.0831 | -49.6337% | 51.2682% | 648 | `{"entry_threshold": 0.0015, "period": 9}` |
