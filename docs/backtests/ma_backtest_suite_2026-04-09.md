# MA 策略回測報告

日期：2026-04-09

## 回測目的

基於目前 `standard_bot` 的 MA 類策略，先做一組可直接比較的基線回測，確認：

- `moving_average_cross` 是否優於較簡單的 `price_moving_average`
- 同一組參數在 `BTCUSDT / ETHUSDT / SOLUSDT` 上的表現差異
- 現階段是否已適合直接進入 demo 或需要先調參

## 回測設定

- 資料來源：Binance Futures REST Kline
- 週期：`1h`
- 樣本數：最近 `500` 根 K 線
- 初始資金：`10000`
- 手續費：`10 bps`
- 滑點：`0 bps`

### 策略 A：`moving_average_cross`

- `fast_window=5`
- `slow_window=20`

### 策略 B：`price_moving_average`

- `ma_period=5`

## 結果總表

| 標的 | 策略 | 總報酬 | 最終資金 | 交易筆數 | 結論 |
| --- | --- | ---: | ---: | ---: | --- |
| BTCUSDT | moving_average_cross | -4.12% | 9588.20 | 34 | 虧損，但明顯優於單價 MA |
| ETHUSDT | moving_average_cross | -0.13% | 9986.59 | 28 | 本輪最佳，接近打平 |
| SOLUSDT | moving_average_cross | -10.07% | 8992.64 | 28 | 表現偏弱 |
| BTCUSDT | price_moving_average | -9.97% | 9003.31 | 126 | 過度交易，費用拖累明顯 |
| ETHUSDT | price_moving_average | -8.63% | 9137.27 | 126 | 較差 |
| SOLUSDT | price_moving_average | -14.50% | 8550.10 | 124 | 本輪最差 |

## 觀察

1. 目前這組參數下，`moving_average_cross` 全面優於 `price_moving_average`。
2. `price_moving_average` 的交易筆數約為 `124-126` 筆，遠高於 `moving_average_cross` 的 `28-34` 筆，在 `10 bps` 手續費下容易被磨損。
3. `ETHUSDT + moving_average_cross(5,20)` 是本輪最接近可用的組合，500 根 `1h` K 線下僅約 `-0.13%`。
4. 以目前結果來看，若要做 demo，建議優先使用 `moving_average_cross`，不要直接用 `price_moving_average` 當主策略。

## 建議下一步

1. 先對 `moving_average_cross` 做一輪參數掃描，例如 `(3,10) / (5,20) / (8,21) / (10,30)`。
2. 補上 `slippage_bps` 測試，避免 demo 成績與實際執行落差過大。
3. 若要挑單一 demo 標的，現階段建議先用 `ETHUSDT`。

## 原始輸出

- `BTCUSDT moving_average_cross`：`docs/backtests/btc_ma_cross_1h_500.json`
- `ETHUSDT moving_average_cross`：`docs/backtests/eth_ma_cross_1h_500.json`
- `SOLUSDT moving_average_cross`：`docs/backtests/sol_ma_cross_1h_500.json`
- `BTCUSDT price_moving_average`：`docs/backtests/btc_price_ma_1h_500.json`
- `ETHUSDT price_moving_average`：`docs/backtests/eth_price_ma_1h_500.json`
- `SOLUSDT price_moving_average`：`docs/backtests/sol_price_ma_1h_500.json`
