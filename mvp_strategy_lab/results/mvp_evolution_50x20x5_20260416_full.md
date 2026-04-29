# LLM Strategy Evolution

- Symbol: `BTCUSDT`
- Primary timeframe: `5m`
- Secondary timeframe: `1h`
- Rounds: `5`
- Best strategy: `donchian_breakout`
- Best Sharpe: `3.1180`
- Best total return: `47.6803%`
- Best max drawdown: `16.7789%`
- Best trade count: `117`

## Round 1

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r1_c49` | `donchian_breakout` | 1.6796 | 21.2897% | 27.4253% | 147 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 2 | `r1_c40` | `donchian_breakout` | 0.6506 | 5.2527% | 27.5863% | 331 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 3 | `r1_c08` | `multi_timeframe_ma_spread` | -0.0417 | -3.8387% | 30.9595% | 123 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 4 | `r1_c20` | `donchian_breakout` | -0.4365 | -9.4348% | 29.9301% | 397 | `{"breakout_buffer_bps": 10.0, "lookback_window": 65}` |
| 5 | `r1_c47` | `multi_timeframe_ma_spread` | -0.4933 | -9.3496% | 35.1636% | 106 | `{"primary_ma_period": 19, "reference_ma_period": 52, "spread_threshold_bps": 40.0}` |
| 6 | `r1_c28` | `multi_timeframe_ma_spread` | -0.5903 | -10.4212% | 36.4572% | 94 | `{"primary_ma_period": 21, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 7 | `r1_c17` | `multi_timeframe_ma_spread` | -0.7565 | -12.6507% | 30.8071% | 366 | `{"primary_ma_period": 5, "reference_ma_period": 22, "spread_threshold_bps": 20.0}` |
| 8 | `r1_c38` | `multi_timeframe_ma_spread` | -0.9350 | -14.3094% | 36.3283% | 110 | `{"primary_ma_period": 23, "reference_ma_period": 55, "spread_threshold_bps": 20.0}` |
| 9 | `r1_c37` | `multi_timeframe_ma_spread` | -1.0531 | -16.0193% | 32.0312% | 251 | `{"primary_ma_period": 13, "reference_ma_period": 22, "spread_threshold_bps": 10.0}` |
| 10 | `r1_c10` | `donchian_breakout` | -1.3352 | -20.0218% | 39.1946% | 437 | `{"breakout_buffer_bps": 10.0, "lookback_window": 55}` |
| 11 | `r1_c18` | `multi_timeframe_ma_spread` | -1.6536 | -21.8837% | 38.3480% | 102 | `{"primary_ma_period": 25, "reference_ma_period": 55, "spread_threshold_bps": 10.0}` |
| 12 | `r1_c27` | `multi_timeframe_ma_spread` | -1.8910 | -24.5682% | 35.6079% | 199 | `{"primary_ma_period": 15, "reference_ma_period": 30, "spread_threshold_bps": 0.0}` |
| 13 | `r1_c13` | `moving_average_cross` | -2.8557 | -23.5672% | 29.7447% | 504 | `{"entry_threshold": 0.002, "fast_window": 22, "slow_window": 95}` |
| 14 | `r1_c46` | `multi_timeframe_ma_spread` | -3.1922 | -36.8292% | 38.7831% | 373 | `{"primary_ma_period": 7, "reference_ma_period": 18, "spread_threshold_bps": 5.0}` |
| 15 | `r1_c30` | `donchian_breakout` | -3.3814 | -39.8343% | 41.6256% | 712 | `{"breakout_buffer_bps": 0.0, "lookback_window": 65}` |
| 16 | `r1_c07` | `multi_timeframe_ma_spread` | -3.8423 | -42.0567% | 43.9621% | 310 | `{"primary_ma_period": 10, "reference_ma_period": 20, "spread_threshold_bps": 0.0}` |
| 17 | `r1_c03` | `moving_average_cross` | -3.9960 | -31.3292% | 34.6263% | 753 | `{"entry_threshold": 0.001, "fast_window": 20, "slow_window": 80}` |
| 18 | `r1_c15` | `rsi_reversion` | -4.2365 | -32.7339% | 34.7901% | 775 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 19 | `r1_c33` | `moving_average_cross` | -4.5523 | -34.8806% | 38.0912% | 789 | `{"entry_threshold": 0.001, "fast_window": 21, "slow_window": 75}` |
| 20 | `r1_c05` | `rsi_reversion` | -5.2653 | -42.7433% | 44.6432% | 1370 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
| 21 | `r1_c35` | `rsi_reversion` | -5.6647 | -47.3324% | 48.9998% | 1528 | `{"overbought": 70.0, "oversold": 35.0, "period": 15}` |
| 22 | `r1_c12` | `moving_average_cross` | -6.0915 | -43.4854% | 46.5840% | 1173 | `{"entry_threshold": 0.001, "fast_window": 8, "slow_window": 55}` |
| 23 | `r1_c23` | `moving_average_cross` | -6.2338 | -43.5600% | 46.7293% | 950 | `{"entry_threshold": 0.0005, "fast_window": 19, "slow_window": 70}` |
| 24 | `r1_c25` | `rsi_reversion` | -6.3387 | -49.9284% | 51.0359% | 1379 | `{"overbought": 70.0, "oversold": 32.5, "period": 15}` |
| 25 | `r1_c21` | `moving_average_cross` | -6.6766 | -47.2994% | 50.1795% | 1622 | `{"entry_threshold": 0.001, "fast_window": 7, "slow_window": 30}` |
| 26 | `r1_c36` | `price_moving_average` | -7.0294 | -49.2867% | 53.2810% | 639 | `{"entry_threshold": 0.0015, "period": 9}` |
| 27 | `r1_c26` | `price_moving_average` | -7.2462 | -52.1810% | 55.8579% | 856 | `{"entry_threshold": 0.001, "period": 13}` |
| 28 | `r1_c32` | `moving_average_cross` | -7.3989 | -50.3397% | 52.6993% | 1512 | `{"entry_threshold": 0.0005, "fast_window": 9, "slow_window": 45}` |
| 29 | `r1_c19` | `donchian_breakout` | -7.5269 | -66.2053% | 67.2415% | 1161 | `{"breakout_buffer_bps": 5.0, "lookback_window": 18}` |
| 30 | `r1_c22` | `moving_average_cross` | -7.7342 | -51.9699% | 54.0969% | 1676 | `{"entry_threshold": 0.0005, "fast_window": 11, "slow_window": 35}` |
| 31 | `r1_c02` | `moving_average_cross` | -7.7814 | -52.1019% | 54.4377% | 1586 | `{"entry_threshold": 0.0005, "fast_window": 10, "slow_window": 40}` |
| 32 | `r1_c29` | `donchian_breakout` | -8.6395 | -71.1411% | 71.4023% | 1552 | `{"breakout_buffer_bps": 0.0, "lookback_window": 22}` |
| 33 | `r1_c42` | `moving_average_cross` | -9.7657 | -60.3279% | 61.3857% | 2053 | `{"entry_threshold": 0.0, "fast_window": 8, "slow_window": 45}` |
| 34 | `r1_c09` | `donchian_breakout` | -9.9333 | -75.9341% | 76.1440% | 1673 | `{"breakout_buffer_bps": 0.0, "lookback_window": 20}` |
| 35 | `r1_c39` | `donchian_breakout` | -10.2690 | -77.0867% | 77.6613% | 1638 | `{"breakout_buffer_bps": 5.0, "lookback_window": 10}` |
| 36 | `r1_c48` | `donchian_breakout` | -11.0648 | -79.5470% | 79.8418% | 2009 | `{"breakout_buffer_bps": 0.0, "lookback_window": 15}` |
| 37 | `r1_c31` | `moving_average_cross` | -11.4329 | -66.4435% | 66.9693% | 2599 | `{"entry_threshold": 0.0, "fast_window": 8, "slow_window": 30}` |
| 38 | `r1_c11` | `moving_average_cross` | -11.5185 | -66.8351% | 68.0221% | 2591 | `{"entry_threshold": 0.0005, "fast_window": 4, "slow_window": 25}` |
| 39 | `r1_c50` | `moving_average_cross` | -13.3575 | -72.3503% | 73.3539% | 2650 | `{"entry_threshold": 0.001, "fast_window": 4, "slow_window": 10}` |
| 40 | `r1_c41` | `moving_average_cross` | -13.4874 | -72.8518% | 73.1347% | 3176 | `{"entry_threshold": 0.0, "fast_window": 6, "slow_window": 25}` |
| 41 | `r1_c04` | `rsi_reversion` | -13.9050 | -75.7535% | 75.8976% | 2702 | `{"overbought": 75.0, "oversold": 25.0, "period": 7}` |
| 42 | `r1_c44` | `rsi_reversion` | -14.8145 | -78.4196% | 78.5991% | 2928 | `{"overbought": 65.0, "oversold": 35.0, "period": 10}` |
| 43 | `r1_c43` | `rsi_reversion` | -16.6706 | -80.3832% | 80.3948% | 3399 | `{"overbought": 70.0, "oversold": 22.5, "period": 6}` |
| 44 | `r1_c01` | `moving_average_cross` | -17.2705 | -81.1635% | 81.2774% | 3906 | `{"entry_threshold": 0.0, "fast_window": 5, "slow_window": 20}` |
| 45 | `r1_c34` | `rsi_reversion` | -18.8054 | -86.0053% | 86.0547% | 3766 | `{"overbought": 80.0, "oversold": 22.5, "period": 5}` |
| 46 | `r1_c06` | `price_moving_average` | -18.9099 | -85.1021% | 85.6326% | 2085 | `{"entry_threshold": 0.0005, "period": 10}` |
| 47 | `r1_c16` | `price_moving_average` | -21.2934 | -87.7916% | 88.3363% | 2200 | `{"entry_threshold": 0.0005, "period": 9}` |
| 48 | `r1_c14` | `rsi_reversion` | -21.7657 | -88.7068% | 88.7466% | 4121 | `{"overbought": 75.0, "oversold": 22.5, "period": 5}` |
| 49 | `r1_c24` | `rsi_reversion` | -23.0413 | -89.8471% | 89.9358% | 4727 | `{"overbought": 70.0, "oversold": 25.0, "period": 5}` |
| 50 | `r1_c45` | `price_moving_average` | -28.3608 | -94.1570% | 94.1738% | 2971 | `{"entry_threshold": 0.0005, "period": 5}` |

## Round 2

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r2_c21` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 2 | `r2_c01` | `donchian_breakout` | 1.6796 | 21.2897% | 27.4253% | 147 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 3 | `r2_c24` | `donchian_breakout` | 0.9742 | 10.0629% | 22.2482% | 325 | `{"breakout_buffer_bps": 15.0, "lookback_window": 60}` |
| 4 | `r2_c02` | `donchian_breakout` | 0.6506 | 5.2527% | 27.5863% | 331 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 5 | `r2_c23` | `multi_timeframe_ma_spread` | 0.5691 | 4.0452% | 23.8181% | 83 | `{"primary_ma_period": 25, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 6 | `r2_c22` | `donchian_breakout` | 0.1136 | -2.2762% | 23.7214% | 390 | `{"breakout_buffer_bps": 10.0, "lookback_window": 67}` |
| 7 | `r2_c30` | `donchian_breakout` | 0.0801 | -2.7167% | 32.9409% | 164 | `{"breakout_buffer_bps": 30.0, "lookback_window": 53}` |
| 8 | `r2_c03` | `multi_timeframe_ma_spread` | -0.0417 | -3.8387% | 30.9595% | 123 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 9 | `r2_c31` | `multi_timeframe_ma_spread` | -0.1652 | -5.3698% | 34.0653% | 88 | `{"primary_ma_period": 24, "reference_ma_period": 60, "spread_threshold_bps": 30.0}` |
| 10 | `r2_c45` | `multi_timeframe_ma_spread` | -0.2477 | -6.3886% | 31.5750% | 90 | `{"primary_ma_period": 24, "reference_ma_period": 54, "spread_threshold_bps": 40.0}` |
| 11 | `r2_c49` | `multi_timeframe_ma_spread` | -0.2707 | -7.0347% | 27.9397% | 341 | `{"primary_ma_period": 12, "reference_ma_period": 12, "spread_threshold_bps": 30.0}` |
| 12 | `r2_c04` | `donchian_breakout` | -0.4365 | -9.4348% | 29.9301% | 397 | `{"breakout_buffer_bps": 10.0, "lookback_window": 65}` |
| 13 | `r2_c05` | `multi_timeframe_ma_spread` | -0.4933 | -9.3496% | 35.1636% | 106 | `{"primary_ma_period": 19, "reference_ma_period": 52, "spread_threshold_bps": 40.0}` |
| 14 | `r2_c25` | `multi_timeframe_ma_spread` | -0.5717 | -10.3588% | 36.3003% | 134 | `{"primary_ma_period": 14, "reference_ma_period": 47, "spread_threshold_bps": 60.0}` |
| 15 | `r2_c06` | `multi_timeframe_ma_spread` | -0.5903 | -10.4212% | 36.4572% | 94 | `{"primary_ma_period": 21, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 16 | `r2_c27` | `multi_timeframe_ma_spread` | -0.6277 | -11.1874% | 35.9403% | 424 | `{"primary_ma_period": 2, "reference_ma_period": 24, "spread_threshold_bps": 40.0}` |
| 17 | `r2_c34` | `multi_timeframe_ma_spread` | -0.6561 | -11.3617% | 27.6871% | 275 | `{"primary_ma_period": 6, "reference_ma_period": 28, "spread_threshold_bps": 25.0}` |
| 18 | `r2_c43` | `multi_timeframe_ma_spread` | -0.7388 | -12.1034% | 34.6413% | 104 | `{"primary_ma_period": 23, "reference_ma_period": 60, "spread_threshold_bps": 20.0}` |
| 19 | `r2_c07` | `multi_timeframe_ma_spread` | -0.7565 | -12.6507% | 30.8071% | 366 | `{"primary_ma_period": 5, "reference_ma_period": 22, "spread_threshold_bps": 20.0}` |
| 20 | `r2_c46` | `multi_timeframe_ma_spread` | -0.7863 | -12.7329% | 32.9708% | 96 | `{"primary_ma_period": 26, "reference_ma_period": 50, "spread_threshold_bps": 30.0}` |
| 21 | `r2_c08` | `multi_timeframe_ma_spread` | -0.9350 | -14.3094% | 36.3283% | 110 | `{"primary_ma_period": 23, "reference_ma_period": 55, "spread_threshold_bps": 20.0}` |
| 22 | `r2_c26` | `multi_timeframe_ma_spread` | -1.0381 | -15.4598% | 39.3759% | 114 | `{"primary_ma_period": 16, "reference_ma_period": 58, "spread_threshold_bps": 30.0}` |
| 23 | `r2_c09` | `multi_timeframe_ma_spread` | -1.0531 | -16.0193% | 32.0312% | 251 | `{"primary_ma_period": 13, "reference_ma_period": 22, "spread_threshold_bps": 10.0}` |
| 24 | `r2_c10` | `donchian_breakout` | -1.3352 | -20.0218% | 39.1946% | 437 | `{"breakout_buffer_bps": 10.0, "lookback_window": 55}` |
| 25 | `r2_c38` | `rsi_reversion` | -1.4046 | -14.2715% | 32.8689% | 410 | `{"overbought": 72.5, "oversold": 25.0, "period": 20}` |
| 26 | `r2_c29` | `multi_timeframe_ma_spread` | -1.4656 | -20.2234% | 34.9005% | 250 | `{"primary_ma_period": 8, "reference_ma_period": 32, "spread_threshold_bps": 15.0}` |
| 27 | `r2_c48` | `multi_timeframe_ma_spread` | -1.5929 | -21.3364% | 37.4441% | 135 | `{"primary_ma_period": 22, "reference_ma_period": 45, "spread_threshold_bps": 15.0}` |
| 28 | `r2_c41` | `donchian_breakout` | -1.6093 | -22.9831% | 42.3902% | 263 | `{"breakout_buffer_bps": 20.0, "lookback_window": 55}` |
| 29 | `r2_c11` | `multi_timeframe_ma_spread` | -1.6536 | -21.8837% | 38.3480% | 102 | `{"primary_ma_period": 25, "reference_ma_period": 55, "spread_threshold_bps": 10.0}` |
| 30 | `r2_c28` | `multi_timeframe_ma_spread` | -1.7902 | -23.4610% | 39.5461% | 124 | `{"primary_ma_period": 26, "reference_ma_period": 45, "spread_threshold_bps": 15.0}` |
| 31 | `r2_c12` | `multi_timeframe_ma_spread` | -1.8910 | -24.5682% | 35.6079% | 199 | `{"primary_ma_period": 15, "reference_ma_period": 30, "spread_threshold_bps": 0.0}` |
| 32 | `r2_c32` | `multi_timeframe_ma_spread` | -2.0579 | -26.1650% | 35.2400% | 178 | `{"primary_ma_period": 16, "reference_ma_period": 35, "spread_threshold_bps": 10.0}` |
| 33 | `r2_c42` | `donchian_breakout` | -2.4724 | -31.6830% | 45.5343% | 451 | `{"breakout_buffer_bps": 10.0, "lookback_window": 52}` |
| 34 | `r2_c33` | `moving_average_cross` | -2.6917 | -22.4157% | 27.7709% | 532 | `{"entry_threshold": 0.0015, "fast_window": 25, "slow_window": 105}` |
| 35 | `r2_c13` | `moving_average_cross` | -2.8557 | -23.5672% | 29.7447% | 504 | `{"entry_threshold": 0.002, "fast_window": 22, "slow_window": 95}` |
| 36 | `r2_c14` | `multi_timeframe_ma_spread` | -3.1922 | -36.8292% | 38.7831% | 373 | `{"primary_ma_period": 7, "reference_ma_period": 18, "spread_threshold_bps": 5.0}` |
| 37 | `r2_c47` | `multi_timeframe_ma_spread` | -3.3465 | -38.5631% | 45.3709% | 650 | `{"primary_ma_period": 2, "reference_ma_period": 12, "spread_threshold_bps": 30.0}` |
| 38 | `r2_c15` | `donchian_breakout` | -3.3814 | -39.8343% | 41.6256% | 712 | `{"breakout_buffer_bps": 0.0, "lookback_window": 65}` |
| 39 | `r2_c36` | `multi_timeframe_ma_spread` | -3.5348 | -39.7318% | 39.7676% | 324 | `{"primary_ma_period": 13, "reference_ma_period": 15, "spread_threshold_bps": 5.0}` |
| 40 | `r2_c44` | `donchian_breakout` | -3.6824 | -42.2710% | 47.1123% | 610 | `{"breakout_buffer_bps": 5.0, "lookback_window": 55}` |
| 41 | `r2_c16` | `multi_timeframe_ma_spread` | -3.8423 | -42.0567% | 43.9621% | 310 | `{"primary_ma_period": 10, "reference_ma_period": 20, "spread_threshold_bps": 0.0}` |
| 42 | `r2_c17` | `moving_average_cross` | -3.9960 | -31.3292% | 34.6263% | 753 | `{"entry_threshold": 0.001, "fast_window": 20, "slow_window": 80}` |
| 43 | `r2_c35` | `donchian_breakout` | -4.0646 | -45.2880% | 47.0557% | 724 | `{"breakout_buffer_bps": 0.0, "lookback_window": 63}` |
| 44 | `r2_c18` | `rsi_reversion` | -4.2365 | -32.7339% | 34.7901% | 775 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 45 | `r2_c37` | `moving_average_cross` | -4.3336 | -33.4311% | 36.3202% | 794 | `{"entry_threshold": 0.0005, "fast_window": 22, "slow_window": 90}` |
| 46 | `r2_c19` | `moving_average_cross` | -4.5523 | -34.8806% | 38.0912% | 789 | `{"entry_threshold": 0.001, "fast_window": 21, "slow_window": 75}` |
| 47 | `r2_c50` | `donchian_breakout` | -5.2535 | -53.5818% | 55.5604% | 755 | `{"breakout_buffer_bps": 0.0, "lookback_window": 60}` |
| 48 | `r2_c20` | `rsi_reversion` | -5.2653 | -42.7433% | 44.6432% | 1370 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
| 49 | `r2_c40` | `rsi_reversion` | -5.5962 | -42.3549% | 44.0178% | 936 | `{"overbought": 70.0, "oversold": 27.5, "period": 16}` |
| 50 | `r2_c39` | `moving_average_cross` | -5.9480 | -42.9200% | 46.0408% | 990 | `{"entry_threshold": 0.0005, "fast_window": 19, "slow_window": 65}` |

## Round 3

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r3_c01` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 2 | `r3_c42` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 70}` |
| 3 | `r3_c22` | `donchian_breakout` | 1.9445 | 25.7324% | 20.6542% | 124 | `{"breakout_buffer_bps": 35.0, "lookback_window": 60}` |
| 4 | `r3_c02` | `donchian_breakout` | 1.6796 | 21.2897% | 27.4253% | 147 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 5 | `r3_c25` | `multi_timeframe_ma_spread` | 1.2762 | 14.0258% | 18.8040% | 85 | `{"primary_ma_period": 26, "reference_ma_period": 55, "spread_threshold_bps": 60.0}` |
| 6 | `r3_c26` | `donchian_breakout` | 1.1587 | 12.9038% | 22.7092% | 310 | `{"breakout_buffer_bps": 15.0, "lookback_window": 65}` |
| 7 | `r3_c46` | `donchian_breakout` | 1.1152 | 12.2208% | 32.6243% | 143 | `{"breakout_buffer_bps": 30.0, "lookback_window": 69}` |
| 8 | `r3_c30` | `multi_timeframe_ma_spread` | 1.0599 | 10.8550% | 24.7628% | 85 | `{"primary_ma_period": 23, "reference_ma_period": 64, "spread_threshold_bps": 50.0}` |
| 9 | `r3_c03` | `donchian_breakout` | 0.9742 | 10.0629% | 22.2482% | 325 | `{"breakout_buffer_bps": 15.0, "lookback_window": 60}` |
| 10 | `r3_c04` | `donchian_breakout` | 0.6506 | 5.2527% | 27.5863% | 331 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 11 | `r3_c05` | `multi_timeframe_ma_spread` | 0.5691 | 4.0452% | 23.8181% | 83 | `{"primary_ma_period": 25, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 12 | `r3_c21` | `donchian_breakout` | 0.5345 | 3.5766% | 24.2719% | 75 | `{"breakout_buffer_bps": 45.0, "lookback_window": 53}` |
| 13 | `r3_c06` | `donchian_breakout` | 0.1136 | -2.2762% | 23.7214% | 390 | `{"breakout_buffer_bps": 10.0, "lookback_window": 67}` |
| 14 | `r3_c07` | `donchian_breakout` | 0.0801 | -2.7167% | 32.9409% | 164 | `{"breakout_buffer_bps": 30.0, "lookback_window": 53}` |
| 15 | `r3_c50` | `multi_timeframe_ma_spread` | 0.0476 | -2.8079% | 31.7631% | 112 | `{"primary_ma_period": 23, "reference_ma_period": 44, "spread_threshold_bps": 60.0}` |
| 16 | `r3_c35` | `multi_timeframe_ma_spread` | 0.0178 | -3.1098% | 31.0702% | 91 | `{"primary_ma_period": 24, "reference_ma_period": 55, "spread_threshold_bps": 35.0}` |
| 17 | `r3_c08` | `multi_timeframe_ma_spread` | -0.0417 | -3.8387% | 30.9595% | 123 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 18 | `r3_c27` | `donchian_breakout` | -0.1126 | -5.2781% | 28.8463% | 248 | `{"breakout_buffer_bps": 20.0, "lookback_window": 63}` |
| 19 | `r3_c31` | `multi_timeframe_ma_spread` | -0.1207 | -5.0626% | 25.1645% | 282 | `{"primary_ma_period": 15, "reference_ma_period": 14, "spread_threshold_bps": 25.0}` |
| 20 | `r3_c48` | `multi_timeframe_ma_spread` | -0.1600 | -5.3159% | 31.0475% | 129 | `{"primary_ma_period": 17, "reference_ma_period": 48, "spread_threshold_bps": 30.0}` |
| 21 | `r3_c09` | `multi_timeframe_ma_spread` | -0.1652 | -5.3698% | 34.0653% | 88 | `{"primary_ma_period": 24, "reference_ma_period": 60, "spread_threshold_bps": 30.0}` |
| 22 | `r3_c10` | `multi_timeframe_ma_spread` | -0.2477 | -6.3886% | 31.5750% | 90 | `{"primary_ma_period": 24, "reference_ma_period": 54, "spread_threshold_bps": 40.0}` |
| 23 | `r3_c11` | `multi_timeframe_ma_spread` | -0.2707 | -7.0347% | 27.9397% | 341 | `{"primary_ma_period": 12, "reference_ma_period": 12, "spread_threshold_bps": 30.0}` |
| 24 | `r3_c44` | `donchian_breakout` | -0.4195 | -9.2197% | 30.4308% | 410 | `{"breakout_buffer_bps": 10.0, "lookback_window": 62}` |
| 25 | `r3_c12` | `donchian_breakout` | -0.4365 | -9.4348% | 29.9301% | 397 | `{"breakout_buffer_bps": 10.0, "lookback_window": 65}` |
| 26 | `r3_c13` | `multi_timeframe_ma_spread` | -0.4933 | -9.3496% | 35.1636% | 106 | `{"primary_ma_period": 19, "reference_ma_period": 52, "spread_threshold_bps": 40.0}` |
| 27 | `r3_c14` | `multi_timeframe_ma_spread` | -0.5717 | -10.3588% | 36.3003% | 134 | `{"primary_ma_period": 14, "reference_ma_period": 47, "spread_threshold_bps": 60.0}` |
| 28 | `r3_c29` | `multi_timeframe_ma_spread` | -0.5743 | -10.2048% | 34.5911% | 110 | `{"primary_ma_period": 19, "reference_ma_period": 62, "spread_threshold_bps": 25.0}` |
| 29 | `r3_c15` | `multi_timeframe_ma_spread` | -0.5903 | -10.4212% | 36.4572% | 94 | `{"primary_ma_period": 21, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 30 | `r3_c41` | `donchian_breakout` | -0.6251 | -11.5809% | 40.4666% | 58 | `{"breakout_buffer_bps": 50.0, "lookback_window": 65}` |
| 31 | `r3_c16` | `multi_timeframe_ma_spread` | -0.6277 | -11.1874% | 35.9403% | 424 | `{"primary_ma_period": 2, "reference_ma_period": 24, "spread_threshold_bps": 40.0}` |
| 32 | `r3_c17` | `multi_timeframe_ma_spread` | -0.6561 | -11.3617% | 27.6871% | 275 | `{"primary_ma_period": 6, "reference_ma_period": 28, "spread_threshold_bps": 25.0}` |
| 33 | `r3_c38` | `multi_timeframe_ma_spread` | -0.6648 | -11.2502% | 35.6798% | 91 | `{"primary_ma_period": 24, "reference_ma_period": 65, "spread_threshold_bps": 30.0}` |
| 34 | `r3_c33` | `multi_timeframe_ma_spread` | -0.6684 | -11.2900% | 36.3697% | 115 | `{"primary_ma_period": 16, "reference_ma_period": 62, "spread_threshold_bps": 30.0}` |
| 35 | `r3_c18` | `multi_timeframe_ma_spread` | -0.7388 | -12.1034% | 34.6413% | 104 | `{"primary_ma_period": 23, "reference_ma_period": 60, "spread_threshold_bps": 20.0}` |
| 36 | `r3_c19` | `multi_timeframe_ma_spread` | -0.7565 | -12.6507% | 30.8071% | 366 | `{"primary_ma_period": 5, "reference_ma_period": 22, "spread_threshold_bps": 20.0}` |
| 37 | `r3_c20` | `multi_timeframe_ma_spread` | -0.7863 | -12.7329% | 32.9708% | 96 | `{"primary_ma_period": 26, "reference_ma_period": 50, "spread_threshold_bps": 30.0}` |
| 38 | `r3_c34` | `multi_timeframe_ma_spread` | -0.7939 | -12.9136% | 38.5939% | 128 | `{"primary_ma_period": 17, "reference_ma_period": 49, "spread_threshold_bps": 60.0}` |
| 39 | `r3_c36` | `multi_timeframe_ma_spread` | -0.7996 | -13.1235% | 28.7560% | 224 | `{"primary_ma_period": 7, "reference_ma_period": 29, "spread_threshold_bps": 60.0}` |
| 40 | `r3_c45` | `multi_timeframe_ma_spread` | -0.8503 | -13.4763% | 35.2603% | 97 | `{"primary_ma_period": 26, "reference_ma_period": 50, "spread_threshold_bps": 40.0}` |
| 41 | `r3_c49` | `multi_timeframe_ma_spread` | -0.9882 | -14.9593% | 35.1009% | 99 | `{"primary_ma_period": 29, "reference_ma_period": 50, "spread_threshold_bps": 25.0}` |
| 42 | `r3_c47` | `donchian_breakout` | -1.1122 | -17.4985% | 38.0261% | 257 | `{"breakout_buffer_bps": 20.0, "lookback_window": 58}` |
| 43 | `r3_c28` | `multi_timeframe_ma_spread` | -1.2592 | -17.8483% | 34.5134% | 156 | `{"primary_ma_period": 15, "reference_ma_period": 45, "spread_threshold_bps": 10.0}` |
| 44 | `r3_c40` | `multi_timeframe_ma_spread` | -1.2606 | -18.0255% | 37.2440% | 140 | `{"primary_ma_period": 21, "reference_ma_period": 40, "spread_threshold_bps": 25.0}` |
| 45 | `r3_c39` | `multi_timeframe_ma_spread` | -1.6606 | -22.2337% | 35.4919% | 391 | `{"primary_ma_period": 2, "reference_ma_period": 32, "spread_threshold_bps": 25.0}` |
| 46 | `r3_c37` | `multi_timeframe_ma_spread` | -1.8996 | -24.6831% | 38.7603% | 243 | `{"primary_ma_period": 5, "reference_ma_period": 38, "spread_threshold_bps": 45.0}` |
| 47 | `r3_c43` | `donchian_breakout` | -2.5804 | -32.7328% | 41.8896% | 596 | `{"breakout_buffer_bps": 5.0, "lookback_window": 58}` |
| 48 | `r3_c32` | `donchian_breakout` | -3.4741 | -40.6115% | 42.0645% | 692 | `{"breakout_buffer_bps": 0.0, "lookback_window": 67}` |
| 49 | `r3_c24` | `donchian_breakout` | -3.6824 | -42.2710% | 47.1123% | 610 | `{"breakout_buffer_bps": 5.0, "lookback_window": 55}` |
| 50 | `r3_c23` | `donchian_breakout` | -5.0674 | -52.3579% | 55.7354% | 647 | `{"breakout_buffer_bps": 5.0, "lookback_window": 50}` |

## Round 4

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r4_c47` | `donchian_breakout` | 3.1180 | 47.6803% | 16.7789% | 117 | `{"breakout_buffer_bps": 35.0, "lookback_window": 64}` |
| 2 | `r4_c01` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 3 | `r4_c23` | `donchian_breakout` | 3.0918 | 47.1767% | 18.8271% | 116 | `{"breakout_buffer_bps": 35.0, "lookback_window": 65}` |
| 4 | `r4_c44` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 67}` |
| 5 | `r4_c02` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 70}` |
| 6 | `r4_c24` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 67}` |
| 7 | `r4_c42` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 68}` |
| 8 | `r4_c03` | `donchian_breakout` | 1.9445 | 25.7324% | 20.6542% | 124 | `{"breakout_buffer_bps": 35.0, "lookback_window": 60}` |
| 9 | `r4_c28` | `multi_timeframe_ma_spread` | 1.9037 | 23.5975% | 26.6440% | 75 | `{"primary_ma_period": 28, "reference_ma_period": 69, "spread_threshold_bps": 60.0}` |
| 10 | `r4_c04` | `donchian_breakout` | 1.6796 | 21.2897% | 27.4253% | 147 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 11 | `r4_c27` | `donchian_breakout` | 1.4591 | 17.6740% | 32.6243% | 137 | `{"breakout_buffer_bps": 30.0, "lookback_window": 79}` |
| 12 | `r4_c31` | `multi_timeframe_ma_spread` | 1.2978 | 14.2972% | 23.1221% | 81 | `{"primary_ma_period": 30, "reference_ma_period": 65, "spread_threshold_bps": 45.0}` |
| 13 | `r4_c05` | `multi_timeframe_ma_spread` | 1.2762 | 14.0258% | 18.8040% | 85 | `{"primary_ma_period": 26, "reference_ma_period": 55, "spread_threshold_bps": 60.0}` |
| 14 | `r4_c06` | `donchian_breakout` | 1.1587 | 12.9038% | 22.7092% | 310 | `{"breakout_buffer_bps": 15.0, "lookback_window": 65}` |
| 15 | `r4_c07` | `donchian_breakout` | 1.1152 | 12.2208% | 32.6243% | 143 | `{"breakout_buffer_bps": 30.0, "lookback_window": 69}` |
| 16 | `r4_c08` | `multi_timeframe_ma_spread` | 1.0599 | 10.8550% | 24.7628% | 85 | `{"primary_ma_period": 23, "reference_ma_period": 64, "spread_threshold_bps": 50.0}` |
| 17 | `r4_c09` | `donchian_breakout` | 0.9742 | 10.0629% | 22.2482% | 325 | `{"breakout_buffer_bps": 15.0, "lookback_window": 60}` |
| 18 | `r4_c49` | `donchian_breakout` | 0.8681 | 8.4660% | 23.5704% | 298 | `{"breakout_buffer_bps": 15.0, "lookback_window": 70}` |
| 19 | `r4_c26` | `donchian_breakout` | 0.7253 | 6.3441% | 27.5838% | 333 | `{"breakout_buffer_bps": 15.0, "lookback_window": 55}` |
| 20 | `r4_c48` | `multi_timeframe_ma_spread` | 0.6547 | 5.2046% | 34.7719% | 79 | `{"primary_ma_period": 20, "reference_ma_period": 74, "spread_threshold_bps": 70.0}` |
| 21 | `r4_c10` | `donchian_breakout` | 0.6506 | 5.2527% | 27.5863% | 331 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 22 | `r4_c32` | `donchian_breakout` | 0.5944 | 4.4283% | 23.6491% | 72 | `{"breakout_buffer_bps": 45.0, "lookback_window": 58}` |
| 23 | `r4_c11` | `multi_timeframe_ma_spread` | 0.5691 | 4.0452% | 23.8181% | 83 | `{"primary_ma_period": 25, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 24 | `r4_c25` | `multi_timeframe_ma_spread` | 0.5676 | 4.0252% | 31.7642% | 78 | `{"primary_ma_period": 25, "reference_ma_period": 65, "spread_threshold_bps": 80.0}` |
| 25 | `r4_c12` | `donchian_breakout` | 0.5345 | 3.5766% | 24.2719% | 75 | `{"breakout_buffer_bps": 45.0, "lookback_window": 53}` |
| 26 | `r4_c41` | `donchian_breakout` | 0.4808 | 2.8283% | 36.6469% | 41 | `{"breakout_buffer_bps": 60.0, "lookback_window": 73}` |
| 27 | `r4_c22` | `donchian_breakout` | 0.3941 | 1.6303% | 37.3850% | 43 | `{"breakout_buffer_bps": 60.0, "lookback_window": 60}` |
| 28 | `r4_c34` | `donchian_breakout` | 0.1524 | -1.7396% | 32.9503% | 168 | `{"breakout_buffer_bps": 30.0, "lookback_window": 48}` |
| 29 | `r4_c13` | `donchian_breakout` | 0.1136 | -2.2762% | 23.7214% | 390 | `{"breakout_buffer_bps": 10.0, "lookback_window": 67}` |
| 30 | `r4_c43` | `donchian_breakout` | 0.0808 | -2.7074% | 32.9409% | 163 | `{"breakout_buffer_bps": 30.0, "lookback_window": 55}` |
| 31 | `r4_c14` | `donchian_breakout` | 0.0801 | -2.7167% | 32.9409% | 164 | `{"breakout_buffer_bps": 30.0, "lookback_window": 53}` |
| 32 | `r4_c15` | `multi_timeframe_ma_spread` | 0.0476 | -2.8079% | 31.7631% | 112 | `{"primary_ma_period": 23, "reference_ma_period": 44, "spread_threshold_bps": 60.0}` |
| 33 | `r4_c16` | `multi_timeframe_ma_spread` | 0.0178 | -3.1098% | 31.0702% | 91 | `{"primary_ma_period": 24, "reference_ma_period": 55, "spread_threshold_bps": 35.0}` |
| 34 | `r4_c17` | `multi_timeframe_ma_spread` | -0.0417 | -3.8387% | 30.9595% | 123 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 35 | `r4_c18` | `donchian_breakout` | -0.1126 | -5.2781% | 28.8463% | 248 | `{"breakout_buffer_bps": 20.0, "lookback_window": 63}` |
| 36 | `r4_c19` | `multi_timeframe_ma_spread` | -0.1207 | -5.0626% | 25.1645% | 282 | `{"primary_ma_period": 15, "reference_ma_period": 14, "spread_threshold_bps": 25.0}` |
| 37 | `r4_c20` | `multi_timeframe_ma_spread` | -0.1600 | -5.3159% | 31.0475% | 129 | `{"primary_ma_period": 17, "reference_ma_period": 48, "spread_threshold_bps": 30.0}` |
| 38 | `r4_c40` | `multi_timeframe_ma_spread` | -0.2520 | -6.4753% | 33.9964% | 110 | `{"primary_ma_period": 22, "reference_ma_period": 50, "spread_threshold_bps": 50.0}` |
| 39 | `r4_c45` | `multi_timeframe_ma_spread` | -0.3776 | -7.9833% | 34.3867% | 89 | `{"primary_ma_period": 29, "reference_ma_period": 50, "spread_threshold_bps": 55.0}` |
| 40 | `r4_c29` | `donchian_breakout` | -0.4365 | -9.4348% | 29.9301% | 397 | `{"breakout_buffer_bps": 10.0, "lookback_window": 65}` |
| 41 | `r4_c36` | `multi_timeframe_ma_spread` | -0.4558 | -8.8866% | 32.6770% | 96 | `{"primary_ma_period": 23, "reference_ma_period": 53, "spread_threshold_bps": 45.0}` |
| 42 | `r4_c39` | `multi_timeframe_ma_spread` | -0.5120 | -9.7486% | 28.6808% | 187 | `{"primary_ma_period": 20, "reference_ma_period": 24, "spread_threshold_bps": 20.0}` |
| 43 | `r4_c21` | `donchian_breakout` | -0.6251 | -11.5809% | 40.4666% | 58 | `{"breakout_buffer_bps": 50.0, "lookback_window": 65}` |
| 44 | `r4_c50` | `donchian_breakout` | -0.6284 | -11.7761% | 32.3664% | 183 | `{"breakout_buffer_bps": 25.0, "lookback_window": 67}` |
| 45 | `r4_c38` | `donchian_breakout` | -0.7075 | -12.7652% | 35.2516% | 231 | `{"breakout_buffer_bps": 20.0, "lookback_window": 73}` |
| 46 | `r4_c37` | `multi_timeframe_ma_spread` | -1.0564 | -15.6337% | 36.7988% | 129 | `{"primary_ma_period": 19, "reference_ma_period": 48, "spread_threshold_bps": 10.0}` |
| 47 | `r4_c30` | `donchian_breakout` | -1.1122 | -17.4985% | 38.0261% | 257 | `{"breakout_buffer_bps": 20.0, "lookback_window": 59}` |
| 48 | `r4_c46` | `donchian_breakout` | -1.1140 | -17.5173% | 38.0402% | 255 | `{"breakout_buffer_bps": 20.0, "lookback_window": 60}` |
| 49 | `r4_c35` | `multi_timeframe_ma_spread` | -1.1652 | -17.0795% | 38.6846% | 112 | `{"primary_ma_period": 28, "reference_ma_period": 39, "spread_threshold_bps": 55.0}` |
| 50 | `r4_c33` | `donchian_breakout` | -2.3083 | -30.1494% | 35.8461% | 625 | `{"breakout_buffer_bps": 0.0, "lookback_window": 77}` |

## Round 5

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r5_c01` | `donchian_breakout` | 3.1180 | 47.6803% | 16.7789% | 117 | `{"breakout_buffer_bps": 35.0, "lookback_window": 64}` |
| 2 | `r5_c02` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 3 | `r5_c03` | `donchian_breakout` | 3.0918 | 47.1767% | 18.8271% | 116 | `{"breakout_buffer_bps": 35.0, "lookback_window": 65}` |
| 4 | `r5_c04` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 67}` |
| 5 | `r5_c05` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 70}` |
| 6 | `r5_c06` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 67}` |
| 7 | `r5_c07` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 68}` |
| 8 | `r5_c08` | `donchian_breakout` | 1.9445 | 25.7324% | 20.6542% | 124 | `{"breakout_buffer_bps": 35.0, "lookback_window": 60}` |
| 9 | `r5_c09` | `multi_timeframe_ma_spread` | 1.9037 | 23.5975% | 26.6440% | 75 | `{"primary_ma_period": 28, "reference_ma_period": 69, "spread_threshold_bps": 60.0}` |
| 10 | `r5_c10` | `donchian_breakout` | 1.6796 | 21.2897% | 27.4253% | 147 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 11 | `r5_c42` | `donchian_breakout` | 1.6073 | 19.9247% | 27.2363% | 100 | `{"breakout_buffer_bps": 40.0, "lookback_window": 53}` |
| 12 | `r5_c29` | `multi_timeframe_ma_spread` | 1.5909 | 18.6755% | 29.1014% | 82 | `{"primary_ma_period": 23, "reference_ma_period": 71, "spread_threshold_bps": 65.0}` |
| 13 | `r5_c33` | `multi_timeframe_ma_spread` | 1.4960 | 17.3027% | 18.6359% | 78 | `{"primary_ma_period": 29, "reference_ma_period": 57, "spread_threshold_bps": 55.0}` |
| 14 | `r5_c49` | `multi_timeframe_ma_spread` | 1.4807 | 17.0156% | 28.3786% | 61 | `{"primary_ma_period": 31, "reference_ma_period": 74, "spread_threshold_bps": 55.0}` |
| 15 | `r5_c11` | `donchian_breakout` | 1.4591 | 17.6740% | 32.6243% | 137 | `{"breakout_buffer_bps": 30.0, "lookback_window": 79}` |
| 16 | `r5_c36` | `multi_timeframe_ma_spread` | 1.4092 | 15.9735% | 22.7751% | 76 | `{"primary_ma_period": 28, "reference_ma_period": 62, "spread_threshold_bps": 70.0}` |
| 17 | `r5_c32` | `multi_timeframe_ma_spread` | 1.3939 | 15.6072% | 29.0230% | 75 | `{"primary_ma_period": 27, "reference_ma_period": 75, "spread_threshold_bps": 35.0}` |
| 18 | `r5_c12` | `multi_timeframe_ma_spread` | 1.2978 | 14.2972% | 23.1221% | 81 | `{"primary_ma_period": 30, "reference_ma_period": 65, "spread_threshold_bps": 45.0}` |
| 19 | `r5_c13` | `multi_timeframe_ma_spread` | 1.2762 | 14.0258% | 18.8040% | 85 | `{"primary_ma_period": 26, "reference_ma_period": 55, "spread_threshold_bps": 60.0}` |
| 20 | `r5_c14` | `donchian_breakout` | 1.1587 | 12.9038% | 22.7092% | 310 | `{"breakout_buffer_bps": 15.0, "lookback_window": 65}` |
| 21 | `r5_c15` | `donchian_breakout` | 1.1152 | 12.2208% | 32.6243% | 143 | `{"breakout_buffer_bps": 30.0, "lookback_window": 69}` |
| 22 | `r5_c44` | `donchian_breakout` | 1.1147 | 12.2137% | 32.6243% | 142 | `{"breakout_buffer_bps": 30.0, "lookback_window": 72}` |
| 23 | `r5_c16` | `multi_timeframe_ma_spread` | 1.0599 | 10.8550% | 24.7628% | 85 | `{"primary_ma_period": 23, "reference_ma_period": 64, "spread_threshold_bps": 50.0}` |
| 24 | `r5_c27` | `donchian_breakout` | 1.0166 | 10.6378% | 29.1547% | 61 | `{"breakout_buffer_bps": 45.0, "lookback_window": 78}` |
| 25 | `r5_c17` | `donchian_breakout` | 0.9742 | 10.0629% | 22.2482% | 325 | `{"breakout_buffer_bps": 15.0, "lookback_window": 60}` |
| 26 | `r5_c18` | `donchian_breakout` | 0.8681 | 8.4660% | 23.5704% | 298 | `{"breakout_buffer_bps": 15.0, "lookback_window": 70}` |
| 27 | `r5_c40` | `multi_timeframe_ma_spread` | 0.7661 | 6.7317% | 34.3781% | 77 | `{"primary_ma_period": 19, "reference_ma_period": 72, "spread_threshold_bps": 80.0}` |
| 28 | `r5_c19` | `donchian_breakout` | 0.7253 | 6.3441% | 27.5838% | 333 | `{"breakout_buffer_bps": 15.0, "lookback_window": 55}` |
| 29 | `r5_c46` | `donchian_breakout` | 0.7113 | 6.1116% | 29.4020% | 69 | `{"breakout_buffer_bps": 45.0, "lookback_window": 65}` |
| 30 | `r5_c20` | `multi_timeframe_ma_spread` | 0.6547 | 5.2046% | 34.7719% | 79 | `{"primary_ma_period": 20, "reference_ma_period": 74, "spread_threshold_bps": 70.0}` |
| 31 | `r5_c21` | `donchian_breakout` | 0.5345 | 3.5766% | 24.2719% | 75 | `{"breakout_buffer_bps": 45.0, "lookback_window": 54}` |
| 32 | `r5_c22` | `donchian_breakout` | 0.4808 | 2.8283% | 36.6469% | 41 | `{"breakout_buffer_bps": 60.0, "lookback_window": 68}` |
| 33 | `r5_c41` | `donchian_breakout` | 0.3508 | 1.0042% | 32.5729% | 67 | `{"breakout_buffer_bps": 45.0, "lookback_window": 69}` |
| 34 | `r5_c28` | `donchian_breakout` | 0.3457 | 0.9341% | 32.5729% | 66 | `{"breakout_buffer_bps": 45.0, "lookback_window": 70}` |
| 35 | `r5_c38` | `donchian_breakout` | 0.1867 | -1.2920% | 30.6835% | 356 | `{"breakout_buffer_bps": 10.0, "lookback_window": 80}` |
| 36 | `r5_c23` | `donchian_breakout` | 0.0808 | -2.7074% | 32.9409% | 163 | `{"breakout_buffer_bps": 30.0, "lookback_window": 55}` |
| 37 | `r5_c47` | `donchian_breakout` | -0.1860 | -6.1177% | 36.7882% | 60 | `{"breakout_buffer_bps": 50.0, "lookback_window": 63}` |
| 38 | `r5_c24` | `donchian_breakout` | -0.4423 | -9.3601% | 44.7961% | 50 | `{"breakout_buffer_bps": 55.0, "lookback_window": 65}` |
| 39 | `r5_c48` | `donchian_breakout` | -0.4752 | -9.8879% | 32.3227% | 200 | `{"breakout_buffer_bps": 25.0, "lookback_window": 62}` |
| 40 | `r5_c34` | `donchian_breakout` | -0.5109 | -10.3768% | 25.3861% | 522 | `{"breakout_buffer_bps": 5.0, "lookback_window": 67}` |
| 41 | `r5_c31` | `donchian_breakout` | -0.6142 | -11.6410% | 34.4172% | 228 | `{"breakout_buffer_bps": 20.0, "lookback_window": 77}` |
| 42 | `r5_c30` | `donchian_breakout` | -0.9712 | -15.8817% | 38.0429% | 235 | `{"breakout_buffer_bps": 20.0, "lookback_window": 70}` |
| 43 | `r5_c25` | `donchian_breakout` | -0.9849 | -15.8367% | 43.1405% | 56 | `{"breakout_buffer_bps": 50.0, "lookback_window": 68}` |
| 44 | `r5_c26` | `donchian_breakout` | -0.9902 | -15.8951% | 43.1405% | 55 | `{"breakout_buffer_bps": 50.0, "lookback_window": 77}` |
| 45 | `r5_c45` | `donchian_breakout` | -0.9902 | -15.8951% | 43.1405% | 55 | `{"breakout_buffer_bps": 50.0, "lookback_window": 75}` |
| 46 | `r5_c50` | `donchian_breakout` | -0.9902 | -15.8951% | 43.1405% | 55 | `{"breakout_buffer_bps": 50.0, "lookback_window": 70}` |
| 47 | `r5_c39` | `donchian_breakout` | -1.0972 | -17.3413% | 37.0685% | 420 | `{"breakout_buffer_bps": 10.0, "lookback_window": 60}` |
| 48 | `r5_c43` | `donchian_breakout` | -1.1193 | -17.4312% | 41.3852% | 53 | `{"breakout_buffer_bps": 55.0, "lookback_window": 60}` |
| 49 | `r5_c35` | `donchian_breakout` | -1.3022 | -19.6368% | 37.9171% | 179 | `{"breakout_buffer_bps": 25.0, "lookback_window": 71}` |
| 50 | `r5_c37` | `donchian_breakout` | -2.0005 | -26.9954% | 43.2724% | 212 | `{"breakout_buffer_bps": 25.0, "lookback_window": 55}` |
