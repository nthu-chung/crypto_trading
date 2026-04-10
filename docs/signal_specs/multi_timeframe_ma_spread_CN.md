# 多週期 MA 訊號規格

## 原始自然語言

```text
5分鐘MA 上漲超過 1hr MA做多
反之5min MA下跌超過 1hr MA做空
```

## 為什麼不能直接拿去跑

這段話還缺少幾個會直接影響結果的欄位：

- `instrument_id`：例如 `BTCUSDT`
- `primary_timeframe`：這裡是 `5m`
- `reference_timeframe`：這裡是 `1h`
- `primary_ma_period`：5 分鐘 MA 用幾根 bar
- `reference_ma_period`：1 小時 MA 用幾根 bar
- `spread_threshold_bps`：高於 / 低於多少才算有效訊號
- `decision_clock`：在哪個週期的收盤點決策
- `execution_model`：訊號後用什麼價格成交
- `positioning_mode`：`long_short` 或 `long_flat`

## 標準化後的策略規格

下面是目前專案可直接執行的標準化版本：

```yaml
plugin_id: multi_timeframe_ma_spread
instrument_id: BTCUSDT
primary_timeframe: 5m
reference_timeframe: 1h
primary_ma_period: 20
reference_ma_period: 20
spread_threshold_bps: 0
decision_clock: 5m_bar_close
positioning_mode: long_short
execution_model: next_primary_bar_open
```

## 訊號語義

定義：

- `primary_ma(t)` = 在 `decision_as_of=t` 當下可見的 `5m` 已收盤 bar 上計算的 SMA
- `reference_ma(t)` = 在 `decision_as_of=t` 當下可見的 `1h` 已收盤 bar 上計算的 SMA
- `spread_bps(t) = (primary_ma(t) - reference_ma(t)) / reference_ma(t) * 10000`

決策：

- 若 `spread_bps(t) > spread_threshold_bps`，輸出 `BUY`
- 若 `spread_bps(t) < -spread_threshold_bps`，輸出 `SELL`
- 否則不輸出新訊號

## Point-in-Time 規範

這個策略在目前架構下遵守以下 PIT 規則：

- 每個 `5m` 決策點只使用 `decision_as_of` 當下已收盤的 `5m` 與 `1h` bar
- 若 `1h` bar 尚未收盤，則不能進入該次計算
- `Signal batch` 與 `Signal step` 使用同一套 `Numba` kernel
- 回測成交假設為：
  - 訊號在 `5m` bar close 產生
  - 在下一根 `5m` bar open 成交

## 對應到目前程式碼

- Signal plugin：`cyqnt_trd/standard_bot/signal/plugins.py`
- Signal kernel：`cyqnt_trd/standard_bot/signal/numba_kernels.py`
- Signal encoder：`cyqnt_trd/standard_bot/signal/encoders.py`
- Backtest runner：`cyqnt_trd/standard_bot/simulation/numba_runner.py`
- Execution kernel：`cyqnt_trd/standard_bot/simulation/execution_kernels.py`
