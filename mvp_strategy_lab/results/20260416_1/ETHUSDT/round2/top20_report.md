# Round 2 Top 20 Report

- Population size: `50`
- Family cap: `5`

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r2_c29` | `donchian_breakout` | 2.4810 | 47.0799% | 19.8418% | 249 | `{"breakout_buffer_bps": 30.0, "lookback_window": 45}` |
| 2 | `r2_c27` | `donchian_breakout` | 1.7122 | 27.8784% | 25.5803% | 245 | `{"breakout_buffer_bps": 25.0, "lookback_window": 67}` |
| 3 | `r2_c22` | `donchian_breakout` | 1.7107 | 27.7557% | 22.8144% | 112 | `{"breakout_buffer_bps": 50.0, "lookback_window": 60}` |
| 4 | `r2_c01` | `multi_timeframe_ma_spread` | 1.5975 | 23.6517% | 26.4034% | 155 | `{"primary_ma_period": 15, "reference_ma_period": 30, "spread_threshold_bps": 0.0}` |
| 5 | `r2_c42` | `donchian_breakout` | 1.5752 | 24.6892% | 26.0907% | 211 | `{"breakout_buffer_bps": 30.0, "lookback_window": 67}` |
| 6 | `r2_c02` | `donchian_breakout` | 1.4897 | 22.7266% | 23.0396% | 216 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 7 | `r2_c03` | `multi_timeframe_ma_spread` | 1.1800 | 15.2005% | 31.7224% | 125 | `{"primary_ma_period": 19, "reference_ma_period": 52, "spread_threshold_bps": 40.0}` |
| 8 | `r2_c21` | `multi_timeframe_ma_spread` | 1.0852 | 13.3582% | 26.9683% | 169 | `{"primary_ma_period": 14, "reference_ma_period": 35, "spread_threshold_bps": 20.0}` |
| 9 | `r2_c04` | `multi_timeframe_ma_spread` | 1.0277 | 12.2308% | 32.7884% | 93 | `{"primary_ma_period": 25, "reference_ma_period": 55, "spread_threshold_bps": 10.0}` |
| 10 | `r2_c05` | `multi_timeframe_ma_spread` | 1.0252 | 12.2052% | 35.2912% | 104 | `{"primary_ma_period": 21, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 11 | `r2_c31` | `moving_average_cross` | -1.8899 | -22.2967% | 32.8337% | 704 | `{"entry_threshold": 0.002, "fast_window": 24, "slow_window": 80}` |
| 12 | `r2_c35` | `moving_average_cross` | -1.9565 | -22.9607% | 33.8956% | 765 | `{"entry_threshold": 0.0015, "fast_window": 20, "slow_window": 85}` |
| 13 | `r2_c33` | `moving_average_cross` | -2.3416 | -26.3858% | 34.7008% | 786 | `{"entry_threshold": 0.0015, "fast_window": 17, "slow_window": 85}` |
| 14 | `r2_c11` | `moving_average_cross` | -2.4233 | -27.3835% | 37.6770% | 955 | `{"entry_threshold": 0.001, "fast_window": 21, "slow_window": 75}` |
| 15 | `r2_c12` | `moving_average_cross` | -2.4455 | -27.2045% | 36.1604% | 661 | `{"entry_threshold": 0.002, "fast_window": 22, "slow_window": 95}` |
| 16 | `r2_c14` | `rsi_reversion` | -3.9315 | -41.5088% | 43.3641% | 833 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 17 | `r2_c40` | `rsi_reversion` | -4.1579 | -49.0106% | 51.5055% | 1406 | `{"overbought": 75.0, "oversold": 30.0, "period": 13}` |
| 18 | `r2_c36` | `rsi_reversion` | -5.0622 | -48.8823% | 49.9801% | 657 | `{"overbought": 70.0, "oversold": 25.0, "period": 18}` |
| 19 | `r2_c16` | `rsi_reversion` | -5.2353 | -54.2027% | 54.7710% | 1541 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
| 20 | `r2_c17` | `price_moving_average` | -5.4435 | -52.1673% | 54.6769% | 893 | `{"entry_threshold": 0.0015, "period": 9}` |
