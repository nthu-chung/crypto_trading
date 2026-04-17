"""
Run a small LLM-style strategy evolution experiment on the standard_bot stack.

The experiment keeps the evaluation path aligned with the repo's mainline
backtest architecture:

    local parquet -> standard_bot signal pipeline -> NumbaBacktestRunner

It is intentionally simple and reproducible:

- Round 1 starts from 10 hand-seeded strategy candidates.
- Each subsequent round keeps the top 4 candidates by Sharpe ratio.
- Those top 4 are carried forward and mutated into a fresh population of 10.
- The process repeats for 5 rounds total.

This is not a full genetic algorithm. The "LLM replacement" here is the
candidate synthesis policy: we choose structured strategy families and mutate
their parameters with domain-informed heuristics rather than crossover.
"""

from __future__ import annotations

import argparse
import copy
import csv
import json
import math
import random
import sys
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cyqnt_trd.standard_bot.core import BacktestRequest, MarketQuery, TimeRange
from cyqnt_trd.standard_bot.data.alignment import timeframe_to_ms
from cyqnt_trd.standard_bot.data.historical import HistoricalParquetMarketDataAdapter, build_history_path, parquet_time_coverage
from cyqnt_trd.standard_bot.entrypoints.common import build_strategy_pipeline
from cyqnt_trd.standard_bot.simulation import NumbaBacktestRunner


@dataclass
class StrategyCandidate:
    candidate_id: str
    strategy: str
    params: Dict[str, float | int]
    origin: str
    parent_ids: List[str] = field(default_factory=list)


@dataclass
class CandidateResult:
    candidate_id: str
    strategy: str
    params: Dict[str, float | int]
    origin: str
    parent_ids: List[str]
    sharpe_ratio: float
    total_return: float
    max_drawdown: float
    trade_count: int
    signal_count: int
    final_equity: float


def candidate_result_from_dict(payload: Dict) -> CandidateResult:
    return CandidateResult(
        candidate_id=str(payload["candidate_id"]),
        strategy=str(payload["strategy"]),
        params=copy.deepcopy(payload["params"]),
        origin=str(payload.get("origin", "seed_result")),
        parent_ids=list(payload.get("parent_ids", [])),
        sharpe_ratio=float(payload.get("sharpe_ratio", float("-inf"))),
        total_return=float(payload.get("total_return", 0.0)),
        max_drawdown=float(payload.get("max_drawdown", 0.0)),
        trade_count=int(payload.get("trade_count", 0)),
        signal_count=int(payload.get("signal_count", 0)),
        final_equity=float(payload.get("final_equity", 0.0)),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="LLM-style strategy evolution over standard_bot numba backtests")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--market-type", choices=["spot", "futures"], default="futures")
    parser.add_argument("--primary-timeframe", default="5m")
    parser.add_argument("--secondary-timeframe", default="1h")
    parser.add_argument("--historical-dir", default="data/mtf_90d")
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--population-size", type=int, default=50)
    parser.add_argument("--survivors", type=int, default=20)
    parser.add_argument("--family-cap", type=int, default=5)
    parser.add_argument("--initial-capital", type=float, default=10_000.0)
    parser.add_argument("--taker-fee-bps", type=float, default=10.0)
    parser.add_argument("--slippage-bps", type=float, default=0.0)
    parser.add_argument("--impact-slippage-bps", type=float, default=0.0)
    parser.add_argument("--max-bar-volume-fraction", type=float, default=0.10)
    parser.add_argument("--seed", type=int, default=20260416)
    parser.add_argument("--seed-json", default=None)
    parser.add_argument("--seed-round", default="final", help="Use 'final' or a 1-based round number from --seed-json")
    parser.add_argument("--seed-top-k", type=int, default=None, help="How many ranked candidates from --seed-json to seed from")
    parser.add_argument("--output-root", default=None, help="Directory root for per-round artifacts")
    parser.add_argument("--output-json", default="docs/backtests/llm_strategy_evolution.json")
    parser.add_argument("--output-md", default="docs/backtests/llm_strategy_evolution.md")
    parser.add_argument("--output-csv", default="docs/backtests/llm_strategy_evolution_candidates.csv")
    return parser


