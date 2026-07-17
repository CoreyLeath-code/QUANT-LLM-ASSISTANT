"""Plotting utilities that do not leak figure resources."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import matplotlib.pyplot as plt


def _finish(fig: Any, save_path: str | None, show: bool) -> None:
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path)
    if show:
        plt.show()
    plt.close(fig)


def plot_time_series(
    dates: Sequence[Any], values: Sequence[float], title: str = "", xlabel: str = "Date",
    ylabel: str = "Value", save_path: str | None = None, *, show: bool = False,
) -> None:
    if len(dates) != len(values) or not values:
        raise ValueError("dates and values must be non-empty and have equal lengths")
    fig, axis = plt.subplots()
    axis.plot(dates, values, marker="o")
    axis.set(title=title, xlabel=xlabel, ylabel=ylabel)
    axis.grid(True)
    _finish(fig, save_path, show)


def plot_histogram(
    values: Sequence[float], bins: int = 20, title: str = "", xlabel: str = "Value",
    ylabel: str = "Frequency", save_path: str | None = None, *, show: bool = False,
) -> None:
    if not values or bins < 1:
        raise ValueError("values must be non-empty and bins must be positive")
    fig, axis = plt.subplots()
    axis.hist(values, bins=bins)
    axis.set(title=title, xlabel=xlabel, ylabel=ylabel)
    axis.grid(True)
    _finish(fig, save_path, show)
