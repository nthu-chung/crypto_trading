# Round 3 Top 20 Report

- Population size: `50`
- Family cap: `5`

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r3_c01` | `donchian_breakout` | 2.4810 | 47.0799% | 19.8418% | 249 | `{"breakout_buffer_bps": 30.0, "lookback_window": 45}` |
| 2 | `r3_c48` | `multi_timeframe_ma_spread` | 1.9415 | 31.2099% | 19.6807% | 158 | `{"primary_ma_period": 17, "reference_ma_period": 33, "spread_threshold_bps": 40.0}` |
| 3 | `r3_c46` | `donchian_breakout` | 1.8603 | 31.2977% | 22.8144% | 116 | `{"breakout_buffer_bps": 50.0, "lookback_window": 55}` |
| 4 | `r3_c02` | `donchian_breakout` | 1.7122 | 27.8784% | 25.5803% | 245 | `{"breakout_buffer_bps": 25.0, "lookback_window": 67}` |
| 5 | `r3_c03` | `donchian_breakout` | 1.7107 | 27.7557% | 22.8144% | 112 | `{"breakout_buffer_bps": 50.0, "lookback_window": 60}` |
| 6 | `r3_c04` | `multi_timeframe_ma_spread` | 1.5975 | 23.6517% | 26.4034% | 155 | `{"primary_ma_period": 15, "reference_ma_period": 30, "spread_threshold_bps": 0.0}` |
| 7 | `r3_c05` | `donchian_breakout` | 1.5752 | 24.6892% | 26.0907% | 211 | `{"breakout_buffer_bps": 30.0, "lookback_window": 67}` |
| 8 | `r3_c30` | `multi_timeframe_ma_spread` | 1.3149 | 17.1948% | 37.4512% | 90 | `{"primary_ma_period": 18, "reference_ma_period": 70, "spread_threshold_bps": 30.0}` |
| 9 | `r3_c07` | `multi_timeframe_ma_spread` | 1.1800 | 15.2005% | 31.7224% | 125 | `{"primary_ma_period": 19, "reference_ma_period": 52, "spread_threshold_bps": 40.0}` |
| 10 | `r3_c08` | `multi_timeframe_ma_spread` | 1.0852 | 13.3582% | 26.9683% | 169 | `{"primary_ma_period": 14, "reference_ma_period": 35, "spread_threshold_bps": 20.0}` |
| 11 | `r3_c11` | `moving_average_cross` | -1.8899 | -22.2967% | 32.8337% | 704 | `{"entry_threshold": 0.002, "fast_window": 24, "slow_window": 80}` |
| 12 | `r3_c31` | `moving_average_cross` | -1.9321 | -22.5527% | 32.0541% | 594 | `{"entry_threshold": 0.0025, "fast_window": 26, "slow_window": 90}` |
| 13 | `r3_c12` | `moving_average_cross` | -1.9565 | -22.9607% | 33.8956% | 765 | `{"entry_threshold": 0.0015, "fast_window": 20, "slow_window": 85}` |
| 14 | `r3_c13` | `moving_average_cross` | -2.3416 | -26.3858% | 34.7008% | 786 | `{"entry_threshold": 0.0015, "fast_window": 17, "slow_window": 85}` |
| 15 | `r3_c35` | `moving_average_cross` | -2.3421 | -26.0986% | 35.5497% | 650 | `{"entry_threshold": 0.0015, "fast_window": 25, "slow_window": 105}` |
| 16 | `r3_c37` | `rsi_reversion` | -2.7910 | -40.7317% | 46.8168% | 806 | `{"overbought": 80.0, "oversold": 35.0, "period": 15}` |
| 17 | `r3_c38` | `rsi_reversion` | -3.7494 | -40.1377% | 43.2315% | 367 | `{"overbought": 75.0, "oversold": 20.0, "period": 17}` |
| 18 | `r3_c16` | `rsi_reversion` | -3.9315 | -41.5088% | 43.3641% | 833 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 19 | `r3_c17` | `rsi_reversion` | -4.1579 | -49.0106% | 51.5055% | 1406 | `{"overbought": 75.0, "oversold": 30.0, "period": 13}` |
| 20 | `r3_c40` | `price_moving_average` | -4.6190 | -46.9388% | 51.1160% | 442 | `{"entry_threshold": 0.0025, "period": 8}` |
