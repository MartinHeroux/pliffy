from typing import Literal, Tuple

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.axes._subplots import Subplot

from pliffy.figure import Figure
from pliffy import parser


EXTRA_Y_TICKS = 3


class FigureAB(Figure):
    """Class to manage plotting AB part of ABD figure

    Parameters
    ----------
    info: FigureInfoAB
        Namedtuple containing parsed data and details to plot AB part of figure
    ax: Subplot
        Matplotlib axis object

    """

    def __init__(self, info: "parser.FigureInfoAB", ax: Subplot = None):
        matplotlib.rcParams.update({"font.size": info.fontsize})
        self.info = info
        if ax is None:
            ax = self._make_figure_axis()
            self.show = True
        self.ax = ax
        self.min_raw_data = self._min_raw_data()
        self.max_raw_data = self._max_raw_data()
        self._plot()
        self.ytick_step, self.yticks = self._tweak_yaxis()

    def _make_figure_axis(self) -> Subplot:
        width_height_in_inches = self.info.width_height_in_inches
        ax = plt.subplots(figsize=width_height_in_inches)[1]
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
        """Find yticks that include all raw data points"""
        current_yticks = self.ax.get_yticks()
        ytick_step = current_yticks[1] - current_yticks[0]
        conservative_yticks = self._gen_conservative_yticks(current_yticks, ytick_step)
        min_ytick = self._find_min_ytick(conservative_yticks)
        max_ytick = self._find_max_ytick(conservative_yticks)
        optimised_yticks = self._gen_optimised_yticks(min_ytick, max_ytick, ytick_step)
        self._set_yticks(optimised_yticks)
        return ytick_step, optimised_yticks

    def _gen_conservative_yticks(self, current_yticks, ytick_step):
        """Add three extra ytick at either end"""
        return tuple(
            np.arange(
                current_yticks[0] - ytick_step * EXTRA_Y_TICKS,
                current_yticks[-1] + EXTRA_Y_TICKS * ytick_step,
                ytick_step,
            )
        )

    def _find_min_ytick(self, conservative_yticks: Tuple[float]) -> float:
        """Find min ytick that includes all raw data point"""
        min_ytick = float()
        for tick in reversed(conservative_yticks):
            if self.min_raw_data > tick:
                min_ytick = tick
                break
        return min_ytick

    def _find_max_ytick(self, conservative_yticks: Tuple[float]) -> float:
        """Find max ytick that includes all raw data point"""
        max_ytick = float()
        for tick in conservative_yticks:
            if self.max_raw_data < tick:
                max_ytick = tick
                break
        return max_ytick

    def _gen_optimised_yticks(self, min_ytick, max_ytick, ytick_step):
        return tuple(np.arange(min_ytick, max_ytick + ytick_step, ytick_step))
