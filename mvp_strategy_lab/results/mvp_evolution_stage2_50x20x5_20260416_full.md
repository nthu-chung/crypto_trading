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
| 1 | `r1_c01` | `donchian_breakout` | 3.1180 | 47.6803% | 16.7789% | 117 | `{"breakout_buffer_bps": 35.0, "lookback_window": 64}` |
| 2 | `r1_c02` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 3 | `r1_c03` | `donchian_breakout` | 3.0918 | 47.1767% | 18.8271% | 116 | `{"breakout_buffer_bps": 35.0, "lookback_window": 65}` |
| 4 | `r1_c04` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 67}` |
| 5 | `r1_c30` | `donchian_breakout` | 2.3896 | 33.4237% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 60}` |
| 6 | `r1_c44` | `donchian_breakout` | 2.3896 | 33.4237% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 62}` |
| 7 | `r1_c05` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 70}` |
| 8 | `r1_c06` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 67}` |
| 9 | `r1_c07` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 68}` |
| 10 | `r1_c46` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 69}` |
| 11 | `r1_c08` | `donchian_breakout` | 1.9445 | 25.7324% | 20.6542% | 124 | `{"breakout_buffer_bps": 35.0, "lookback_window": 60}` |
| 12 | `r1_c09` | `multi_timeframe_ma_spread` | 1.9037 | 23.5975% | 26.6440% | 75 | `{"primary_ma_period": 28, "reference_ma_period": 69, "spread_threshold_bps": 60.0}` |
| 13 | `r1_c39` | `multi_timeframe_ma_spread` | 1.8299 | 22.4958% | 23.1998% | 75 | `{"primary_ma_period": 25, "reference_ma_period": 60, "spread_threshold_bps": 80.0}` |
| 14 | `r1_c24` | `donchian_breakout` | 1.8265 | 23.7497% | 22.4945% | 112 | `{"breakout_buffer_bps": 35.0, "lookback_window": 77}` |
| 15 | `r1_c50` | `donchian_breakout` | 1.8105 | 23.3239% | 24.7050% | 89 | `{"breakout_buffer_bps": 40.0, "lookback_window": 75}` |
| 16 | `r1_c10` | `donchian_breakout` | 1.6796 | 21.2897% | 27.4253% | 147 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 17 | `r1_c34` | `multi_timeframe_ma_spread` | 1.6106 | 18.9252% | 27.7778% | 63 | `{"primary_ma_period": 34, "reference_ma_period": 79, "spread_threshold_bps": 55.0}` |
| 18 | `r1_c11` | `donchian_breakout` | 1.6073 | 19.9247% | 27.2363% | 100 | `{"breakout_buffer_bps": 40.0, "lookback_window": 53}` |
| 19 | `r1_c31` | `donchian_breakout` | 1.6073 | 19.9247% | 27.2363% | 100 | `{"breakout_buffer_bps": 40.0, "lookback_window": 51}` |
| 20 | `r1_c29` | `multi_timeframe_ma_spread` | 1.6061 | 18.9307% | 24.9083% | 71 | `{"primary_ma_period": 33, "reference_ma_period": 67, "spread_threshold_bps": 55.0}` |
| 21 | `r1_c12` | `multi_timeframe_ma_spread` | 1.5909 | 18.6755% | 29.1014% | 82 | `{"primary_ma_period": 23, "reference_ma_period": 71, "spread_threshold_bps": 65.0}` |
| 22 | `r1_c13` | `multi_timeframe_ma_spread` | 1.4960 | 17.3027% | 18.6359% | 78 | `{"primary_ma_period": 29, "reference_ma_period": 57, "spread_threshold_bps": 55.0}` |
| 23 | `r1_c14` | `multi_timeframe_ma_spread` | 1.4807 | 17.0156% | 28.3786% | 61 | `{"primary_ma_period": 31, "reference_ma_period": 74, "spread_threshold_bps": 55.0}` |
| 24 | `r1_c36` | `multi_timeframe_ma_spread` | 1.4632 | 16.8870% | 20.2774% | 92 | `{"primary_ma_period": 27, "reference_ma_period": 52, "spread_threshold_bps": 75.0}` |
| 25 | `r1_c25` | `donchian_breakout` | 1.4630 | 17.7361% | 32.6243% | 136 | `{"breakout_buffer_bps": 30.0, "lookback_window": 80}` |
| 26 | `r1_c15` | `donchian_breakout` | 1.4591 | 17.6740% | 32.6243% | 137 | `{"breakout_buffer_bps": 30.0, "lookback_window": 79}` |
| 27 | `r1_c16` | `multi_timeframe_ma_spread` | 1.4092 | 15.9735% | 22.7751% | 76 | `{"primary_ma_period": 28, "reference_ma_period": 62, "spread_threshold_bps": 70.0}` |
| 28 | `r1_c17` | `multi_timeframe_ma_spread` | 1.3939 | 15.6072% | 29.0230% | 75 | `{"primary_ma_period": 27, "reference_ma_period": 75, "spread_threshold_bps": 35.0}` |
| 29 | `r1_c49` | `multi_timeframe_ma_spread` | 1.3588 | 15.1970% | 33.7113% | 69 | `{"primary_ma_period": 29, "reference_ma_period": 74, "spread_threshold_bps": 70.0}` |
| 30 | `r1_c28` | `donchian_breakout` | 1.3225 | 15.3571% | 23.2508% | 71 | `{"breakout_buffer_bps": 45.0, "lookback_window": 62}` |
| 31 | `r1_c18` | `multi_timeframe_ma_spread` | 1.2978 | 14.2972% | 23.1221% | 81 | `{"primary_ma_period": 30, "reference_ma_period": 65, "spread_threshold_bps": 45.0}` |
| 32 | `r1_c19` | `multi_timeframe_ma_spread` | 1.2762 | 14.0258% | 18.8040% | 85 | `{"primary_ma_period": 26, "reference_ma_period": 55, "spread_threshold_bps": 60.0}` |
| 33 | `r1_c22` | `donchian_breakout` | 1.2627 | 14.5118% | 27.4888% | 158 | `{"breakout_buffer_bps": 30.0, "lookback_window": 61}` |
| 34 | `r1_c42` | `donchian_breakout` | 1.1678 | 13.0063% | 25.0644% | 128 | `{"breakout_buffer_bps": 35.0, "lookback_window": 53}` |
| 35 | `r1_c20` | `donchian_breakout` | 1.1587 | 12.9038% | 22.7092% | 310 | `{"breakout_buffer_bps": 15.0, "lookback_window": 65}` |
| 36 | `r1_c38` | `multi_timeframe_ma_spread` | 1.0802 | 11.1503% | 26.2552% | 71 | `{"primary_ma_period": 35, "reference_ma_period": 63, "spread_threshold_bps": 65.0}` |
| 37 | `r1_c32` | `multi_timeframe_ma_spread` | 1.0625 | 10.8973% | 33.5233% | 78 | `{"primary_ma_period": 22, "reference_ma_period": 69, "spread_threshold_bps": 75.0}` |
| 38 | `r1_c47` | `donchian_breakout` | 1.0166 | 10.6378% | 29.1547% | 61 | `{"breakout_buffer_bps": 45.0, "lookback_window": 78}` |
| 39 | `r1_c37` | `multi_timeframe_ma_spread` | 0.6892 | 5.5911% | 30.5174% | 70 | `{"primary_ma_period": 30, "reference_ma_period": 80, "spread_threshold_bps": 25.0}` |
| 40 | `r1_c45` | `donchian_breakout` | 0.6323 | 4.9732% | 23.2508% | 72 | `{"breakout_buffer_bps": 45.0, "lookback_window": 60}` |
| 41 | `r1_c26` | `donchian_breakout` | 0.4808 | 2.8283% | 36.6469% | 41 | `{"breakout_buffer_bps": 60.0, "lookback_window": 69}` |
| 42 | `r1_c33` | `multi_timeframe_ma_spread` | 0.4003 | 1.7928% | 27.6376% | 91 | `{"primary_ma_period": 24, "reference_ma_period": 52, "spread_threshold_bps": 65.0}` |
| 43 | `r1_c21` | `donchian_breakout` | 0.0801 | -2.7167% | 32.9409% | 164 | `{"breakout_buffer_bps": 30.0, "lookback_window": 54}` |
| 44 | `r1_c41` | `donchian_breakout` | -0.0036 | -3.7596% | 41.3852% | 52 | `{"breakout_buffer_bps": 55.0, "lookback_window": 62}` |
| 45 | `r1_c27` | `donchian_breakout` | -0.1860 | -6.1177% | 36.7882% | 60 | `{"breakout_buffer_bps": 50.0, "lookback_window": 63}` |
| 46 | `r1_c43` | `donchian_breakout` | -0.8019 | -13.7228% | 47.2756% | 48 | `{"breakout_buffer_bps": 55.0, "lookback_window": 67}` |
| 47 | `r1_c48` | `donchian_breakout` | -0.8252 | -14.0248% | 39.0085% | 54 | `{"breakout_buffer_bps": 55.0, "lookback_window": 58}` |
| 48 | `r1_c40` | `donchian_breakout` | -1.4786 | -21.6234% | 37.7605% | 488 | `{"breakout_buffer_bps": 5.0, "lookback_window": 75}` |
| 49 | `r1_c35` | `donchian_breakout` | -1.4953 | -21.7582% | 39.5560% | 177 | `{"breakout_buffer_bps": 25.0, "lookback_window": 74}` |
| 50 | `r1_c23` | `donchian_breakout` | -2.0005 | -26.9954% | 43.2724% | 212 | `{"breakout_buffer_bps": 25.0, "lookback_window": 55}` |

## Round 2

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r2_c01` | `donchian_breakout` | 3.1180 | 47.6803% | 16.7789% | 117 | `{"breakout_buffer_bps": 35.0, "lookback_window": 64}` |
| 2 | `r2_c02` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 3 | `r2_c30` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 64}` |
| 4 | `r2_c03` | `donchian_breakout` | 3.0918 | 47.1767% | 18.8271% | 116 | `{"breakout_buffer_bps": 35.0, "lookback_window": 65}` |
| 5 | `r2_c04` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 67}` |
| 6 | `r2_c25` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 70}` |
| 7 | `r2_c47` | `donchian_breakout` | 2.7273 | 40.0449% | 22.4945% | 114 | `{"breakout_buffer_bps": 35.0, "lookback_window": 72}` |
| 8 | `r2_c05` | `donchian_breakout` | 2.3896 | 33.4237% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 60}` |
| 9 | `r2_c06` | `donchian_breakout` | 2.3896 | 33.4237% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 62}` |
| 10 | `r2_c07` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 70}` |
| 11 | `r2_c08` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 67}` |
| 12 | `r2_c09` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 68}` |
| 13 | `r2_c10` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 69}` |
| 14 | `r2_c41` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 66}` |
| 15 | `r2_c44` | `donchian_breakout` | 2.3820 | 33.3094% | 24.7050% | 90 | `{"breakout_buffer_bps": 40.0, "lookback_window": 72}` |
| 16 | `r2_c29` | `donchian_breakout` | 2.0400 | 27.2496% | 24.7050% | 86 | `{"breakout_buffer_bps": 40.0, "lookback_window": 78}` |
| 17 | `r2_c11` | `donchian_breakout` | 1.9445 | 25.7324% | 20.6542% | 124 | `{"breakout_buffer_bps": 35.0, "lookback_window": 60}` |
| 18 | `r2_c21` | `donchian_breakout` | 1.9079 | 25.1078% | 20.6542% | 124 | `{"breakout_buffer_bps": 35.0, "lookback_window": 59}` |
| 19 | `r2_c12` | `multi_timeframe_ma_spread` | 1.9037 | 23.5975% | 26.6440% | 75 | `{"primary_ma_period": 28, "reference_ma_period": 69, "spread_threshold_bps": 60.0}` |
| 20 | `r2_c13` | `multi_timeframe_ma_spread` | 1.8299 | 22.4958% | 23.1998% | 75 | `{"primary_ma_period": 25, "reference_ma_period": 60, "spread_threshold_bps": 80.0}` |
| 21 | `r2_c14` | `donchian_breakout` | 1.8265 | 23.7497% | 22.4945% | 112 | `{"breakout_buffer_bps": 35.0, "lookback_window": 77}` |
| 22 | `r2_c15` | `donchian_breakout` | 1.8105 | 23.3239% | 24.7050% | 89 | `{"breakout_buffer_bps": 40.0, "lookback_window": 75}` |
| 23 | `r2_c16` | `donchian_breakout` | 1.6796 | 21.2897% | 27.4253% | 147 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 24 | `r2_c17` | `multi_timeframe_ma_spread` | 1.6106 | 18.9252% | 27.7778% | 63 | `{"primary_ma_period": 34, "reference_ma_period": 79, "spread_threshold_bps": 55.0}` |
| 25 | `r2_c18` | `donchian_breakout` | 1.6073 | 19.9247% | 27.2363% | 100 | `{"breakout_buffer_bps": 40.0, "lookback_window": 53}` |
| 26 | `r2_c19` | `donchian_breakout` | 1.6073 | 19.9247% | 27.2363% | 100 | `{"breakout_buffer_bps": 40.0, "lookback_window": 51}` |
| 27 | `r2_c45` | `donchian_breakout` | 1.6073 | 19.9247% | 27.2363% | 100 | `{"breakout_buffer_bps": 40.0, "lookback_window": 50}` |
| 28 | `r2_c20` | `multi_timeframe_ma_spread` | 1.6061 | 18.9307% | 24.9083% | 71 | `{"primary_ma_period": 33, "reference_ma_period": 67, "spread_threshold_bps": 55.0}` |
| 29 | `r2_c40` | `multi_timeframe_ma_spread` | 1.4393 | 16.3766% | 28.7778% | 68 | `{"primary_ma_period": 32, "reference_ma_period": 72, "spread_threshold_bps": 50.0}` |
| 30 | `r2_c32` | `multi_timeframe_ma_spread` | 1.4047 | 15.8896% | 24.6103% | 73 | `{"primary_ma_period": 29, "reference_ma_period": 64, "spread_threshold_bps": 60.0}` |
| 31 | `r2_c23` | `donchian_breakout` | 1.3225 | 15.3571% | 23.2508% | 71 | `{"breakout_buffer_bps": 45.0, "lookback_window": 63}` |
| 32 | `r2_c46` | `donchian_breakout` | 1.1727 | 13.0811% | 25.0644% | 129 | `{"breakout_buffer_bps": 35.0, "lookback_window": 52}` |
| 33 | `r2_c50` | `donchian_breakout` | 1.0166 | 10.6378% | 29.1547% | 61 | `{"breakout_buffer_bps": 45.0, "lookback_window": 79}` |
| 34 | `r2_c37` | `multi_timeframe_ma_spread` | 0.9491 | 9.2630% | 29.3018% | 61 | `{"primary_ma_period": 37, "reference_ma_period": 81, "spread_threshold_bps": 75.0}` |
| 35 | `r2_c42` | `donchian_breakout` | 0.6323 | 4.9732% | 23.2508% | 72 | `{"breakout_buffer_bps": 45.0, "lookback_window": 61}` |
| 36 | `r2_c43` | `donchian_breakout` | 0.6323 | 4.9732% | 23.2508% | 72 | `{"breakout_buffer_bps": 45.0, "lookback_window": 60}` |
| 37 | `r2_c48` | `donchian_breakout` | 0.5944 | 4.4283% | 23.6491% | 72 | `{"breakout_buffer_bps": 45.0, "lookback_window": 57}` |
| 38 | `r2_c27` | `donchian_breakout` | 0.5920 | 4.3952% | 33.1521% | 60 | `{"breakout_buffer_bps": 45.0, "lookback_window": 80}` |
| 39 | `r2_c35` | `donchian_breakout` | 0.4784 | 2.7946% | 36.6676% | 42 | `{"breakout_buffer_bps": 60.0, "lookback_window": 65}` |
| 40 | `r2_c22` | `donchian_breakout` | 0.4070 | 1.8072% | 37.3850% | 44 | `{"breakout_buffer_bps": 60.0, "lookback_window": 58}` |
| 41 | `r2_c39` | `donchian_breakout` | 0.3941 | 1.6303% | 37.3850% | 43 | `{"breakout_buffer_bps": 60.0, "lookback_window": 61}` |
| 42 | `r2_c33` | `multi_timeframe_ma_spread` | 0.3890 | 1.6348% | 26.6057% | 107 | `{"primary_ma_period": 22, "reference_ma_period": 50, "spread_threshold_bps": 70.0}` |
| 43 | `r2_c24` | `donchian_breakout` | 0.3457 | 0.9341% | 32.5729% | 66 | `{"breakout_buffer_bps": 45.0, "lookback_window": 72}` |
| 44 | `r2_c31` | `donchian_breakout` | 0.0808 | -2.7074% | 32.9409% | 163 | `{"breakout_buffer_bps": 30.0, "lookback_window": 55}` |
| 45 | `r2_c38` | `donchian_breakout` | -0.1860 | -6.1177% | 36.7882% | 60 | `{"breakout_buffer_bps": 50.0, "lookback_window": 63}` |
| 46 | `r2_c36` | `donchian_breakout` | -0.5772 | -11.0458% | 34.3304% | 62 | `{"breakout_buffer_bps": 50.0, "lookback_window": 55}` |
| 47 | `r2_c34` | `donchian_breakout` | -0.6284 | -11.7761% | 32.3664% | 183 | `{"breakout_buffer_bps": 25.0, "lookback_window": 67}` |
| 48 | `r2_c26` | `donchian_breakout` | -0.9902 | -15.8951% | 43.1405% | 55 | `{"breakout_buffer_bps": 50.0, "lookback_window": 72}` |
| 49 | `r2_c49` | `donchian_breakout` | -0.9902 | -15.8951% | 43.1405% | 55 | `{"breakout_buffer_bps": 50.0, "lookback_window": 70}` |
| 50 | `r2_c28` | `donchian_breakout` | -1.3170 | -19.5989% | 37.6593% | 45 | `{"breakout_buffer_bps": 60.0, "lookback_window": 57}` |

