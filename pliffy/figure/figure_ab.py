from typing import Literal, Tuple

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.axes._subplots import Subplot

from pliffy.figure import Figure
from pliffy import parser

# TODO: Add documentation and tests
DPI = 600
WIDTH_HEIGHT_IN_INCHES = (8.2 / 2.54, 8.2 / 2.54)
EXTRA_Y_TICKS = 3


class FigureAB(Figure):
    def __init__(self, info: "parser.ABFigureInfo", ax: Subplot = None):
        self.info = info
        matplotlib.rcParams.update({"font.size": info.fontsize})
        if ax is None:
            ax = self._make_figure_axis()
            self.show = True
        self.ax = ax
        self.min_raw_data = self._min_raw_data()
        self.max_raw_data = self._max_raw_data()
        self._plot()
        self.ytick_step, self.yticks = self._tweak_yaxis()

    def _make_figure_axis(self) -> Subplot:
        width_height_in_inches = WIDTH_HEIGHT_IN_INCHES
        _, ax = plt.subplots(figsize=width_height_in_inches, dpi=DPI)
        return ax

    def _min_raw_data(self) -> float:
        return min(min(self.info.raw_a.data), min(self.info.raw_b.data))

    def _max_raw_data(self) -> float:
        return max(max(self.info.raw_a.data), max(self.info.raw_b.data))

    def _plot(self):
        self._plot_ab_raw_data()
        self._plot_ab_means_cis()
        self._tweak_xaxis()

    def _plot_ab_means_cis(self):
        self._plot_mean_ci(self.info.mean_a, self.info.ci_a)
        self._plot_mean_ci(self.info.mean_b, self.info.ci_b)

    def _plot_ab_raw_data(self):
        if self._data_paired_and_want_lines():
            self._plot_paired_lines(self.info.paired_lines)
        else:
            self._plot_raw_data(self.info.raw_a)
            self._plot_raw_data(self.info.raw_b)

    def _data_paired_and_want_lines(self) -> Literal[True, False]:
        return (self.info.design == "paired") and self.info.plot_paired_lines

    def _tweak_xaxis(self):
        self._remove_ax_spine("top")
        self._set_xlim(self.info.xlim)
        self._set_xticks(self.info.xticks)

    def _tweak_yaxis(self):
        self._remove_ax_spine("right")
        self._set_ylabel(self.info.ylabel)
        ytick_step, yticks = self._optimise_yticks()
        self._set_ylim((yticks[0], yticks[-1]))
        return ytick_step, yticks

    def _optimise_yticks(self) -> Tuple[float, Tuple[float]]:
        current_yticks = self.ax.get_yticks()
        ytick_step = current_yticks[1] - current_yticks[0]
        conservative_yticks = tuple(
            np.arange(
                current_yticks[0] - ytick_step * EXTRA_Y_TICKS,
                current_yticks[-1] + EXTRA_Y_TICKS * ytick_step,
                ytick_step,
            )
        )
        min_ytick = self._min_ytick(conservative_yticks)
        max_ytick = self._max_ytick(conservative_yticks)
        yticks = tuple(
            np.arange(min_ytick, max_ytick + ytick_step, ytick_step)
        )
        self._set_yticks(yticks)
        return ytick_step, yticks

    def _min_ytick(self, conservative_yticks: Tuple[float]) -> float:
        min_ytick = float()
        for tick in reversed(conservative_yticks):
            if self.min_raw_data > tick:
                min_ytick = tick
                break
        return min_ytick

    def _max_ytick(self, conservative_yticks: Tuple[float]) -> float:
        max_ytick = float()
        for tick in conservative_yticks:
            if self.max_raw_data < tick:
                max_ytick = tick
                break
        return max_ytick
