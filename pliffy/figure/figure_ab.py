import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from pliffy.figure import Figure


class FigureAB(Figure):
    def __init__(self, info, ax=None):
        self.info = info
        matplotlib.rcParams.update({"font.size": info.fontsize})
        if ax is None:
            ax = self._make_figure_axis()
            self.show = True
        self.ax = ax
        self.min_raw_data = min(min(self.info.raw_a.data), min(self.info.raw_b.data))
        self.max_raw_data = max(max(self.info.raw_a.data), max(self.info.raw_b.data))
        self._plot()

    def _make_figure_axis(self):
        width_height_in_inches = (8.2 / 2.54, 8.2 / 2.54)
        _, ax = plt.subplots(figsize=width_height_in_inches, dpi=600)
        return ax

    def _plot(self):
        self._plot_ab_raw_data()
        self._plot_ab_means_cis()
        self._tweak_xaxis()
        self._tweak_yaxis()

    def _plot_ab_means_cis(self):
        self._plot_mean_ci(self.info.mean_a, self.info.ci_a)
        self._plot_mean_ci(self.info.mean_b, self.info.ci_b)

    def _plot_ab_raw_data(self):
        if self._data_paired_and_want_lines():
            self._plot_paired_lines(self.info.paired_lines)
        else:
            self._plot_raw_data(self.info.raw_a)
            self._plot_raw_data(self.info.raw_b)

    def _data_paired_and_want_lines(self):
        return (self.info.design == "paired") and self.info.plot_paired_lines

    def _tweak_xaxis(self):
        self._remove_ax_spine("top")
        self._set_xlim(self.info.xlim)
        self._set_xticks(self.info.xticks)

    def _tweak_yaxis(self):
        self._remove_ax_spine("right")
        self._set_ylabel(self.info.ylabel)
        self._optimise_yticks()
        self._set_ylim((self.yticks[0], self.yticks[-1]))

    def _optimise_yticks(self):
        current_yticks = self.ax.get_yticks()
        ytick_step = current_yticks[1] - current_yticks[0]
        conservative_yticks = np.arange(current_yticks[0]-ytick_step*3, current_yticks[-1] + 3*ytick_step, ytick_step)
        min_ytick = self._min_ytick(conservative_yticks)
        max_ytick = self._max_ytick(conservative_yticks)
        self.yticks = np.arange(min_ytick, max_ytick + ytick_step, ytick_step)
        self._set_yticks(self.yticks)

    def _min_ytick(self, conservative_yticks):
        min_ytick = float()
        for tick in reversed(conservative_yticks):
            if self.min_raw_data > tick:
                min_ytick = tick
                break
        return min_ytick

    def _max_ytick(self, conservative_yticks):
        max_ytick = float()
        for tick in conservative_yticks:
            if self.max_raw_data < tick:
                max_ytick = tick
                break
        return max_ytick