## Round 3

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r3_c01` | `donchian_breakout` | 3.1180 | 47.6803% | 16.7789% | 117 | `{"breakout_buffer_bps": 35.0, "lookback_window": 64}` |
| 2 | `r3_c02` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 3 | `r3_c03` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 64}` |
| 4 | `r3_c04` | `donchian_breakout` | 3.0918 | 47.1767% | 18.8271% | 116 | `{"breakout_buffer_bps": 35.0, "lookback_window": 65}` |
| 5 | `r3_c05` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 67}` |
| 6 | `r3_c06` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 70}` |
| 7 | `r3_c22` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 68}` |
| 8 | `r3_c23` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 69}` |
| 9 | `r3_c43` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 66}` |
| 10 | `r3_c07` | `donchian_breakout` | 2.7273 | 40.0449% | 22.4945% | 114 | `{"breakout_buffer_bps": 35.0, "lookback_window": 72}` |
| 11 | `r3_c21` | `donchian_breakout` | 2.4195 | 34.1847% | 20.6542% | 119 | `{"breakout_buffer_bps": 35.0, "lookback_window": 62}` |
| 12 | `r3_c08` | `donchian_breakout` | 2.3896 | 33.4237% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 60}` |
| 13 | `r3_c09` | `donchian_breakout` | 2.3896 | 33.4237% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 62}` |
| 14 | `r3_c10` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 70}` |
| 15 | `r3_c11` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 67}` |
| 16 | `r3_c12` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 68}` |
| 17 | `r3_c13` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 69}` |
| 18 | `r3_c14` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 66}` |
| 19 | `r3_c15` | `donchian_breakout` | 2.3820 | 33.3094% | 24.7050% | 90 | `{"breakout_buffer_bps": 40.0, "lookback_window": 72}` |
| 20 | `r3_c41` | `donchian_breakout` | 2.3526 | 32.7615% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 59}` |
| 21 | `r3_c16` | `donchian_breakout` | 2.0400 | 27.2496% | 24.7050% | 86 | `{"breakout_buffer_bps": 40.0, "lookback_window": 78}` |
| 22 | `r3_c17` | `donchian_breakout` | 1.9445 | 25.7324% | 20.6542% | 124 | `{"breakout_buffer_bps": 35.0, "lookback_window": 60}` |
| 23 | `r3_c18` | `donchian_breakout` | 1.9079 | 25.1078% | 20.6542% | 124 | `{"breakout_buffer_bps": 35.0, "lookback_window": 59}` |
| 24 | `r3_c19` | `multi_timeframe_ma_spread` | 1.9037 | 23.5975% | 26.6440% | 75 | `{"primary_ma_period": 28, "reference_ma_period": 69, "spread_threshold_bps": 60.0}` |
| 25 | `r3_c20` | `multi_timeframe_ma_spread` | 1.8299 | 22.4958% | 23.1998% | 75 | `{"primary_ma_period": 25, "reference_ma_period": 60, "spread_threshold_bps": 80.0}` |
| 26 | `r3_c45` | `donchian_breakout` | 1.8265 | 23.7497% | 22.4945% | 112 | `{"breakout_buffer_bps": 35.0, "lookback_window": 77}` |
| 27 | `r3_c40` | `multi_timeframe_ma_spread` | 1.3711 | 15.3982% | 30.6722% | 79 | `{"primary_ma_period": 20, "reference_ma_period": 70, "spread_threshold_bps": 70.0}` |
| 28 | `r3_c38` | `donchian_breakout` | 1.1152 | 12.2208% | 32.6243% | 143 | `{"breakout_buffer_bps": 30.0, "lookback_window": 69}` |
| 29 | `r3_c27` | `donchian_breakout` | 1.0110 | 10.6189% | 32.6243% | 142 | `{"breakout_buffer_bps": 30.0, "lookback_window": 74}` |
| 30 | `r3_c39` | `multi_timeframe_ma_spread` | 0.7949 | 7.1223% | 32.8547% | 69 | `{"primary_ma_period": 29, "reference_ma_period": 71, "spread_threshold_bps": 65.0}` |
| 31 | `r3_c26` | `donchian_breakout` | 0.7113 | 6.1116% | 29.4020% | 69 | `{"breakout_buffer_bps": 45.0, "lookback_window": 65}` |
| 32 | `r3_c42` | `donchian_breakout` | 0.5944 | 4.4283% | 23.6491% | 72 | `{"breakout_buffer_bps": 45.0, "lookback_window": 58}` |
| 33 | `r3_c35` | `donchian_breakout` | 0.5920 | 4.3952% | 33.1521% | 60 | `{"breakout_buffer_bps": 45.0, "lookback_window": 82}` |
| 34 | `r3_c28` | `donchian_breakout` | 0.4808 | 2.8283% | 36.6469% | 41 | `{"breakout_buffer_bps": 60.0, "lookback_window": 70}` |
| 35 | `r3_c33` | `donchian_breakout` | 0.4808 | 2.8283% | 36.6469% | 41 | `{"breakout_buffer_bps": 60.0, "lookback_window": 74}` |
| 36 | `r3_c31` | `donchian_breakout` | 0.4784 | 2.7946% | 36.6676% | 42 | `{"breakout_buffer_bps": 60.0, "lookback_window": 65}` |
| 37 | `r3_c29` | `donchian_breakout` | 0.3941 | 1.6303% | 37.3850% | 43 | `{"breakout_buffer_bps": 60.0, "lookback_window": 60}` |
| 38 | `r3_c30` | `donchian_breakout` | 0.3508 | 1.0042% | 32.5729% | 67 | `{"breakout_buffer_bps": 45.0, "lookback_window": 68}` |
| 39 | `r3_c32` | `donchian_breakout` | 0.3485 | 0.9724% | 32.5941% | 68 | `{"breakout_buffer_bps": 45.0, "lookback_window": 66}` |
| 40 | `r3_c48` | `donchian_breakout` | 0.1524 | -1.7403% | 32.9503% | 167 | `{"breakout_buffer_bps": 30.0, "lookback_window": 50}` |
| 41 | `r3_c34` | `donchian_breakout` | 0.0808 | -2.7074% | 32.9409% | 163 | `{"breakout_buffer_bps": 30.0, "lookback_window": 56}` |
| 42 | `r3_c44` | `donchian_breakout` | 0.0808 | -2.7074% | 32.9409% | 163 | `{"breakout_buffer_bps": 30.0, "lookback_window": 55}` |
| 43 | `r3_c49` | `donchian_breakout` | 0.0808 | -2.7074% | 32.9409% | 163 | `{"breakout_buffer_bps": 30.0, "lookback_window": 57}` |
| 44 | `r3_c47` | `donchian_breakout` | -0.0687 | -4.6153% | 41.7100% | 47 | `{"breakout_buffer_bps": 55.0, "lookback_window": 77}` |
| 45 | `r3_c46` | `donchian_breakout` | -0.4423 | -9.3601% | 44.7961% | 50 | `{"breakout_buffer_bps": 55.0, "lookback_window": 65}` |
| 46 | `r3_c50` | `donchian_breakout` | -0.6251 | -11.5809% | 40.4666% | 58 | `{"breakout_buffer_bps": 50.0, "lookback_window": 65}` |
| 47 | `r3_c36` | `donchian_breakout` | -0.6782 | -12.2258% | 40.6599% | 54 | `{"breakout_buffer_bps": 50.0, "lookback_window": 80}` |
| 48 | `r3_c37` | `donchian_breakout` | -0.8252 | -14.0248% | 39.0085% | 54 | `{"breakout_buffer_bps": 55.0, "lookback_window": 58}` |
| 49 | `r3_c25` | `donchian_breakout` | -0.9321 | -15.2569% | 48.2131% | 48 | `{"breakout_buffer_bps": 55.0, "lookback_window": 72}` |
| 50 | `r3_c24` | `donchian_breakout` | -1.2021 | -18.4875% | 38.7838% | 206 | `{"breakout_buffer_bps": 25.0, "lookback_window": 60}` |

## Round 4

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r4_c01` | `donchian_breakout` | 3.1180 | 47.6803% | 16.7789% | 117 | `{"breakout_buffer_bps": 35.0, "lookback_window": 64}` |
| 2 | `r4_c02` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 3 | `r4_c03` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 64}` |
| 4 | `r4_c04` | `donchian_breakout` | 3.0918 | 47.1767% | 18.8271% | 116 | `{"breakout_buffer_bps": 35.0, "lookback_window": 65}` |
| 5 | `r4_c47` | `donchian_breakout` | 2.7700 | 40.8034% | 20.6542% | 118 | `{"breakout_buffer_bps": 35.0, "lookback_window": 63}` |
| 6 | `r4_c05` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 67}` |
| 7 | `r4_c06` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 70}` |
| 8 | `r4_c07` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 68}` |
| 9 | `r4_c08` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 69}` |
| 10 | `r4_c09` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 66}` |
| 11 | `r4_c10` | `donchian_breakout` | 2.7273 | 40.0449% | 22.4945% | 114 | `{"breakout_buffer_bps": 35.0, "lookback_window": 72}` |
| 12 | `r4_c49` | `donchian_breakout` | 2.7273 | 40.0449% | 22.4945% | 114 | `{"breakout_buffer_bps": 35.0, "lookback_window": 71}` |
| 13 | `r4_c11` | `donchian_breakout` | 2.4195 | 34.1847% | 20.6542% | 119 | `{"breakout_buffer_bps": 35.0, "lookback_window": 62}` |
| 14 | `r4_c12` | `donchian_breakout` | 2.3896 | 33.4237% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 60}` |
| 15 | `r4_c13` | `donchian_breakout` | 2.3896 | 33.4237% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 62}` |
| 16 | `r4_c14` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 70}` |
| 17 | `r4_c15` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 67}` |
| 18 | `r4_c16` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 68}` |
| 19 | `r4_c17` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 69}` |
| 20 | `r4_c18` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 66}` |
| 21 | `r4_c19` | `donchian_breakout` | 2.3820 | 33.3094% | 24.7050% | 90 | `{"breakout_buffer_bps": 40.0, "lookback_window": 72}` |
| 22 | `r4_c20` | `donchian_breakout` | 2.3526 | 32.7615% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 59}` |
| 23 | `r4_c39` | `donchian_breakout` | 2.0541 | 27.6852% | 22.4945% | 107 | `{"breakout_buffer_bps": 35.0, "lookback_window": 82}` |
| 24 | `r4_c34` | `donchian_breakout` | 2.0372 | 27.1985% | 24.7050% | 85 | `{"breakout_buffer_bps": 40.0, "lookback_window": 80}` |
| 25 | `r4_c43` | `donchian_breakout` | 1.8265 | 23.7497% | 22.4945% | 112 | `{"breakout_buffer_bps": 35.0, "lookback_window": 74}` |
| 26 | `r4_c41` | `donchian_breakout` | 1.8105 | 23.3239% | 24.7050% | 89 | `{"breakout_buffer_bps": 40.0, "lookback_window": 74}` |
| 27 | `r4_c22` | `donchian_breakout` | 1.6796 | 21.2897% | 27.4253% | 147 | `{"breakout_buffer_bps": 30.0, "lookback_window": 65}` |
| 28 | `r4_c33` | `donchian_breakout` | 1.5821 | 19.6733% | 28.1500% | 145 | `{"breakout_buffer_bps": 30.0, "lookback_window": 67}` |
| 29 | `r4_c36` | `donchian_breakout` | 1.5821 | 19.6733% | 28.1500% | 145 | `{"breakout_buffer_bps": 30.0, "lookback_window": 66}` |
| 30 | `r4_c50` | `donchian_breakout` | 1.4628 | 17.7326% | 32.6243% | 135 | `{"breakout_buffer_bps": 30.0, "lookback_window": 82}` |
| 31 | `r4_c37` | `donchian_breakout` | 1.1147 | 12.2137% | 32.6243% | 142 | `{"breakout_buffer_bps": 30.0, "lookback_window": 71}` |
| 32 | `r4_c35` | `donchian_breakout` | 0.7875 | 7.2246% | 29.1547% | 63 | `{"breakout_buffer_bps": 45.0, "lookback_window": 77}` |
| 33 | `r4_c46` | `donchian_breakout` | 0.7113 | 6.1116% | 29.4020% | 69 | `{"breakout_buffer_bps": 45.0, "lookback_window": 65}` |
| 34 | `r4_c29` | `donchian_breakout` | 0.6323 | 4.9732% | 23.2508% | 72 | `{"breakout_buffer_bps": 45.0, "lookback_window": 61}` |
| 35 | `r4_c44` | `donchian_breakout` | 0.6323 | 4.9732% | 23.2508% | 72 | `{"breakout_buffer_bps": 45.0, "lookback_window": 60}` |
| 36 | `r4_c42` | `donchian_breakout` | 0.5345 | 3.5766% | 24.2719% | 75 | `{"breakout_buffer_bps": 45.0, "lookback_window": 53}` |
| 37 | `r4_c38` | `donchian_breakout` | 0.4808 | 2.8283% | 36.6469% | 41 | `{"breakout_buffer_bps": 60.0, "lookback_window": 71}` |
| 38 | `r4_c40` | `donchian_breakout` | 0.4784 | 2.7946% | 36.6676% | 42 | `{"breakout_buffer_bps": 60.0, "lookback_window": 64}` |
| 39 | `r4_c24` | `donchian_breakout` | 0.3457 | 0.9341% | 32.5729% | 66 | `{"breakout_buffer_bps": 45.0, "lookback_window": 70}` |
| 40 | `r4_c31` | `donchian_breakout` | 0.3457 | 0.9341% | 32.5729% | 66 | `{"breakout_buffer_bps": 45.0, "lookback_window": 72}` |
| 41 | `r4_c45` | `donchian_breakout` | -0.4752 | -9.8879% | 32.3227% | 200 | `{"breakout_buffer_bps": 25.0, "lookback_window": 62}` |
| 42 | `r4_c23` | `donchian_breakout` | -0.5664 | -10.9031% | 34.2250% | 61 | `{"breakout_buffer_bps": 50.0, "lookback_window": 59}` |
| 43 | `r4_c32` | `donchian_breakout` | -0.5772 | -11.0458% | 34.3304% | 62 | `{"breakout_buffer_bps": 50.0, "lookback_window": 55}` |
| 44 | `r4_c30` | `donchian_breakout` | -0.8019 | -13.7228% | 47.2756% | 48 | `{"breakout_buffer_bps": 55.0, "lookback_window": 67}` |
| 45 | `r4_c25` | `donchian_breakout` | -0.8681 | -14.6333% | 34.5461% | 192 | `{"breakout_buffer_bps": 25.0, "lookback_window": 65}` |
| 46 | `r4_c21` | `donchian_breakout` | -0.9321 | -15.2569% | 48.2131% | 48 | `{"breakout_buffer_bps": 55.0, "lookback_window": 74}` |
| 47 | `r4_c26` | `donchian_breakout` | -1.0176 | -16.4136% | 35.4271% | 170 | `{"breakout_buffer_bps": 25.0, "lookback_window": 80}` |
| 48 | `r4_c27` | `donchian_breakout` | -1.2985 | -19.6005% | 37.8891% | 178 | `{"breakout_buffer_bps": 25.0, "lookback_window": 73}` |
| 49 | `r4_c28` | `donchian_breakout` | -1.4953 | -21.7582% | 39.5560% | 177 | `{"breakout_buffer_bps": 25.0, "lookback_window": 74}` |
| 50 | `r4_c48` | `donchian_breakout` | -1.5527 | -22.3432% | 41.6795% | 209 | `{"breakout_buffer_bps": 25.0, "lookback_window": 59}` |

