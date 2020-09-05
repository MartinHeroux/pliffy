import numpy as np

DIFF_X = 2.5
DIFF_WIDTH = 0.5

class DiffAxCreator:
    def __init__(self, figure, info, diff_fig_info):

        self.figure = figure
        self.info = info
        self.diff_fig_info = diff_fig_info
        self.x = DIFF_X
        self.width = DIFF_WIDTH
        self.ytick_step = self._ytick_step()
        self.n_below = self._num_yticks_below_zero()
        self.n_above = self._num_yticks_above_zero()
        self.yticks = self._diff_yticks()
        self.y = self._calc_diff_y()
        self.height = self._diff_height()

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

    def _ytick_step(self):
        return self.figure.yticks[1] - self.figure.yticks[0]

    def _calc_diff_y(self):
        return self.figure.info.mean_a.data[1] - (self.n_below * self.ytick_step)

    def _num_yticks_below_zero(self):
        bottom_limit = self._find_bottom_limit()
        bottom_included = True
        num = 0
        while bottom_included:
            if (num * -self.ytick_step) > bottom_limit:
                num += 1
            else:
                break
        if (self.figure.info.mean_a.data[1] - self.figure.info.mean_b.data[1]) < 0:
            num += 1
        return num

    def _find_bottom_limit(self):
        if self.figure.info.design == "paired":
            return min(self.diff_fig_info.raw_diff.data)
        else:
            return self.diff_fig_info.ci_diff.data[1][0]

    def _num_yticks_above_zero(self):
        top_limit = self._find_top_limit()
        top_included = True
        num = 0
        while top_included:
            if (num * self.ytick_step) < top_limit:
                num += 1
            else:
                break
        if (self.figure.info.mean_a.data[1] - self.figure.info.mean_b.data[1]) >= 0:
            num += 1
        return num

    def _find_top_limit(self):
        if self.figure.info.design == "paired":
            return max(self.diff_fig_info.raw_diff.data)
        else:
            return self.diff_fig_info.ci_diff.data[1][1]

    def _diff_height(self):
        return self.yticks[-1] - self.yticks[0]

    def _diff_yticks(self):
        return list(
            np.arange(
                -self.n_below * self.ytick_step,
                self.ytick_step * self.n_above,
                self.ytick_step,
            )
        )

    def diff_ax(self):
        return self._create_diff_ax()

    def _create_diff_ax(self):
        diff_ax = self.figure.ax.inset_axes(
            [self.x, self.y, self.width, self.height], transform=self.figure.ax.transData,
        )
        diff_ax.set_yticks(self.yticks)
        diff_ax.set_ylim((min(self.yticks), max(self.yticks)))
        return diff_ax
