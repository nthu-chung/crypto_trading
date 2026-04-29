# Round 4 Top 20 Report

- Population size: `50`
- Family cap: `5`

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r4_c01` | `donchian_breakout` | 2.4810 | 47.0799% | 19.8418% | 249 | `{"breakout_buffer_bps": 30.0, "lookback_window": 45}` |
| 2 | `r4_c22` | `multi_timeframe_ma_spread` | 2.0994 | 34.9010% | 23.8483% | 149 | `{"primary_ma_period": 20, "reference_ma_period": 28, "spread_threshold_bps": 45.0}` |
| 3 | `r4_c02` | `multi_timeframe_ma_spread` | 1.9415 | 31.2099% | 19.6807% | 158 | `{"primary_ma_period": 17, "reference_ma_period": 33, "spread_threshold_bps": 40.0}` |
| 4 | `r4_c50` | `multi_timeframe_ma_spread` | 1.8747 | 29.5981% | 21.4764% | 164 | `{"primary_ma_period": 15, "reference_ma_period": 30, "spread_threshold_bps": 15.0}` |
| 5 | `r4_c03` | `donchian_breakout` | 1.8603 | 31.2977% | 22.8144% | 116 | `{"breakout_buffer_bps": 50.0, "lookback_window": 55}` |
| 6 | `r4_c30` | `multi_timeframe_ma_spread` | 1.8145 | 28.3754% | 19.8207% | 143 | `{"primary_ma_period": 19, "reference_ma_period": 33, "spread_threshold_bps": 40.0}` |
| 7 | `r4_c27` | `donchian_breakout` | 1.8005 | 29.9220% | 20.6736% | 254 | `{"breakout_buffer_bps": 25.0, "lookback_window": 62}` |
| 8 | `r4_c04` | `donchian_breakout` | 1.7122 | 27.8784% | 25.5803% | 245 | `{"breakout_buffer_bps": 25.0, "lookback_window": 67}` |
| 9 | `r4_c05` | `donchian_breakout` | 1.7107 | 27.7557% | 22.8144% | 112 | `{"breakout_buffer_bps": 50.0, "lookback_window": 60}` |
| 10 | `r4_c06` | `multi_timeframe_ma_spread` | 1.5975 | 23.6517% | 26.4034% | 155 | `{"primary_ma_period": 15, "reference_ma_period": 30, "spread_threshold_bps": 0.0}` |
| 11 | `r4_c32` | `moving_average_cross` | -1.5706 | -19.2559% | 31.8363% | 506 | `{"entry_threshold": 0.003, "fast_window": 29, "slow_window": 95}` |
| 12 | `r4_c31` | `moving_average_cross` | -1.6803 | -20.3267% | 31.6501% | 544 | `{"entry_threshold": 0.003, "fast_window": 27, "slow_window": 75}` |
| 13 | `r4_c11` | `moving_average_cross` | -1.8899 | -22.2967% | 32.8337% | 704 | `{"entry_threshold": 0.002, "fast_window": 24, "slow_window": 80}` |
| 14 | `r4_c12` | `moving_average_cross` | -1.9321 | -22.5527% | 32.0541% | 594 | `{"entry_threshold": 0.0025, "fast_window": 26, "slow_window": 90}` |
| 15 | `r4_c13` | `moving_average_cross` | -1.9565 | -22.9607% | 33.8956% | 765 | `{"entry_threshold": 0.0015, "fast_window": 20, "slow_window": 85}` |
| 16 | `r4_c40` | `price_moving_average` | -2.5636 | -31.7634% | 46.3695% | 340 | `{"entry_threshold": 0.003, "period": 7}` |
| 17 | `r4_c37` | `rsi_reversion` | -2.7495 | -35.4907% | 47.3384% | 132 | `{"overbought": 80.0, "oversold": 20.0, "period": 21}` |
| 18 | `r4_c16` | `rsi_reversion` | -2.7910 | -40.7317% | 46.8168% | 806 | `{"overbought": 80.0, "oversold": 35.0, "period": 15}` |
| 19 | `r4_c17` | `rsi_reversion` | -3.7494 | -40.1377% | 43.2315% | 367 | `{"overbought": 75.0, "oversold": 20.0, "period": 17}` |
| 20 | `r4_c18` | `rsi_reversion` | -3.9315 | -41.5088% | 43.3641% | 833 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