def base_seed_candidates() -> List[StrategyCandidate]:
    return [
        StrategyCandidate("r1_c01", "moving_average_cross", {"fast_window": 5, "slow_window": 20, "entry_threshold": 0.0}, "seed"),
        StrategyCandidate("r1_c02", "moving_average_cross", {"fast_window": 10, "slow_window": 40, "entry_threshold": 0.0005}, "seed"),
        StrategyCandidate("r1_c03", "moving_average_cross", {"fast_window": 20, "slow_window": 80, "entry_threshold": 0.0010}, "seed"),
        StrategyCandidate("r1_c04", "rsi_reversion", {"period": 7, "oversold": 25.0, "overbought": 75.0}, "seed"),
        StrategyCandidate("r1_c05", "rsi_reversion", {"period": 14, "oversold": 30.0, "overbought": 70.0}, "seed"),
        StrategyCandidate("r1_c06", "price_moving_average", {"period": 10, "entry_threshold": 0.0005}, "seed"),
        StrategyCandidate("r1_c07", "multi_timeframe_ma_spread", {"primary_ma_period": 10, "reference_ma_period": 20, "spread_threshold_bps": 0.0}, "seed"),
        StrategyCandidate("r1_c08", "multi_timeframe_ma_spread", {"primary_ma_period": 20, "reference_ma_period": 50, "spread_threshold_bps": 20.0}, "seed"),
        StrategyCandidate("r1_c09", "donchian_breakout", {"lookback_window": 20, "breakout_buffer_bps": 0.0}, "seed"),
        StrategyCandidate("r1_c10", "donchian_breakout", {"lookback_window": 55, "breakout_buffer_bps": 10.0}, "seed"),
        StrategyCandidate("r1_c11", "adx_trend_strength", {"period": 14, "adx_threshold": 25.0}, "seed"),
        StrategyCandidate("r1_c12", "adx_trend_strength", {"period": 20, "adx_threshold": 30.0}, "seed"),
        StrategyCandidate("r1_c13", "atr_breakout", {"ma_period": 20, "atr_period": 14, "atr_multiplier": 1.5}, "seed"),
        StrategyCandidate("r1_c14", "atr_breakout", {"ma_period": 50, "atr_period": 14, "atr_multiplier": 2.5}, "seed"),
        StrategyCandidate("r1_c15", "bollinger_mean_reversion", {"period": 20, "stddev_multiplier": 2.0}, "seed"),
        StrategyCandidate("r1_c16", "bollinger_mean_reversion", {"period": 30, "stddev_multiplier": 2.5}, "seed"),
        StrategyCandidate("r1_c17", "macd_trend_follow", {"fast_period": 12, "slow_period": 26, "signal_period": 9, "histogram_threshold": 0.0}, "seed"),
        StrategyCandidate("r1_c18", "macd_trend_follow", {"fast_period": 8, "slow_period": 21, "signal_period": 5, "histogram_threshold": 0.0005}, "seed"),
    ]


def generate_initial_population(population_size: int, *, rng: random.Random) -> List[StrategyCandidate]:
    if population_size <= 0:
        raise ValueError("population_size must be positive")

    seeds = base_seed_candidates()
    population: List[StrategyCandidate] = []
    seen = set()

    for index, seed in enumerate(seeds[:population_size], start=1):
        candidate = StrategyCandidate(
            candidate_id=f"r1_c{index:02d}",
            strategy=seed.strategy,
            params=copy.deepcopy(seed.params),
            origin="seed",
            parent_ids=[],
        )
        population.append(candidate)
        seen.add(candidate_signature(candidate))

    parent_index = 0
    child_index = len(population) + 1
    while len(population) < population_size:
        parent = seeds[parent_index % len(seeds)]
        mutated = mutate_candidate(
            StrategyCandidate(
                candidate_id=parent.candidate_id,
                strategy=parent.strategy,
                params=copy.deepcopy(parent.params),
                origin=parent.origin,
                parent_ids=copy.deepcopy(parent.parent_ids),
            ),
            round_index=1,
            child_index=child_index,
            rng=rng,
        )
        signature = candidate_signature(mutated)
        if signature in seen:
            parent_index += 1
            continue
        population.append(mutated)
        seen.add(signature)
        parent_index += 1
        child_index += 1

    return population


def generate_population_from_seed_results(
    seed_results: Sequence[CandidateResult],
    *,
    population_size: int,
    rng: random.Random,
) -> List[StrategyCandidate]:
    if not seed_results:
        raise ValueError("seed_results must not be empty")
    if population_size <= len(seed_results):
        raise ValueError("population_size must be greater than the number of seed_results")

    population: List[StrategyCandidate] = []
    seen = set()

    for index, seed in enumerate(seed_results, start=1):
        candidate = StrategyCandidate(
            candidate_id=f"r1_c{index:02d}",
            strategy=seed.strategy,
            params=copy.deepcopy(seed.params),
            origin="seed_from_result",
            parent_ids=[seed.candidate_id],
        )
        population.append(candidate)
        seen.add(candidate_signature(candidate))

    child_index = len(population) + 1
    while len(population) < population_size:
        parent = seed_results[(child_index - 1) % len(seed_results)]
        mutated = mutate_candidate(
            StrategyCandidate(
                candidate_id=parent.candidate_id,
                strategy=parent.strategy,
                params=copy.deepcopy(parent.params),
                origin=parent.origin,
                parent_ids=copy.deepcopy(parent.parent_ids),
            ),
            round_index=1,
            child_index=child_index,
            rng=rng,
        )
        signature = candidate_signature(mutated)
        if signature in seen:
            continue
        population.append(mutated)
        seen.add(signature)
        child_index += 1

    return population


