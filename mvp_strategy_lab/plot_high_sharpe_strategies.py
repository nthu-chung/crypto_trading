from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Dict, List

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cyqnt_trd.standard_bot.core import MarketQuery, TimeRange
from cyqnt_trd.standard_bot.data.alignment import timeframe_to_ms
from cyqnt_trd.standard_bot.data.historical import HistoricalParquetMarketDataAdapter, build_history_path, parquet_time_coverage
from cyqnt_trd.standard_bot.simulation import NumbaBacktestRunner
from scripts.llm_strategy_evolution import StrategyCandidate, create_request


@dataclass
class RankedCandidate:
    experiment_json: Path
    symbol: str
    market_type: str
    primary_timeframe: str
    secondary_timeframe: str
    initial_capital: float
    taker_fee_bps: float
    slippage_bps: float
    impact_slippage_bps: float
    max_bar_volume_fraction: float
    candidate_id: str
    strategy: str
    params: Dict[str, float | int]
    sharpe_ratio: float
    total_return: float
    max_drawdown: float
    trade_count: int
    signal_count: int
    final_equity: float
    win_rate: float | None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plot top strategies across one or more evolution runs")
    parser.add_argument("--experiment-json", nargs="+", required=True, help="One or more experiment_summary.json files")
    parser.add_argument("--historical-dir", default=str(REPO_ROOT / "data" / "mtf_90d"))
    parser.add_argument("--top-n", type=int, default=5)
    parser.add_argument("--output-dir", required=True)
    return parser


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_final_round_candidates(experiment_json: Path) -> List[RankedCandidate]:
    payload = load_json(experiment_json)
    experiment = payload["experiment"]
    final_round = payload["rounds"][-1]
    candidates: List[RankedCandidate] = []
    for item in final_round["ranked"]:
        candidates.append(
            RankedCandidate(
                experiment_json=experiment_json,
                symbol=str(experiment["symbol"]),
                market_type=str(experiment["market_type"]),
                primary_timeframe=str(experiment["primary_timeframe"]),
                secondary_timeframe=str(experiment["secondary_timeframe"]),
                initial_capital=float(experiment["initial_capital"]),
                taker_fee_bps=float(experiment["taker_fee_bps"]),
                slippage_bps=float(experiment["slippage_bps"]),
                impact_slippage_bps=float(experiment["impact_slippage_bps"]),
                max_bar_volume_fraction=float(experiment["max_bar_volume_fraction"]),
                candidate_id=str(item["candidate_id"]),
                strategy=str(item["strategy"]),
                params=dict(item["params"]),
                sharpe_ratio=float(item["sharpe_ratio"]),
                total_return=float(item["total_return"]),
                max_drawdown=float(item["max_drawdown"]),
                trade_count=int(item["trade_count"]),
                signal_count=int(item["signal_count"]),
                final_equity=float(item["final_equity"]),
                win_rate=None if item.get("win_rate") is None else float(item["win_rate"]),
            )
        )
    return candidates


def load_market_bundle(candidate: RankedCandidate, *, historical_dir: str):
    history_path = build_history_path(historical_dir, candidate.market_type, candidate.symbol, "1m")
    start_ts, end_ts = parquet_time_coverage(history_path)
    if start_ts is None or end_ts is None:
        raise RuntimeError(f"unable to determine parquet coverage for {history_path}")

    safe_query_start_ts = int(start_ts) + max(
        timeframe_to_ms(candidate.primary_timeframe),
        timeframe_to_ms(candidate.secondary_timeframe),
    )

    adapter = HistoricalParquetMarketDataAdapter(
        data_root=historical_dir,
        market_type=candidate.market_type,
        resample_source_timeframe="1m",
    )
    market_bundle = adapter.fetch_market(
        MarketQuery(
            instruments=[candidate.symbol],
            timeframes=[candidate.primary_timeframe, candidate.secondary_timeframe],
            time_range=TimeRange(start_ts=safe_query_start_ts, end_ts=int(end_ts)),
        )
    )
    primary_key = market_bundle.key(candidate.symbol, candidate.primary_timeframe)
    primary_bars = market_bundle.bars.get(primary_key, [])
    if not primary_bars:
        raise RuntimeError(f"no bars loaded for {primary_key}")
    return market_bundle, int(primary_bars[0].timestamp), int(primary_bars[-1].timestamp)


