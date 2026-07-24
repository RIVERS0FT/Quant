"""Tests for Week 9 Day 5 performance metrics."""

import math

import numpy as np
import pandas as pd
import pytest

from performance_metrics_day05 import (
    align_return_series,
    calmar_ratio,
    information_ratio,
    maximum_drawdown_from_returns,
    relative_performance_tables,
)


def test_calmar_known_result() -> None:
    returns = pd.Series([0.10, -0.20, 0.25])
    result = calmar_ratio(returns, periods_per_year=3)
    assert np.isclose(result, 0.50)


def test_first_period_loss_is_drawdown() -> None:
    returns = pd.Series([-0.20, 0.25])
    result = maximum_drawdown_from_returns(returns)
    assert np.isclose(result, -0.20)


def test_zero_drawdown_calmar_is_nan() -> None:
    returns = pd.Series([0.01, 0.01, 0.01])
    result = calmar_ratio(returns, periods_per_year=3)
    assert math.isnan(result)


def test_relative_metrics_known_result() -> None:
    dates = pd.date_range("2026-01-31", periods=4, freq="ME")
    strategy = pd.Series([0.10, -0.05, 0.08, 0.02], index=dates)
    benchmark = pd.Series([0.06, -0.03, 0.05, 0.01], index=dates)

    _, relative = relative_performance_tables(
        strategy,
        benchmark,
        periods_per_year=12,
    )

    assert np.isclose(
        relative.loc["cumulative_return_difference", "value"],
        0.0607659,
    )
    assert np.isclose(
        relative.loc["relative_wealth_return", "value"],
        0.0557277696814058,
    )
    assert np.isclose(
        relative.loc["tracking_error", "value"],
        0.0916515138991168,
    )


def test_duplicate_index_raises() -> None:
    date = pd.Timestamp("2026-01-05")
    strategy = pd.Series([0.01, 0.02], index=[date, date])
    benchmark = pd.Series([0.00], index=[date])

    with pytest.raises(ValueError):
        align_return_series(strategy, benchmark)


def test_no_common_dates_raises() -> None:
    strategy = pd.Series(
        [0.01],
        index=[pd.Timestamp("2026-01-05")],
    )
    benchmark = pd.Series(
        [0.00],
        index=[pd.Timestamp("2026-01-06")],
    )

    with pytest.raises(ValueError):
        align_return_series(strategy, benchmark)


def test_zero_tracking_error_information_ratio_is_nan() -> None:
    strategy = pd.Series([0.02, 0.02, 0.02])
    benchmark = pd.Series([0.01, 0.01, 0.01])
    result = information_ratio(strategy, benchmark, periods_per_year=3)
    assert math.isnan(result)
