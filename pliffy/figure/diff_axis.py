from typing import Literal, Tuple

import numpy as np
from matplotlib.axes._subplots import Subplot

from pliffy import utils, parser

DIFF_X = 2.5
DIFF_WIDTH = 0.5

# TODO: Add documentation and tests


class DiffAxCreator:
    def __init__(
        self,
        parent_figure: Subplot,
        pliffy_info: "utils.PliffyInfoABD",
        diff_fig_info: "parser.Diff_figure_info",
    ):

        self.parent_figure = parent_figure
        self.info = pliffy_info
        self.diff_fig_info = diff_fig_info
        self.x = DIFF_X
        self.width = DIFF_WIDTH
        self.ytick_step = self._ytick_step()
        self.min_diff = self._min_diff()
        self.max_diff = self._max_diff()
        self.yticks = self._optimize_diff_yticks()
        self.y = self._calc_diff_y()
        self.height = self._calc_diff_height()

    """

    diff axis is create by specifying x, y, width, height.
        - x, y: coordinates of the bottom-left corner of the diff axis
        - width, height: Of the diff axis, where the origin is x, y

    Because we will create the diff axis in data coordinates of the main ab_axis,
    (transform=self.ax_ab.transData), `x, y, width, height` must all be specified
    in data coordinates of the main ab_axis.

    Returns
    -------

    """

    def _min_diff(self) -> float:
        if self._plot_raw_diff():
            return min(self.diff_fig_info.raw_diff.data)
        else:
            return self.diff_fig_info.ci_diff.data[1][0]

    def _plot_raw_diff(self) -> Literal[True, False]:
        return (
            self.parent_figure.info.design == "paired"
            and self.diff_fig_info.plot_raw_diff
        )

    def _max_diff(self) -> float:
        if self._plot_raw_diff():
            return max(self.diff_fig_info.raw_diff.data)
        else:
            return self.diff_fig_info.ci_diff.data[1][1]

    def _ytick_step(self) -> float:
        return self.parent_figure.ytick_step

    def _calc_diff_y(self) -> float:
        return self.parent_figure.info.mean_a.data[1] - abs(self.yticks[0])

    def _optimize_diff_yticks(self) -> Tuple[float]:
        min_ytick = 0
        while True:
            if self.min_diff < min_ytick:
                min_ytick -= self.ytick_step
            else:
                break
        max_ytick = 0
        while True:
            if self.max_diff > max_ytick:
                max_ytick += self.ytick_step
            else:
                break
        return tuple(np.arange(min_ytick, max_ytick + self.ytick_step, self.ytick_step))

    def _calc_diff_height(self) -> float:
        return self.yticks[-1] - self.yticks[0]

    def diff_ax(self) -> Subplot:
        diff_ax = self.parent_figure.ax.inset_axes(
            [self.x, self.y, self.width, self.height],
            transform=self.parent_figure.ax.transData,
        )
        diff_ax.set_yticks(self.yticks)
        diff_ax.set_ylim((min(self.yticks), max(self.yticks)))
        return diff_ax
