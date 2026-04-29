#!/bin/zsh
set -euo pipefail

ROOT="/Users/hankchung/Dev/crypto_trading-main"
VENV="$ROOT/.venv-mvp"
PY="$VENV/bin/python"
OUT_DIR="$ROOT/mvp_strategy_lab/results"
DAY_STAMP="$(date +%Y%m%d)"
RUN_INDEX=1
while [[ -e "$OUT_DIR/${DAY_STAMP}_${RUN_INDEX}" ]]; do
  RUN_INDEX=$((RUN_INDEX + 1))
done
RUN_DIR="$OUT_DIR/${DAY_STAMP}_${RUN_INDEX}"

mkdir -p "$OUT_DIR"

exec "$PY" "$ROOT/scripts/llm_strategy_evolution.py" \
  --symbol BTCUSDT \
  --market-type futures \
  --primary-timeframe 5m \
  --secondary-timeframe 1h \
  --historical-dir "$ROOT/data/mtf_90d" \
  --rounds 5 \
  --population-size 50 \
  --survivors 20 \
  --family-cap 5 \
  --initial-capital 10000 \
  --taker-fee-bps 10 \
  --slippage-bps 0 \
  --impact-slippage-bps 0 \
  --max-bar-volume-fraction 0.10 \
  --seed 20260416 \
  --output-root "$RUN_DIR"
