# LLM Strategy Evolution

- Symbol: `MNQ`
- Primary timeframe: `5m`
- Secondary timeframe: `15m`
- Rounds: `5`
- Best strategy: `price_moving_average`
- Best Sharpe: `6.1799`
- Best total return: `13.3346%`
- Best max drawdown: `3.3198%`
- Best trade count: `58`

## Round 1

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r1_c13` | `price_moving_average` | 6.1799 | 13.3346% | 3.3198% | 58 | `{"entry_threshold": 0.001, "period": 55}` |
| 2 | `r1_c07` | `moving_average_cross` | 4.5838 | 9.2014% | 4.7197% | 124 | `{"entry_threshold": 0.0005, "fast_window": 34, "slow_window": 89}` |
| 3 | `r1_c06` | `moving_average_cross` | 4.3748 | 10.8043% | 3.1442% | 198 | `{"entry_threshold": 0.0005, "fast_window": 20, "slow_window": 50}` |
| 4 | `r1_c10` | `price_moving_average` | 2.9486 | 5.3178% | 5.8540% | 609 | `{"entry_threshold": 0.0003, "period": 13}` |
| 5 | `r1_c12` | `price_moving_average` | 2.8010 | 6.8544% | 4.6911% | 217 | `{"entry_threshold": 0.0005, "period": 34}` |
| 6 | `r1_c43` | `atr_breakout` | 2.6213 | 7.5867% | 6.9631% | 110 | `{"atr_multiplier": 3.0, "atr_period": 21, "ma_period": 80}` |
| 7 | `r1_c16` | `rsi_reversion` | 2.4999 | 6.1767% | 4.9242% | 600 | `{"overbought": 70.0, "oversold": 30.0, "period": 9}` |
| 8 | `r1_c15` | `rsi_reversion` | 2.2004 | 5.2302% | 4.4997% | 683 | `{"overbought": 75.0, "oversold": 25.0, "period": 7}` |
| 9 | `r1_c11` | `price_moving_average` | 1.9690 | 4.6370% | 5.3515% | 294 | `{"entry_threshold": 0.0005, "period": 21}` |
| 10 | `r1_c03` | `moving_average_cross` | 1.8919 | 3.2787% | 5.7756% | 725 | `{"entry_threshold": 0.0, "fast_window": 8, "slow_window": 21}` |
| 11 | `r1_c42` | `atr_breakout` | 1.6766 | 4.7762% | 8.4746% | 155 | `{"atr_multiplier": 2.5, "atr_period": 21, "ma_period": 50}` |
| 12 | `r1_c44` | `bollinger_mean_reversion` | 1.5214 | 4.6881% | 7.7073% | 835 | `{"period": 10, "stddev_multiplier": 1.5}` |
| 13 | `r1_c05` | `moving_average_cross` | 1.1612 | 2.0316% | 5.8849% | 342 | `{"entry_threshold": 0.0003, "fast_window": 13, "slow_window": 34}` |
| 14 | `r1_c27` | `multi_timeframe_ma_spread` | 0.9833 | 2.3622% | 6.9323% | 113 | `{"primary_ma_period": 20, "reference_ma_period": 34, "spread_threshold_bps": 10.0}` |
| 15 | `r1_c46` | `bollinger_mean_reversion` | 0.7098 | 1.9740% | 8.2394% | 149 | `{"period": 30, "stddev_multiplier": 2.5}` |
| 16 | `r1_c14` | `rsi_reversion` | 0.5261 | 1.0560% | 7.0926% | 894 | `{"overbought": 80.0, "oversold": 20.0, "period": 5}` |
| 17 | `r1_c47` | `bollinger_mean_reversion` | 0.5046 | 1.2582% | 9.0287% | 62 | `{"period": 50, "stddev_multiplier": 3.0}` |
| 18 | `r1_c24` | `multi_timeframe_ma_spread` | 0.2326 | 0.3415% | 6.8465% | 141 | `{"primary_ma_period": 20, "reference_ma_period": 20, "spread_threshold_bps": 10.0}` |
| 19 | `r1_c18` | `rsi_reversion` | 0.0307 | -0.1376% | 6.3438% | 427 | `{"overbought": 65.0, "oversold": 35.0, "period": 14}` |
| 20 | `r1_c08` | `moving_average_cross` | -0.2970 | -0.5748% | 6.9809% | 274 | `{"entry_threshold": 0.001, "fast_window": 5, "slow_window": 34}` |
| 21 | `r1_c04` | `moving_average_cross` | -0.3863 | -0.7884% | 8.2964% | 427 | `{"entry_threshold": 0.0002, "fast_window": 10, "slow_window": 30}` |
| 22 | `r1_c26` | `multi_timeframe_ma_spread` | -0.4170 | -1.3565% | 8.4537% | 277 | `{"primary_ma_period": 8, "reference_ma_period": 21, "spread_threshold_bps": 2.0}` |
| 23 | `r1_c45` | `bollinger_mean_reversion` | -0.5580 | -2.0965% | 9.5267% | 296 | `{"period": 20, "stddev_multiplier": 2.0}` |
| 24 | `r1_c19` | `rsi_reversion` | -0.7282 | -1.8903% | 10.4890% | 160 | `{"overbought": 70.0, "oversold": 30.0, "period": 21}` |
| 25 | `r1_c40` | `atr_breakout` | -0.8147 | -2.4694% | 9.1051% | 356 | `{"atr_multiplier": 1.5, "atr_period": 14, "ma_period": 20}` |
| 26 | `r1_c17` | `rsi_reversion` | -1.0269 | -2.4341% | 7.8203% | 303 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
| 27 | `r1_c38` | `adx_trend_strength` | -1.1882 | -3.5834% | 9.2301% | 167 | `{"adx_threshold": 35.0, "period": 28}` |
| 28 | `r1_c37` | `adx_trend_strength` | -1.5847 | -3.9066% | 5.8535% | 384 | `{"adx_threshold": 30.0, "period": 20}` |
| 29 | `r1_c25` | `multi_timeframe_ma_spread` | -1.6333 | -4.2630% | 8.8154% | 416 | `{"primary_ma_period": 5, "reference_ma_period": 20, "spread_threshold_bps": 0.0}` |
| 30 | `r1_c30` | `donchian_breakout` | -1.7872 | -4.5595% | 9.9343% | 135 | `{"breakout_buffer_bps": 5.0, "lookback_window": 30}` |
| 31 | `r1_c41` | `atr_breakout` | -1.9962 | -5.0560% | 8.8216% | 239 | `{"atr_multiplier": 2.0, "atr_period": 14, "ma_period": 34}` |
| 32 | `r1_c21` | `multi_timeframe_ma_spread` | -2.4096 | -5.6528% | 9.7388% | 496 | `{"primary_ma_period": 8, "reference_ma_period": 8, "spread_threshold_bps": 2.0}` |
| 33 | `r1_c09` | `price_moving_average` | -2.4178 | -3.2697% | 7.9565% | 1151 | `{"entry_threshold": 0.0002, "period": 8}` |
| 34 | `r1_c29` | `donchian_breakout` | -2.5499 | -6.3943% | 12.0348% | 298 | `{"breakout_buffer_bps": 0.0, "lookback_window": 20}` |
| 35 | `r1_c31` | `donchian_breakout` | -2.6824 | -6.1725% | 7.9150% | 56 | `{"breakout_buffer_bps": 10.0, "lookback_window": 55}` |
| 36 | `r1_c02` | `moving_average_cross` | -2.9616 | -3.8456% | 7.8433% | 1174 | `{"entry_threshold": 0.0, "fast_window": 5, "slow_window": 13}` |
| 37 | `r1_c49` | `macd_trend_follow` | -3.0044 | -5.9826% | 7.5906% | 1007 | `{"fast_period": 12, "histogram_threshold": 0.0, "signal_period": 9, "slow_period": 26}` |
| 38 | `r1_c01` | `moving_average_cross` | -3.0441 | -4.5091% | 8.5583% | 1771 | `{"entry_threshold": 0.0, "fast_window": 3, "slow_window": 9}` |
| 39 | `r1_c35` | `adx_trend_strength` | -3.0882 | -6.3351% | 6.7992% | 905 | `{"adx_threshold": 22.0, "period": 14}` |
| 40 | `r1_c23` | `multi_timeframe_ma_spread` | -3.0887 | -7.6031% | 10.4329% | 272 | `{"primary_ma_period": 13, "reference_ma_period": 13, "spread_threshold_bps": 5.0}` |
| 41 | `r1_c22` | `multi_timeframe_ma_spread` | -3.1379 | -7.0974% | 11.0199% | 332 | `{"primary_ma_period": 10, "reference_ma_period": 10, "spread_threshold_bps": 5.0}` |
| 42 | `r1_c28` | `donchian_breakout` | -3.6148 | -7.5819% | 8.8712% | 552 | `{"breakout_buffer_bps": 0.0, "lookback_window": 10}` |
| 43 | `r1_c32` | `donchian_breakout` | -3.6780 | -8.2896% | 9.5946% | 50 | `{"breakout_buffer_bps": 10.0, "lookback_window": 80}` |
| 44 | `r1_c33` | `donchian_breakout` | -4.6462 | -8.8806% | 10.4880% | 13 | `{"breakout_buffer_bps": 20.0, "lookback_window": 120}` |
| 45 | `r1_c50` | `macd_trend_follow` | -5.2553 | -10.5512% | 11.6993% | 306 | `{"fast_period": 16, "histogram_threshold": 0.0002, "signal_period": 9, "slow_period": 39}` |
| 46 | `r1_c39` | `atr_breakout` | -5.2588 | -9.8870% | 11.7874% | 650 | `{"atr_multiplier": 1.0, "atr_period": 7, "ma_period": 10}` |
| 47 | `r1_c48` | `macd_trend_follow` | -5.4495 | -11.0223% | 12.4754% | 1641 | `{"fast_period": 8, "histogram_threshold": 0.0, "signal_period": 5, "slow_period": 21}` |
| 48 | `r1_c20` | `multi_timeframe_ma_spread` | -5.7575 | -10.7001% | 11.4631% | 1186 | `{"primary_ma_period": 5, "reference_ma_period": 5, "spread_threshold_bps": 0.0}` |
| 49 | `r1_c34` | `adx_trend_strength` | -6.1408 | -11.5150% | 12.2287% | 1799 | `{"adx_threshold": 18.0, "period": 7}` |
| 50 | `r1_c36` | `adx_trend_strength` | -6.1793 | -11.6486% | 11.8582% | 802 | `{"adx_threshold": 25.0, "period": 14}` |

## Round 2

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r2_c01` | `price_moving_average` | 6.1799 | 13.3346% | 3.3198% | 58 | `{"entry_threshold": 0.001, "period": 55}` |
| 2 | `r2_c22` | `moving_average_cross` | 4.8277 | 9.2712% | 5.1654% | 147 | `{"entry_threshold": 0.0, "fast_window": 37, "slow_window": 99}` |
| 3 | `r2_c41` | `price_moving_average` | 4.7859 | 12.1620% | 3.4801% | 168 | `{"entry_threshold": 0.0005, "period": 54}` |
| 4 | `r2_c02` | `moving_average_cross` | 4.5838 | 9.2014% | 4.7197% | 124 | `{"entry_threshold": 0.0005, "fast_window": 34, "slow_window": 89}` |
| 5 | `r2_c03` | `moving_average_cross` | 4.3748 | 10.8043% | 3.1442% | 198 | `{"entry_threshold": 0.0005, "fast_window": 20, "slow_window": 50}` |
| 6 | `r2_c23` | `moving_average_cross` | 4.3509 | 9.3658% | 6.8969% | 96 | `{"entry_threshold": 0.0015, "fast_window": 19, "slow_window": 60}` |
| 7 | `r2_c21` | `price_moving_average` | 4.0797 | 6.8483% | 2.9178% | 61 | `{"entry_threshold": 0.001, "period": 50}` |
| 8 | `r2_c42` | `moving_average_cross` | 3.8756 | 8.4053% | 6.1385% | 99 | `{"entry_threshold": 0.001, "fast_window": 33, "slow_window": 94}` |
| 9 | `r2_c29` | `price_moving_average` | 3.6029 | 7.9871% | 7.4059% | 110 | `{"entry_threshold": 0.001, "period": 18}` |
| 10 | `r2_c43` | `moving_average_cross` | 3.5433 | 8.4230% | 4.2321% | 130 | `{"entry_threshold": 0.001, "fast_window": 21, "slow_window": 40}` |
| 11 | `r2_c24` | `price_moving_average` | 3.1987 | 7.1555% | 4.5284% | 658 | `{"entry_threshold": 0.0003, "period": 12}` |
| 12 | `r2_c32` | `bollinger_mean_reversion` | 3.0472 | 10.0954% | 8.2017% | 728 | `{"period": 12, "stddev_multiplier": 1.5}` |
| 13 | `r2_c04` | `price_moving_average` | 2.9486 | 5.3178% | 5.8540% | 609 | `{"entry_threshold": 0.0003, "period": 13}` |
| 14 | `r2_c25` | `price_moving_average` | 2.8941 | 7.3629% | 5.3879% | 74 | `{"entry_threshold": 0.001, "period": 37}` |
| 15 | `r2_c05` | `price_moving_average` | 2.8010 | 6.8544% | 4.6911% | 217 | `{"entry_threshold": 0.0005, "period": 34}` |
| 16 | `r2_c06` | `atr_breakout` | 2.6213 | 7.5867% | 6.9631% | 110 | `{"atr_multiplier": 3.0, "atr_period": 21, "ma_period": 80}` |
| 17 | `r2_c39` | `rsi_reversion` | 2.6001 | 5.8336% | 3.9109% | 650 | `{"overbought": 60.0, "oversold": 30.0, "period": 10}` |
| 18 | `r2_c50` | `moving_average_cross` | 2.5846 | 4.6229% | 5.2866% | 927 | `{"entry_threshold": 0.0, "fast_window": 9, "slow_window": 16}` |
| 19 | `r2_c26` | `atr_breakout` | 2.5840 | 7.0670% | 6.1299% | 126 | `{"atr_multiplier": 2.5, "atr_period": 19, "ma_period": 90}` |
| 20 | `r2_c28` | `rsi_reversion` | 2.5225 | 5.3794% | 3.8880% | 412 | `{"overbought": 70.0, "oversold": 20.0, "period": 9}` |
| 21 | `r2_c07` | `rsi_reversion` | 2.4999 | 6.1767% | 4.9242% | 600 | `{"overbought": 70.0, "oversold": 30.0, "period": 9}` |
| 22 | `r2_c08` | `rsi_reversion` | 2.2004 | 5.2302% | 4.4997% | 683 | `{"overbought": 75.0, "oversold": 25.0, "period": 7}` |
| 23 | `r2_c09` | `price_moving_average` | 1.9690 | 4.6370% | 5.3515% | 294 | `{"entry_threshold": 0.0005, "period": 21}` |
| 24 | `r2_c36` | `rsi_reversion` | 1.9322 | 5.1477% | 6.1161% | 395 | `{"overbought": 80.0, "oversold": 25.0, "period": 9}` |
| 25 | `r2_c10` | `moving_average_cross` | 1.8919 | 3.2787% | 5.7756% | 725 | `{"entry_threshold": 0.0, "fast_window": 8, "slow_window": 21}` |
| 26 | `r2_c11` | `atr_breakout` | 1.6766 | 4.7762% | 8.4746% | 155 | `{"atr_multiplier": 2.5, "atr_period": 21, "ma_period": 50}` |
| 27 | `r2_c31` | `atr_breakout` | 1.5663 | 4.3084% | 7.3015% | 154 | `{"atr_multiplier": 2.5, "atr_period": 17, "ma_period": 52}` |
| 28 | `r2_c48` | `rsi_reversion` | 1.5620 | 3.7464% | 6.0477% | 895 | `{"overbought": 75.0, "oversold": 27.5, "period": 6}` |
| 29 | `r2_c12` | `bollinger_mean_reversion` | 1.5214 | 4.6881% | 7.7073% | 835 | `{"period": 10, "stddev_multiplier": 1.5}` |
| 30 | `r2_c45` | `price_moving_average` | 1.3933 | 2.8814% | 5.1741% | 1257 | `{"entry_threshold": 0.0, "period": 29}` |
| 31 | `r2_c49` | `price_moving_average` | 1.2469 | 2.0661% | 6.3491% | 1407 | `{"entry_threshold": 0.0, "period": 24}` |
| 32 | `r2_c13` | `moving_average_cross` | 1.1612 | 2.0316% | 5.8849% | 342 | `{"entry_threshold": 0.0003, "fast_window": 13, "slow_window": 34}` |
| 33 | `r2_c27` | `rsi_reversion` | 1.0841 | 2.7427% | 6.5639% | 478 | `{"overbought": 72.5, "oversold": 35.0, "period": 11}` |
| 34 | `r2_c14` | `multi_timeframe_ma_spread` | 0.9833 | 2.3622% | 6.9323% | 113 | `{"primary_ma_period": 20, "reference_ma_period": 34, "spread_threshold_bps": 10.0}` |
| 35 | `r2_c15` | `bollinger_mean_reversion` | 0.7098 | 1.9740% | 8.2394% | 149 | `{"period": 30, "stddev_multiplier": 2.5}` |
| 36 | `r2_c46` | `atr_breakout` | 0.6927 | 1.6472% | 7.2017% | 98 | `{"atr_multiplier": 3.5, "atr_period": 20, "ma_period": 75}` |
| 37 | `r2_c16` | `rsi_reversion` | 0.5261 | 1.0560% | 7.0926% | 894 | `{"overbought": 80.0, "oversold": 20.0, "period": 5}` |
| 38 | `r2_c17` | `bollinger_mean_reversion` | 0.5046 | 1.2582% | 9.0287% | 62 | `{"period": 50, "stddev_multiplier": 3.0}` |
| 39 | `r2_c33` | `moving_average_cross` | 0.4712 | 0.6803% | 7.5173% | 232 | `{"entry_threshold": 0.0008, "fast_window": 12, "slow_window": 29}` |
| 40 | `r2_c18` | `multi_timeframe_ma_spread` | 0.2326 | 0.3415% | 6.8465% | 141 | `{"primary_ma_period": 20, "reference_ma_period": 20, "spread_threshold_bps": 10.0}` |
| 41 | `r2_c40` | `multi_timeframe_ma_spread` | 0.1407 | 0.0874% | 8.8593% | 195 | `{"primary_ma_period": 7, "reference_ma_period": 16, "spread_threshold_bps": 12.0}` |
| 42 | `r2_c35` | `bollinger_mean_reversion` | 0.0545 | -0.1925% | 8.7995% | 91 | `{"period": 40, "stddev_multiplier": 2.75}` |
| 43 | `r2_c19` | `rsi_reversion` | 0.0307 | -0.1376% | 6.3438% | 427 | `{"overbought": 65.0, "oversold": 35.0, "period": 14}` |
| 44 | `r2_c30` | `moving_average_cross` | -0.2380 | -0.5369% | 7.3864% | 280 | `{"entry_threshold": 0.001, "fast_window": 5, "slow_window": 26}` |
| 45 | `r2_c47` | `rsi_reversion` | -0.2410 | -0.6505% | 5.3074% | 873 | `{"overbought": 65.0, "oversold": 27.5, "period": 7}` |
| 46 | `r2_c20` | `multi_timeframe_ma_spread` | -0.4170 | -1.3565% | 8.4537% | 277 | `{"primary_ma_period": 8, "reference_ma_period": 21, "spread_threshold_bps": 2.0}` |
| 47 | `r2_c38` | `multi_timeframe_ma_spread` | -0.6756 | -2.1163% | 9.3375% | 86 | `{"primary_ma_period": 19, "reference_ma_period": 25, "spread_threshold_bps": 20.0}` |
| 48 | `r2_c34` | `multi_timeframe_ma_spread` | -0.8886 | -2.1724% | 5.8705% | 79 | `{"primary_ma_period": 25, "reference_ma_period": 44, "spread_threshold_bps": 15.0}` |
| 49 | `r2_c37` | `bollinger_mean_reversion` | -1.6883 | -5.3503% | 12.3382% | 103 | `{"period": 52, "stddev_multiplier": 2.5}` |
| 50 | `r2_c44` | `price_moving_average` | -3.4130 | -4.8926% | 8.3051% | 2237 | `{"entry_threshold": 0.0, "period": 10}` |

