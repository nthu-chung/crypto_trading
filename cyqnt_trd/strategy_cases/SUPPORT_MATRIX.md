# Strategy Case Support Matrix

This matrix explains how external strategy cases relate to the current
`cyqnt_trd.standard_bot` architecture.

It is designed to answer four practical questions:

1. Does a case match the current `standard_bot` plugin model?
2. Which current plugins or data paths already cover part of the case?
3. What is still missing before the case becomes a real backtestable plugin?
4. Should the case be prioritized for conversion?

## Support Levels

- `High`: close to current plugin architecture and mostly expressible with
  existing factors and backtest semantics.
- `Medium`: several parts already exist, but the case is still a bundle of
  filters, scoring, or orchestration rather than one clean plugin.
- `Low`: concept is useful, but the current system lacks major building blocks.

## Curated Packaged Cases

| Case | Category | Support | Current Mapping | Main Gaps | Recommendation |
| --- | --- | --- | --- | --- | --- |
| `rsi-mean-reversion` | Mean reversion | High | `rsi_reversion` | multi-mode packaging, laddered short semantics, case-style rescan exits | Best first candidate to convert into a tighter executable preset |
| `btc-multi-factor-trend` | Trend following | Medium | `moving_average_cross`, `macd_trend_follow`, `adx_trend_strength`, `oi_funding_breakout`, `multi_timeframe_ma_spread` | one composite scorer, bundled risk profiles, single-plugin orchestration | Strong second-wave target after baseline presets are stable |
| `bb-squeeze-momentum` | Volatility breakout | Medium | `bollinger_mean_reversion`, `macd_trend_follow`, `adx_trend_strength` | squeeze state / bandwidth breakout, StochRSI, volume-surge scoring | Good plugin candidate once squeeze logic is added |
| `quadruple-filter-breakout` | Trend breakout | Medium | `multi_timeframe_ma_spread`, `donchian_breakout`, `atr_breakout` | strict sequential 4-TF hard gate, case-specific rescan exit | Good bundle preset now, dedicated plugin later |
| `structure-breakout-priceaction` | Price action breakout | Low | `donchian_breakout` only covers a small slice | pivots, structural box engine, pattern-quality scoring, candlestick confirmation | Keep as concept bundle until a structure layer exists |

## Additional Promising Cases From The Source Library

These are not yet packaged as first-class case bundles, but they are the next
most reasonable candidates.

| Case | Category | Support | Why It Is Interesting | Main Missing Pieces |
| --- | --- | --- | --- | --- |
| `golden-ratio-fibonacci` | Structure / retracement | Low-Medium | strong user-facing logic, clear entry/TP narrative | swing detection, fib engine, reversal confirmation |
| `neurogrid-supertrend-compound` | Trend + scaling | Medium | can reuse ADX/ATR/MACD/EMA-style factors and later compound logic | SuperTrend family, add-on position logic, exposure scheduler |
| `stochrsi-mdi-trend-v1` | Oscillator trend | Medium | close to existing indicator style families | StochRSI factor family, MDI divergence logic |
| `funding-rate-scanner` | Scanner | Medium | matches current derivatives expansion path | scanner/report layer rather than a single plugin |
| `volume-surge-scanner` | Scanner | Medium | close to current OHLCV pipeline and future anomaly detection | native volume anomaly factor and ranking workflow |
| `position-sizer` | Risk tool | High as utility, not as plugin | directly useful across many strategies | formal risk utility interface rather than signal plugin |

## Cases That Should Usually Stay As Templates Or References

These cases are valuable, but they are poor first candidates for direct plugin
conversion because they rely heavily on social feeds, exchange-specific
execution behavior, or workflow-heavy orchestration.

| Case | Why It Should Stay Reference-First |
| --- | --- |
| `case_lana` | depends on attention-first discovery and execution workflow, not just signal logic |
| `case_smart_momentum` | mixes hotrank, smart-money, funding, posting, and live orchestration |
| `lana-square-momentum` | content-driven discovery and Square integration are central to the case |
| `trend-grid-bot` | grid trading needs different position semantics than current signal plugins |
| `okx-maker-entry` | orderbook-aware maker execution is an execution-system problem, not a simple backtest plugin |
| `okx-pair-spread` | spread/pairs logic needs portfolio-level backtest semantics |
| `rolling-position` | rolling and expiry management are lifecycle workflows, not just entry/exit signals |

## Priority Order For Real Plugin Conversion

If the goal is to steadily turn cases into real `standard_bot` strategies,
the most practical order is:

1. `rsi-mean-reversion`
2. `bb-squeeze-momentum`
3. `quadruple-filter-breakout`
4. `btc-multi-factor-trend`
5. `golden-ratio-fibonacci`
6. `structure-breakout-priceaction`

## Why Not Convert Everything Immediately?

Because a case is usually wider than a plugin.

In this codebase:

- a **case** is often an end-to-end trading workflow
- a **plugin** is the backtestable and step-alignable strategy core

That means many cases must first be decomposed into:

- signal logic
- filter logic
- scoring logic
- sizing logic
- monitoring / rescan logic

Only the signal core should be forced into a `standard_bot` plugin.

## Recommended Working Rule

When evaluating any future case, classify it as one of:

- `direct_plugin_candidate`
- `bundle_preset_candidate`
- `reference_only_for_now`

This keeps the package honest and avoids pretending a workflow-heavy case is
already a clean backtestable strategy.