def load_seed_results(seed_json: Path, *, seed_round: str, seed_top_k: int | None) -> List[CandidateResult]:
    payload = json.loads(seed_json.read_text(encoding="utf-8"))
    rounds = payload.get("rounds", [])
    if not rounds:
        raise ValueError(f"seed json has no rounds: {seed_json}")

    if seed_round == "final":
        round_payload = rounds[-1]
    else:
        round_number = int(seed_round)
        matching = [item for item in rounds if int(item.get("round", -1)) == round_number]
        if not matching:
            raise ValueError(f"seed round {seed_round} not found in {seed_json}")
        round_payload = matching[0]

    ranked = round_payload.get("ranked", [])
    if not ranked:
        raise ValueError(f"selected seed round has no ranked candidates: {seed_json}")

    limit = seed_top_k if seed_top_k is not None else len(round_payload.get("survivors", []))
    if limit <= 0:
        raise ValueError("seed_top_k must be positive")
    return [candidate_result_from_dict(item) for item in ranked[:limit]]


def candidate_signature(candidate: StrategyCandidate) -> tuple[str, tuple[tuple[str, float | int], ...]]:
    return candidate.strategy, tuple(sorted(candidate.params.items()))


def clamp_int(value: int, low: int, high: int) -> int:
    return max(low, min(high, int(value)))


def clamp_float(value: float, low: float, high: float) -> float:
    return max(low, min(high, float(value)))