def rerun_backtest(candidate: RankedCandidate, *, historical_dir: str) -> dict:
    market_bundle, backtest_start_ts, backtest_end_ts = load_market_bundle(candidate, historical_dir=historical_dir)
    request = create_request(
        StrategyCandidate(
            candidate_id=candidate.candidate_id,
            strategy=candidate.strategy,
            params=dict(candidate.params),
            origin="plot_rerun",
            parent_ids=[],
        ),
        symbol=candidate.symbol,
        primary_timeframe=candidate.primary_timeframe,
        secondary_timeframe=candidate.secondary_timeframe,
        start_ts=backtest_start_ts,
        end_ts=backtest_end_ts,
        initial_capital=candidate.initial_capital,
        taker_fee_bps=candidate.taker_fee_bps,
        slippage_bps=candidate.slippage_bps,
        impact_slippage_bps=candidate.impact_slippage_bps,
        max_bar_volume_fraction=candidate.max_bar_volume_fraction,
    )
    runner = NumbaBacktestRunner()
    result = runner.run(request=request, market_bundle=market_bundle)
    return {
        "request_id": result.request_id,
        "total_return": result.total_return,
        "equity_curve": result.equity_curve,
        "metrics": result.metrics,
        "signal_batches": result.signal_batches,
        "extras": result.extras,
    }


def make_jsonable(value):
    if is_dataclass(value):
        return make_jsonable(asdict(value))
    if isinstance(value, dict):
        return {key: make_jsonable(inner) for key, inner in value.items()}
    if isinstance(value, list):
        return [make_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [make_jsonable(item) for item in value]
    return value


def plot_backtest(backtest: dict, candidate: RankedCandidate, *, rank: int, output_png: Path) -> dict:
    equity_curve = pd.DataFrame(backtest.get("equity_curve", []))
    if equity_curve.empty:
        raise RuntimeError(f"equity_curve is empty for {candidate.candidate_id}")

    metrics = backtest.get("metrics", {})
    equity_curve["timestamp"] = pd.to_datetime(equity_curve["timestamp"], unit="ms", utc=True).dt.tz_convert(None)
    equity_curve["equity"] = equity_curve["equity"].astype(float)
    equity_curve["pnl"] = equity_curve["equity"] - candidate.initial_capital

    sharpe = float(metrics.get("sharpe_ratio", 0.0))
    max_drawdown = float(metrics.get("max_drawdown", 0.0)) * 100.0
    total_return = float(metrics.get("total_return", 0.0)) * 100.0
    final_equity = float(metrics.get("final_equity", 0.0))
    pnl = final_equity - candidate.initial_capital
    start_date = equity_curve["timestamp"].iloc[0].strftime("%Y-%m-%d")
    end_date = equity_curve["timestamp"].iloc[-1].strftime("%Y-%m-%d")

    fig, axes = plt.subplots(2, 1, figsize=(16, 9), sharex=True)

    axes[0].plot(equity_curve["timestamp"], equity_curve["equity"], color="#2563eb", linewidth=1.6)
    axes[0].axhline(candidate.initial_capital, color="#94a3b8", linewidth=1.0, linestyle="--", alpha=0.9)
    axes[0].set_title(f"Rank {rank} | {candidate.symbol} | {candidate.strategy}")
    axes[0].set_ylabel("Equity")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(equity_curve["timestamp"], equity_curve["pnl"], color="#16a34a", linewidth=1.3)
    axes[1].axhline(0.0, color="black", linewidth=0.8, alpha=0.5)
    axes[1].set_ylabel("PnL")
    axes[1].set_xlabel("Date")
    axes[1].grid(True, alpha=0.3)
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate()

    param_text = "\n".join([f"{k}: {v}" for k, v in candidate.params.items()])
    summary_text = (
        f"Symbol: {candidate.symbol}\n"
        f"Date: {start_date} -> {end_date}\n"
        f"PnL: {pnl:.2f}\n"
        f"Sharpe Ratio: {sharpe:.4f}\n"
        f"Max Drawdown: {max_drawdown:.2f}%\n"
        f"Returns: {total_return:.2f}%\n"
        f"Trades: {int(metrics.get('trade_count', 0.0))}\n"
        f"Params:\n{param_text}"
    )
    fig.text(
        0.79,
        0.5,
        summary_text,
        fontsize=11,
        va="center",
        ha="left",
        bbox=dict(boxstyle="round", facecolor="#f8fafc", alpha=0.95),
    )
    fig.tight_layout(rect=[0, 0, 0.76, 1])
    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_png, dpi=180, bbox_inches="tight")
    plt.close(fig)

    return {
        "rank": rank,
        "symbol": candidate.symbol,
        "strategy": candidate.strategy,
        "candidate_id": candidate.candidate_id,
        "params": candidate.params,
        "date_start": start_date,
        "date_end": end_date,
        "pnl": pnl,
        "sharpe_ratio": sharpe,
        "max_drawdown_pct": max_drawdown,
        "returns_pct": total_return,
        "trade_count": int(metrics.get("trade_count", 0.0)),
        "signal_count": int(metrics.get("signal_count", 0.0)),
        "plot_png": str(output_png),
    }