## Round 5

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r5_c01` | `donchian_breakout` | 3.1180 | 47.6803% | 16.7789% | 117 | `{"breakout_buffer_bps": 35.0, "lookback_window": 64}` |
| 2 | `r5_c02` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 63}` |
| 3 | `r5_c03` | `donchian_breakout` | 3.0925 | 46.8427% | 19.1910% | 94 | `{"breakout_buffer_bps": 40.0, "lookback_window": 64}` |
| 4 | `r5_c04` | `donchian_breakout` | 3.0918 | 47.1767% | 18.8271% | 116 | `{"breakout_buffer_bps": 35.0, "lookback_window": 65}` |
| 5 | `r5_c05` | `donchian_breakout` | 2.7700 | 40.8034% | 20.6542% | 118 | `{"breakout_buffer_bps": 35.0, "lookback_window": 63}` |
| 6 | `r5_c42` | `donchian_breakout` | 2.7491 | 40.1035% | 21.1393% | 92 | `{"breakout_buffer_bps": 40.0, "lookback_window": 65}` |
| 7 | `r5_c06` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 67}` |
| 8 | `r5_c07` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 70}` |
| 9 | `r5_c08` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 68}` |
| 10 | `r5_c09` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 69}` |
| 11 | `r5_c10` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 66}` |
| 12 | `r5_c11` | `donchian_breakout` | 2.7273 | 40.0449% | 22.4945% | 114 | `{"breakout_buffer_bps": 35.0, "lookback_window": 72}` |
| 13 | `r5_c12` | `donchian_breakout` | 2.7273 | 40.0449% | 22.4945% | 114 | `{"breakout_buffer_bps": 35.0, "lookback_window": 71}` |
| 14 | `r5_c13` | `donchian_breakout` | 2.4195 | 34.1847% | 20.6542% | 119 | `{"breakout_buffer_bps": 35.0, "lookback_window": 62}` |
| 15 | `r5_c14` | `donchian_breakout` | 2.3896 | 33.4237% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 60}` |
| 16 | `r5_c15` | `donchian_breakout` | 2.3896 | 33.4237% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 62}` |
| 17 | `r5_c32` | `donchian_breakout` | 2.3896 | 33.4237% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 61}` |
| 18 | `r5_c16` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 70}` |
| 19 | `r5_c17` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 67}` |
| 20 | `r5_c18` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 68}` |
| 21 | `r5_c19` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 69}` |
| 22 | `r5_c20` | `donchian_breakout` | 2.3825 | 33.3179% | 24.7050% | 91 | `{"breakout_buffer_bps": 40.0, "lookback_window": 66}` |
| 23 | `r5_c39` | `donchian_breakout` | 2.3526 | 32.7615% | 22.9539% | 96 | `{"breakout_buffer_bps": 40.0, "lookback_window": 59}` |
| 24 | `r5_c29` | `donchian_breakout` | 2.0543 | 27.6889% | 22.4945% | 108 | `{"breakout_buffer_bps": 35.0, "lookback_window": 79}` |
| 25 | `r5_c49` | `donchian_breakout` | 1.8265 | 23.7497% | 22.4945% | 112 | `{"breakout_buffer_bps": 35.0, "lookback_window": 74}` |
| 26 | `r5_c31` | `donchian_breakout` | 1.8105 | 23.3239% | 24.7050% | 89 | `{"breakout_buffer_bps": 40.0, "lookback_window": 77}` |
| 27 | `r5_c30` | `donchian_breakout` | 1.7996 | 23.2431% | 20.6542% | 121 | `{"breakout_buffer_bps": 35.0, "lookback_window": 61}` |
| 28 | `r5_c40` | `donchian_breakout` | 1.6073 | 19.9247% | 27.2363% | 100 | `{"breakout_buffer_bps": 40.0, "lookback_window": 56}` |
| 29 | `r5_c45` | `donchian_breakout` | 1.6073 | 19.9247% | 27.2363% | 100 | `{"breakout_buffer_bps": 40.0, "lookback_window": 53}` |
| 30 | `r5_c43` | `donchian_breakout` | 1.5821 | 19.6733% | 28.1500% | 145 | `{"breakout_buffer_bps": 30.0, "lookback_window": 66}` |
| 31 | `r5_c38` | `donchian_breakout` | 1.4591 | 17.6740% | 32.6243% | 137 | `{"breakout_buffer_bps": 30.0, "lookback_window": 78}` |
| 32 | `r5_c26` | `donchian_breakout` | 1.3768 | 16.3265% | 29.0747% | 152 | `{"breakout_buffer_bps": 30.0, "lookback_window": 62}` |
| 33 | `r5_c37` | `donchian_breakout` | 1.3225 | 15.3571% | 23.2508% | 71 | `{"breakout_buffer_bps": 45.0, "lookback_window": 62}` |
| 34 | `r5_c48` | `donchian_breakout` | 1.3225 | 15.3571% | 23.2508% | 71 | `{"breakout_buffer_bps": 45.0, "lookback_window": 63}` |
| 35 | `r5_c22` | `donchian_breakout` | 1.2627 | 14.5118% | 27.4888% | 158 | `{"breakout_buffer_bps": 30.0, "lookback_window": 61}` |
| 36 | `r5_c33` | `donchian_breakout` | 1.1727 | 13.0811% | 25.0644% | 129 | `{"breakout_buffer_bps": 35.0, "lookback_window": 52}` |
| 37 | `r5_c24` | `donchian_breakout` | 1.1678 | 13.0063% | 25.0644% | 128 | `{"breakout_buffer_bps": 35.0, "lookback_window": 55}` |
| 38 | `r5_c41` | `donchian_breakout` | 1.1678 | 13.0063% | 25.0644% | 128 | `{"breakout_buffer_bps": 35.0, "lookback_window": 54}` |
| 39 | `r5_c27` | `donchian_breakout` | 1.1147 | 12.2137% | 32.6243% | 142 | `{"breakout_buffer_bps": 30.0, "lookback_window": 72}` |
| 40 | `r5_c23` | `donchian_breakout` | 0.5345 | 3.5766% | 24.2719% | 75 | `{"breakout_buffer_bps": 45.0, "lookback_window": 54}` |
| 41 | `r5_c34` | `donchian_breakout` | 0.4808 | 2.8283% | 36.6469% | 41 | `{"breakout_buffer_bps": 60.0, "lookback_window": 70}` |
| 42 | `r5_c36` | `donchian_breakout` | 0.4808 | 2.8283% | 36.6469% | 41 | `{"breakout_buffer_bps": 60.0, "lookback_window": 75}` |
| 43 | `r5_c50` | `donchian_breakout` | 0.3508 | 1.0042% | 32.5729% | 67 | `{"breakout_buffer_bps": 45.0, "lookback_window": 68}` |
| 44 | `r5_c21` | `donchian_breakout` | -0.0036 | -3.7596% | 41.3852% | 52 | `{"breakout_buffer_bps": 55.0, "lookback_window": 62}` |
| 45 | `r5_c35` | `donchian_breakout` | -0.5664 | -10.9031% | 34.2250% | 61 | `{"breakout_buffer_bps": 50.0, "lookback_window": 57}` |
| 46 | `r5_c25` | `donchian_breakout` | -0.9321 | -15.2569% | 48.2131% | 48 | `{"breakout_buffer_bps": 55.0, "lookback_window": 73}` |
| 47 | `r5_c46` | `donchian_breakout` | -0.9321 | -15.2569% | 48.2131% | 48 | `{"breakout_buffer_bps": 55.0, "lookback_window": 69}` |
| 48 | `r5_c47` | `donchian_breakout` | -0.9321 | -15.2569% | 48.2131% | 48 | `{"breakout_buffer_bps": 55.0, "lookback_window": 72}` |
| 49 | `r5_c44` | `donchian_breakout` | -1.1193 | -17.4312% | 41.3852% | 53 | `{"breakout_buffer_bps": 55.0, "lookback_window": 60}` |
| 50 | `r5_c28` | `donchian_breakout` | -1.5527 | -22.3432% | 41.6795% | 209 | `{"breakout_buffer_bps": 25.0, "lookback_window": 58}` |
