# LLM Strategy Evolution

- Symbol: `BTCUSDT`
- Primary timeframe: `5m`
- Secondary timeframe: `1h`
- Rounds: `5`
- Best strategy: `donchian_breakout`
- Best Sharpe: `2.7277`
- Best total return: `40.0539%`
- Best max drawdown: `22.4945%`
- Best trade count: `115`

## Round 1

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r1_c08` | `multi_timeframe_ma_spread` | -0.0417 | -3.8387% | 30.9595% | 123 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 2 | `r1_c10` | `donchian_breakout` | -1.3352 | -20.0218% | 39.1946% | 437 | `{"breakout_buffer_bps": 10.0, "lookback_window": 55}` |
| 3 | `r1_c07` | `multi_timeframe_ma_spread` | -3.8423 | -42.0567% | 43.9621% | 310 | `{"primary_ma_period": 10, "reference_ma_period": 20, "spread_threshold_bps": 0.0}` |
| 4 | `r1_c03` | `moving_average_cross` | -3.9960 | -31.3292% | 34.6263% | 753 | `{"entry_threshold": 0.001, "fast_window": 20, "slow_window": 80}` |
| 5 | `r1_c05` | `rsi_reversion` | -5.2653 | -42.7433% | 44.6432% | 1370 | `{"overbought": 70.0, "oversold": 30.0, "period": 14}` |
| 6 | `r1_c02` | `moving_average_cross` | -7.7814 | -52.1019% | 54.4377% | 1586 | `{"entry_threshold": 0.0005, "fast_window": 10, "slow_window": 40}` |
| 7 | `r1_c09` | `donchian_breakout` | -9.9333 | -75.9341% | 76.1440% | 1673 | `{"breakout_buffer_bps": 0.0, "lookback_window": 20}` |
| 8 | `r1_c04` | `rsi_reversion` | -13.9050 | -75.7535% | 75.8976% | 2702 | `{"overbought": 75.0, "oversold": 25.0, "period": 7}` |
| 9 | `r1_c01` | `moving_average_cross` | -17.2705 | -81.1635% | 81.2774% | 3906 | `{"entry_threshold": 0.0, "fast_window": 5, "slow_window": 20}` |
| 10 | `r1_c06` | `price_moving_average` | -18.9099 | -85.1021% | 85.6326% | 2085 | `{"entry_threshold": 0.0005, "period": 10}` |

## Round 2

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r2_c06` | `donchian_breakout` | 0.6506 | 5.2527% | 27.5863% | 331 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 2 | `r2_c01` | `multi_timeframe_ma_spread` | -0.0417 | -3.8387% | 30.9595% | 123 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 3 | `r2_c05` | `multi_timeframe_ma_spread` | -0.9398 | -14.3753% | 39.7605% | 94 | `{"primary_ma_period": 19, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 4 | `r2_c02` | `donchian_breakout` | -1.3352 | -20.0218% | 39.1946% | 437 | `{"breakout_buffer_bps": 10.0, "lookback_window": 55}` |
| 5 | `r2_c09` | `multi_timeframe_ma_spread` | -1.4534 | -19.8339% | 37.5562% | 137 | `{"primary_ma_period": 15, "reference_ma_period": 52, "spread_threshold_bps": 10.0}` |
| 6 | `r2_c07` | `multi_timeframe_ma_spread` | -3.0061 | -34.8653% | 43.5932% | 276 | `{"primary_ma_period": 9, "reference_ma_period": 25, "spread_threshold_bps": 0.0}` |
| 7 | `r2_c03` | `multi_timeframe_ma_spread` | -3.8423 | -42.0567% | 43.9621% | 310 | `{"primary_ma_period": 10, "reference_ma_period": 20, "spread_threshold_bps": 0.0}` |
| 8 | `r2_c04` | `moving_average_cross` | -3.9960 | -31.3292% | 34.6263% | 753 | `{"entry_threshold": 0.001, "fast_window": 20, "slow_window": 80}` |
| 9 | `r2_c08` | `moving_average_cross` | -4.1719 | -31.6867% | 34.0512% | 627 | `{"entry_threshold": 0.0015, "fast_window": 22, "slow_window": 85}` |
| 10 | `r2_c10` | `donchian_breakout` | -6.4260 | -60.5432% | 61.6419% | 824 | `{"breakout_buffer_bps": 0.0, "lookback_window": 53}` |

## Round 3

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r3_c01` | `donchian_breakout` | 0.6506 | 5.2527% | 27.5863% | 331 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 2 | `r3_c02` | `multi_timeframe_ma_spread` | -0.0417 | -3.8387% | 30.9595% | 123 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 3 | `r3_c07` | `multi_timeframe_ma_spread` | -0.7416 | -12.1633% | 37.9806% | 99 | `{"primary_ma_period": 22, "reference_ma_period": 58, "spread_threshold_bps": 35.0}` |
| 4 | `r3_c03` | `multi_timeframe_ma_spread` | -0.9398 | -14.3753% | 39.7605% | 94 | `{"primary_ma_period": 19, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 5 | `r3_c06` | `multi_timeframe_ma_spread` | -1.0600 | -15.6857% | 37.7043% | 110 | `{"primary_ma_period": 21, "reference_ma_period": 55, "spread_threshold_bps": 25.0}` |
| 6 | `r3_c04` | `donchian_breakout` | -1.3352 | -20.0218% | 39.1946% | 437 | `{"breakout_buffer_bps": 10.0, "lookback_window": 55}` |
| 7 | `r3_c08` | `donchian_breakout` | -1.7072 | -24.0171% | 42.9354% | 261 | `{"breakout_buffer_bps": 20.0, "lookback_window": 57}` |
| 8 | `r3_c05` | `donchian_breakout` | -1.8384 | -25.3395% | 42.0503% | 218 | `{"breakout_buffer_bps": 25.0, "lookback_window": 52}` |
| 9 | `r3_c10` | `multi_timeframe_ma_spread` | -2.5261 | -30.5425% | 41.3522% | 171 | `{"primary_ma_period": 15, "reference_ma_period": 40, "spread_threshold_bps": 15.0}` |
| 10 | `r3_c09` | `donchian_breakout` | -3.1515 | -37.7949% | 46.2104% | 487 | `{"breakout_buffer_bps": 10.0, "lookback_window": 47}` |

## Round 4

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r4_c05` | `donchian_breakout` | 2.4195 | 34.1847% | 20.6542% | 119 | `{"breakout_buffer_bps": 35.0, "lookback_window": 62}` |
| 2 | `r4_c09` | `donchian_breakout` | 1.9137 | 25.3092% | 18.1406% | 317 | `{"breakout_buffer_bps": 15.0, "lookback_window": 62}` |
| 3 | `r4_c01` | `donchian_breakout` | 0.6506 | 5.2527% | 27.5863% | 331 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 4 | `r4_c02` | `multi_timeframe_ma_spread` | -0.0417 | -3.8387% | 30.9595% | 123 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 5 | `r4_c07` | `multi_timeframe_ma_spread` | -0.5935 | -10.4421% | 36.9657% | 103 | `{"primary_ma_period": 19, "reference_ma_period": 63, "spread_threshold_bps": 40.0}` |
| 6 | `r4_c03` | `multi_timeframe_ma_spread` | -0.7416 | -12.1633% | 37.9806% | 99 | `{"primary_ma_period": 22, "reference_ma_period": 58, "spread_threshold_bps": 35.0}` |
| 7 | `r4_c08` | `multi_timeframe_ma_spread` | -0.7654 | -12.3849% | 37.5813% | 102 | `{"primary_ma_period": 20, "reference_ma_period": 65, "spread_threshold_bps": 35.0}` |
| 8 | `r4_c04` | `multi_timeframe_ma_spread` | -0.9398 | -14.3753% | 39.7605% | 94 | `{"primary_ma_period": 19, "reference_ma_period": 60, "spread_threshold_bps": 40.0}` |
| 9 | `r4_c10` | `multi_timeframe_ma_spread` | -1.6259 | -21.6226% | 38.0904% | 120 | `{"primary_ma_period": 19, "reference_ma_period": 55, "spread_threshold_bps": 15.0}` |
| 10 | `r4_c06` | `multi_timeframe_ma_spread` | -1.8233 | -23.6239% | 39.3816% | 123 | `{"primary_ma_period": 23, "reference_ma_period": 45, "spread_threshold_bps": 10.0}` |

