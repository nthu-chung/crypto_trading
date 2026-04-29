# CME / MNQ 回测接入说明

## 目前支持内容

- `market_type=cme`
- `symbol=MNQ`
- 本地 parquet 路径：`<historical-dir>/cme/MNQ/<interval>.parquet`
- MNQ 合约乘数：`2.0`
- MNQ tick size：`0.25`
- MNQ tick value：`0.50`
- 支持 `5m`、`15m`、`1h` 等标准 timeframe
- 回测主线沿用 `standard_bot -> mvp_backtest.py -> NumbaBacktestRunner`

## 推荐正式流程：CSV 先落地成本地 parquet

如果你有 CME DataMine、券商、TradingView 或其它来源导出的 OHLCV CSV，先转成本地 parquet：

```bash
python -m cyqnt_trd.standard_bot.entrypoints.cme_ingest \
  --csv /path/to/MNQ_1m.csv \
  --symbol MNQ \
  --interval 1m \
  --historical-dir data/cme_mnq \
  --timestamp-column timestamp \
  --timezone UTC
```

然后跑 5m / 15m 多周期回测：

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
  --spread-threshold-bps 0 \
  --historical-dir data/cme_mnq \
  --commission-bps 0.5 \
  --slippage-bps 0.25 \
  --max-bar-volume-fraction 0.05 \
  --output-json docs/backtests/mnq_mtf_ma_spread_5m_15m.json
```

## Bootstrap 流程：Yahoo delayed chart

也可以先用 Yahoo delayed chart bootstrap 数据：

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
  --spread-threshold-bps 0 \
  --historical-dir data/cme_mnq_demo \
  --start-ts <START_TS_MS> \
  --end-ts <END_TS_MS> \
  --download-missing \
  --commission-bps 0.5 \
  --slippage-bps 0.25 \
  --max-bar-volume-fraction 0.05 \
  --output-json docs/backtests/mnq_mtf_ma_spread_5m_15m_smoke.json
```

注意：Yahoo delayed chart 是非官方免费来源，可能回 `429 Too Many Requests`。正式研究建议使用 CME 或券商导出的本地 CSV/parquet。

## 免费历史数据流程：Hugging Face NQ 1m proxy

目前可先用 Hugging Face 上的免费 NQ 1m OHLCV parquet 作为 MNQ 价格 proxy。价格序列使用 NQ，系统落地时会写成 `symbol=MNQ`，并用 MNQ 合约乘数 `2.0` 计算名义成交额与 PnL。

下载并转换 2025 年资料：

```bash
python -m cyqnt_trd.standard_bot.entrypoints.cme_hf_ingest \
  --symbol MNQ \
  --years 2025 \
  --historical-dir data/cme_mnq
```

输出路径：

```text
data/cme_mnq/cme/MNQ/1m.parquet
```

跑 5m / 15m K bar 多周期回测：

```bash
python -m cyqnt_trd.standard_bot.entrypoints.mvp_backtest \
  --engine numba \
  --market-type cme \
  --symbol MNQ \
  --interval 5m \
  --secondary-interval 15m \
  --strategy multi_timeframe_ma_spread \
  --primary-ma-period 20 \
  --reference-ma-period 20 \
  --spread-threshold-bps 2 \
  --historical-dir data/cme_mnq \
  --storage-timeframe 1m \
  --limit 5000 \
  --initial-capital 100000 \
  --commission-bps 0 \
  --slippage-bps 0 \
  --max-bar-volume-fraction 0.05 \
  --output-json docs/backtests/mnq_nq_proxy_mtf_ma_spread_5m_15m_2025.json
```

本次 smoke 回测结果：

- 资料：2025 NQ 1m proxy，自动 resample 成 5m / 15m。
- 样本：`4998` 根 5m bar。
- 交易：`89` 笔。
- 初始资金：`100000`。
- 期末权益：`98376.80`。
- 总收益：`-1.6232%`。
- 最大回撤：`4.7213%`。

注意：这次费用与滑点设为 0，只用于验证 K bar 回测链路。正式策略评估前还需要加入 MNQ 固定手续费、tick slippage、整数合约数量、换月/连续合约规则。

## 近期 yfinance 流程：MNQ 5m / 15m

yfinance 可以抓 Yahoo 的近期 intraday 数据，适合快速验证最近 30-60 天的 5m / 15m K bar 策略。先安装可选依赖：

```bash
.venv-standard-bot/bin/pip install yfinance
```

下载并转换 `MNQ=F`：

```bash
python -m cyqnt_trd.standard_bot.entrypoints.cme_yfinance_ingest \
  --symbol MNQ \
  --provider-symbol MNQ=F \
  --period 60d \
  --historical-dir data/yfinance_mnq
```

输出路径：

```text
data/yfinance_mnq/cme/MNQ/5m.parquet
data/yfinance_mnq/cme/MNQ/15m.parquet
```

跑 5 轮 LLM-style 策略搜索：

```bash
python scripts/llm_strategy_evolution.py \
  --symbol MNQ \
  --market-type cme \
  --primary-timeframe 5m \
  --secondary-timeframe 15m \
  --historical-dir data/yfinance_mnq \
  --rounds 5 \
  --population-size 50 \
  --survivors 20 \
  --family-cap 4 \
  --initial-capital 100000 \
  --taker-fee-bps 0.25 \
  --fixed-fee-per-contract 0.60 \
  --slippage-bps 0.10 \
  --max-bar-volume-fraction 0.05 \
  --quantity-step 1 \
  --min-quantity 1 \
  --output-root docs/backtests/mnq_yfinance_llm_5rounds_2026-04-24
```

## CSV 栏位要求

最小栏位：

- `timestamp`
- `open`
- `high`
- `low`
- `close`
- `volume`

可选栏位：

- `trades`
- `open_time`

如果没有 `timestamp`，也可以使用 `date + time` 两个栏位。系统会转成 UTC 毫秒时间戳，并写入标准 parquet schema。

## 回测假设

- signal 在已收盘 K bar 上产生。
- 执行假设为下一根 K bar open 成交。
- MNQ PnL 使用 `contract_multiplier=2.0`。
- `volume` 视为合约张数。
- `quote_volume` 按 `close * volume * contract_multiplier` 估算。
- 目前不处理合约换月、连续合约回调、CME session break 与假日规则；这些应在正式数据清洗层补齐。