def mutate_candidate(parent: StrategyCandidate, *, round_index: int, child_index: int, rng: random.Random) -> StrategyCandidate:
    params = copy.deepcopy(parent.params)
    strategy = parent.strategy

    if strategy == "moving_average_cross":
        fast = clamp_int(int(params["fast_window"]) + rng.choice([-3, -2, -1, 1, 2, 3]), 2, 60)
        slow = clamp_int(int(params["slow_window"]) + rng.choice([-10, -5, 5, 10, 15]), 5, 200)
        if slow <= fast:
            slow = fast + rng.randint(2, 20)
        params["fast_window"] = fast
        params["slow_window"] = slow
        params["entry_threshold"] = round(
            clamp_float(float(params["entry_threshold"]) + rng.choice([-0.0005, 0.0, 0.0005, 0.001]), 0.0, 0.01),
            6,
        )
    elif strategy == "price_moving_average":
        params["period"] = clamp_int(int(params["period"]) + rng.choice([-5, -3, -1, 1, 3, 5]), 2, 100)
        params["entry_threshold"] = round(
            clamp_float(float(params["entry_threshold"]) + rng.choice([-0.0005, 0.0, 0.0005, 0.001]), 0.0, 0.01),
            6,
        )
    elif strategy == "rsi_reversion":
        params["period"] = clamp_int(int(params["period"]) + rng.choice([-4, -2, -1, 1, 2, 4]), 2, 50)
        oversold = clamp_float(float(params["oversold"]) + rng.choice([-5.0, -2.5, 0.0, 2.5, 5.0]), 10.0, 45.0)
        overbought = clamp_float(float(params["overbought"]) + rng.choice([-5.0, -2.5, 0.0, 2.5, 5.0]), 55.0, 90.0)
        if oversold >= overbought:
            midpoint = (oversold + overbought) / 2.0
            oversold = max(10.0, midpoint - 10.0)
            overbought = min(90.0, midpoint + 10.0)
        params["oversold"] = round(oversold, 2)
        params["overbought"] = round(overbought, 2)
    elif strategy == "multi_timeframe_ma_spread":
        primary = clamp_int(int(params["primary_ma_period"]) + rng.choice([-5, -3, -1, 1, 3, 5]), 2, 80)
        reference = clamp_int(int(params["reference_ma_period"]) + rng.choice([-10, -5, -2, 2, 5, 10]), 2, 120)
        params["primary_ma_period"] = primary
        params["reference_ma_period"] = reference
        params["spread_threshold_bps"] = round(
            clamp_float(float(params["spread_threshold_bps"]) + rng.choice([-10.0, -5.0, 0.0, 5.0, 10.0, 20.0]), 0.0, 100.0),
            2,
        )
    elif strategy == "donchian_breakout":
        params["lookback_window"] = clamp_int(int(params["lookback_window"]) + rng.choice([-10, -5, -2, 2, 5, 10]), 5, 120)
        params["breakout_buffer_bps"] = round(
            clamp_float(float(params["breakout_buffer_bps"]) + rng.choice([-10.0, -5.0, 0.0, 5.0, 10.0, 20.0]), 0.0, 100.0),
            2,
        )
    elif strategy == "adx_trend_strength":
        params["period"] = clamp_int(int(params["period"]) + rng.choice([-4, -2, -1, 1, 2, 4]), 2, 50)
        params["adx_threshold"] = round(
            clamp_float(float(params["adx_threshold"]) + rng.choice([-5.0, -2.5, 0.0, 2.5, 5.0]), 10.0, 60.0),
            2,
        )
    elif strategy == "atr_breakout":
        params["ma_period"] = clamp_int(int(params["ma_period"]) + rng.choice([-10, -5, -2, 2, 5, 10]), 5, 120)
        params["atr_period"] = clamp_int(int(params["atr_period"]) + rng.choice([-4, -2, -1, 1, 2, 4]), 2, 50)
        params["atr_multiplier"] = round(
            clamp_float(float(params["atr_multiplier"]) + rng.choice([-0.5, -0.25, 0.0, 0.25, 0.5]), 0.5, 5.0),
            2,
        )
    elif strategy == "bollinger_mean_reversion":
        params["period"] = clamp_int(int(params["period"]) + rng.choice([-10, -5, -2, 2, 5, 10]), 5, 120)
        params["stddev_multiplier"] = round(
            clamp_float(float(params["stddev_multiplier"]) + rng.choice([-0.5, -0.25, 0.0, 0.25, 0.5]), 1.0, 4.0),
            2,
        )
    elif strategy == "macd_trend_follow":
        fast = clamp_int(int(params["fast_period"]) + rng.choice([-3, -2, -1, 1, 2, 3]), 2, 30)
        slow = clamp_int(int(params["slow_period"]) + rng.choice([-8, -5, -2, 2, 5, 8]), 5, 80)
        if slow <= fast:
            slow = fast + rng.randint(2, 20)
        params["fast_period"] = fast
        params["slow_period"] = slow
        params["signal_period"] = clamp_int(int(params["signal_period"]) + rng.choice([-3, -2, -1, 1, 2, 3]), 2, 30)
        params["histogram_threshold"] = round(
            clamp_float(float(params["histogram_threshold"]) + rng.choice([-0.0005, -0.0002, 0.0, 0.0002, 0.0005]), 0.0, 0.02),
            6,
        )
    else:
        raise ValueError(f"unsupported strategy family for mutation: {strategy}")

    return StrategyCandidate(
        candidate_id=f"r{round_index}_c{child_index:02d}",
        strategy=strategy,
        params=params,
        origin="mutation",
        parent_ids=[parent.candidate_id],
    )


def build_population_from_survivors(
    survivors: Sequence[CandidateResult],
    *,
    round_index: int,
    population_size: int,
    rng: random.Random,
) -> List[StrategyCandidate]:
    population: List[StrategyCandidate] = []
    seen = set()

    for child_index, survivor in enumerate(survivors, start=1):
        elite = StrategyCandidate(
            candidate_id=f"r{round_index}_c{child_index:02d}",
            strategy=survivor.strategy,
            params=copy.deepcopy(survivor.params),
            origin="elite",
            parent_ids=[survivor.candidate_id],
        )
        population.append(elite)
        seen.add(candidate_signature(elite))

    child_index = len(population) + 1
    while len(population) < population_size:
        parent = survivors[(child_index - 1) % len(survivors)]
        mutated = mutate_candidate(
            StrategyCandidate(
                candidate_id=parent.candidate_id,
                strategy=parent.strategy,
                params=copy.deepcopy(parent.params),
                origin=parent.origin,
                parent_ids=copy.deepcopy(parent.parent_ids),
            ),
            round_index=round_index,
            child_index=child_index,
            rng=rng,
        )
        signature = candidate_signature(mutated)
        if signature in seen:
            continue
        population.append(mutated)
        seen.add(signature)
        child_index += 1

    return population