## Round 5

| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `r5_c06` | `donchian_breakout` | 2.7277 | 40.0539% | 22.4945% | 115 | `{"breakout_buffer_bps": 35.0, "lookback_window": 67}` |
| 2 | `r5_c01` | `donchian_breakout` | 2.4195 | 34.1847% | 20.6542% | 119 | `{"breakout_buffer_bps": 35.0, "lookback_window": 62}` |
| 3 | `r5_c09` | `donchian_breakout` | 1.9245 | 25.4449% | 25.6107% | 148 | `{"breakout_buffer_bps": 30.0, "lookback_window": 64}` |
| 4 | `r5_c02` | `donchian_breakout` | 1.9137 | 25.3092% | 18.1406% | 317 | `{"breakout_buffer_bps": 15.0, "lookback_window": 62}` |
| 5 | `r5_c03` | `donchian_breakout` | 0.6506 | 5.2527% | 27.5863% | 331 | `{"breakout_buffer_bps": 15.0, "lookback_window": 57}` |
| 6 | `r5_c04` | `multi_timeframe_ma_spread` | -0.0417 | -3.8387% | 30.9595% | 123 | `{"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}` |
| 7 | `r5_c07` | `donchian_breakout` | -0.4195 | -9.2197% | 30.4308% | 410 | `{"breakout_buffer_bps": 10.0, "lookback_window": 62}` |
| 8 | `r5_c05` | `donchian_breakout` | -0.8019 | -13.7228% | 47.2756% | 48 | `{"breakout_buffer_bps": 55.0, "lookback_window": 67}` |
| 9 | `r5_c10` | `donchian_breakout` | -1.5151 | -21.9880% | 39.5833% | 434 | `{"breakout_buffer_bps": 10.0, "lookback_window": 57}` |
| 10 | `r5_c08` | `multi_timeframe_ma_spread` | -1.6051 | -21.3474% | 38.9847% | 118 | `{"primary_ma_period": 19, "reference_ma_period": 55, "spread_threshold_bps": 10.0}` |
