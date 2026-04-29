# Round 2 Top 20 Report

- Population size: `50`
- Family cap: `5`

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r2_c21` | `donchian_breakout` | 3.6157 | 58.1413% | 19.1910% | 95 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 2 | `r2_c01` | `donchian_breakout` | 1.6962 | 21.5874% | 27.4253% | 148 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 3 | `r2_c27` | `multi_timeframe_ma_spread` | 0.8113 | 7.3561% | 30.5089% | 74 | `{"primary_ma_period": 22, "reference_ma_period": 70, "spread_threshold_bps": 50.0}` |
| 4 | `r2_c23` | `multi_timeframe_ma_spread` | 0.3008 | 0.4902% | 23.8181% | 79 | `{"primary_ma_period": 25, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 5 | `r2_c02` | `donchian_breakout` | 0.2473 | -0.4669% | 27.5863% | 338 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 6 | `r2_c29` | `donchian_breakout` | 0.0389 | -3.2747% | 32.9503% | 171 | `{"breakout_buffer_bps": 30.0, "lookback_window": 45}` |
| 7 | `r2_c03` | `multi_timeframe_ma_spread` | -0.1297 | -4.9402% | 30.9595% | 119 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 8 | `r2_c22` | `donchian_breakout` | -0.2436 | -7.0208% | 23.7214% | 395 | `{"breakout_buffer_bps": 10.0, "lookback_window": 67}` |
| 9 | `r2_c47` | `multi_timeframe_ma_spread` | -0.3429 | -7.5145% | 34.7930% | 97 | `{"primary_ma_period": 18, "reference_ma_period": 58, "spread_threshold_bps": 30.0}` |
| 10 | `r2_c04` | `multi_timeframe_ma_spread` | -0.6201 | -11.0834% | 32.2154% | 367 | `{"primary_ma_period": 5, "reference_ma_period": 22, "spread_threshold_bps": 20.0}` |
| 11 | `r2_c30` | `moving_average_cross` | -1.7108 | -15.6087% | 19.5592% | 417 | `{"entry_threshold": 0.0025, "fast_window": 23, "slow_window": 100}` |
| 12 | `r2_c50` | `moving_average_cross` | -2.2933 | -20.0511% | 25.1260% | 411 | `{"entry_threshold": 0.003, "fast_window": 23, "slow_window": 90}` |
| 13 | `r2_c10` | `moving_average_cross` | -2.6816 | -22.5187% | 28.1404% | 509 | `{"entry_threshold": 0.002, "fast_window": 22, "slow_window": 95}` |
| 14 | `r2_c36` | `rsi_reversion` | -3.2614 | -33.1825% | 40.9330% | 914 | `{"overbought": 72.5, "oversold": 35.0, "period": 19}` |
| 15 | `r2_c32` | `rsi_reversion` | -3.6577 | -35.4586% | 39.8875% | 732 | `{"overbought": 75.0, "oversold": 30.0, "period": 17}` |
| 16 | `r2_c12` | `rsi_reversion` | -3.8160 | -30.3388% | 33.5824% | 783 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 17 | `r2_c13` | `moving_average_cross` | -4.3204 | -33.4226% | 34.6653% | 768 | `{"entry_threshold": 0.001, "fast_window": 20, "slow_window": 80}` |
| 18 | `r2_c34` | `moving_average_cross` | -4.3790 | -33.4596% | 35.1526% | 604 | `{"entry_threshold": 0.002, "fast_window": 23, "slow_window": 70}` |
| 19 | `r2_c38` | `rsi_reversion` | -5.1651 | -41.4939% | 43.6047% | 963 | `{"overbought": 70.0, "oversold": 30.0, "period": 17}` |
| 20 | `r2_c15` | `rsi_reversion` | -5.5360 | -44.3946% | 45.1756% | 1373 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