def compute_win_rate(trades: Sequence[dict]) -> float | None:
    if not trades:
        return None
    closed = []
    open_trade = None
    for trade in trades:
        action = trade.get("action")
        if action in {"open_long", "open_short", "flip_to_long", "flip_to_short"}:
            if open_trade is not None and action.startswith("flip_"):
                closed.append((open_trade, trade))
            open_trade = trade
        elif action in {"close_long", "cover_short"} and open_trade is not None:
            closed.append((open_trade, trade))
            open_trade = None
    if not closed:
        return None

    wins = 0
    for entry, exit_trade in closed:
        entry_price = float(entry["price"])
        exit_price = float(exit_trade["price"])
        quantity = float(exit_trade["quantity"])
        fees = float(entry.get("fee", 0.0)) + float(exit_trade.get("fee", 0.0))
        if entry["side"] == "buy":
            pnl = (exit_price - entry_price) * quantity - fees
        else:
            pnl = (entry_price - exit_price) * quantity - fees
        if pnl > 0:
            wins += 1
    return wins / len(closed)


def create_request(
    candidate: StrategyCandidate,
    *,
    symbol: str,
    primary_timeframe: str,
    secondary_timeframe: str,
    start_ts: int,
    end_ts: int,
    initial_capital: float,
    taker_fee_bps: float,
    slippage_bps: float,
    impact_slippage_bps: float,
    max_bar_volume_fraction: float,
) -> BacktestRequest:
    pipeline = build_strategy_pipeline(
        strategy=candidate.strategy,
        symbol=symbol,
        interval=primary_timeframe,
        secondary_interval=secondary_timeframe,
        fast_window=int(candidate.params.get("fast_window", 5)),
        slow_window=int(candidate.params.get("slow_window", 20)),
        entry_threshold=float(candidate.params.get("entry_threshold", 0.0)),
        ma_period=int(candidate.params.get("period", 5)),
        rsi_period=int(candidate.params.get("period", 14)),
        oversold=float(candidate.params.get("oversold", 30.0)),
        overbought=float(candidate.params.get("overbought", 70.0)),
        donchian_window=int(candidate.params.get("lookback_window", 20)),
        breakout_buffer_bps=float(candidate.params.get("breakout_buffer_bps", 0.0)),
        adx_period=int(candidate.params.get("period", 14)),
        adx_threshold=float(candidate.params.get("adx_threshold", 25.0)),
        atr_ma_period=int(candidate.params.get("ma_period", 20)),
        atr_period=int(candidate.params.get("atr_period", 14)),
        atr_multiplier=float(candidate.params.get("atr_multiplier", 2.0)),
        bollinger_period=int(candidate.params.get("period", 20)),
        bollinger_stddev_multiplier=float(candidate.params.get("stddev_multiplier", 2.0)),
        macd_fast_period=int(candidate.params.get("fast_period", 12)),
        macd_slow_period=int(candidate.params.get("slow_period", 26)),
        macd_signal_period=int(candidate.params.get("signal_period", 9)),
        macd_histogram_threshold=float(candidate.params.get("histogram_threshold", 0.0)),
        primary_ma_period=int(candidate.params.get("primary_ma_period", 20)),
        reference_ma_period=int(candidate.params.get("reference_ma_period", 20)),
        spread_threshold_bps=float(candidate.params.get("spread_threshold_bps", 0.0)),
    )
    return BacktestRequest(
        request_id=str(uuid.uuid4()),
        instruments=[symbol],
        primary_timeframe=primary_timeframe,
        start_ts=start_ts,
        end_ts=end_ts,
        signal_pipeline=pipeline,
        initial_capital=initial_capital,
        fee_model={
            "commission_bps": taker_fee_bps,
            "taker_fee_bps": taker_fee_bps,
            "funding_bps_per_bar": 0.0,
        },
        slippage_model={
            "slippage_bps": slippage_bps,
            "impact_slippage_bps": impact_slippage_bps,
            "max_bar_volume_fraction": max_bar_volume_fraction,
        },
        extras={"engine": "numba", "experiment": "llm_strategy_evolution"},
    )


def to_serializable_result(result: CandidateResult, *, win_rate: float | None) -> Dict:
    payload = asdict(result)
    payload["win_rate"] = win_rate
    return payload


def select_survivors_with_family_cap(
    ranked_internal: Sequence[tuple[CandidateResult, float | None]],
    *,
    survivor_count: int,
    family_cap: int,
) -> List[tuple[CandidateResult, float | None]]:
    family_counts: Dict[str, int] = {}
    selected: List[tuple[CandidateResult, float | None]] = []

    for item in ranked_internal:
        strategy = item[0].strategy
        current_count = family_counts.get(strategy, 0)
        if current_count >= family_cap:
            continue
        selected.append(item)
        family_counts[strategy] = current_count + 1
        if len(selected) >= survivor_count:
            break

    return selected


