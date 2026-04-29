# cyqnt-trd 0.1.9.dev0 使用教學

這篇教學說明如何使用 `cyqnt-trd==0.1.9.dev0` 的 `standard_bot` 主線完成：

- 安裝套件
- 下載 Binance K bar 到本地 parquet
- 使用 `NumbaBacktestRunner` 回測
- 產生 paper signal
- 啟動 paper monitor
- 讓 OpenClaw 依照固定流程使用

> 本文以 PyPI 上的 `cyqnt-trd==0.1.9.dev0` 為準。GitHub `main` 可能已包含更多新策略或研究工具；若需要修改程式碼或使用尚未發布到 PyPI 的功能，再 clone source repo。

## 1. 核心概念

`cyqnt-trd` 目前推薦使用 `standard_bot` 主線。

標準資料與回測流程是：

```text
Binance API
-> local 1m parquet
-> local resample
-> standard_bot signal
-> NumbaBacktestRunner
-> JSON result
```

重要原則：

- 回測不要直接用 Binance API 即時回傳結果當最終輸入。
- 先把 K bar 下載成 local parquet。
- 高週期資料優先由本地 `1m` parquet 重採樣。
- 回測優先使用 `--engine numba`。
- 不要預設使用 legacy `cyqnt_trd/backtesting/*` 或 `strategy_backtest.py`。

## 2. 安裝

建議建立乾淨環境：

```bash
python3 -m venv .venv-standard-bot
source .venv-standard-bot/bin/activate
python -m pip install -U pip
python -m pip install cyqnt-trd==0.1.9.dev0
```

確認可以 import：

```bash
python - <<'PY'
import cyqnt_trd
from cyqnt_trd.standard_bot.simulation.numba_runner import NumbaBacktestRunner

print("cyqnt_trd version:", getattr(cyqnt_trd, "__version__", "unknown"))
print("runner:", NumbaBacktestRunner.__name__)
PY
```

## 3. 準備時間區間

`standard_bot` 的歷史下載需要毫秒 timestamp。

例如要抓最近 90 天：

```bash
python - <<'PY'
from datetime import datetime, timedelta, timezone

end = datetime.now(timezone.utc)
start = end - timedelta(days=90)

print("START_TS=", int(start.timestamp() * 1000))
print("END_TS=", int(end.timestamp() * 1000))
print("START_UTC=", start.isoformat())
print("END_UTC=", end.isoformat())
PY
```

把輸出的 `START_TS` 與 `END_TS` 帶進後面的命令。

## 4. 下載資料並回測

以下範例會：

- 使用 Binance futures K bar
- 若本地資料不存在，就自動下載
- 儲存到 `data/mtf_90d`
- 回測 `BTCUSDT`
- 使用 `multi_timeframe_ma_spread`
- 輸出 JSON 到 `docs/backtests/`

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest \
  --engine numba \
  --market-type futures \
  --strategy multi_timeframe_ma_spread \
  --symbol BTCUSDT \
  --interval 5m \
  --secondary-interval 1h \
  --primary-ma-period 20 \
  --reference-ma-period 20 \
  --spread-threshold-bps 0 \
  --historical-dir data/mtf_90d \
  --start-ts <START_TS> \
  --end-ts <END_TS> \
  --download-missing \
  --output-json docs/backtests/btc_mtf_ma_spread_90d.json
```

若只想先快速測試，也可以用較短時間窗。

## 5. 常用策略

`0.1.9.dev0` 主線建議先使用這些策略：

| Strategy | 用途 |
| --- | --- |
| `moving_average_cross` | 快慢均線交叉 |
| `price_moving_average` | 價格與均線關係 |
| `rsi_reversion` | RSI 均值回歸 |
| `multi_timeframe_ma_spread` | 多週期均線 spread |
| `donchian_breakout` | Donchian channel 突破 |

如果使用 GitHub `main`，可能已經有更多策略家族；但 OpenClaw 若固定安裝 `cyqnt-trd==0.1.9.dev0`，應以此版本可用策略為準。

### CME / MNQ 研究補充

本 repo 版本已加入 CME/MNQ 研究接入，主線仍走 `standard_bot -> mvp_backtest.py -> NumbaBacktestRunner`。

推荐先把 CME / 券商 / TradingView 导出的 MNQ CSV 转成本地 parquet：

```bash
python -m cyqnt_trd.standard_bot.entrypoints.cme_ingest \
  --csv /path/to/MNQ_1m.csv \
  --symbol MNQ \
  --interval 1m \
  --historical-dir data/cme_mnq
```

然后跑 5m / 15m 回测：

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest \
  --engine numba \
  --market-type cme \
  --symbol MNQ \
  --interval 5m \
  --secondary-interval 15m \
  --strategy multi_timeframe_ma_spread \
  --primary-ma-period 5 \
  --reference-ma-period 5 \
  --historical-dir data/cme_mnq \
  --commission-bps 0.5 \
  --slippage-bps 0.25 \
  --output-json docs/backtests/mnq_mtf_ma_spread_5m_15m.json
```

详细说明见 `docs/cme_mnq_backtest.md`。Yahoo delayed chart 仅作为 bootstrap 来源，可能被限流；正式研究建议使用本地 CSV/parquet。

