# LLM Strategy Evolution

- Symbol: `BTCUSDT`
- Primary timeframe: `5m`
- Secondary timeframe: `1h`
- Rounds: `5`
- Best strategy: `donchian_breakout`
- Best Sharpe: `3.6157`
- Best total return: `58.1413%`
- Best max drawdown: `19.1910%`
- Best trade count: `95`

## Round 1

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r1_c49` | `donchian_breakout` | 1.6962 | 21.5874% | 27.4253% | 148 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 2 | `r1_c40` | `donchian_breakout` | 0.2473 | -0.4669% | 27.5863% | 338 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 3 | `r1_c08` | `multi_timeframe_ma_spread` | -0.1297 | -4.9402% | 30.9595% | 119 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 4 | `r1_c17` | `multi_timeframe_ma_spread` | -0.6201 | -11.0834% | 32.2154% | 367 | `{"primary_ma_period": 5, "reference_ma_period": 22, "spread_threshold_bps": 20.0}` |
| 5 | `r1_c47` | `multi_timeframe_ma_spread` | -0.7282 | -12.0953% | 35.1636% | 104 | `{"primary_ma_period": 19, "reference_ma_period": 52, "spread_threshold_bps": 40.0}` |
| 6 | `r1_c38` | `multi_timeframe_ma_spread` | -0.8714 | -13.6337% | 36.3283% | 105 | `{"primary_ma_period": 23, "reference_ma_period": 55, "spread_threshold_bps": 20.0}` |
| 7 | `r1_c28` | `multi_timeframe_ma_spread` | -0.8853 | -13.8147% | 36.4572% | 90 | `{"primary_ma_period": 21, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 8 | `r1_c37` | `multi_timeframe_ma_spread` | -0.9028 | -14.3622% | 34.2886% | 247 | `{"primary_ma_period": 13, "reference_ma_period": 22, "spread_threshold_bps": 10.0}` |
| 9 | `r1_c20` | `donchian_breakout` | -0.9965 | -16.2469% | 32.3411% | 403 | `{"breakout_buffer_bps": 10.0, "lookback_window": 65}` |
| 10 | `r1_c18` | `multi_timeframe_ma_spread` | -1.4700 | -20.0689% | 38.3480% | 101 | `{"primary_ma_period": 25, "reference_ma_period": 55, "spread_threshold_bps": 10.0}` |
| 11 | `r1_c27` | `multi_timeframe_ma_spread` | -1.7774 | -23.4752% | 36.5911% | 193 | `{"primary_ma_period": 15, "reference_ma_period": 30, "spread_threshold_bps": 0.0}` |
| 12 | `r1_c10` | `donchian_breakout` | -1.9221 | -26.3494% | 40.4562% | 446 | `{"breakout_buffer_bps": 10.0, "lookback_window": 55}` |
| 13 | `r1_c13` | `moving_average_cross` | -2.6816 | -22.5187% | 28.1404% | 509 | `{"entry_threshold": 0.002, "fast_window": 22, "slow_window": 95}` |
| 14 | `r1_c46` | `multi_timeframe_ma_spread` | -2.7371 | -32.9392% | 37.2387% | 366 | `{"primary_ma_period": 7, "reference_ma_period": 18, "spread_threshold_bps": 5.0}` |
| 15 | `r1_c07` | `multi_timeframe_ma_spread` | -3.3461 | -38.1439% | 39.6265% | 305 | `{"primary_ma_period": 10, "reference_ma_period": 20, "spread_threshold_bps": 0.0}` |
| 16 | `r1_c30` | `donchian_breakout` | -3.6580 | -42.2029% | 43.5453% | 707 | `{"breakout_buffer_bps": 0.0, "lookback_window": 65}` |
| 17 | `r1_c15` | `rsi_reversion` | -3.8160 | -30.3388% | 33.5824% | 783 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 18 | `r1_c03` | `moving_average_cross` | -4.3204 | -33.4226% | 34.6653% | 768 | `{"entry_threshold": 0.001, "fast_window": 20, "slow_window": 80}` |
| 19 | `r1_c33` | `moving_average_cross` | -4.8654 | -36.8236% | 38.1461% | 802 | `{"entry_threshold": 0.001, "fast_window": 21, "slow_window": 75}` |
| 20 | `r1_c05` | `rsi_reversion` | -5.5360 | -44.3946% | 45.1756% | 1373 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
| 21 | `r1_c35` | `rsi_reversion` | -5.8727 | -48.6186% | 49.5008% | 1529 | `{"overbought": 70.0, "oversold": 35.0, "period": 15}` |
| 22 | `r1_c12` | `moving_average_cross` | -6.2837 | -44.5821% | 45.6250% | 1183 | `{"entry_threshold": 0.001, "fast_window": 8, "slow_window": 55}` |
| 23 | `r1_c25` | `rsi_reversion` | -6.5085 | -50.9000% | 51.8592% | 1378 | `{"overbought": 70.0, "oversold": 32.5, "period": 15}` |
| 24 | `r1_c23` | `moving_average_cross` | -6.5181 | -45.1253% | 46.4828% | 962 | `{"entry_threshold": 0.0005, "fast_window": 19, "slow_window": 70}` |
| 25 | `r1_c21` | `moving_average_cross` | -6.6996 | -47.6462% | 48.4993% | 1637 | `{"entry_threshold": 0.001, "fast_window": 7, "slow_window": 30}` |
| 26 | `r1_c36` | `price_moving_average` | -7.0831 | -49.6337% | 51.2682% | 648 | `{"entry_threshold": 0.0015, "period": 9}` |
| 27 | `r1_c32` | `moving_average_cross` | -7.3175 | -50.1073% | 51.5891% | 1497 | `{"entry_threshold": 0.0005, "fast_window": 9, "slow_window": 45}` |
| 28 | `r1_c22` | `moving_average_cross` | -7.6402 | -51.6762% | 52.4351% | 1679 | `{"entry_threshold": 0.0005, "fast_window": 11, "slow_window": 35}` |
| 29 | `r1_c26` | `price_moving_average` | -7.7484 | -54.6074% | 54.8542% | 875 | `{"entry_threshold": 0.001, "period": 13}` |
| 30 | `r1_c02` | `moving_average_cross` | -7.7993 | -52.3283% | 53.6538% | 1581 | `{"entry_threshold": 0.0005, "fast_window": 10, "slow_window": 40}` |
| 31 | `r1_c19` | `donchian_breakout` | -7.8439 | -67.7901% | 68.1406% | 1172 | `{"breakout_buffer_bps": 5.0, "lookback_window": 18}` |
| 32 | `r1_c29` | `donchian_breakout` | -8.4592 | -70.4963% | 70.6960% | 1535 | `{"breakout_buffer_bps": 0.0, "lookback_window": 22}` |
| 33 | `r1_c42` | `moving_average_cross` | -9.4180 | -59.2153% | 60.2233% | 2031 | `{"entry_threshold": 0.0, "fast_window": 8, "slow_window": 45}` |
| 34 | `r1_c09` | `donchian_breakout` | -9.7237 | -75.3027% | 75.4159% | 1656 | `{"breakout_buffer_bps": 0.0, "lookback_window": 20}` |
| 35 | `r1_c39` | `donchian_breakout` | -10.6394 | -78.3533% | 78.7981% | 1647 | `{"breakout_buffer_bps": 5.0, "lookback_window": 10}` |
| 36 | `r1_c48` | `donchian_breakout` | -11.0474 | -79.5713% | 79.6865% | 1988 | `{"breakout_buffer_bps": 0.0, "lookback_window": 15}` |
| 37 | `r1_c31` | `moving_average_cross` | -11.3389 | -66.3169% | 66.3195% | 2594 | `{"entry_threshold": 0.0, "fast_window": 8, "slow_window": 30}` |
| 38 | `r1_c11` | `moving_average_cross` | -11.6578 | -67.5093% | 67.5125% | 2608 | `{"entry_threshold": 0.0005, "fast_window": 4, "slow_window": 25}` |
| 39 | `r1_c50` | `moving_average_cross` | -13.7600 | -73.5618% | 73.7261% | 2689 | `{"entry_threshold": 0.001, "fast_window": 4, "slow_window": 10}` |
| 40 | `r1_c41` | `moving_average_cross` | -13.8201 | -73.9293% | 73.9316% | 3194 | `{"entry_threshold": 0.0, "fast_window": 6, "slow_window": 25}` |
| 41 | `r1_c04` | `rsi_reversion` | -13.9647 | -75.9795% | 76.2754% | 2708 | `{"overbought": 75.0, "oversold": 25.0, "period": 7}` |
| 42 | `r1_c44` | `rsi_reversion` | -14.8639 | -78.5814% | 78.7502% | 2930 | `{"overbought": 65.0, "oversold": 35.0, "period": 10}` |
| 43 | `r1_c43` | `rsi_reversion` | -16.8718 | -80.6925% | 80.6925% | 3411 | `{"overbought": 70.0, "oversold": 22.5, "period": 6}` |
| 44 | `r1_c01` | `moving_average_cross` | -17.5257 | -81.8478% | 81.8558% | 3945 | `{"entry_threshold": 0.0, "fast_window": 5, "slow_window": 20}` |
| 45 | `r1_c34` | `rsi_reversion` | -18.7635 | -85.9355% | 85.9408% | 3761 | `{"overbought": 80.0, "oversold": 22.5, "period": 5}` |
| 46 | `r1_c06` | `price_moving_average` | -19.2527 | -85.7267% | 85.7372% | 2100 | `{"entry_threshold": 0.0005, "period": 10}` |
| 47 | `r1_c16` | `price_moving_average` | -21.6784 | -88.3832% | 88.3929% | 2220 | `{"entry_threshold": 0.0005, "period": 9}` |
| 48 | `r1_c14` | `rsi_reversion` | -21.8065 | -88.7323% | 88.7359% | 4119 | `{"overbought": 75.0, "oversold": 22.5, "period": 5}` |
| 49 | `r1_c24` | `rsi_reversion` | -23.2788 | -90.0537% | 90.0537% | 4728 | `{"overbought": 70.0, "oversold": 25.0, "period": 5}` |
| 50 | `r1_c45` | `price_moving_average` | -28.4674 | -94.3114% | 94.3114% | 3005 | `{"entry_threshold": 0.0005, "period": 5}` |

## Round 2

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
| 11 | `r2_c05` | `multi_timeframe_ma_spread` | -0.7282 | -12.0953% | 35.1636% | 104 | `{"primary_ma_period": 19, "reference_ma_period": 52, "spread_threshold_bps": 40.0}` |
| 12 | `r2_c42` | `donchian_breakout` | -0.8247 | -14.1903% | 34.8492% | 245 | `{"breakout_buffer_bps": 20.0, "lookback_window": 67}` |
| 13 | `r2_c46` | `multi_timeframe_ma_spread` | -0.8274 | -13.1167% | 35.7336% | 113 | `{"primary_ma_period": 22, "reference_ma_period": 53, "spread_threshold_bps": 10.0}` |
| 14 | `r2_c06` | `multi_timeframe_ma_spread` | -0.8714 | -13.6337% | 36.3283% | 105 | `{"primary_ma_period": 23, "reference_ma_period": 55, "spread_threshold_bps": 20.0}` |
| 15 | `r2_c48` | `donchian_breakout` | -0.8762 | -14.8082% | 36.5985% | 236 | `{"breakout_buffer_bps": 20.0, "lookback_window": 75}` |
| 16 | `r2_c07` | `multi_timeframe_ma_spread` | -0.8853 | -13.8147% | 36.4572% | 90 | `{"primary_ma_period": 21, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 17 | `r2_c25` | `multi_timeframe_ma_spread` | -0.8990 | -13.9385% | 36.3697% | 108 | `{"primary_ma_period": 16, "reference_ma_period": 62, "spread_threshold_bps": 30.0}` |
| 18 | `r2_c43` | `multi_timeframe_ma_spread` | -0.9250 | -14.2406% | 35.8983% | 108 | `{"primary_ma_period": 19, "reference_ma_period": 60, "spread_threshold_bps": 10.0}` |
| 19 | `r2_c08` | `donchian_breakout` | -0.9965 | -16.2469% | 32.3411% | 403 | `{"breakout_buffer_bps": 10.0, "lookback_window": 65}` |
| 20 | `r2_c45` | `multi_timeframe_ma_spread` | -1.1888 | -17.2241% | 34.2240% | 109 | `{"primary_ma_period": 22, "reference_ma_period": 47, "spread_threshold_bps": 35.0}` |
| 21 | `r2_c31` | `donchian_breakout` | -1.3278 | -19.9649% | 40.4401% | 242 | `{"breakout_buffer_bps": 20.0, "lookback_window": 70}` |
| 22 | `r2_c30` | `moving_average_cross` | -1.7108 | -15.6087% | 19.5592% | 417 | `{"entry_threshold": 0.0025, "fast_window": 23, "slow_window": 100}` |
| 23 | `r2_c26` | `multi_timeframe_ma_spread` | -1.7159 | -22.6313% | 38.3530% | 133 | `{"primary_ma_period": 22, "reference_ma_period": 45, "spread_threshold_bps": 15.0}` |
| 24 | `r2_c09` | `donchian_breakout` | -1.9221 | -26.3494% | 40.4562% | 446 | `{"breakout_buffer_bps": 10.0, "lookback_window": 55}` |
| 25 | `r2_c50` | `moving_average_cross` | -2.2933 | -20.0511% | 25.1260% | 411 | `{"entry_threshold": 0.003, "fast_window": 23, "slow_window": 90}` |
| 26 | `r2_c41` | `donchian_breakout` | -2.3936 | -30.8966% | 45.4673% | 216 | `{"breakout_buffer_bps": 25.0, "lookback_window": 55}` |
| 27 | `r2_c10` | `moving_average_cross` | -2.6816 | -22.5187% | 28.1404% | 509 | `{"entry_threshold": 0.002, "fast_window": 22, "slow_window": 95}` |
| 28 | `r2_c24` | `multi_timeframe_ma_spread` | -2.7444 | -32.7492% | 46.6804% | 515 | `{"primary_ma_period": 2, "reference_ma_period": 24, "spread_threshold_bps": 10.0}` |
| 29 | `r2_c36` | `rsi_reversion` | -3.2614 | -33.1825% | 40.9330% | 914 | `{"overbought": 72.5, "oversold": 35.0, "period": 19}` |
| 30 | `r2_c32` | `rsi_reversion` | -3.6577 | -35.4586% | 39.8875% | 732 | `{"overbought": 75.0, "oversold": 30.0, "period": 17}` |
| 31 | `r2_c11` | `donchian_breakout` | -3.6580 | -42.2029% | 43.5453% | 707 | `{"breakout_buffer_bps": 0.0, "lookback_window": 65}` |
| 32 | `r2_c28` | `donchian_breakout` | -3.7141 | -42.6291% | 47.3154% | 605 | `{"breakout_buffer_bps": 5.0, "lookback_window": 55}` |
| 33 | `r2_c12` | `rsi_reversion` | -3.8160 | -30.3388% | 33.5824% | 783 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 34 | `r2_c13` | `moving_average_cross` | -4.3204 | -33.4226% | 34.6653% | 768 | `{"entry_threshold": 0.001, "fast_window": 20, "slow_window": 80}` |
| 35 | `r2_c34` | `moving_average_cross` | -4.3790 | -33.4596% | 35.1526% | 604 | `{"entry_threshold": 0.002, "fast_window": 23, "slow_window": 70}` |
| 36 | `r2_c33` | `moving_average_cross` | -4.5321 | -34.6712% | 35.6111% | 807 | `{"entry_threshold": 0.0005, "fast_window": 23, "slow_window": 90}` |
| 37 | `r2_c44` | `multi_timeframe_ma_spread` | -4.5670 | -47.5809% | 49.6502% | 633 | `{"primary_ma_period": 2, "reference_ma_period": 17, "spread_threshold_bps": 10.0}` |
| 38 | `r2_c14` | `moving_average_cross` | -4.8654 | -36.8236% | 38.1461% | 802 | `{"entry_threshold": 0.001, "fast_window": 21, "slow_window": 75}` |
| 39 | `r2_c38` | `rsi_reversion` | -5.1651 | -41.4939% | 43.6047% | 963 | `{"overbought": 70.0, "oversold": 30.0, "period": 17}` |
| 40 | `r2_c15` | `rsi_reversion` | -5.5360 | -44.3946% | 45.1756% | 1373 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
| 41 | `r2_c16` | `rsi_reversion` | -5.8727 | -48.6186% | 49.5008% | 1529 | `{"overbought": 70.0, "oversold": 35.0, "period": 15}` |
| 42 | `r2_c40` | `price_moving_average` | -6.2831 | -45.3463% | 48.1598% | 472 | `{"entry_threshold": 0.002, "period": 6}` |
| 43 | `r2_c17` | `moving_average_cross` | -6.2837 | -44.5821% | 45.6250% | 1183 | `{"entry_threshold": 0.001, "fast_window": 8, "slow_window": 55}` |
| 44 | `r2_c18` | `rsi_reversion` | -6.5085 | -50.9000% | 51.8592% | 1378 | `{"overbought": 70.0, "oversold": 32.5, "period": 15}` |
| 45 | `r2_c19` | `moving_average_cross` | -6.5181 | -45.1253% | 46.4828% | 962 | `{"entry_threshold": 0.0005, "fast_window": 19, "slow_window": 70}` |
| 46 | `r2_c49` | `donchian_breakout` | -6.9814 | -63.5836% | 63.7705% | 912 | `{"breakout_buffer_bps": 0.0, "lookback_window": 45}` |
| 47 | `r2_c20` | `price_moving_average` | -7.0831 | -49.6337% | 51.2682% | 648 | `{"entry_threshold": 0.0015, "period": 9}` |
| 48 | `r2_c39` | `moving_average_cross` | -7.3962 | -50.0248% | 50.9754% | 1166 | `{"entry_threshold": 0.0005, "fast_window": 16, "slow_window": 60}` |
| 49 | `r2_c35` | `rsi_reversion` | -8.1439 | -55.9623% | 56.6506% | 1432 | `{"overbought": 65.0, "oversold": 32.5, "period": 16}` |
| 50 | `r2_c37` | `moving_average_cross` | -8.3883 | -54.9610% | 56.2252% | 1664 | `{"entry_threshold": 0.0005, "fast_window": 6, "slow_window": 45}` |

## Round 3

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r3_c01` | `donchian_breakout` | 3.6157 | 58.1413% | 19.1910% | 95 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 2 | `r3_c41` | `donchian_breakout` | 2.5582 | 36.7902% | 22.9539% | 99 | `{"breakout_buffer_bps": 40.0, "lookback_window": 58}` |
| 3 | `r3_c46` | `donchian_breakout` | 2.1396 | 29.1521% | 27.2363% | 101 | `{"breakout_buffer_bps": 40.0, "lookback_window": 55}` |
| 4 | `r3_c02` | `donchian_breakout` | 1.6962 | 21.5874% | 27.4253% | 148 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 5 | `r3_c23` | `multi_timeframe_ma_spread` | 1.2244 | 13.2600% | 26.4470% | 83 | `{"primary_ma_period": 23, "reference_ma_period": 65, "spread_threshold_bps": 70.0}` |
| 6 | `r3_c03` | `multi_timeframe_ma_spread` | 0.8113 | 7.3561% | 30.5089% | 74 | `{"primary_ma_period": 22, "reference_ma_period": 70, "spread_threshold_bps": 50.0}` |
| 7 | `r3_c24` | `multi_timeframe_ma_spread` | 0.5605 | 3.9286% | 24.6558% | 79 | `{"primary_ma_period": 24, "reference_ma_period": 62, "spread_threshold_bps": 60.0}` |
| 8 | `r3_c50` | `multi_timeframe_ma_spread` | 0.4289 | 2.1591% | 20.1719% | 227 | `{"primary_ma_period": 10, "reference_ma_period": 27, "spread_threshold_bps": 30.0}` |
| 9 | `r3_c04` | `multi_timeframe_ma_spread` | 0.3008 | 0.4902% | 23.8181% | 79 | `{"primary_ma_period": 25, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 10 | `r3_c05` | `donchian_breakout` | 0.2473 | -0.4669% | 27.5863% | 338 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 11 | `r3_c43` | `multi_timeframe_ma_spread` | 0.1226 | -1.7918% | 29.3540% | 97 | `{"primary_ma_period": 17, "reference_ma_period": 65, "spread_threshold_bps": 50.0}` |
| 12 | `r3_c21` | `donchian_breakout` | 0.0985 | -2.4779% | 32.9409% | 165 | `{"breakout_buffer_bps": 30.0, "lookback_window": 53}` |
| 13 | `r3_c06` | `donchian_breakout` | 0.0389 | -3.2747% | 32.9503% | 171 | `{"breakout_buffer_bps": 30.0, "lookback_window": 45}` |
| 14 | `r3_c07` | `multi_timeframe_ma_spread` | -0.1297 | -4.9402% | 30.9595% | 119 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 15 | `r3_c44` | `multi_timeframe_ma_spread` | -0.1689 | -5.4120% | 33.1283% | 82 | `{"primary_ma_period": 20, "reference_ma_period": 70, "spread_threshold_bps": 45.0}` |
| 16 | `r3_c08` | `donchian_breakout` | -0.2436 | -7.0208% | 23.7214% | 395 | `{"breakout_buffer_bps": 10.0, "lookback_window": 67}` |
| 17 | `r3_c22` | `donchian_breakout` | -0.3290 | -8.1019% | 29.9322% | 255 | `{"breakout_buffer_bps": 20.0, "lookback_window": 63}` |
| 18 | `r3_c09` | `multi_timeframe_ma_spread` | -0.3429 | -7.5145% | 34.7930% | 97 | `{"primary_ma_period": 18, "reference_ma_period": 58, "spread_threshold_bps": 30.0}` |
| 19 | `r3_c47` | `multi_timeframe_ma_spread` | -0.3700 | -7.8624% | 32.4029% | 111 | `{"primary_ma_period": 19, "reference_ma_period": 52, "spread_threshold_bps": 30.0}` |
| 20 | `r3_c42` | `donchian_breakout` | -0.5338 | -10.5794% | 43.1405% | 53 | `{"breakout_buffer_bps": 50.0, "lookback_window": 70}` |
| 21 | `r3_c29` | `multi_timeframe_ma_spread` | -0.5786 | -10.3386% | 34.6180% | 103 | `{"primary_ma_period": 19, "reference_ma_period": 53, "spread_threshold_bps": 35.0}` |
| 22 | `r3_c10` | `multi_timeframe_ma_spread` | -0.6201 | -11.0834% | 32.2154% | 367 | `{"primary_ma_period": 5, "reference_ma_period": 22, "spread_threshold_bps": 20.0}` |
| 23 | `r3_c27` | `multi_timeframe_ma_spread` | -0.9423 | -14.4093% | 35.1937% | 119 | `{"primary_ma_period": 15, "reference_ma_period": 52, "spread_threshold_bps": 15.0}` |
| 24 | `r3_c35` | `rsi_reversion` | -1.0403 | -13.4128% | 35.1398% | 333 | `{"overbought": 77.5, "oversold": 25.0, "period": 19}` |
| 25 | `r3_c31` | `moving_average_cross` | -1.2215 | -11.8356% | 17.8382% | 335 | `{"entry_threshold": 0.0035, "fast_window": 20, "slow_window": 115}` |
| 26 | `r3_c32` | `moving_average_cross` | -1.4310 | -13.5543% | 20.2304% | 369 | `{"entry_threshold": 0.003, "fast_window": 22, "slow_window": 105}` |
| 27 | `r3_c28` | `donchian_breakout` | -1.4698 | -21.5263% | 41.5983% | 240 | `{"breakout_buffer_bps": 20.0, "lookback_window": 72}` |
| 28 | `r3_c49` | `multi_timeframe_ma_spread` | -1.5962 | -21.2650% | 41.6416% | 99 | `{"primary_ma_period": 17, "reference_ma_period": 68, "spread_threshold_bps": 30.0}` |
| 29 | `r3_c33` | `moving_average_cross` | -1.6575 | -15.1465% | 20.7508% | 413 | `{"entry_threshold": 0.0025, "fast_window": 20, "slow_window": 110}` |
| 30 | `r3_c45` | `donchian_breakout` | -1.6706 | -23.7441% | 35.0342% | 553 | `{"breakout_buffer_bps": 5.0, "lookback_window": 62}` |
| 31 | `r3_c30` | `multi_timeframe_ma_spread` | -1.7102 | -23.1870% | 31.4358% | 529 | `{"primary_ma_period": 2, "reference_ma_period": 17, "spread_threshold_bps": 40.0}` |
| 32 | `r3_c11` | `moving_average_cross` | -1.7108 | -15.6087% | 19.5592% | 417 | `{"entry_threshold": 0.0025, "fast_window": 23, "slow_window": 100}` |
| 33 | `r3_c34` | `rsi_reversion` | -2.0816 | -26.4070% | 36.8319% | 278 | `{"overbought": 77.5, "oversold": 37.5, "period": 23}` |
| 34 | `r3_c12` | `moving_average_cross` | -2.2933 | -20.0511% | 25.1260% | 411 | `{"entry_threshold": 0.003, "fast_window": 23, "slow_window": 90}` |
| 35 | `r3_c48` | `donchian_breakout` | -2.5726 | -32.7421% | 38.9367% | 617 | `{"breakout_buffer_bps": 0.0, "lookback_window": 77}` |
| 36 | `r3_c13` | `moving_average_cross` | -2.6816 | -22.5187% | 28.1404% | 509 | `{"entry_threshold": 0.002, "fast_window": 22, "slow_window": 95}` |
| 37 | `r3_c38` | `moving_average_cross` | -2.6868 | -22.3249% | 27.7299% | 541 | `{"entry_threshold": 0.002, "fast_window": 20, "slow_window": 85}` |
| 38 | `r3_c26` | `donchian_breakout` | -3.0371 | -36.8633% | 48.1437% | 308 | `{"breakout_buffer_bps": 20.0, "lookback_window": 40}` |
| 39 | `r3_c14` | `rsi_reversion` | -3.2614 | -33.1825% | 40.9330% | 914 | `{"overbought": 72.5, "oversold": 35.0, "period": 19}` |
| 40 | `r3_c39` | `rsi_reversion` | -3.3755 | -28.0852% | 33.0385% | 597 | `{"overbought": 70.0, "oversold": 25.0, "period": 18}` |
| 41 | `r3_c15` | `rsi_reversion` | -3.6577 | -35.4586% | 39.8875% | 732 | `{"overbought": 75.0, "oversold": 30.0, "period": 17}` |
| 42 | `r3_c37` | `moving_average_cross` | -3.7983 | -30.2772% | 32.1472% | 609 | `{"entry_threshold": 0.0015, "fast_window": 21, "slow_window": 95}` |
| 43 | `r3_c16` | `rsi_reversion` | -3.8160 | -30.3388% | 33.5824% | 783 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 44 | `r3_c17` | `moving_average_cross` | -4.3204 | -33.4226% | 34.6653% | 768 | `{"entry_threshold": 0.001, "fast_window": 20, "slow_window": 80}` |
| 45 | `r3_c18` | `moving_average_cross` | -4.3790 | -33.4596% | 35.1526% | 604 | `{"entry_threshold": 0.002, "fast_window": 23, "slow_window": 70}` |
| 46 | `r3_c19` | `rsi_reversion` | -5.1651 | -41.4939% | 43.6047% | 963 | `{"overbought": 70.0, "oversold": 30.0, "period": 17}` |
| 47 | `r3_c36` | `rsi_reversion` | -5.3321 | -34.5782% | 35.1566% | 937 | `{"overbought": 67.5, "oversold": 20.0, "period": 12}` |
| 48 | `r3_c20` | `rsi_reversion` | -5.5360 | -44.3946% | 45.1756% | 1373 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
| 49 | `r3_c25` | `donchian_breakout` | -6.2985 | -59.9664% | 61.0636% | 666 | `{"breakout_buffer_bps": 5.0, "lookback_window": 47}` |
| 50 | `r3_c40` | `rsi_reversion` | -8.7183 | -59.7340% | 60.2276% | 1767 | `{"overbought": 65.0, "oversold": 35.0, "period": 15}` |

## Round 4

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r4_c01` | `donchian_breakout` | 3.6157 | 58.1413% | 19.1910% | 95 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 2 | `r4_c21` | `donchian_breakout` | 3.0899 | 47.2702% | 22.4945% | 114 | `{"breakout_buffer_bps": 35.0, "lookback_window": 68}` |
| 3 | `r4_c42` | `donchian_breakout` | 2.9172 | 43.6898% | 22.9539% | 97 | `{"breakout_buffer_bps": 40.0, "lookback_window": 60}` |
| 4 | `r4_c24` | `donchian_breakout` | 2.9098 | 43.5758% | 24.7050% | 92 | `{"breakout_buffer_bps": 40.0, "lookback_window": 67}` |
| 5 | `r4_c02` | `donchian_breakout` | 2.5582 | 36.7902% | 22.9539% | 99 | `{"breakout_buffer_bps": 40.0, "lookback_window": 58}` |
| 6 | `r4_c03` | `donchian_breakout` | 2.1396 | 29.1521% | 27.2363% | 101 | `{"breakout_buffer_bps": 40.0, "lookback_window": 55}` |
| 7 | `r4_c04` | `donchian_breakout` | 1.6962 | 21.5874% | 27.4253% | 148 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 8 | `r4_c30` | `donchian_breakout` | 1.5319 | 18.8290% | 25.0644% | 127 | `{"breakout_buffer_bps": 35.0, "lookback_window": 55}` |
| 9 | `r4_c05` | `multi_timeframe_ma_spread` | 1.2244 | 13.2600% | 26.4470% | 83 | `{"primary_ma_period": 23, "reference_ma_period": 65, "spread_threshold_bps": 70.0}` |
| 10 | `r4_c22` | `donchian_breakout` | 1.1702 | 13.0499% | 23.2508% | 72 | `{"breakout_buffer_bps": 45.0, "lookback_window": 60}` |
| 11 | `r4_c47` | `multi_timeframe_ma_spread` | 1.1327 | 11.9660% | 22.5710% | 91 | `{"primary_ma_period": 21, "reference_ma_period": 57, "spread_threshold_bps": 80.0}` |
| 12 | `r4_c45` | `multi_timeframe_ma_spread` | 1.1176 | 11.7475% | 24.6780% | 90 | `{"primary_ma_period": 18, "reference_ma_period": 60, "spread_threshold_bps": 90.0}` |
| 13 | `r4_c41` | `donchian_breakout` | 1.0731 | 11.5458% | 24.2719% | 75 | `{"breakout_buffer_bps": 45.0, "lookback_window": 53}` |
| 14 | `r4_c26` | `multi_timeframe_ma_spread` | 0.9383 | 9.1433% | 28.6257% | 81 | `{"primary_ma_period": 19, "reference_ma_period": 68, "spread_threshold_bps": 70.0}` |
| 15 | `r4_c50` | `donchian_breakout` | 0.8871 | 8.7598% | 19.7456% | 310 | `{"breakout_buffer_bps": 15.0, "lookback_window": 67}` |
| 16 | `r4_c06` | `multi_timeframe_ma_spread` | 0.8113 | 7.3561% | 30.5089% | 74 | `{"primary_ma_period": 22, "reference_ma_period": 70, "spread_threshold_bps": 50.0}` |
| 17 | `r4_c46` | `multi_timeframe_ma_spread` | 0.7705 | 6.7841% | 31.9180% | 77 | `{"primary_ma_period": 17, "reference_ma_period": 75, "spread_threshold_bps": 55.0}` |
| 18 | `r4_c27` | `multi_timeframe_ma_spread` | 0.6062 | 4.5488% | 21.5967% | 91 | `{"primary_ma_period": 21, "reference_ma_period": 57, "spread_threshold_bps": 60.0}` |
| 19 | `r4_c07` | `multi_timeframe_ma_spread` | 0.5605 | 3.9286% | 24.6558% | 79 | `{"primary_ma_period": 24, "reference_ma_period": 62, "spread_threshold_bps": 60.0}` |
| 20 | `r4_c08` | `multi_timeframe_ma_spread` | 0.4289 | 2.1591% | 20.1719% | 227 | `{"primary_ma_period": 10, "reference_ma_period": 27, "spread_threshold_bps": 30.0}` |
| 21 | `r4_c09` | `multi_timeframe_ma_spread` | 0.3008 | 0.4902% | 23.8181% | 79 | `{"primary_ma_period": 25, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 22 | `r4_c25` | `multi_timeframe_ma_spread` | 0.2756 | 0.1738% | 33.9179% | 71 | `{"primary_ma_period": 22, "reference_ma_period": 75, "spread_threshold_bps": 60.0}` |
| 23 | `r4_c10` | `donchian_breakout` | 0.2473 | -0.4669% | 27.5863% | 338 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 24 | `r4_c44` | `donchian_breakout` | 0.0992 | -2.4686% | 32.9409% | 164 | `{"breakout_buffer_bps": 30.0, "lookback_window": 55}` |
| 25 | `r4_c32` | `moving_average_cross` | -0.0640 | -2.2015% | 13.6485% | 284 | `{"entry_threshold": 0.004, "fast_window": 23, "slow_window": 120}` |
| 26 | `r4_c23` | `donchian_breakout` | -0.1708 | -5.9925% | 40.4666% | 56 | `{"breakout_buffer_bps": 50.0, "lookback_window": 65}` |
| 27 | `r4_c43` | `donchian_breakout` | -0.4015 | -8.9632% | 36.7882% | 59 | `{"breakout_buffer_bps": 50.0, "lookback_window": 60}` |
| 28 | `r4_c29` | `multi_timeframe_ma_spread` | -0.4283 | -8.5928% | 31.8371% | 99 | `{"primary_ma_period": 24, "reference_ma_period": 50, "spread_threshold_bps": 60.0}` |
| 29 | `r4_c34` | `moving_average_cross` | -0.5502 | -6.2025% | 13.5433% | 370 | `{"entry_threshold": 0.0025, "fast_window": 21, "slow_window": 125}` |
| 30 | `r4_c49` | `multi_timeframe_ma_spread` | -0.7317 | -12.0692% | 36.4881% | 103 | `{"primary_ma_period": 20, "reference_ma_period": 62, "spread_threshold_bps": 35.0}` |
| 31 | `r4_c33` | `moving_average_cross` | -0.8246 | -8.7424% | 15.1407% | 319 | `{"entry_threshold": 0.004, "fast_window": 20, "slow_window": 100}` |
| 32 | `r4_c11` | `rsi_reversion` | -1.0403 | -13.4128% | 35.1398% | 333 | `{"overbought": 77.5, "oversold": 25.0, "period": 19}` |
| 33 | `r4_c12` | `moving_average_cross` | -1.2215 | -11.8356% | 17.8382% | 335 | `{"entry_threshold": 0.0035, "fast_window": 20, "slow_window": 115}` |
| 34 | `r4_c48` | `multi_timeframe_ma_spread` | -1.3647 | -19.2477% | 33.0988% | 185 | `{"primary_ma_period": 13, "reference_ma_period": 29, "spread_threshold_bps": 35.0}` |
| 35 | `r4_c28` | `multi_timeframe_ma_spread` | -1.3743 | -19.3385% | 31.9837% | 218 | `{"primary_ma_period": 9, "reference_ma_period": 32, "spread_threshold_bps": 30.0}` |
| 36 | `r4_c13` | `moving_average_cross` | -1.4310 | -13.5543% | 20.2304% | 369 | `{"entry_threshold": 0.003, "fast_window": 22, "slow_window": 105}` |
| 37 | `r4_c35` | `moving_average_cross` | -1.6377 | -15.1892% | 20.2464% | 364 | `{"entry_threshold": 0.0035, "fast_window": 21, "slow_window": 95}` |
| 38 | `r4_c14` | `moving_average_cross` | -1.6575 | -15.1465% | 20.7508% | 413 | `{"entry_threshold": 0.0025, "fast_window": 20, "slow_window": 110}` |
| 39 | `r4_c15` | `moving_average_cross` | -1.7108 | -15.6087% | 19.5592% | 417 | `{"entry_threshold": 0.0025, "fast_window": 23, "slow_window": 100}` |
| 40 | `r4_c31` | `rsi_reversion` | -1.9067 | -21.2446% | 35.5903% | 108 | `{"overbought": 80.0, "oversold": 22.5, "period": 23}` |
| 41 | `r4_c37` | `moving_average_cross` | -1.9336 | -17.4047% | 22.7361% | 417 | `{"entry_threshold": 0.0025, "fast_window": 26, "slow_window": 95}` |
| 42 | `r4_c16` | `rsi_reversion` | -2.0816 | -26.4070% | 36.8319% | 278 | `{"overbought": 77.5, "oversold": 37.5, "period": 23}` |
| 43 | `r4_c17` | `moving_average_cross` | -2.2933 | -20.0511% | 25.1260% | 411 | `{"entry_threshold": 0.003, "fast_window": 23, "slow_window": 90}` |
| 44 | `r4_c36` | `rsi_reversion` | -2.4526 | -28.9402% | 37.5825% | 569 | `{"overbought": 75.0, "oversold": 40.0, "period": 21}` |
| 45 | `r4_c40` | `rsi_reversion` | -2.8513 | -31.7035% | 40.0661% | 547 | `{"overbought": 80.0, "oversold": 32.5, "period": 16}` |
| 46 | `r4_c18` | `rsi_reversion` | -3.2614 | -33.1825% | 40.9330% | 914 | `{"overbought": 72.5, "oversold": 35.0, "period": 19}` |
| 47 | `r4_c19` | `rsi_reversion` | -3.3755 | -28.0852% | 33.0385% | 597 | `{"overbought": 70.0, "oversold": 25.0, "period": 18}` |
| 48 | `r4_c20` | `rsi_reversion` | -3.6577 | -35.4586% | 39.8875% | 732 | `{"overbought": 75.0, "oversold": 30.0, "period": 17}` |
| 49 | `r4_c39` | `rsi_reversion` | -3.8160 | -30.3388% | 33.5824% | 783 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 50 | `r4_c38` | `rsi_reversion` | -4.1173 | -39.0597% | 42.6427% | 1186 | `{"overbought": 67.5, "oversold": 40.0, "period": 21}` |

## Round 5

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r5_c01` | `donchian_breakout` | 3.6157 | 58.1413% | 19.1910% | 95 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 2 | `r5_c02` | `donchian_breakout` | 3.0899 | 47.2702% | 22.4945% | 114 | `{"breakout_buffer_bps": 35.0, "lookback_window": 68}` |
| 3 | `r5_c44` | `donchian_breakout` | 3.0895 | 47.2608% | 22.4945% | 113 | `{"breakout_buffer_bps": 35.0, "lookback_window": 72}` |
| 4 | `r5_c21` | `donchian_breakout` | 2.9854 | 45.1720% | 22.4945% | 112 | `{"breakout_buffer_bps": 35.0, "lookback_window": 73}` |
| 5 | `r5_c03` | `donchian_breakout` | 2.9172 | 43.6898% | 22.9539% | 97 | `{"breakout_buffer_bps": 40.0, "lookback_window": 60}` |
| 6 | `r5_c24` | `donchian_breakout` | 2.9172 | 43.6898% | 22.9539% | 97 | `{"breakout_buffer_bps": 40.0, "lookback_window": 62}` |
| 7 | `r5_c04` | `donchian_breakout` | 2.9098 | 43.5758% | 24.7050% | 92 | `{"breakout_buffer_bps": 40.0, "lookback_window": 67}` |
| 8 | `r5_c43` | `donchian_breakout` | 2.9098 | 43.5758% | 24.7050% | 92 | `{"breakout_buffer_bps": 40.0, "lookback_window": 70}` |
| 9 | `r5_c05` | `donchian_breakout` | 2.5582 | 36.7902% | 22.9539% | 99 | `{"breakout_buffer_bps": 40.0, "lookback_window": 58}` |
| 10 | `r5_c41` | `donchian_breakout` | 2.1633 | 29.5932% | 20.6542% | 120 | `{"breakout_buffer_bps": 35.0, "lookback_window": 61}` |
| 11 | `r5_c45` | `donchian_breakout` | 1.5319 | 18.8290% | 25.0644% | 127 | `{"breakout_buffer_bps": 35.0, "lookback_window": 53}` |
| 12 | `r5_c26` | `multi_timeframe_ma_spread` | 1.4207 | 16.1496% | 26.1799% | 76 | `{"primary_ma_period": 26, "reference_ma_period": 70, "spread_threshold_bps": 60.0}` |
| 13 | `r5_c27` | `multi_timeframe_ma_spread` | 1.2705 | 14.0849% | 20.1863% | 98 | `{"primary_ma_period": 20, "reference_ma_period": 52, "spread_threshold_bps": 100.0}` |
| 14 | `r5_c06` | `multi_timeframe_ma_spread` | 1.2244 | 13.2600% | 26.4470% | 83 | `{"primary_ma_period": 23, "reference_ma_period": 65, "spread_threshold_bps": 70.0}` |
| 15 | `r5_c42` | `donchian_breakout` | 1.1331 | 12.4631% | 23.6491% | 72 | `{"breakout_buffer_bps": 45.0, "lookback_window": 58}` |
| 16 | `r5_c07` | `multi_timeframe_ma_spread` | 1.1327 | 11.9660% | 22.5710% | 91 | `{"primary_ma_period": 21, "reference_ma_period": 57, "spread_threshold_bps": 80.0}` |
| 17 | `r5_c08` | `multi_timeframe_ma_spread` | 1.1176 | 11.7475% | 24.6780% | 90 | `{"primary_ma_period": 18, "reference_ma_period": 60, "spread_threshold_bps": 90.0}` |
| 18 | `r5_c28` | `multi_timeframe_ma_spread` | 1.0586 | 10.9134% | 26.6901% | 85 | `{"primary_ma_period": 21, "reference_ma_period": 55, "spread_threshold_bps": 100.0}` |
| 19 | `r5_c09` | `multi_timeframe_ma_spread` | 0.9383 | 9.1433% | 28.6257% | 81 | `{"primary_ma_period": 19, "reference_ma_period": 68, "spread_threshold_bps": 70.0}` |
| 20 | `r5_c49` | `multi_timeframe_ma_spread` | 0.9106 | 8.7567% | 30.4428% | 67 | `{"primary_ma_period": 24, "reference_ma_period": 66, "spread_threshold_bps": 90.0}` |
| 21 | `r5_c30` | `multi_timeframe_ma_spread` | 0.8636 | 8.0661% | 32.4657% | 72 | `{"primary_ma_period": 19, "reference_ma_period": 75, "spread_threshold_bps": 55.0}` |
| 22 | `r5_c10` | `multi_timeframe_ma_spread` | 0.8113 | 7.3561% | 30.5089% | 74 | `{"primary_ma_period": 22, "reference_ma_period": 70, "spread_threshold_bps": 50.0}` |
| 23 | `r5_c50` | `multi_timeframe_ma_spread` | 0.7542 | 6.5702% | 29.2661% | 74 | `{"primary_ma_period": 23, "reference_ma_period": 68, "spread_threshold_bps": 60.0}` |
| 24 | `r5_c29` | `multi_timeframe_ma_spread` | 0.5300 | 3.5200% | 32.2642% | 78 | `{"primary_ma_period": 22, "reference_ma_period": 66, "spread_threshold_bps": 75.0}` |
| 25 | `r5_c48` | `multi_timeframe_ma_spread` | 0.5278 | 3.4907% | 21.3797% | 109 | `{"primary_ma_period": 13, "reference_ma_period": 55, "spread_threshold_bps": 85.0}` |
| 26 | `r5_c47` | `multi_timeframe_ma_spread` | 0.2116 | -0.6711% | 35.1091% | 84 | `{"primary_ma_period": 18, "reference_ma_period": 67, "spread_threshold_bps": 100.0}` |
| 27 | `r5_c36` | `moving_average_cross` | 0.1641 | -0.1582% | 11.1118% | 289 | `{"entry_threshold": 0.004, "fast_window": 23, "slow_window": 115}` |
| 28 | `r5_c46` | `multi_timeframe_ma_spread` | 0.1612 | -1.3201% | 35.5169% | 78 | `{"primary_ma_period": 20, "reference_ma_period": 75, "spread_threshold_bps": 80.0}` |
| 29 | `r5_c31` | `moving_average_cross` | -0.0633 | -2.1288% | 13.7270% | 289 | `{"entry_threshold": 0.004, "fast_window": 20, "slow_window": 135}` |
| 30 | `r5_c11` | `moving_average_cross` | -0.0640 | -2.2015% | 13.6485% | 284 | `{"entry_threshold": 0.004, "fast_window": 23, "slow_window": 120}` |
| 31 | `r5_c23` | `donchian_breakout` | -0.1247 | -5.4236% | 34.3304% | 60 | `{"breakout_buffer_bps": 50.0, "lookback_window": 55}` |
| 32 | `r5_c25` | `donchian_breakout` | -0.1247 | -5.4236% | 34.3304% | 60 | `{"breakout_buffer_bps": 50.0, "lookback_window": 56}` |
| 33 | `r5_c22` | `donchian_breakout` | -0.4770 | -9.9008% | 48.2131% | 46 | `{"breakout_buffer_bps": 55.0, "lookback_window": 73}` |
| 34 | `r5_c12` | `moving_average_cross` | -0.5502 | -6.2025% | 13.5433% | 370 | `{"entry_threshold": 0.0025, "fast_window": 21, "slow_window": 125}` |
| 35 | `r5_c35` | `moving_average_cross` | -0.6394 | -7.1487% | 13.7101% | 334 | `{"entry_threshold": 0.0035, "fast_window": 22, "slow_window": 110}` |
| 36 | `r5_c37` | `rsi_reversion` | -0.6899 | -9.3087% | 28.2476% | 211 | `{"overbought": 80.0, "oversold": 22.5, "period": 19}` |
| 37 | `r5_c32` | `moving_average_cross` | -0.7725 | -8.0558% | 17.4808% | 309 | `{"entry_threshold": 0.003, "fast_window": 24, "slow_window": 140}` |
| 38 | `r5_c13` | `moving_average_cross` | -0.8246 | -8.7424% | 15.1407% | 319 | `{"entry_threshold": 0.004, "fast_window": 20, "slow_window": 100}` |
| 39 | `r5_c14` | `rsi_reversion` | -1.0403 | -13.4128% | 35.1398% | 333 | `{"overbought": 77.5, "oversold": 25.0, "period": 19}` |
| 40 | `r5_c15` | `moving_average_cross` | -1.2215 | -11.8356% | 17.8382% | 335 | `{"entry_threshold": 0.0035, "fast_window": 20, "slow_window": 115}` |
| 41 | `r5_c16` | `moving_average_cross` | -1.4310 | -13.5543% | 20.2304% | 369 | `{"entry_threshold": 0.003, "fast_window": 22, "slow_window": 105}` |
| 42 | `r5_c33` | `moving_average_cross` | -1.4508 | -13.7626% | 18.3142% | 343 | `{"entry_threshold": 0.004, "fast_window": 18, "slow_window": 95}` |
| 43 | `r5_c38` | `rsi_reversion` | -1.5252 | -21.7704% | 37.2801% | 34 | `{"overbought": 82.5, "oversold": 37.5, "period": 27}` |
| 44 | `r5_c17` | `rsi_reversion` | -1.9067 | -21.2446% | 35.5903% | 108 | `{"overbought": 80.0, "oversold": 22.5, "period": 23}` |
| 45 | `r5_c18` | `rsi_reversion` | -2.0816 | -26.4070% | 36.8319% | 278 | `{"overbought": 77.5, "oversold": 37.5, "period": 23}` |
| 46 | `r5_c40` | `rsi_reversion` | -2.2540 | -26.9629% | 37.3940% | 535 | `{"overbought": 82.5, "oversold": 30.0, "period": 14}` |
| 47 | `r5_c19` | `rsi_reversion` | -2.4526 | -28.9402% | 37.5825% | 569 | `{"overbought": 75.0, "oversold": 40.0, "period": 21}` |
| 48 | `r5_c34` | `rsi_reversion` | -2.5469 | -25.2428% | 32.9859% | 433 | `{"overbought": 72.5, "oversold": 27.5, "period": 21}` |
| 49 | `r5_c20` | `rsi_reversion` | -2.8513 | -31.7035% | 40.0661% | 547 | `{"overbought": 80.0, "oversold": 32.5, "period": 16}` |
| 50 | `r5_c39` | `rsi_reversion` | -3.3384 | -35.4164% | 42.0065% | 973 | `{"overbought": 75.0, "oversold": 40.0, "period": 17}` |