## Round 3

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r3_c01` | `price_moving_average` | 6.1799 | 13.3346% | 3.3198% | 58 | `{"entry_threshold": 0.001, "period": 55}` |
| 2 | `r3_c47` | `price_moving_average` | 5.5424 | 10.4998% | 2.9984% | 63 | `{"entry_threshold": 0.001, "period": 49}` |
| 3 | `r3_c42` | `moving_average_cross` | 4.9812 | 9.6089% | 4.6987% | 142 | `{"entry_threshold": 0.0, "fast_window": 34, "slow_window": 104}` |
| 4 | `r3_c44` | `moving_average_cross` | 4.9098 | 9.6682% | 4.9127% | 120 | `{"entry_threshold": 0.0005, "fast_window": 32, "slow_window": 94}` |
| 5 | `r3_c02` | `moving_average_cross` | 4.8277 | 9.2712% | 5.1654% | 147 | `{"entry_threshold": 0.0, "fast_window": 37, "slow_window": 99}` |
| 6 | `r3_c03` | `price_moving_average` | 4.7859 | 12.1620% | 3.4801% | 168 | `{"entry_threshold": 0.0005, "period": 54}` |
| 7 | `r3_c23` | `price_moving_average` | 4.6271 | 9.1107% | 3.4051% | 62 | `{"entry_threshold": 0.001, "period": 51}` |
| 8 | `r3_c04` | `moving_average_cross` | 4.5838 | 9.2014% | 4.7197% | 124 | `{"entry_threshold": 0.0005, "fast_window": 34, "slow_window": 89}` |
| 9 | `r3_c05` | `moving_average_cross` | 4.3748 | 10.8043% | 3.1442% | 198 | `{"entry_threshold": 0.0005, "fast_window": 20, "slow_window": 50}` |
| 10 | `r3_c22` | `moving_average_cross` | 4.3552 | 8.9053% | 5.4590% | 110 | `{"entry_threshold": 0.0005, "fast_window": 39, "slow_window": 104}` |
| 11 | `r3_c06` | `moving_average_cross` | 4.3509 | 9.3658% | 6.8969% | 96 | `{"entry_threshold": 0.0015, "fast_window": 19, "slow_window": 60}` |
| 12 | `r3_c07` | `price_moving_average` | 4.0797 | 6.8483% | 2.9178% | 61 | `{"entry_threshold": 0.001, "period": 50}` |
| 13 | `r3_c21` | `price_moving_average` | 3.9556 | 9.8196% | 5.5740% | 20 | `{"entry_threshold": 0.0015, "period": 56}` |
| 14 | `r3_c41` | `price_moving_average` | 3.9032 | 9.5471% | 5.5337% | 24 | `{"entry_threshold": 0.0015, "period": 58}` |
| 15 | `r3_c24` | `moving_average_cross` | 3.8542 | 8.0339% | 5.8052% | 95 | `{"entry_threshold": 0.001, "fast_window": 36, "slow_window": 84}` |
| 16 | `r3_c46` | `moving_average_cross` | 3.7251 | 7.2036% | 5.9250% | 94 | `{"entry_threshold": 0.0015, "fast_window": 21, "slow_window": 75}` |
| 17 | `r3_c08` | `price_moving_average` | 3.6029 | 7.9871% | 7.4059% | 110 | `{"entry_threshold": 0.001, "period": 18}` |
| 18 | `r3_c43` | `price_moving_average` | 3.5379 | 8.8024% | 5.5740% | 22 | `{"entry_threshold": 0.0015, "period": 57}` |
| 19 | `r3_c45` | `moving_average_cross` | 3.2996 | 6.5821% | 5.4904% | 243 | `{"entry_threshold": 0.0, "fast_window": 17, "slow_window": 65}` |
| 20 | `r3_c26` | `moving_average_cross` | 3.1464 | 6.6198% | 5.6561% | 60 | `{"entry_threshold": 0.0025, "fast_window": 17, "slow_window": 55}` |
| 21 | `r3_c09` | `bollinger_mean_reversion` | 3.0472 | 10.0954% | 8.2017% | 728 | `{"period": 12, "stddev_multiplier": 1.5}` |
| 22 | `r3_c10` | `atr_breakout` | 2.6213 | 7.5867% | 6.9631% | 110 | `{"atr_multiplier": 3.0, "atr_period": 21, "ma_period": 80}` |
| 23 | `r3_c11` | `rsi_reversion` | 2.6001 | 5.8336% | 3.9109% | 650 | `{"overbought": 60.0, "oversold": 30.0, "period": 10}` |
| 24 | `r3_c12` | `atr_breakout` | 2.5840 | 7.0670% | 6.1299% | 126 | `{"atr_multiplier": 2.5, "atr_period": 19, "ma_period": 90}` |
| 25 | `r3_c25` | `moving_average_cross` | 2.5269 | 5.9134% | 4.1175% | 225 | `{"entry_threshold": 0.0005, "fast_window": 19, "slow_window": 45}` |
| 26 | `r3_c13` | `rsi_reversion` | 2.5225 | 5.3794% | 3.8880% | 412 | `{"overbought": 70.0, "oversold": 20.0, "period": 9}` |
| 27 | `r3_c32` | `atr_breakout` | 2.5126 | 7.1018% | 6.3530% | 141 | `{"atr_multiplier": 2.25, "atr_period": 15, "ma_period": 88}` |
| 28 | `r3_c14` | `rsi_reversion` | 2.4999 | 6.1767% | 4.9242% | 600 | `{"overbought": 70.0, "oversold": 30.0, "period": 9}` |
| 29 | `r3_c15` | `rsi_reversion` | 2.2004 | 5.2302% | 4.4997% | 683 | `{"overbought": 75.0, "oversold": 25.0, "period": 7}` |
| 30 | `r3_c33` | `rsi_reversion` | 2.1414 | 5.1287% | 4.9450% | 322 | `{"overbought": 72.5, "oversold": 22.5, "period": 11}` |
| 31 | `r3_c48` | `price_moving_average` | 1.9690 | 4.6370% | 5.3515% | 294 | `{"entry_threshold": 0.0005, "period": 21}` |
| 32 | `r3_c50` | `atr_breakout` | 1.9531 | 5.0396% | 8.3889% | 88 | `{"atr_multiplier": 3.5, "atr_period": 25, "ma_period": 85}` |
| 33 | `r3_c16` | `atr_breakout` | 1.6766 | 4.7762% | 8.4746% | 155 | `{"atr_multiplier": 2.5, "atr_period": 21, "ma_period": 50}` |
| 34 | `r3_c17` | `atr_breakout` | 1.5663 | 4.3084% | 7.3015% | 154 | `{"atr_multiplier": 2.5, "atr_period": 17, "ma_period": 52}` |
| 35 | `r3_c36` | `atr_breakout` | 1.5448 | 4.2451% | 6.8381% | 147 | `{"atr_multiplier": 2.75, "atr_period": 20, "ma_period": 45}` |
| 36 | `r3_c18` | `bollinger_mean_reversion` | 1.5214 | 4.6881% | 7.7073% | 835 | `{"period": 10, "stddev_multiplier": 1.5}` |
| 37 | `r3_c35` | `rsi_reversion` | 1.4848 | 3.2069% | 3.7746% | 818 | `{"overbought": 70.0, "oversold": 20.0, "period": 6}` |
| 38 | `r3_c39` | `multi_timeframe_ma_spread` | 0.9899 | 2.7120% | 7.5740% | 85 | `{"primary_ma_period": 17, "reference_ma_period": 24, "spread_threshold_bps": 20.0}` |
| 39 | `r3_c19` | `multi_timeframe_ma_spread` | 0.9833 | 2.3622% | 6.9323% | 113 | `{"primary_ma_period": 20, "reference_ma_period": 34, "spread_threshold_bps": 10.0}` |
| 40 | `r3_c20` | `bollinger_mean_reversion` | 0.7098 | 1.9740% | 8.2394% | 149 | `{"period": 30, "stddev_multiplier": 2.5}` |
| 41 | `r3_c28` | `price_moving_average` | 0.6773 | 1.3353% | 8.6404% | 105 | `{"entry_threshold": 0.001, "period": 19}` |
| 42 | `r3_c40` | `bollinger_mean_reversion` | 0.4397 | 0.9203% | 7.5926% | 80 | `{"period": 28, "stddev_multiplier": 3.0}` |
| 43 | `r3_c37` | `atr_breakout` | 0.2594 | 0.4108% | 6.2971% | 177 | `{"atr_multiplier": 2.0, "atr_period": 19, "ma_period": 62}` |
| 44 | `r3_c31` | `rsi_reversion` | -0.3439 | -0.6367% | 4.3443% | 349 | `{"overbought": 55.0, "oversold": 27.5, "period": 14}` |
| 45 | `r3_c27` | `price_moving_average` | -0.3831 | -1.2077% | 9.3007% | 19 | `{"entry_threshold": 0.002, "period": 55}` |
| 46 | `r3_c34` | `rsi_reversion` | -0.4858 | -1.2251% | 6.2644% | 1368 | `{"overbought": 70.0, "oversold": 32.5, "period": 5}` |
| 47 | `r3_c30` | `atr_breakout` | -0.6679 | -1.9778% | 7.5760% | 86 | `{"atr_multiplier": 3.5, "atr_period": 17, "ma_period": 90}` |
| 48 | `r3_c38` | `bollinger_mean_reversion` | -1.1575 | -3.9565% | 10.9046% | 701 | `{"period": 15, "stddev_multiplier": 1.25}` |
| 49 | `r3_c49` | `bollinger_mean_reversion` | -1.5350 | -4.6502% | 7.2856% | 433 | `{"period": 10, "stddev_multiplier": 2.0}` |
| 50 | `r3_c29` | `bollinger_mean_reversion` | -2.2290 | -6.8777% | 11.8971% | 567 | `{"period": 5, "stddev_multiplier": 1.75}` |

## Round 4

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r4_c01` | `price_moving_average` | 6.1799 | 13.3346% | 3.3198% | 58 | `{"entry_threshold": 0.001, "period": 55}` |
| 2 | `r4_c22` | `price_moving_average` | 5.7141 | 12.5340% | 3.8392% | 23 | `{"entry_threshold": 0.0015, "period": 52}` |
| 3 | `r4_c47` | `price_moving_average` | 5.6514 | 11.9016% | 3.3853% | 51 | `{"entry_threshold": 0.001, "period": 54}` |
| 4 | `r4_c02` | `price_moving_average` | 5.5424 | 10.4998% | 2.9984% | 63 | `{"entry_threshold": 0.001, "period": 49}` |
| 5 | `r4_c27` | `price_moving_average` | 5.2179 | 11.5791% | 3.2948% | 22 | `{"entry_threshold": 0.0015, "period": 48}` |
| 6 | `r4_c48` | `moving_average_cross` | 5.1393 | 9.8855% | 5.9975% | 180 | `{"entry_threshold": 0.0, "fast_window": 37, "slow_window": 79}` |
| 7 | `r4_c03` | `moving_average_cross` | 4.9812 | 9.6089% | 4.6987% | 142 | `{"entry_threshold": 0.0, "fast_window": 34, "slow_window": 104}` |
| 8 | `r4_c45` | `moving_average_cross` | 4.9536 | 9.6422% | 4.9152% | 155 | `{"entry_threshold": 0.0, "fast_window": 38, "slow_window": 94}` |
| 9 | `r4_c04` | `moving_average_cross` | 4.9098 | 9.6682% | 4.9127% | 120 | `{"entry_threshold": 0.0005, "fast_window": 32, "slow_window": 94}` |
| 10 | `r4_c46` | `price_moving_average` | 4.8778 | 12.2937% | 3.3820% | 168 | `{"entry_threshold": 0.0005, "period": 53}` |
| 11 | `r4_c05` | `moving_average_cross` | 4.8277 | 9.2712% | 5.1654% | 147 | `{"entry_threshold": 0.0, "fast_window": 37, "slow_window": 99}` |
| 12 | `r4_c41` | `price_moving_average` | 4.7891 | 10.5047% | 6.0033% | 183 | `{"entry_threshold": 0.0005, "period": 50}` |
| 13 | `r4_c06` | `price_moving_average` | 4.7859 | 12.1620% | 3.4801% | 168 | `{"entry_threshold": 0.0005, "period": 54}` |
| 14 | `r4_c23` | `moving_average_cross` | 4.7661 | 9.1289% | 4.8017% | 147 | `{"entry_threshold": 0.0, "fast_window": 36, "slow_window": 99}` |
| 15 | `r4_c07` | `price_moving_average` | 4.6271 | 9.1107% | 3.4051% | 62 | `{"entry_threshold": 0.001, "period": 51}` |
| 16 | `r4_c08` | `moving_average_cross` | 4.5838 | 9.2014% | 4.7197% | 124 | `{"entry_threshold": 0.0005, "fast_window": 34, "slow_window": 89}` |
| 17 | `r4_c25` | `moving_average_cross` | 4.4456 | 9.5666% | 5.3024% | 101 | `{"entry_threshold": 0.0005, "fast_window": 34, "slow_window": 114}` |
| 18 | `r4_c43` | `moving_average_cross` | 4.3635 | 8.7854% | 5.8811% | 127 | `{"entry_threshold": 0.0, "fast_window": 32, "slow_window": 119}` |
| 19 | `r4_c26` | `price_moving_average` | 4.2122 | 9.3908% | 6.7684% | 185 | `{"entry_threshold": 0.0005, "period": 49}` |
| 20 | `r4_c21` | `price_moving_average` | 4.0797 | 6.8483% | 2.9178% | 61 | `{"entry_threshold": 0.001, "period": 50}` |
| 21 | `r4_c42` | `price_moving_average` | 3.9349 | 9.6916% | 5.5878% | 25 | `{"entry_threshold": 0.0015, "period": 54}` |
| 22 | `r4_c24` | `moving_average_cross` | 3.8849 | 7.4294% | 5.5052% | 146 | `{"entry_threshold": 0.0, "fast_window": 29, "slow_window": 104}` |
| 23 | `r4_c35` | `rsi_reversion` | 3.5135 | 9.4131% | 5.1043% | 426 | `{"overbought": 75.0, "oversold": 27.5, "period": 10}` |
| 24 | `r4_c44` | `moving_average_cross` | 3.4650 | 7.3655% | 5.0302% | 75 | `{"entry_threshold": 0.0015, "fast_window": 31, "slow_window": 109}` |
| 25 | `r4_c28` | `moving_average_cross` | 3.2274 | 6.9998% | 6.5159% | 79 | `{"entry_threshold": 0.0015, "fast_window": 32, "slow_window": 79}` |
| 26 | `r4_c50` | `atr_breakout` | 3.1326 | 9.0252% | 6.5676% | 128 | `{"atr_multiplier": 2.5, "atr_period": 22, "ma_period": 78}` |
| 27 | `r4_c09` | `bollinger_mean_reversion` | 3.0472 | 10.0954% | 8.2017% | 728 | `{"period": 12, "stddev_multiplier": 1.5}` |
| 28 | `r4_c10` | `atr_breakout` | 2.6213 | 7.5867% | 6.9631% | 110 | `{"atr_multiplier": 3.0, "atr_period": 21, "ma_period": 80}` |
| 29 | `r4_c11` | `rsi_reversion` | 2.6001 | 5.8336% | 3.9109% | 650 | `{"overbought": 60.0, "oversold": 30.0, "period": 10}` |
| 30 | `r4_c12` | `atr_breakout` | 2.5840 | 7.0670% | 6.1299% | 126 | `{"atr_multiplier": 2.5, "atr_period": 19, "ma_period": 90}` |
| 31 | `r4_c13` | `rsi_reversion` | 2.5225 | 5.3794% | 3.8880% | 412 | `{"overbought": 70.0, "oversold": 20.0, "period": 9}` |
| 32 | `r4_c32` | `atr_breakout` | 2.5133 | 7.1954% | 6.7232% | 133 | `{"atr_multiplier": 2.25, "atr_period": 15, "ma_period": 92}` |
| 33 | `r4_c14` | `atr_breakout` | 2.5126 | 7.1018% | 6.3530% | 141 | `{"atr_multiplier": 2.25, "atr_period": 15, "ma_period": 88}` |
| 34 | `r4_c15` | `rsi_reversion` | 2.4999 | 6.1767% | 4.9242% | 600 | `{"overbought": 70.0, "oversold": 30.0, "period": 9}` |
| 35 | `r4_c37` | `atr_breakout` | 2.4545 | 6.6684% | 7.0806% | 107 | `{"atr_multiplier": 3.0, "atr_period": 26, "ma_period": 87}` |
| 36 | `r4_c16` | `rsi_reversion` | 2.2004 | 5.2302% | 4.4997% | 683 | `{"overbought": 75.0, "oversold": 25.0, "period": 7}` |
| 37 | `r4_c30` | `atr_breakout` | 2.1783 | 5.7936% | 6.9793% | 107 | `{"atr_multiplier": 3.0, "atr_period": 19, "ma_period": 85}` |
| 38 | `r4_c34` | `atr_breakout` | 1.9728 | 5.2277% | 6.7518% | 162 | `{"atr_multiplier": 1.75, "atr_period": 11, "ma_period": 83}` |
| 39 | `r4_c17` | `atr_breakout` | 1.9531 | 5.0396% | 8.3889% | 88 | `{"atr_multiplier": 3.5, "atr_period": 25, "ma_period": 85}` |
| 40 | `r4_c18` | `bollinger_mean_reversion` | 1.5214 | 4.6881% | 7.7073% | 835 | `{"period": 10, "stddev_multiplier": 1.5}` |
| 41 | `r4_c39` | `multi_timeframe_ma_spread` | 1.2321 | 3.1957% | 8.4216% | 97 | `{"primary_ma_period": 16, "reference_ma_period": 22, "spread_threshold_bps": 20.0}` |
| 42 | `r4_c31` | `rsi_reversion` | 1.0086 | 2.2062% | 6.1943% | 556 | `{"overbought": 65.0, "oversold": 32.5, "period": 11}` |
| 43 | `r4_c19` | `multi_timeframe_ma_spread` | 0.9899 | 2.7120% | 7.5740% | 85 | `{"primary_ma_period": 17, "reference_ma_period": 24, "spread_threshold_bps": 20.0}` |
| 44 | `r4_c20` | `multi_timeframe_ma_spread` | 0.9833 | 2.3622% | 6.9323% | 113 | `{"primary_ma_period": 20, "reference_ma_period": 34, "spread_threshold_bps": 10.0}` |
| 45 | `r4_c33` | `rsi_reversion` | 0.9165 | 1.5596% | 4.8776% | 237 | `{"overbought": 72.5, "oversold": 17.5, "period": 11}` |
| 46 | `r4_c38` | `bollinger_mean_reversion` | -0.4703 | -1.8913% | 9.1943% | 567 | `{"period": 20, "stddev_multiplier": 1.25}` |
| 47 | `r4_c29` | `bollinger_mean_reversion` | -0.4931 | -1.8450% | 7.1373% | 515 | `{"period": 14, "stddev_multiplier": 1.75}` |
| 48 | `r4_c36` | `rsi_reversion` | -0.7416 | -1.6573% | 5.3990% | 2329 | `{"overbought": 72.5, "oversold": 30.0, "period": 3}` |
| 49 | `r4_c40` | `multi_timeframe_ma_spread` | -1.2208 | -3.7179% | 8.1408% | 58 | `{"primary_ma_period": 21, "reference_ma_period": 36, "spread_threshold_bps": 30.0}` |
| 50 | `r4_c49` | `bollinger_mean_reversion` | -1.5244 | -5.1466% | 12.7994% | 729 | `{"period": 17, "stddev_multiplier": 1.0}` |