## 6. Donchian breakout 範例

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest \
  --engine numba \
  --market-type futures \
  --strategy donchian_breakout \
  --symbol BTCUSDT \
  --interval 5m \
  --donchian-window 63 \
  --breakout-buffer-bps 40 \
  --historical-dir data/mtf_90d \
  --start-ts <START_TS> \
  --end-ts <END_TS> \
  --download-missing \
  --output-json docs/backtests/btc_donchian_90d.json
```

## 7. 讀取回測結果

回測 JSON 通常包含：

- `total_return`
- `metrics.max_drawdown`
- `metrics.sharpe_ratio`
- `metrics.trade_count`
- `metrics.signal_count`
- `metrics.final_equity`
- `equity_curve`
- `trades`

可以用 Python 快速讀取：

```bash
python - <<'PY'
import json
from pathlib import Path

path = Path("docs/backtests/btc_donchian_90d.json")
payload = json.loads(path.read_text())
metrics = payload["metrics"]

print("total_return:", payload["total_return"])
print("sharpe:", metrics.get("sharpe_ratio"))
print("max_drawdown:", metrics.get("max_drawdown"))
print("trade_count:", metrics.get("trade_count"))
print("final_equity:", metrics.get("final_equity"))
PY
```

## 8. 產生 paper signal

`mvp_paper` 會跑一次 paper execution cycle。這可以用來讓 OpenClaw 取得最新 signal，但不直接真實交易。

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_paper \
  --market-type futures \
  --strategy donchian_breakout \
  --symbol BTCUSDT \
  --interval 5m \
  --donchian-window 63 \
  --breakout-buffer-bps 40 \
  --historical-dir data/mtf_90d \
  --start-ts <START_TS> \
  --end-ts <END_TS> \
  --download-missing \
  --dry-run
```

重點：

- paper signal 不需要 `CONFIRM`。
- 真實交易前必須先展示餘額、risk controls、交易計畫與 session duration。
- 真實交易只能跟隨 paper-generated signal，不應由 OpenClaw 重算另一套訊號。

## 9. 啟動 paper monitor

可以啟動一個 HTTP monitor，供外部系統呼叫 `/run`。

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_monitor_http \
  --broker paper \
  --market-type futures \
  --host 127.0.0.1 \
  --port 8787
```

健康檢查：

```bash
curl http://127.0.0.1:8787/health
```

觸發一次 signal：

```bash
curl -X POST http://127.0.0.1:8787/run \
  -H 'Content-Type: application/json' \
  -d '{
    "symbol": "BTCUSDT",
    "interval": "5m",
    "strategy": "donchian_breakout",
    "donchian_window": 63,
    "breakout_buffer_bps": 40,
    "signal_only": true,
    "dry_run": true
  }'
```

## 10. OpenClaw 建議流程

OpenClaw 若要使用 `cyqnt-trd==0.1.9.dev0`，建議遵守這條主線：

```text
user request
-> formal strategy spec
-> pip install cyqnt-trd==0.1.9.dev0
-> standard_bot
-> local parquet refresh
-> numba backtest
-> paper signal
-> balance / risk / duration display
-> user CONFIRM
-> watcher subagent
-> live execution handled by OpenClaw tools
```

不可跳過：

- local historical parquet 檢查
- `standard_bot -> mvp_backtest.py -> NumbaBacktestRunner`
- paper-generated signal
- balance display
- risk controls
- explicit `CONFIRM`
- watcher status / stop handling

## 11. 什麼時候需要 clone source repo

一般使用不需要 clone repo，直接安裝 package 即可：

```bash
python -m pip install cyqnt-trd==0.1.9.dev0
```

只有在這些情況才 clone source：

- 要查看原始碼
- 要修改策略 plugin
- 要新增 Numba kernel
- 要 debug package 內部問題
- 要使用尚未發布到 PyPI 的新功能

source fallback：

```bash
git clone https://github.com/binance-agentic-finance/crypto_trading
cd crypto_trading
```

## 12. 常見問題

### 為什麼要先下載成 parquet？

因為回測需要可重現的資料。  
直接用 API 即時回傳結果會讓每次回測不容易對齊，也不利於 debug。

### `--download-missing` 為什麼需要 `--start-ts` 和 `--end-ts`？

因為 downloader 必須知道要補哪段時間。  
若只給 `limit`，它無法安全判定該下載哪個完整歷史區間。

### 可以下載 Binance TradFi perpetual 嗎？

如果 symbol 存在於 Binance USDⓈ-M Futures API，例如 `TSMUSDT` 這類 `TRADIFI_PERPETUAL`，目前 futures Kline 下載流程可以抓。  
但如果商品剛上市，實際歷史資料可能不足 90 天。

### 可以直接真實交易嗎？

不建議直接跳到真實交易。  
正確流程是：

```text
backtest -> paper signal -> balance/risk/duration display -> CONFIRM -> watcher -> live session
```

### 如果 OpenClaw 遇到錯誤可以改走別的腳本嗎？

不可以默默改走別的流程。  
應該停止、回報使用者哪一步失敗，並繼續 debug 正確主線。

## 13. 一句話總結

`cyqnt-trd==0.1.9.dev0` 的正確使用方式是：

```text
install fixed package
-> refresh local parquet
-> run standard_bot
-> use NumbaBacktestRunner
-> read JSON metrics
-> generate paper signal
-> only then consider confirmed, monitored live execution
```