def write_round_report(path: Path, *, round_payload: Dict, selected_payload: Sequence[Dict]) -> None:
    family_cap = round_payload.get("family_cap")
    lines = [
        f"# Round {round_payload['round']} Top {len(selected_payload)} Report",
        "",
        f"- Population size: `{round_payload['population_size']}`",
        f"- Family cap: `{family_cap}`",
        "",
        "| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for rank, candidate in enumerate(selected_payload, start=1):
        lines.append(
            "| %s | `%s` | `%s` | %.4f | %.4f%% | %.4f%% | %s | `%s` |"
            % (
                rank,
                candidate["candidate_id"],
                candidate["strategy"],
                candidate["sharpe_ratio"],
                candidate["total_return"] * 100.0,
                candidate["max_drawdown"] * 100.0,
                candidate["trade_count"],
                json.dumps(candidate["params"], ensure_ascii=False, sort_keys=True),
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_round_artifacts(
    round_dir: Path,
    *,
    round_payload: Dict,
    selected_payload: Sequence[Dict],
) -> None:
    round_dir.mkdir(parents=True, exist_ok=True)
    candidates_dir = round_dir / "candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)

    selected_ids = {candidate["candidate_id"] for candidate in selected_payload}
    ranked_with_flags: List[Dict] = []
    for rank, candidate in enumerate(round_payload["ranked"], start=1):
        candidate_payload = copy.deepcopy(candidate)
        candidate_payload["rank"] = rank
        candidate_payload["selected_for_next_round"] = candidate["candidate_id"] in selected_ids
        ranked_with_flags.append(candidate_payload)
        candidate_path = candidates_dir / f"rank_{rank:02d}_{candidate['candidate_id']}.json"
        candidate_path.write_text(json.dumps(candidate_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    (round_dir / "ranked_all.json").write_text(
        json.dumps(ranked_with_flags, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (round_dir / "selected_top20.json").write_text(
        json.dumps(list(selected_payload), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    round_summary = {
        "round": round_payload["round"],
        "population_size": round_payload["population_size"],
        "family_cap": round_payload["family_cap"],
        "selected_count": len(selected_payload),
        "selected_candidate_ids": [candidate["candidate_id"] for candidate in selected_payload],
    }
    (round_dir / "round_summary.json").write_text(
        json.dumps(round_summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_round_report(
        round_dir / f"top{len(selected_payload)}_report.md",
        round_payload=round_payload,
        selected_payload=selected_payload,
    )


def write_markdown(
    path: Path,
    *,
    rounds_payload: List[Dict],
    best_overall: Dict,
    symbol: str,
    primary_timeframe: str,
    secondary_timeframe: str,
) -> None:
    lines = [
        "# LLM Strategy Evolution",
        "",
        f"- Symbol: `{symbol}`",
        f"- Primary timeframe: `{primary_timeframe}`",
        f"- Secondary timeframe: `{secondary_timeframe}`",
        f"- Rounds: `{len(rounds_payload)}`",
        f"- Best strategy: `{best_overall['strategy']}`",
        f"- Best Sharpe: `{best_overall['sharpe_ratio']:.4f}`",
        f"- Best total return: `{best_overall['total_return']:.4%}`",
        f"- Best max drawdown: `{best_overall['max_drawdown']:.4%}`",
        f"- Best trade count: `{best_overall['trade_count']}`",
        "",
    ]
    for round_payload in rounds_payload:
        lines.extend(
            [
                f"## Round {round_payload['round']}",
                "",
                "| Rank | Candidate | Strategy | Sharpe | Return | Max DD | Trades | Params |",
                "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
            ]
        )
        for index, candidate in enumerate(round_payload["ranked"], start=1):
            lines.append(
                "| %s | `%s` | `%s` | %.4f | %.4f%% | %.4f%% | %s | `%s` |"
                % (
                    index,
                    candidate["candidate_id"],
                    candidate["strategy"],
                    candidate["sharpe_ratio"],
                    candidate["total_return"] * 100.0,
                    candidate["max_drawdown"] * 100.0,
                    candidate["trade_count"],
                    json.dumps(candidate["params"], ensure_ascii=False, sort_keys=True),
                )
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_candidate_csv(path: Path, *, rounds_payload: Sequence[Dict]) -> None:
    fieldnames = [
        "round",
        "rank",
        "candidate_id",
        "strategy",
        "origin",
        "parent_ids",
        "is_survivor",
        "sharpe_ratio",
        "total_return",
        "max_drawdown",
        "trade_count",
        "signal_count",
        "final_equity",
        "win_rate",
        "params_json",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for round_payload in rounds_payload:
            survivor_ids = set(round_payload["survivors"])
            for rank, candidate in enumerate(round_payload["ranked"], start=1):
                writer.writerow(
                    {
                        "round": round_payload["round"],
                        "rank": rank,
                        "candidate_id": candidate["candidate_id"],
                        "strategy": candidate["strategy"],
                        "origin": candidate["origin"],
                        "parent_ids": "|".join(candidate["parent_ids"]),
                        "is_survivor": candidate["candidate_id"] in survivor_ids,
                        "sharpe_ratio": candidate["sharpe_ratio"],
                        "total_return": candidate["total_return"],
                        "max_drawdown": candidate["max_drawdown"],
                        "trade_count": candidate["trade_count"],
                        "signal_count": candidate["signal_count"],
                        "final_equity": candidate["final_equity"],
                        "win_rate": candidate["win_rate"],
                        "params_json": json.dumps(candidate["params"], ensure_ascii=False, sort_keys=True),
                    }
                )


def main() -> int:
    args = build_parser().parse_args()
    if args.survivors <= 0:
        raise ValueError("--survivors must be positive")
    if args.population_size <= args.survivors:
        raise ValueError("--population-size must be greater than --survivors")
    if args.family_cap <= 0:
        raise ValueError("--family-cap must be positive")

    rng = random.Random(args.seed)

    data_root = Path(args.historical_dir)
    history_path = build_history_path(str(data_root), args.market_type, args.symbol.upper(), "1m")
    if not history_path.exists():
        raise FileNotFoundError(f"missing local historical source: {history_path}")
    start_ts, end_ts = parquet_time_coverage(history_path)
    if start_ts is None or end_ts is None:
        raise RuntimeError(f"unable to determine parquet coverage for {history_path}")
    safe_query_start_ts = int(start_ts) + max(
        timeframe_to_ms(args.primary_timeframe),
        timeframe_to_ms(args.secondary_timeframe),
    )

    adapter = HistoricalParquetMarketDataAdapter(
        data_root=str(data_root),
        market_type=args.market_type,
        resample_source_timeframe="1m",
    )
    market_bundle = adapter.fetch_market(
        MarketQuery(
            instruments=[args.symbol.upper()],
            timeframes=[args.primary_timeframe, args.secondary_timeframe],
            time_range=TimeRange(start_ts=safe_query_start_ts, end_ts=int(end_ts)),
        )
    )

    primary_key = market_bundle.key(args.symbol.upper(), args.primary_timeframe)
    primary_bars = market_bundle.bars.get(primary_key, [])
    if not primary_bars:
        raise RuntimeError(f"no bars loaded for {primary_key}")

    backtest_start_ts = int(primary_bars[0].timestamp)
    backtest_end_ts = int(primary_bars[-1].timestamp)
    runner = NumbaBacktestRunner()

    seed_source = None
    if args.seed_json:
        seed_json_path = Path(args.seed_json)
        seed_results = load_seed_results(seed_json_path, seed_round=args.seed_round, seed_top_k=args.seed_top_k or args.survivors)
        population = generate_population_from_seed_results(
            seed_results,
            population_size=args.population_size,
            rng=rng,
        )
        seed_source = {
            "seed_json": str(seed_json_path),
            "seed_round": args.seed_round,
            "seed_top_k": args.seed_top_k or args.survivors,
        }
    else:
        population = generate_initial_population(args.population_size, rng=rng)
    rounds_payload: List[Dict] = []
    best_overall: Dict | None = None

    output_root_path = Path(args.output_root) if args.output_root else None
    if output_root_path is not None:
        output_root_path.mkdir(parents=True, exist_ok=True)

    for round_index in range(1, args.rounds + 1):
        ranked_internal: List[tuple[CandidateResult, float | None]] = []

        for candidate in population:
            request = create_request(
                candidate,
                symbol=args.symbol.upper(),
                primary_timeframe=args.primary_timeframe,
                secondary_timeframe=args.secondary_timeframe,
                start_ts=backtest_start_ts,
                end_ts=backtest_end_ts,
                initial_capital=args.initial_capital,
                taker_fee_bps=args.taker_fee_bps,
                slippage_bps=args.slippage_bps,
                impact_slippage_bps=args.impact_slippage_bps,
                max_bar_volume_fraction=args.max_bar_volume_fraction,
            )
            result = runner.run(request=request, market_bundle=market_bundle)
            trades = result.extras.get("trades", [])
            win_rate = compute_win_rate(trades)
            sharpe = float(result.metrics.get("sharpe_ratio", float("-inf")))
            if math.isnan(sharpe):
                sharpe = float("-inf")
            candidate_result = CandidateResult(
                candidate_id=candidate.candidate_id,
                strategy=candidate.strategy,
                params=copy.deepcopy(candidate.params),
                origin=candidate.origin,
                parent_ids=copy.deepcopy(candidate.parent_ids),
                sharpe_ratio=sharpe,
                total_return=float(result.metrics.get("total_return", result.total_return)),
                max_drawdown=float(result.metrics.get("max_drawdown", 0.0)),
                trade_count=int(result.metrics.get("trade_count", 0.0)),
                signal_count=int(result.metrics.get("signal_count", 0.0)),
                final_equity=float(result.metrics.get("final_equity", args.initial_capital)),
            )
            ranked_internal.append((candidate_result, win_rate))

        ranked_internal.sort(
            key=lambda item: (
                item[0].sharpe_ratio,
                item[0].total_return,
                -item[0].max_drawdown,
                -item[0].trade_count,
            ),
            reverse=True,
        )
        evaluated = [to_serializable_result(result, win_rate=win_rate) for result, win_rate in ranked_internal]
        selected_internal = select_survivors_with_family_cap(
            ranked_internal,
            survivor_count=args.survivors,
            family_cap=args.family_cap,
        )
        if len(selected_internal) < args.survivors:
            raise RuntimeError(
                "unable to select %s survivors under family cap %s; only %s candidates satisfied the cap"
                % (args.survivors, args.family_cap, len(selected_internal))
            )
        selected_payload = [to_serializable_result(result, win_rate=win_rate) for result, win_rate in selected_internal]
        survivors = [result for result, _ in selected_internal]
        round_payload = {
            "round": round_index,
            "population_size": len(population),
            "family_cap": args.family_cap,
            "ranked": evaluated,
            "survivors": [item["candidate_id"] for item in selected_payload],
            "selected_top20": selected_payload,
        }
        rounds_payload.append(round_payload)

        if output_root_path is not None:
            write_round_artifacts(
                output_root_path / f"round{round_index}",
                round_payload=round_payload,
                selected_payload=selected_payload,
            )

        if best_overall is None or evaluated[0]["sharpe_ratio"] > best_overall["sharpe_ratio"]:
            best_overall = copy.deepcopy(evaluated[0])

        if round_index < args.rounds:
            population = build_population_from_survivors(
                survivors,
                round_index=round_index + 1,
                population_size=args.population_size,
                rng=rng,
            )

    output_payload = {
        "experiment": {
            "symbol": args.symbol.upper(),
            "market_type": args.market_type,
            "primary_timeframe": args.primary_timeframe,
            "secondary_timeframe": args.secondary_timeframe,
            "rounds": args.rounds,
            "population_size": args.population_size,
            "survivors": args.survivors,
            "seed": args.seed,
            "initial_capital": args.initial_capital,
            "family_cap": args.family_cap,
            "taker_fee_bps": args.taker_fee_bps,
            "slippage_bps": args.slippage_bps,
            "impact_slippage_bps": args.impact_slippage_bps,
            "max_bar_volume_fraction": args.max_bar_volume_fraction,
            "history_path": str(history_path),
            "backtest_start_ts": backtest_start_ts,
            "backtest_end_ts": backtest_end_ts,
            "seed_source": seed_source,
            "output_root": None if output_root_path is None else str(output_root_path),
        },
        "rounds": rounds_payload,
        "best_overall": best_overall,
    }

    output_json_path = (output_root_path / "experiment_summary.json") if output_root_path is not None else Path(args.output_json)
    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    output_json_path.write_text(json.dumps(output_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    output_md_path = (output_root_path / "experiment_summary.md") if output_root_path is not None else Path(args.output_md)
    output_md_path.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(
        output_md_path,
        rounds_payload=rounds_payload,
        best_overall=best_overall or {},
        symbol=args.symbol.upper(),
        primary_timeframe=args.primary_timeframe,
        secondary_timeframe=args.secondary_timeframe,
    )

    output_csv_path = (output_root_path / "candidates_long.csv") if output_root_path is not None else Path(args.output_csv)
    write_candidate_csv(output_csv_path, rounds_payload=rounds_payload)

    print("wrote_json=%s" % output_json_path)
    print("wrote_md=%s" % output_md_path)
    print("wrote_csv=%s" % output_csv_path)
    if best_overall is not None:
        print(
            "best=%s strategy=%s sharpe=%.4f total_return=%.4f max_drawdown=%.4f trades=%s"
            % (
                best_overall["candidate_id"],
                best_overall["strategy"],
                best_overall["sharpe_ratio"],
                best_overall["total_return"],
                best_overall["max_drawdown"],
                best_overall["trade_count"],
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
