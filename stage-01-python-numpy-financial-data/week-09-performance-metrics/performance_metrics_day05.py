from __future__ import annotations

import math
import numpy as np
import pandas as pd


def _clean(values: pd.Series, name: str) -> pd.Series:
    """清洗简单收益率序列。"""
    result = pd.Series(values, dtype="float64", copy=True, name=name)
    if result.index.has_duplicates:
        raise ValueError(f"{name} 的索引不能重复")
    result = result.sort_index().dropna()
    if result.empty:
        raise ValueError(f"{name} 不能为空")
    if not np.isfinite(result.to_numpy()).all():
        raise ValueError(f"{name} 必须为有限数")
    if (result < -1.0).any():
        raise ValueError(f"{name} 不能小于 -100%")
    return result


def align_return_series(
    strategy_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> pd.DataFrame:
    """按共同索引对齐策略和基准。"""
    strategy = _clean(strategy_returns, "strategy_return")
    benchmark = _clean(benchmark_returns, "benchmark_return")
    result = pd.concat([strategy, benchmark], axis=1, join="inner")
    if result.empty:
        raise ValueError("策略与基准没有共同有效日期")
    result.attrs.update(
        strategy_before_alignment=int(strategy.size),
        benchmark_before_alignment=int(benchmark.size),
        matched_observations=int(result.shape[0]),
    )
    return result


def annualized_return(
    returns: pd.Series,
    periods_per_year: int = 252,
) -> float:
    """计算几何年化收益。"""
    clean = _clean(returns, "return")
    if periods_per_year <= 0:
        raise ValueError("periods_per_year 必须为正数")
    growth = float((1.0 + clean).prod())
    return -1.0 if growth == 0.0 else growth ** (
        periods_per_year / clean.size
    ) - 1.0


def wealth_values_from_returns(
    returns: pd.Series,
    initial_nav: float = 1.0,
) -> np.ndarray:
    """构造包含期初点的财富序列。"""
    clean = _clean(returns, "return")
    if not np.isfinite(initial_nav) or initial_nav <= 0.0:
        raise ValueError("initial_nav 必须为有限正数")
    ending = initial_nav * np.cumprod(1.0 + clean.to_numpy())
    return np.r_[initial_nav, ending]


def _maximum_drawdown(values: np.ndarray) -> float:
    values = np.asarray(values, dtype="float64")
    if values.size == 0 or not np.isfinite(values).all():
        raise ValueError("财富序列必须包含有限数")
    if values[0] <= 0.0 or (values < 0.0).any():
        raise ValueError("财富序列口径错误")
    peaks = np.maximum.accumulate(values)
    return float((values / peaks - 1.0).min())


def maximum_drawdown_from_returns(returns: pd.Series) -> float:
    """从收益率计算带符号最大回撤。"""
    return _maximum_drawdown(wealth_values_from_returns(returns))


def calmar_ratio(
    returns: pd.Series,
    periods_per_year: int = 252,
    zero_tolerance: float = 1e-12,
) -> float:
    """计算 Calmar 比率。"""
    if zero_tolerance < 0.0:
        raise ValueError("zero_tolerance 不能为负数")
    clean = _clean(returns, "return")
    annual = annualized_return(clean, periods_per_year)
    magnitude = -maximum_drawdown_from_returns(clean)
    return float("nan") if magnitude <= zero_tolerance else annual / magnitude


def active_return_series(
    strategy_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> pd.Series:
    """计算逐期主动收益。"""
    aligned = align_return_series(strategy_returns, benchmark_returns)
    return (
        aligned["strategy_return"] - aligned["benchmark_return"]
    ).rename("active_return")


def relative_wealth_series(
    strategy_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> pd.Series:
    """计算相对财富序列。"""
    aligned = align_return_series(strategy_returns, benchmark_returns)
    benchmark = aligned["benchmark_return"]
    if (benchmark <= -1.0).any():
        raise ValueError("基准收益为 -100% 时相对净值无定义")
    ratio = (1.0 + aligned["strategy_return"]) / (1.0 + benchmark)
    return ratio.cumprod().rename("relative_wealth")


def tracking_error(
    strategy_returns: pd.Series,
    benchmark_returns: pd.Series,
    periods_per_year: int = 252,
) -> float:
    """计算年化跟踪误差。"""
    if periods_per_year <= 0:
        raise ValueError("periods_per_year 必须为正数")
    active = active_return_series(strategy_returns, benchmark_returns)
    if active.size < 2:
        return float("nan")
    return float(active.std(ddof=1) * math.sqrt(periods_per_year))


def information_ratio(
    strategy_returns: pd.Series,
    benchmark_returns: pd.Series,
    periods_per_year: int = 252,
    zero_tolerance: float = 1e-12,
) -> float:
    """计算年化信息比率。"""
    if periods_per_year <= 0:
        raise ValueError("periods_per_year 必须为正数")
    active = active_return_series(strategy_returns, benchmark_returns)
    if active.size < 2:
        return float("nan")
    active_std = float(active.std(ddof=1))
    if active_std <= zero_tolerance:
        return float("nan")
    return float(
        active.mean() / active_std * math.sqrt(periods_per_year)
    )


def relative_performance_tables(
    strategy_returns: pd.Series,
    benchmark_returns: pd.Series,
    periods_per_year: int = 252,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """生成策略、基准和相对绩效表。"""
    aligned = align_return_series(strategy_returns, benchmark_returns)
    strategy = aligned["strategy_return"]
    benchmark = aligned["benchmark_return"]
    active = strategy - benchmark
    n = int(aligned.shape[0])

    strategy_growth = float((1.0 + strategy).prod())
    benchmark_growth = float((1.0 + benchmark).prod())
    strategy_cum = strategy_growth - 1.0
    benchmark_cum = benchmark_growth - 1.0
    strategy_ann = annualized_return(strategy, periods_per_year)
    benchmark_ann = annualized_return(benchmark, periods_per_year)

    def absolute_metrics(returns: pd.Series) -> dict[str, float]:
        magnitude = -maximum_drawdown_from_returns(returns)
        return {
            "observations": float(n),
            "cumulative_return": float((1.0 + returns).prod() - 1.0),
            "annualized_return": annualized_return(
                returns, periods_per_year
            ),
            "max_drawdown_magnitude": magnitude,
            "calmar_ratio": calmar_ratio(returns, periods_per_year),
        }

    comparison = pd.DataFrame(
        {
            "strategy": absolute_metrics(strategy),
            "benchmark": absolute_metrics(benchmark),
        }
    )

    if benchmark_growth == 0.0:
        relative_return = relative_ann = relative_mdd = float("nan")
    else:
        relative_growth = strategy_growth / benchmark_growth
        relative_return = relative_growth - 1.0
        relative_ann = -1.0 if relative_growth == 0.0 else (
            relative_growth ** (periods_per_year / n) - 1.0
        )
        relative_values = np.r_[
            1.0,
            relative_wealth_series(strategy, benchmark).to_numpy(),
        ]
        relative_mdd = -_maximum_drawdown(relative_values)

    active_std = float(active.std(ddof=1)) if n >= 2 else float("nan")
    te = (
        active_std * math.sqrt(periods_per_year)
        if n >= 2 else float("nan")
    )
    ir = (
        float(active.mean()) / active_std * math.sqrt(periods_per_year)
        if n >= 2 and active_std > 1e-12 else float("nan")
    )

    relative = pd.Series(
        {
            "observations": n,
            "cumulative_return_difference": strategy_cum - benchmark_cum,
            "relative_wealth_return": relative_return,
            "annualized_return_difference": strategy_ann - benchmark_ann,
            "annualized_relative_wealth_return": relative_ann,
            "relative_max_drawdown_magnitude": relative_mdd,
            "tracking_error": te,
            "information_ratio": ir,
            "period_outperformance_rate": float((active > 0.0).mean()),
        },
        name="value",
        dtype="float64",
    ).to_frame()

    for table in (comparison, relative):
        table.attrs.update(
            periods_per_year=periods_per_year,
            start=aligned.index[0],
            end=aligned.index[-1],
            strategy_before_alignment=aligned.attrs[
                "strategy_before_alignment"
            ],
            benchmark_before_alignment=aligned.attrs[
                "benchmark_before_alignment"
            ],
            matched_observations=aligned.attrs["matched_observations"],
        )
    return comparison, relative
