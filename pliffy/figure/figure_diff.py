from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes._subplots import Subplot

from pliffy.figure import Figure
from pliffy import parser


class FigureDiff(Figure):
    """Class to manage plotting Diff part of ABD figure

    Parameters
    ----------
    info: FigureInfoDiff
        Namedtuple containing parsed data and details to plot Diff part of figure
    ax: Subplot
        Matplotlib axis object to plot floating axis
    save: Save
        NamedTuple containing parsed information related to saving figure

    """

    def __init__(self, info: "parser.FigureInfoDiff", ax: Subplot, save: "parser.Save"):
        self.info = info
        self.ax = ax
        self.save = save
        self._plot()

    def _plot(self):
        self._plot_diff_mean_ci()
        self._plot_diff_raw_data()
        self._plot_zero_line()
        self._tweak_axes()
        plt.tight_layout()
        self._save()
        self._show()

    def _plot_diff_mean_ci(self):
        self._plot_mean_ci(self.info.mean_diff, self.info.ci_diff)

    def _plot_diff_raw_data(self):
        if self._plot_raw_diff_true():
            self._plot_raw_data(self.info.raw_diff)

    def _plot_raw_diff_true(self):
        return (self.info.raw_diff.data is not None) and self.info.plot_raw_diff

    def _plot_zero_line(self):
        self.ax.plot(
            [0, 0.5],
            [0, 0],
            "--",
            color=self.info.zero_line.color,
            linewidth=self.info.zero_line.width,
        )

    def _tweak_axes(self):
        self.ax.tick_params(
            axis="y",
            which="both",
            left=False,
            right=True,
            labelleft=False,
            labelright=True,
        )
        self.ax.tick_params(
            axis="x",
            which="both",
            top=False,
            bottom=False,
            labeltop=False,
            labelbottom=False,
        )
        self._remove_ax_spine("top")
        self._remove_ax_spine("bottom")
        self._remove_ax_spine("left")

    def _save(self):
        if self.save.yes_no:
            name = self.save.name + "." + self.save.type_
            fig_path = Path(self.save.path) / name
            plt.savefig(fig_path, dpi=self.save.dpi)

    def _show(self):
        if self.info.show:
            plt.show()
