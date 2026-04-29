# LLM Strategy Evolution

- Symbol: `ETHUSDT`
- Primary timeframe: `5m`
- Secondary timeframe: `1h`
- Rounds: `5`
- Best strategy: `donchian_breakout`
- Best Sharpe: `2.4810`
- Best total return: `47.0799%`
- Best max drawdown: `19.8418%`
- Best trade count: `249`

## Round 1

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r1_c27` | `multi_timeframe_ma_spread` | 1.5975 | 23.6517% | 26.4034% | 155 | `{"primary_ma_period": 15, "reference_ma_period": 30, "spread_threshold_bps": 0.0}` |
| 2 | `r1_c49` | `donchian_breakout` | 1.4897 | 22.7266% | 23.0396% | 216 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 3 | `r1_c47` | `multi_timeframe_ma_spread` | 1.1800 | 15.2005% | 31.7224% | 125 | `{"primary_ma_period": 19, "reference_ma_period": 52, "spread_threshold_bps": 40.0}` |
| 4 | `r1_c18` | `multi_timeframe_ma_spread` | 1.0277 | 12.2308% | 32.7884% | 93 | `{"primary_ma_period": 25, "reference_ma_period": 55, "spread_threshold_bps": 10.0}` |
| 5 | `r1_c28` | `multi_timeframe_ma_spread` | 1.0252 | 12.2052% | 35.2912% | 104 | `{"primary_ma_period": 21, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 6 | `r1_c38` | `multi_timeframe_ma_spread` | 0.7852 | 7.7602% | 34.9988% | 105 | `{"primary_ma_period": 23, "reference_ma_period": 55, "spread_threshold_bps": 20.0}` |
| 7 | `r1_c40` | `donchian_breakout` | 0.6163 | 4.5663% | 33.6929% | 375 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 8 | `r1_c20` | `donchian_breakout` | 0.2041 | -3.0750% | 33.7503% | 443 | `{"breakout_buffer_bps": 10.0, "lookback_window": 65}` |
| 9 | `r1_c08` | `multi_timeframe_ma_spread` | 0.0285 | -5.1941% | 34.4540% | 122 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 10 | `r1_c37` | `multi_timeframe_ma_spread` | -0.2343 | -9.5508% | 37.4216% | 253 | `{"primary_ma_period": 13, "reference_ma_period": 22, "spread_threshold_bps": 10.0}` |
| 11 | `r1_c17` | `multi_timeframe_ma_spread` | -0.3942 | -12.0201% | 41.5561% | 341 | `{"primary_ma_period": 5, "reference_ma_period": 22, "spread_threshold_bps": 20.0}` |
| 12 | `r1_c10` | `donchian_breakout` | -0.3962 | -13.2208% | 46.1740% | 479 | `{"breakout_buffer_bps": 10.0, "lookback_window": 55}` |
| 13 | `r1_c30` | `donchian_breakout` | -0.6086 | -16.5576% | 41.9903% | 629 | `{"breakout_buffer_bps": 0.0, "lookback_window": 65}` |
| 14 | `r1_c33` | `moving_average_cross` | -2.4233 | -27.3835% | 37.6770% | 955 | `{"entry_threshold": 0.001, "fast_window": 21, "slow_window": 75}` |
| 15 | `r1_c13` | `moving_average_cross` | -2.4455 | -27.2045% | 36.1604% | 661 | `{"entry_threshold": 0.002, "fast_window": 22, "slow_window": 95}` |
| 16 | `r1_c07` | `multi_timeframe_ma_spread` | -2.8529 | -42.6279% | 53.4605% | 304 | `{"primary_ma_period": 10, "reference_ma_period": 20, "spread_threshold_bps": 0.0}` |
| 17 | `r1_c03` | `moving_average_cross` | -3.4977 | -36.0372% | 41.7864% | 931 | `{"entry_threshold": 0.001, "fast_window": 20, "slow_window": 80}` |
| 18 | `r1_c46` | `multi_timeframe_ma_spread` | -3.6322 | -50.4813% | 58.5238% | 366 | `{"primary_ma_period": 7, "reference_ma_period": 18, "spread_threshold_bps": 5.0}` |
| 19 | `r1_c15` | `rsi_reversion` | -3.9315 | -41.5088% | 43.3641% | 833 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 20 | `r1_c23` | `moving_average_cross` | -4.8634 | -45.4964% | 50.6981% | 1196 | `{"entry_threshold": 0.0005, "fast_window": 19, "slow_window": 70}` |
| 21 | `r1_c05` | `rsi_reversion` | -5.2353 | -54.2027% | 54.7710% | 1541 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
| 22 | `r1_c36` | `price_moving_average` | -5.4435 | -52.1673% | 54.6769% | 893 | `{"entry_threshold": 0.0015, "period": 9}` |
| 23 | `r1_c19` | `donchian_breakout` | -5.6710 | -67.2134% | 71.7577% | 1240 | `{"breakout_buffer_bps": 5.0, "lookback_window": 18}` |
| 24 | `r1_c12` | `moving_average_cross` | -5.6714 | -50.3728% | 53.3706% | 1537 | `{"entry_threshold": 0.001, "fast_window": 8, "slow_window": 55}` |
| 25 | `r1_c35` | `rsi_reversion` | -5.6870 | -59.0846% | 60.5257% | 1733 | `{"overbought": 70.0, "oversold": 35.0, "period": 15}` |
| 26 | `r1_c25` | `rsi_reversion` | -5.8204 | -59.0218% | 60.1991% | 1576 | `{"overbought": 70.0, "oversold": 32.5, "period": 15}` |
| 27 | `r1_c09` | `donchian_breakout` | -6.0802 | -69.6108% | 71.3124% | 1552 | `{"breakout_buffer_bps": 0.0, "lookback_window": 20}` |
| 28 | `r1_c32` | `moving_average_cross` | -6.3705 | -55.2466% | 56.8356% | 1972 | `{"entry_threshold": 0.0005, "fast_window": 9, "slow_window": 45}` |
| 29 | `r1_c29` | `donchian_breakout` | -6.5512 | -72.1498% | 74.2947% | 1463 | `{"breakout_buffer_bps": 0.0, "lookback_window": 22}` |
| 30 | `r1_c21` | `moving_average_cross` | -7.1773 | -59.0808% | 59.4949% | 2207 | `{"entry_threshold": 0.001, "fast_window": 7, "slow_window": 30}` |
| 31 | `r1_c02` | `moving_average_cross` | -7.4741 | -60.2902% | 61.1446% | 2041 | `{"entry_threshold": 0.0005, "fast_window": 10, "slow_window": 40}` |
| 32 | `r1_c22` | `moving_average_cross` | -7.7846 | -61.6966% | 62.5971% | 2159 | `{"entry_threshold": 0.0005, "fast_window": 11, "slow_window": 35}` |
| 33 | `r1_c39` | `donchian_breakout` | -8.0550 | -78.9914% | 80.4304% | 1805 | `{"breakout_buffer_bps": 5.0, "lookback_window": 10}` |
| 34 | `r1_c48` | `donchian_breakout` | -8.3614 | -80.1090% | 80.6019% | 1867 | `{"breakout_buffer_bps": 0.0, "lookback_window": 15}` |
| 35 | `r1_c42` | `moving_average_cross` | -8.4793 | -64.5455% | 65.0284% | 2454 | `{"entry_threshold": 0.0, "fast_window": 8, "slow_window": 45}` |
| 36 | `r1_c26` | `price_moving_average` | -8.8636 | -68.1027% | 68.4002% | 1174 | `{"entry_threshold": 0.001, "period": 13}` |
| 37 | `r1_c31` | `moving_average_cross` | -9.0290 | -68.3254% | 68.8309% | 3118 | `{"entry_threshold": 0.0, "fast_window": 8, "slow_window": 30}` |
| 38 | `r1_c11` | `moving_average_cross` | -9.4314 | -70.1733% | 70.3315% | 3250 | `{"entry_threshold": 0.0005, "fast_window": 4, "slow_window": 25}` |
| 39 | `r1_c04` | `rsi_reversion` | -10.6344 | -77.7665% | 77.9938% | 3178 | `{"overbought": 75.0, "oversold": 25.0, "period": 7}` |
| 40 | `r1_c41` | `moving_average_cross` | -10.7684 | -74.8649% | 75.2934% | 3833 | `{"entry_threshold": 0.0, "fast_window": 6, "slow_window": 25}` |
| 41 | `r1_c44` | `rsi_reversion` | -11.9316 | -80.7058% | 80.9562% | 3470 | `{"overbought": 65.0, "oversold": 35.0, "period": 10}` |
| 42 | `r1_c01` | `moving_average_cross` | -12.7863 | -80.7157% | 81.0714% | 4589 | `{"entry_threshold": 0.0, "fast_window": 5, "slow_window": 20}` |
| 43 | `r1_c50` | `moving_average_cross` | -13.2509 | -80.6834% | 80.7322% | 3787 | `{"entry_threshold": 0.001, "fast_window": 4, "slow_window": 10}` |
| 44 | `r1_c06` | `price_moving_average` | -14.7307 | -85.5237% | 85.5615% | 2298 | `{"entry_threshold": 0.0005, "period": 10}` |
| 45 | `r1_c43` | `rsi_reversion` | -14.8095 | -85.1990% | 85.2759% | 3749 | `{"overbought": 70.0, "oversold": 22.5, "period": 6}` |
| 46 | `r1_c16` | `price_moving_average` | -15.4013 | -86.6864% | 86.6990% | 2389 | `{"entry_threshold": 0.0005, "period": 9}` |
| 47 | `r1_c34` | `rsi_reversion` | -15.6910 | -89.0843% | 89.0990% | 4157 | `{"overbought": 80.0, "oversold": 22.5, "period": 5}` |
| 48 | `r1_c14` | `rsi_reversion` | -17.4766 | -90.7171% | 90.7171% | 4440 | `{"overbought": 75.0, "oversold": 22.5, "period": 5}` |
| 49 | `r1_c24` | `rsi_reversion` | -18.9136 | -92.1190% | 92.1190% | 5056 | `{"overbought": 70.0, "oversold": 25.0, "period": 5}` |
| 50 | `r1_c45` | `price_moving_average` | -22.9889 | -95.0740% | 95.0740% | 3297 | `{"entry_threshold": 0.0005, "period": 5}` |

## Round 2

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
| 11 | `r2_c45` | `multi_timeframe_ma_spread` | 0.9786 | 11.3486% | 31.5609% | 120 | `{"primary_ma_period": 18, "reference_ma_period": 55, "spread_threshold_bps": 40.0}` |
| 12 | `r2_c41` | `multi_timeframe_ma_spread` | 0.8509 | 8.9752% | 29.1177% | 173 | `{"primary_ma_period": 20, "reference_ma_period": 28, "spread_threshold_bps": 0.0}` |
| 13 | `r2_c06` | `multi_timeframe_ma_spread` | 0.7852 | 7.7602% | 34.9988% | 105 | `{"primary_ma_period": 23, "reference_ma_period": 55, "spread_threshold_bps": 20.0}` |
| 14 | `r2_c07` | `donchian_breakout` | 0.6163 | 4.5663% | 33.6929% | 375 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 15 | `r2_c23` | `multi_timeframe_ma_spread` | 0.4409 | 1.8392% | 36.6590% | 82 | `{"primary_ma_period": 24, "reference_ma_period": 62, "spread_threshold_bps": 35.0}` |
| 16 | `r2_c25` | `multi_timeframe_ma_spread` | 0.3827 | 0.6452% | 36.3537% | 111 | `{"primary_ma_period": 26, "reference_ma_period": 50, "spread_threshold_bps": 40.0}` |
| 17 | `r2_c08` | `donchian_breakout` | 0.2041 | -3.0750% | 33.7503% | 443 | `{"breakout_buffer_bps": 10.0, "lookback_window": 65}` |
| 18 | `r2_c26` | `multi_timeframe_ma_spread` | -0.1101 | -7.3927% | 33.6684% | 133 | `{"primary_ma_period": 18, "reference_ma_period": 50, "spread_threshold_bps": 25.0}` |
| 19 | `r2_c09` | `donchian_breakout` | -0.3962 | -13.2208% | 46.1740% | 479 | `{"breakout_buffer_bps": 10.0, "lookback_window": 55}` |
| 20 | `r2_c48` | `donchian_breakout` | -0.4242 | -13.6964% | 43.0734% | 525 | `{"breakout_buffer_bps": 5.0, "lookback_window": 67}` |
| 21 | `r2_c10` | `donchian_breakout` | -0.6086 | -16.5576% | 41.9903% | 629 | `{"breakout_buffer_bps": 0.0, "lookback_window": 65}` |
| 22 | `r2_c24` | `multi_timeframe_ma_spread` | -0.7278 | -16.5018% | 36.3893% | 120 | `{"primary_ma_period": 26, "reference_ma_period": 45, "spread_threshold_bps": 5.0}` |
| 23 | `r2_c46` | `multi_timeframe_ma_spread` | -0.9892 | -20.1446% | 38.2746% | 151 | `{"primary_ma_period": 22, "reference_ma_period": 45, "spread_threshold_bps": 15.0}` |
| 24 | `r2_c44` | `multi_timeframe_ma_spread` | -1.0442 | -20.9784% | 38.2910% | 140 | `{"primary_ma_period": 22, "reference_ma_period": 45, "spread_threshold_bps": 20.0}` |
| 25 | `r2_c43` | `multi_timeframe_ma_spread` | -1.1725 | -22.7381% | 44.9568% | 133 | `{"primary_ma_period": 24, "reference_ma_period": 42, "spread_threshold_bps": 30.0}` |
| 26 | `r2_c28` | `donchian_breakout` | -1.1947 | -25.0930% | 50.8468% | 586 | `{"breakout_buffer_bps": 5.0, "lookback_window": 55}` |
| 27 | `r2_c30` | `donchian_breakout` | -1.4372 | -28.4226% | 47.3924% | 618 | `{"breakout_buffer_bps": 0.0, "lookback_window": 67}` |
| 28 | `r2_c49` | `donchian_breakout` | -1.4774 | -28.9092% | 47.9229% | 684 | `{"breakout_buffer_bps": 0.0, "lookback_window": 57}` |
| 29 | `r2_c31` | `moving_average_cross` | -1.8899 | -22.2967% | 32.8337% | 704 | `{"entry_threshold": 0.002, "fast_window": 24, "slow_window": 80}` |
| 30 | `r2_c35` | `moving_average_cross` | -1.9565 | -22.9607% | 33.8956% | 765 | `{"entry_threshold": 0.0015, "fast_window": 20, "slow_window": 85}` |
| 31 | `r2_c47` | `donchian_breakout` | -2.2007 | -37.7179% | 56.9246% | 658 | `{"breakout_buffer_bps": 5.0, "lookback_window": 47}` |
| 32 | `r2_c50` | `donchian_breakout` | -2.3173 | -39.1172% | 54.7351% | 714 | `{"breakout_buffer_bps": 0.0, "lookback_window": 55}` |
| 33 | `r2_c33` | `moving_average_cross` | -2.3416 | -26.3858% | 34.7008% | 786 | `{"entry_threshold": 0.0015, "fast_window": 17, "slow_window": 85}` |
| 34 | `r2_c11` | `moving_average_cross` | -2.4233 | -27.3835% | 37.6770% | 955 | `{"entry_threshold": 0.001, "fast_window": 21, "slow_window": 75}` |
| 35 | `r2_c12` | `moving_average_cross` | -2.4455 | -27.2045% | 36.1604% | 661 | `{"entry_threshold": 0.002, "fast_window": 22, "slow_window": 95}` |
| 36 | `r2_c32` | `moving_average_cross` | -2.9630 | -31.0205% | 37.9656% | 548 | `{"entry_threshold": 0.003, "fast_window": 24, "slow_window": 110}` |
| 37 | `r2_c13` | `moving_average_cross` | -3.4977 | -36.0372% | 41.7864% | 931 | `{"entry_threshold": 0.001, "fast_window": 20, "slow_window": 80}` |
| 38 | `r2_c14` | `rsi_reversion` | -3.9315 | -41.5088% | 43.3641% | 833 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 39 | `r2_c40` | `rsi_reversion` | -4.1579 | -49.0106% | 51.5055% | 1406 | `{"overbought": 75.0, "oversold": 30.0, "period": 13}` |
| 40 | `r2_c15` | `moving_average_cross` | -4.8634 | -45.4964% | 50.6981% | 1196 | `{"entry_threshold": 0.0005, "fast_window": 19, "slow_window": 70}` |
| 41 | `r2_c36` | `rsi_reversion` | -5.0622 | -48.8823% | 49.9801% | 657 | `{"overbought": 70.0, "oversold": 25.0, "period": 18}` |
| 42 | `r2_c16` | `rsi_reversion` | -5.2353 | -54.2027% | 54.7710% | 1541 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
| 43 | `r2_c17` | `price_moving_average` | -5.4435 | -52.1673% | 54.6769% | 893 | `{"entry_threshold": 0.0015, "period": 9}` |
| 44 | `r2_c18` | `moving_average_cross` | -5.6714 | -50.3728% | 53.3706% | 1537 | `{"entry_threshold": 0.001, "fast_window": 8, "slow_window": 55}` |
| 45 | `r2_c19` | `rsi_reversion` | -5.6870 | -59.0846% | 60.5257% | 1733 | `{"overbought": 70.0, "oversold": 35.0, "period": 15}` |
| 46 | `r2_c34` | `rsi_reversion` | -5.8117 | -55.9609% | 56.5672% | 1627 | `{"overbought": 67.5, "oversold": 30.0, "period": 14}` |
| 47 | `r2_c20` | `rsi_reversion` | -5.8204 | -59.0218% | 60.1991% | 1576 | `{"overbought": 70.0, "oversold": 32.5, "period": 15}` |
| 48 | `r2_c37` | `price_moving_average` | -6.2625 | -57.1641% | 58.6819% | 826 | `{"entry_threshold": 0.0015, "period": 10}` |
| 49 | `r2_c38` | `moving_average_cross` | -6.3985 | -55.3288% | 56.6414% | 1942 | `{"entry_threshold": 0.001, "fast_window": 5, "slow_window": 45}` |
| 50 | `r2_c39` | `rsi_reversion` | -6.5113 | -58.0869% | 58.9191% | 1726 | `{"overbought": 65.0, "oversold": 30.0, "period": 14}` |

## Round 3

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r3_c01` | `donchian_breakout` | 2.4810 | 47.0799% | 19.8418% | 249 | `{"breakout_buffer_bps": 30.0, "lookback_window": 45}` |
| 2 | `r3_c48` | `multi_timeframe_ma_spread` | 1.9415 | 31.2099% | 19.6807% | 158 | `{"primary_ma_period": 17, "reference_ma_period": 33, "spread_threshold_bps": 40.0}` |
| 3 | `r3_c46` | `donchian_breakout` | 1.8603 | 31.2977% | 22.8144% | 116 | `{"breakout_buffer_bps": 50.0, "lookback_window": 55}` |
| 4 | `r3_c02` | `donchian_breakout` | 1.7122 | 27.8784% | 25.5803% | 245 | `{"breakout_buffer_bps": 25.0, "lookback_window": 67}` |
| 5 | `r3_c03` | `donchian_breakout` | 1.7107 | 27.7557% | 22.8144% | 112 | `{"breakout_buffer_bps": 50.0, "lookback_window": 60}` |
| 6 | `r3_c04` | `multi_timeframe_ma_spread` | 1.5975 | 23.6517% | 26.4034% | 155 | `{"primary_ma_period": 15, "reference_ma_period": 30, "spread_threshold_bps": 0.0}` |
| 7 | `r3_c05` | `donchian_breakout` | 1.5752 | 24.6892% | 26.0907% | 211 | `{"breakout_buffer_bps": 30.0, "lookback_window": 67}` |
| 8 | `r3_c06` | `donchian_breakout` | 1.4897 | 22.7266% | 23.0396% | 216 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 9 | `r3_c30` | `multi_timeframe_ma_spread` | 1.3149 | 17.1948% | 37.4512% | 90 | `{"primary_ma_period": 18, "reference_ma_period": 70, "spread_threshold_bps": 30.0}` |
| 10 | `r3_c21` | `donchian_breakout` | 1.2657 | 17.7536% | 25.0339% | 229 | `{"breakout_buffer_bps": 35.0, "lookback_window": 35}` |
| 11 | `r3_c07` | `multi_timeframe_ma_spread` | 1.1800 | 15.2005% | 31.7224% | 125 | `{"primary_ma_period": 19, "reference_ma_period": 52, "spread_threshold_bps": 40.0}` |
| 12 | `r3_c08` | `multi_timeframe_ma_spread` | 1.0852 | 13.3582% | 26.9683% | 169 | `{"primary_ma_period": 14, "reference_ma_period": 35, "spread_threshold_bps": 20.0}` |
| 13 | `r3_c09` | `multi_timeframe_ma_spread` | 1.0277 | 12.2308% | 32.7884% | 93 | `{"primary_ma_period": 25, "reference_ma_period": 55, "spread_threshold_bps": 10.0}` |
| 14 | `r3_c10` | `multi_timeframe_ma_spread` | 1.0252 | 12.2052% | 35.2912% | 104 | `{"primary_ma_period": 21, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 15 | `r3_c29` | `multi_timeframe_ma_spread` | 0.9259 | 10.1343% | 32.7695% | 83 | `{"primary_ma_period": 22, "reference_ma_period": 57, "spread_threshold_bps": 0.0}` |
| 16 | `r3_c22` | `donchian_breakout` | 0.8328 | 8.8060% | 23.7467% | 133 | `{"breakout_buffer_bps": 45.0, "lookback_window": 62}` |
| 17 | `r3_c50` | `multi_timeframe_ma_spread` | 0.7602 | 7.3029% | 36.3070% | 97 | `{"primary_ma_period": 26, "reference_ma_period": 58, "spread_threshold_bps": 60.0}` |
| 18 | `r3_c47` | `multi_timeframe_ma_spread` | 0.6973 | 6.1696% | 34.9968% | 121 | `{"primary_ma_period": 22, "reference_ma_period": 50, "spread_threshold_bps": 45.0}` |
| 19 | `r3_c26` | `donchian_breakout` | 0.6877 | 5.9571% | 24.3092% | 191 | `{"breakout_buffer_bps": 35.0, "lookback_window": 55}` |
| 20 | `r3_c44` | `multi_timeframe_ma_spread` | 0.5456 | 3.4047% | 28.0678% | 251 | `{"primary_ma_period": 14, "reference_ma_period": 20, "spread_threshold_bps": 20.0}` |
| 21 | `r3_c42` | `donchian_breakout` | 0.5118 | 2.5879% | 34.2099% | 317 | `{"breakout_buffer_bps": 20.0, "lookback_window": 57}` |
| 22 | `r3_c43` | `donchian_breakout` | 0.2199 | -2.6265% | 27.1456% | 80 | `{"breakout_buffer_bps": 60.0, "lookback_window": 58}` |
| 23 | `r3_c25` | `donchian_breakout` | 0.2070 | -2.9958% | 36.5524% | 308 | `{"breakout_buffer_bps": 20.0, "lookback_window": 62}` |
| 24 | `r3_c27` | `multi_timeframe_ma_spread` | 0.1547 | -3.1683% | 36.3015% | 125 | `{"primary_ma_period": 16, "reference_ma_period": 50, "spread_threshold_bps": 60.0}` |
| 25 | `r3_c23` | `donchian_breakout` | 0.0141 | -6.3101% | 29.3545% | 94 | `{"breakout_buffer_bps": 55.0, "lookback_window": 58}` |
| 26 | `r3_c41` | `donchian_breakout` | -0.2454 | -10.6558% | 28.0573% | 166 | `{"breakout_buffer_bps": 40.0, "lookback_window": 55}` |
| 27 | `r3_c28` | `multi_timeframe_ma_spread` | -0.3136 | -10.5474% | 33.9179% | 142 | `{"primary_ma_period": 17, "reference_ma_period": 40, "spread_threshold_bps": 25.0}` |
| 28 | `r3_c45` | `donchian_breakout` | -0.3368 | -12.1745% | 31.5986% | 150 | `{"breakout_buffer_bps": 40.0, "lookback_window": 69}` |
| 29 | `r3_c49` | `multi_timeframe_ma_spread` | -0.9455 | -19.5548% | 37.7332% | 117 | `{"primary_ma_period": 30, "reference_ma_period": 45, "spread_threshold_bps": 10.0}` |
| 30 | `r3_c24` | `multi_timeframe_ma_spread` | -1.7258 | -29.9910% | 46.7880% | 228 | `{"primary_ma_period": 20, "reference_ma_period": 20, "spread_threshold_bps": 0.0}` |
| 31 | `r3_c11` | `moving_average_cross` | -1.8899 | -22.2967% | 32.8337% | 704 | `{"entry_threshold": 0.002, "fast_window": 24, "slow_window": 80}` |
| 32 | `r3_c31` | `moving_average_cross` | -1.9321 | -22.5527% | 32.0541% | 594 | `{"entry_threshold": 0.0025, "fast_window": 26, "slow_window": 90}` |
| 33 | `r3_c12` | `moving_average_cross` | -1.9565 | -22.9607% | 33.8956% | 765 | `{"entry_threshold": 0.0015, "fast_window": 20, "slow_window": 85}` |
| 34 | `r3_c13` | `moving_average_cross` | -2.3416 | -26.3858% | 34.7008% | 786 | `{"entry_threshold": 0.0015, "fast_window": 17, "slow_window": 85}` |
| 35 | `r3_c35` | `moving_average_cross` | -2.3421 | -26.0986% | 35.5497% | 650 | `{"entry_threshold": 0.0015, "fast_window": 25, "slow_window": 105}` |
| 36 | `r3_c32` | `moving_average_cross` | -2.3468 | -26.7839% | 36.4353% | 801 | `{"entry_threshold": 0.0015, "fast_window": 22, "slow_window": 80}` |
| 37 | `r3_c14` | `moving_average_cross` | -2.4233 | -27.3835% | 37.6770% | 955 | `{"entry_threshold": 0.001, "fast_window": 21, "slow_window": 75}` |
| 38 | `r3_c15` | `moving_average_cross` | -2.4455 | -27.2045% | 36.1604% | 661 | `{"entry_threshold": 0.002, "fast_window": 22, "slow_window": 95}` |
| 39 | `r3_c34` | `moving_average_cross` | -2.6940 | -29.5225% | 37.0508% | 950 | `{"entry_threshold": 0.0005, "fast_window": 24, "slow_window": 85}` |
| 40 | `r3_c37` | `rsi_reversion` | -2.7910 | -40.7317% | 46.8168% | 806 | `{"overbought": 80.0, "oversold": 35.0, "period": 15}` |
| 41 | `r3_c33` | `moving_average_cross` | -2.7922 | -30.0261% | 38.8525% | 655 | `{"entry_threshold": 0.002, "fast_window": 20, "slow_window": 100}` |
| 42 | `r3_c38` | `rsi_reversion` | -3.7494 | -40.1377% | 43.2315% | 367 | `{"overbought": 75.0, "oversold": 20.0, "period": 17}` |
| 43 | `r3_c16` | `rsi_reversion` | -3.9315 | -41.5088% | 43.3641% | 833 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 44 | `r3_c17` | `rsi_reversion` | -4.1579 | -49.0106% | 51.5055% | 1406 | `{"overbought": 75.0, "oversold": 30.0, "period": 13}` |
| 45 | `r3_c40` | `price_moving_average` | -4.6190 | -46.9388% | 51.1160% | 442 | `{"entry_threshold": 0.0025, "period": 8}` |
| 46 | `r3_c36` | `rsi_reversion` | -4.6255 | -46.9409% | 49.1464% | 1183 | `{"overbought": 72.5, "oversold": 22.5, "period": 12}` |
| 47 | `r3_c18` | `rsi_reversion` | -5.0622 | -48.8823% | 49.9801% | 657 | `{"overbought": 70.0, "oversold": 25.0, "period": 18}` |
| 48 | `r3_c19` | `rsi_reversion` | -5.2353 | -54.2027% | 54.7710% | 1541 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
| 49 | `r3_c20` | `price_moving_average` | -5.4435 | -52.1673% | 54.6769% | 893 | `{"entry_threshold": 0.0015, "period": 9}` |
| 50 | `r3_c39` | `rsi_reversion` | -9.0395 | -71.2580% | 71.6974% | 2518 | `{"overbought": 65.0, "oversold": 32.5, "period": 12}` |

## Round 4

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
| 11 | `r4_c42` | `multi_timeframe_ma_spread` | 1.5935 | 23.7291% | 24.9165% | 155 | `{"primary_ma_period": 20, "reference_ma_period": 28, "spread_threshold_bps": 40.0}` |
| 12 | `r4_c07` | `donchian_breakout` | 1.5752 | 24.6892% | 26.0907% | 211 | `{"breakout_buffer_bps": 30.0, "lookback_window": 67}` |
| 13 | `r4_c25` | `donchian_breakout` | 1.4568 | 21.9570% | 26.2780% | 110 | `{"breakout_buffer_bps": 50.0, "lookback_window": 65}` |
| 14 | `r4_c41` | `donchian_breakout` | 1.3883 | 20.4265% | 24.7116% | 123 | `{"breakout_buffer_bps": 50.0, "lookback_window": 50}` |
| 15 | `r4_c48` | `multi_timeframe_ma_spread` | 1.3355 | 18.2250% | 32.1281% | 93 | `{"primary_ma_period": 17, "reference_ma_period": 60, "spread_threshold_bps": 25.0}` |
| 16 | `r4_c08` | `multi_timeframe_ma_spread` | 1.3149 | 17.1948% | 37.4512% | 90 | `{"primary_ma_period": 18, "reference_ma_period": 70, "spread_threshold_bps": 30.0}` |
| 17 | `r4_c46` | `multi_timeframe_ma_spread` | 1.3132 | 17.8792% | 28.1906% | 181 | `{"primary_ma_period": 16, "reference_ma_period": 28, "spread_threshold_bps": 10.0}` |
| 18 | `r4_c24` | `donchian_breakout` | 1.1807 | 15.9854% | 30.8506% | 205 | `{"breakout_buffer_bps": 30.0, "lookback_window": 72}` |
| 19 | `r4_c09` | `multi_timeframe_ma_spread` | 1.1800 | 15.2005% | 31.7224% | 125 | `{"primary_ma_period": 19, "reference_ma_period": 52, "spread_threshold_bps": 40.0}` |
| 20 | `r4_c10` | `multi_timeframe_ma_spread` | 1.0852 | 13.3582% | 26.9683% | 169 | `{"primary_ma_period": 14, "reference_ma_period": 35, "spread_threshold_bps": 20.0}` |
| 21 | `r4_c44` | `donchian_breakout` | 1.0842 | 13.9461% | 36.1890% | 168 | `{"breakout_buffer_bps": 35.0, "lookback_window": 77}` |
| 22 | `r4_c28` | `multi_timeframe_ma_spread` | 0.7145 | 6.4398% | 41.4284% | 94 | `{"primary_ma_period": 17, "reference_ma_period": 68, "spread_threshold_bps": 40.0}` |
| 23 | `r4_c23` | `donchian_breakout` | 0.1557 | -3.7612% | 34.6333% | 55 | `{"breakout_buffer_bps": 70.0, "lookback_window": 57}` |
| 24 | `r4_c43` | `donchian_breakout` | 0.0220 | -6.2162% | 28.5265% | 90 | `{"breakout_buffer_bps": 55.0, "lookback_window": 65}` |
| 25 | `r4_c45` | `donchian_breakout` | -0.1831 | -9.6000% | 35.1543% | 100 | `{"breakout_buffer_bps": 55.0, "lookback_window": 50}` |
| 26 | `r4_c21` | `donchian_breakout` | -0.1973 | -9.8546% | 26.0551% | 175 | `{"breakout_buffer_bps": 40.0, "lookback_window": 50}` |
| 27 | `r4_c29` | `multi_timeframe_ma_spread` | -0.2575 | -9.7118% | 34.5930% | 135 | `{"primary_ma_period": 18, "reference_ma_period": 50, "spread_threshold_bps": 30.0}` |
| 28 | `r4_c47` | `donchian_breakout` | -0.2755 | -11.2545% | 45.5584% | 287 | `{"breakout_buffer_bps": 20.0, "lookback_window": 72}` |
| 29 | `r4_c49` | `multi_timeframe_ma_spread` | -1.2399 | -23.6830% | 42.3470% | 127 | `{"primary_ma_period": 24, "reference_ma_period": 42, "spread_threshold_bps": 50.0}` |
| 30 | `r4_c32` | `moving_average_cross` | -1.5706 | -19.2559% | 31.8363% | 506 | `{"entry_threshold": 0.003, "fast_window": 29, "slow_window": 95}` |
| 31 | `r4_c31` | `moving_average_cross` | -1.6803 | -20.3267% | 31.6501% | 544 | `{"entry_threshold": 0.003, "fast_window": 27, "slow_window": 75}` |
| 32 | `r4_c26` | `multi_timeframe_ma_spread` | -1.7258 | -29.9910% | 46.7880% | 228 | `{"primary_ma_period": 20, "reference_ma_period": 20, "spread_threshold_bps": 0.0}` |
| 33 | `r4_c11` | `moving_average_cross` | -1.8899 | -22.2967% | 32.8337% | 704 | `{"entry_threshold": 0.002, "fast_window": 24, "slow_window": 80}` |
| 34 | `r4_c12` | `moving_average_cross` | -1.9321 | -22.5527% | 32.0541% | 594 | `{"entry_threshold": 0.0025, "fast_window": 26, "slow_window": 90}` |
| 35 | `r4_c13` | `moving_average_cross` | -1.9565 | -22.9607% | 33.8956% | 765 | `{"entry_threshold": 0.0015, "fast_window": 20, "slow_window": 85}` |
| 36 | `r4_c14` | `moving_average_cross` | -2.3416 | -26.3858% | 34.7008% | 786 | `{"entry_threshold": 0.0015, "fast_window": 17, "slow_window": 85}` |
| 37 | `r4_c15` | `moving_average_cross` | -2.3421 | -26.0986% | 35.5497% | 650 | `{"entry_threshold": 0.0015, "fast_window": 25, "slow_window": 105}` |
| 38 | `r4_c40` | `price_moving_average` | -2.5636 | -31.7634% | 46.3695% | 340 | `{"entry_threshold": 0.003, "period": 7}` |
| 39 | `r4_c33` | `moving_average_cross` | -2.6280 | -28.7379% | 37.2258% | 694 | `{"entry_threshold": 0.0025, "fast_window": 18, "slow_window": 80}` |
| 40 | `r4_c35` | `moving_average_cross` | -2.6433 | -28.6681% | 36.1369% | 611 | `{"entry_threshold": 0.0025, "fast_window": 23, "slow_window": 100}` |
| 41 | `r4_c37` | `rsi_reversion` | -2.7495 | -35.4907% | 47.3384% | 132 | `{"overbought": 80.0, "oversold": 20.0, "period": 21}` |
| 42 | `r4_c16` | `rsi_reversion` | -2.7910 | -40.7317% | 46.8168% | 806 | `{"overbought": 80.0, "oversold": 35.0, "period": 15}` |
| 43 | `r4_c34` | `moving_average_cross` | -2.8256 | -30.3346% | 39.6026% | 731 | `{"entry_threshold": 0.0015, "fast_window": 18, "slow_window": 100}` |
| 44 | `r4_c17` | `rsi_reversion` | -3.7494 | -40.1377% | 43.2315% | 367 | `{"overbought": 75.0, "oversold": 20.0, "period": 17}` |
| 45 | `r4_c18` | `rsi_reversion` | -3.9315 | -41.5088% | 43.3641% | 833 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
| 46 | `r4_c19` | `rsi_reversion` | -4.1579 | -49.0106% | 51.5055% | 1406 | `{"overbought": 75.0, "oversold": 30.0, "period": 13}` |
| 47 | `r4_c36` | `rsi_reversion` | -4.4540 | -53.8283% | 54.9590% | 1489 | `{"overbought": 77.5, "oversold": 37.5, "period": 13}` |
| 48 | `r4_c39` | `rsi_reversion` | -4.5225 | -47.4273% | 48.6943% | 678 | `{"overbought": 72.5, "oversold": 25.0, "period": 17}` |
| 49 | `r4_c20` | `price_moving_average` | -4.6190 | -46.9388% | 51.1160% | 442 | `{"entry_threshold": 0.0025, "period": 8}` |
| 50 | `r4_c38` | `rsi_reversion` | -4.9992 | -54.4179% | 56.3804% | 1692 | `{"overbought": 75.0, "oversold": 30.0, "period": 12}` |

## Round 5

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r5_c01` | `donchian_breakout` | 2.4810 | 47.0799% | 19.8418% | 249 | `{"breakout_buffer_bps": 30.0, "lookback_window": 45}` |
| 2 | `r5_c02` | `multi_timeframe_ma_spread` | 2.0994 | 34.9010% | 23.8483% | 149 | `{"primary_ma_period": 20, "reference_ma_period": 28, "spread_threshold_bps": 45.0}` |
| 3 | `r5_c27` | `donchian_breakout` | 1.9657 | 33.9173% | 20.6736% | 256 | `{"breakout_buffer_bps": 25.0, "lookback_window": 60}` |
| 4 | `r5_c03` | `multi_timeframe_ma_spread` | 1.9415 | 31.2099% | 19.6807% | 158 | `{"primary_ma_period": 17, "reference_ma_period": 33, "spread_threshold_bps": 40.0}` |
| 5 | `r5_c22` | `multi_timeframe_ma_spread` | 1.8844 | 29.9402% | 24.1515% | 146 | `{"primary_ma_period": 21, "reference_ma_period": 30, "spread_threshold_bps": 35.0}` |
| 6 | `r5_c04` | `multi_timeframe_ma_spread` | 1.8747 | 29.5981% | 21.4764% | 164 | `{"primary_ma_period": 15, "reference_ma_period": 30, "spread_threshold_bps": 15.0}` |
| 7 | `r5_c05` | `donchian_breakout` | 1.8603 | 31.2977% | 22.8144% | 116 | `{"breakout_buffer_bps": 50.0, "lookback_window": 55}` |
| 8 | `r5_c06` | `multi_timeframe_ma_spread` | 1.8145 | 28.3754% | 19.8207% | 143 | `{"primary_ma_period": 19, "reference_ma_period": 33, "spread_threshold_bps": 40.0}` |
| 9 | `r5_c07` | `donchian_breakout` | 1.8005 | 29.9220% | 20.6736% | 254 | `{"breakout_buffer_bps": 25.0, "lookback_window": 62}` |
| 10 | `r5_c25` | `donchian_breakout` | 1.7752 | 29.0457% | 20.3496% | 54 | `{"breakout_buffer_bps": 70.0, "lookback_window": 60}` |
| 11 | `r5_c08` | `donchian_breakout` | 1.7122 | 27.8784% | 25.5803% | 245 | `{"breakout_buffer_bps": 25.0, "lookback_window": 67}` |
| 12 | `r5_c09` | `donchian_breakout` | 1.7107 | 27.7557% | 22.8144% | 112 | `{"breakout_buffer_bps": 50.0, "lookback_window": 60}` |
| 13 | `r5_c30` | `multi_timeframe_ma_spread` | 1.6592 | 25.0835% | 25.1523% | 198 | `{"primary_ma_period": 14, "reference_ma_period": 25, "spread_threshold_bps": 20.0}` |
| 14 | `r5_c46` | `multi_timeframe_ma_spread` | 1.6543 | 24.9945% | 20.6543% | 135 | `{"primary_ma_period": 24, "reference_ma_period": 31, "spread_threshold_bps": 50.0}` |
| 15 | `r5_c10` | `multi_timeframe_ma_spread` | 1.5975 | 23.6517% | 26.4034% | 155 | `{"primary_ma_period": 15, "reference_ma_period": 30, "spread_threshold_bps": 0.0}` |
| 16 | `r5_c43` | `multi_timeframe_ma_spread` | 1.5463 | 22.7016% | 23.3276% | 161 | `{"primary_ma_period": 16, "reference_ma_period": 28, "spread_threshold_bps": 35.0}` |
| 17 | `r5_c23` | `multi_timeframe_ma_spread` | 1.4478 | 20.7212% | 25.9675% | 165 | `{"primary_ma_period": 18, "reference_ma_period": 28, "spread_threshold_bps": 60.0}` |
| 18 | `r5_c44` | `multi_timeframe_ma_spread` | 1.3132 | 17.8792% | 28.1906% | 181 | `{"primary_ma_period": 16, "reference_ma_period": 28, "spread_threshold_bps": 10.0}` |
| 19 | `r5_c47` | `donchian_breakout` | 0.5118 | 2.5879% | 34.2099% | 317 | `{"breakout_buffer_bps": 20.0, "lookback_window": 57}` |
| 20 | `r5_c28` | `donchian_breakout` | 0.4667 | 1.7474% | 33.1044% | 174 | `{"breakout_buffer_bps": 35.0, "lookback_window": 72}` |
| 21 | `r5_c45` | `donchian_breakout` | 0.2643 | -1.8844% | 38.5870% | 93 | `{"breakout_buffer_bps": 60.0, "lookback_window": 45}` |
| 22 | `r5_c48` | `donchian_breakout` | 0.2070 | -2.9958% | 36.5524% | 308 | `{"breakout_buffer_bps": 20.0, "lookback_window": 62}` |
| 23 | `r5_c26` | `multi_timeframe_ma_spread` | 0.1101 | -3.8950% | 30.4169% | 155 | `{"primary_ma_period": 16, "reference_ma_period": 38, "spread_threshold_bps": 35.0}` |
| 24 | `r5_c41` | `donchian_breakout` | 0.0715 | -5.3054% | 29.8245% | 186 | `{"breakout_buffer_bps": 40.0, "lookback_window": 43}` |
| 25 | `r5_c49` | `donchian_breakout` | -0.1524 | -9.1029% | 29.3026% | 71 | `{"breakout_buffer_bps": 60.0, "lookback_window": 70}` |
| 26 | `r5_c32` | `moving_average_cross` | -0.2003 | -5.0280% | 22.1828% | 400 | `{"entry_threshold": 0.004, "fast_window": 28, "slow_window": 70}` |
| 27 | `r5_c50` | `multi_timeframe_ma_spread` | -0.2130 | -8.9872% | 35.8151% | 172 | `{"primary_ma_period": 12, "reference_ma_period": 40, "spread_threshold_bps": 20.0}` |
| 28 | `r5_c21` | `donchian_breakout` | -0.2454 | -10.6558% | 28.0573% | 166 | `{"breakout_buffer_bps": 40.0, "lookback_window": 55}` |
| 29 | `r5_c29` | `donchian_breakout` | -0.3032 | -11.6024% | 31.2959% | 157 | `{"breakout_buffer_bps": 40.0, "lookback_window": 65}` |
| 30 | `r5_c42` | `multi_timeframe_ma_spread` | -0.3359 | -10.9034% | 36.2169% | 150 | `{"primary_ma_period": 15, "reference_ma_period": 38, "spread_threshold_bps": 45.0}` |
| 31 | `r5_c24` | `multi_timeframe_ma_spread` | -0.4712 | -12.8762% | 38.5868% | 160 | `{"primary_ma_period": 14, "reference_ma_period": 40, "spread_threshold_bps": 10.0}` |
| 32 | `r5_c31` | `moving_average_cross` | -0.5744 | -9.1053% | 25.3953% | 430 | `{"entry_threshold": 0.0035, "fast_window": 31, "slow_window": 90}` |
| 33 | `r5_c11` | `moving_average_cross` | -1.5706 | -19.2559% | 31.8363% | 506 | `{"entry_threshold": 0.003, "fast_window": 29, "slow_window": 95}` |
| 34 | `r5_c12` | `moving_average_cross` | -1.6803 | -20.3267% | 31.6501% | 544 | `{"entry_threshold": 0.003, "fast_window": 27, "slow_window": 75}` |
| 35 | `r5_c39` | `rsi_reversion` | -1.7415 | -19.4986% | 25.0383% | 424 | `{"overbought": 70.0, "oversold": 22.5, "period": 19}` |
| 36 | `r5_c13` | `moving_average_cross` | -1.8899 | -22.2967% | 32.8337% | 704 | `{"entry_threshold": 0.002, "fast_window": 24, "slow_window": 80}` |
| 37 | `r5_c14` | `moving_average_cross` | -1.9321 | -22.5527% | 32.0541% | 594 | `{"entry_threshold": 0.0025, "fast_window": 26, "slow_window": 90}` |
| 38 | `r5_c15` | `moving_average_cross` | -1.9565 | -22.9607% | 33.8956% | 765 | `{"entry_threshold": 0.0015, "fast_window": 20, "slow_window": 85}` |
| 39 | `r5_c33` | `moving_average_cross` | -2.2492 | -25.5775% | 35.2069% | 662 | `{"entry_threshold": 0.002, "fast_window": 21, "slow_window": 95}` |
| 40 | `r5_c34` | `moving_average_cross` | -2.3697 | -26.0548% | 34.5885% | 489 | `{"entry_threshold": 0.003, "fast_window": 29, "slow_window": 105}` |
| 41 | `r5_c36` | `price_moving_average` | -2.3898 | -30.9812% | 45.1352% | 159 | `{"entry_threshold": 0.004, "period": 10}` |
| 42 | `r5_c16` | `price_moving_average` | -2.5636 | -31.7634% | 46.3695% | 340 | `{"entry_threshold": 0.003, "period": 7}` |
| 43 | `r5_c17` | `rsi_reversion` | -2.7495 | -35.4907% | 47.3384% | 132 | `{"overbought": 80.0, "oversold": 20.0, "period": 21}` |
| 44 | `r5_c18` | `rsi_reversion` | -2.7910 | -40.7317% | 46.8168% | 806 | `{"overbought": 80.0, "oversold": 35.0, "period": 15}` |
| 45 | `r5_c38` | `rsi_reversion` | -2.8780 | -42.0527% | 52.5875% | 948 | `{"overbought": 82.5, "oversold": 37.5, "period": 13}` |
| 46 | `r5_c40` | `rsi_reversion` | -2.9439 | -33.5341% | 38.0814% | 527 | `{"overbought": 70.0, "oversold": 25.0, "period": 20}` |
| 47 | `r5_c35` | `moving_average_cross` | -2.9908 | -32.0748% | 39.0469% | 830 | `{"entry_threshold": 0.0015, "fast_window": 18, "slow_window": 80}` |
| 48 | `r5_c37` | `rsi_reversion` | -3.0392 | -38.8652% | 43.9427% | 542 | `{"overbought": 77.5, "oversold": 25.0, "period": 17}` |
| 49 | `r5_c19` | `rsi_reversion` | -3.7494 | -40.1377% | 43.2315% | 367 | `{"overbought": 75.0, "oversold": 20.0, "period": 17}` |
| 50 | `r5_c20` | `rsi_reversion` | -3.9315 | -41.5088% | 43.3641% | 833 | `{"overbought": 70.0, "oversold": 25.0, "period": 16}` |