def write_summary_markdown(path: Path, top_summaries: List[dict]) -> None:
    lines = [
        "# Combined Top 5 Strategies",
        "",
        "| Rank | Symbol | Candidate | Strategy | Sharpe | Return | Max DD | PnL | Trades | Params |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for item in top_summaries:
        lines.append(
            "| %s | `%s` | `%s` | `%s` | %.4f | %.2f%% | %.2f%% | %.2f | %s | `%s` |"
            % (
                item["rank"],
                item["symbol"],
                item["candidate_id"],
                item["strategy"],
                item["sharpe_ratio"],
                item["returns_pct"],
                item["max_drawdown_pct"],
                item["pnl"],
                item["trade_count"],
                json.dumps(item["params"], ensure_ascii=False, sort_keys=True),
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = build_parser().parse_args()
    experiment_jsons = [Path(item) for item in args.experiment_json]
    output_dir = Path(args.output_dir)
    plots_dir = output_dir / "top5_plots"
    backtests_dir = output_dir / "top5_backtests"
    output_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)
    backtests_dir.mkdir(parents=True, exist_ok=True)

    ranked_candidates: List[RankedCandidate] = []
    for experiment_json in experiment_jsons:
        ranked_candidates.extend(extract_final_round_candidates(experiment_json))

    ranked_candidates.sort(
        key=lambda item: (item.sharpe_ratio, item.total_return, -item.max_drawdown, -item.trade_count),
        reverse=True,
    )
    top_candidates = ranked_candidates[: args.top_n]
    if not top_candidates:
        raise SystemExit("no candidates found")

    top_summaries: List[dict] = []
    for rank, candidate in enumerate(top_candidates, start=1):
        backtest = make_jsonable(rerun_backtest(candidate, historical_dir=args.historical_dir))
        backtest_path = backtests_dir / f"rank_{rank:02d}_{candidate.symbol}_{candidate.candidate_id}.json"
        backtest_path.write_text(json.dumps(backtest, ensure_ascii=False, indent=2), encoding="utf-8")
        plot_path = plots_dir / f"rank_{rank:02d}_{candidate.symbol}_{candidate.candidate_id}.png"
        summary = plot_backtest(backtest, candidate, rank=rank, output_png=plot_path)
        summary["source_experiment_json"] = str(candidate.experiment_json)
        summary["backtest_json"] = str(backtest_path)
        top_summaries.append(summary)

    (output_dir / "top5_summary.json").write_text(
        json.dumps(top_summaries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_summary_markdown(output_dir / "top5_summary.md", top_summaries)
    print(json.dumps(top_summaries, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