## Round 5

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
| 9 | `r5_c08` | `moving_average_cross` | 4.9098 | 9.6682% | 4.9127% | 120 | `{"entry_threshold": 0.0005, "fast_window": 32, "slow_window": 94}` |
| 10 | `r5_c21` | `price_moving_average` | 4.8973 | 11.4762% | 4.5644% | 50 | `{"entry_threshold": 0.001, "period": 60}` |
| 11 | `r5_c25` | `moving_average_cross` | 4.8603 | 9.4537% | 5.5878% | 174 | `{"entry_threshold": 0.0, "fast_window": 39, "slow_window": 84}` |
| 12 | `r5_c44` | `price_moving_average` | 4.7859 | 12.1620% | 3.4801% | 168 | `{"entry_threshold": 0.0005, "period": 54}` |
| 13 | `r5_c28` | `moving_average_cross` | 4.7740 | 9.2635% | 4.9205% | 127 | `{"entry_threshold": 0.0005, "fast_window": 29, "slow_window": 84}` |
| 14 | `r5_c43` | `price_moving_average` | 4.6271 | 9.1107% | 3.4051% | 62 | `{"entry_threshold": 0.001, "period": 51}` |
| 15 | `r5_c27` | `moving_average_cross` | 4.5603 | 9.4282% | 4.6751% | 110 | `{"entry_threshold": 0.0005, "fast_window": 37, "slow_window": 104}` |
| 16 | `r5_c26` | `moving_average_cross` | 4.5599 | 9.3211% | 5.3840% | 126 | `{"entry_threshold": 0.0, "fast_window": 35, "slow_window": 119}` |
| 17 | `r5_c47` | `moving_average_cross` | 4.3552 | 8.9053% | 5.4590% | 110 | `{"entry_threshold": 0.0005, "fast_window": 39, "slow_window": 104}` |
| 18 | `r5_c46` | `moving_average_cross` | 4.2852 | 8.8580% | 4.8783% | 84 | `{"entry_threshold": 0.001, "fast_window": 37, "slow_window": 114}` |
| 19 | `r5_c41` | `price_moving_average` | 3.9556 | 9.8196% | 5.5740% | 20 | `{"entry_threshold": 0.0015, "period": 56}` |
| 20 | `r5_c48` | `moving_average_cross` | 3.9085 | 7.5808% | 5.4494% | 100 | `{"entry_threshold": 0.001, "fast_window": 35, "slow_window": 84}` |
| 21 | `r5_c42` | `price_moving_average` | 3.5379 | 8.8024% | 5.5740% | 22 | `{"entry_threshold": 0.0015, "period": 57}` |
| 22 | `r5_c09` | `rsi_reversion` | 3.5135 | 9.4131% | 5.1043% | 426 | `{"overbought": 75.0, "oversold": 27.5, "period": 10}` |
| 23 | `r5_c30` | `atr_breakout` | 3.4897 | 10.8193% | 7.3457% | 110 | `{"atr_multiplier": 2.75, "atr_period": 18, "ma_period": 73}` |
| 24 | `r5_c23` | `price_moving_average` | 3.2641 | 7.7471% | 4.7457% | 18 | `{"entry_threshold": 0.002, "period": 51}` |
| 25 | `r5_c10` | `atr_breakout` | 3.1326 | 9.0252% | 6.5676% | 128 | `{"atr_multiplier": 2.5, "atr_period": 22, "ma_period": 78}` |
| 26 | `r5_c11` | `bollinger_mean_reversion` | 3.0472 | 10.0954% | 8.2017% | 728 | `{"period": 12, "stddev_multiplier": 1.5}` |
| 27 | `r5_c12` | `atr_breakout` | 2.6213 | 7.5867% | 6.9631% | 110 | `{"atr_multiplier": 3.0, "atr_period": 21, "ma_period": 80}` |
| 28 | `r5_c13` | `rsi_reversion` | 2.6001 | 5.8336% | 3.9109% | 650 | `{"overbought": 60.0, "oversold": 30.0, "period": 10}` |
| 29 | `r5_c14` | `atr_breakout` | 2.5840 | 7.0670% | 6.1299% | 126 | `{"atr_multiplier": 2.5, "atr_period": 19, "ma_period": 90}` |
| 30 | `r5_c15` | `rsi_reversion` | 2.5225 | 5.3794% | 3.8880% | 412 | `{"overbought": 70.0, "oversold": 20.0, "period": 9}` |
| 31 | `r5_c40` | `multi_timeframe_ma_spread` | 2.5195 | 6.9442% | 6.3773% | 113 | `{"primary_ma_period": 18, "reference_ma_period": 34, "spread_threshold_bps": 10.0}` |
| 32 | `r5_c16` | `atr_breakout` | 2.5133 | 7.1954% | 6.7232% | 133 | `{"atr_multiplier": 2.25, "atr_period": 15, "ma_period": 92}` |
| 33 | `r5_c17` | `rsi_reversion` | 2.4999 | 6.1767% | 4.9242% | 600 | `{"overbought": 70.0, "oversold": 30.0, "period": 9}` |
| 34 | `r5_c36` | `atr_breakout` | 2.2863 | 6.4520% | 7.0097% | 131 | `{"atr_multiplier": 2.25, "atr_period": 13, "ma_period": 97}` |
| 35 | `r5_c39` | `multi_timeframe_ma_spread` | 2.2652 | 6.1120% | 9.2817% | 106 | `{"primary_ma_period": 11, "reference_ma_period": 17, "spread_threshold_bps": 20.0}` |
| 36 | `r5_c32` | `atr_breakout` | 2.2473 | 6.2611% | 7.4813% | 121 | `{"atr_multiplier": 2.75, "atr_period": 25, "ma_period": 78}` |
| 37 | `r5_c50` | `atr_breakout` | 2.1921 | 5.9308% | 6.1597% | 135 | `{"atr_multiplier": 2.5, "atr_period": 20, "ma_period": 83}` |
| 38 | `r5_c33` | `rsi_reversion` | 1.8275 | 3.5404% | 4.8545% | 1104 | `{"overbought": 55.0, "oversold": 35.0, "period": 8}` |
| 39 | `r5_c18` | `bollinger_mean_reversion` | 1.5214 | 4.6881% | 7.7073% | 835 | `{"period": 10, "stddev_multiplier": 1.5}` |
| 40 | `r5_c49` | `rsi_reversion` | 1.4744 | 3.5953% | 6.0079% | 271 | `{"overbought": 80.0, "oversold": 25.0, "period": 11}` |
| 41 | `r5_c19` | `multi_timeframe_ma_spread` | 1.2321 | 3.1957% | 8.4216% | 97 | `{"primary_ma_period": 16, "reference_ma_period": 22, "spread_threshold_bps": 20.0}` |
| 42 | `r5_c20` | `multi_timeframe_ma_spread` | 0.9899 | 2.7120% | 7.5740% | 85 | `{"primary_ma_period": 17, "reference_ma_period": 24, "spread_threshold_bps": 20.0}` |
| 43 | `r5_c38` | `bollinger_mean_reversion` | 0.8802 | 2.5114% | 11.2253% | 984 | `{"period": 12, "stddev_multiplier": 1.0}` |
| 44 | `r5_c34` | `atr_breakout` | 0.2003 | 0.2591% | 8.2498% | 132 | `{"atr_multiplier": 2.25, "atr_period": 21, "ma_period": 95}` |
| 45 | `r5_c29` | `rsi_reversion` | 0.1374 | 0.1131% | 8.5685% | 159 | `{"overbought": 77.5, "oversold": 22.5, "period": 14}` |
| 46 | `r5_c24` | `price_moving_average` | 0.1102 | 0.0722% | 7.3838% | 19 | `{"entry_threshold": 0.002, "period": 46}` |
| 47 | `r5_c31` | `bollinger_mean_reversion` | 0.0000 | 0.0000% | 0.0000% | 0 | `{"period": 5, "stddev_multiplier": 2.0}` |
| 48 | `r5_c35` | `rsi_reversion` | -0.1570 | -0.3440% | 5.2965% | 189 | `{"overbought": 72.5, "oversold": 15.0, "period": 11}` |
| 49 | `r5_c37` | `rsi_reversion` | -0.2410 | -0.6505% | 5.3074% | 873 | `{"overbought": 65.0, "oversold": 27.5, "period": 7}` |
| 50 | `r5_c22` | `price_moving_average` | -0.3831 | -1.2077% | 9.3007% | 19 | `{"entry_threshold": 0.002, "period": 55}` |
