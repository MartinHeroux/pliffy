from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes._subplots import Subplot

from pliffy.figure import Figure
from pliffy import parser

# TODO: Add documentation and tests


class FigureDiff(Figure):
    def __init__(self, info: "parser.Diff_figure_info", ax: Subplot, save: "parser.Save"):
        self.info = info
        self.ax = ax
        self.save = save
        self._plot()

    def _plot(self):
        self._plot_diff_mean_ci()
        self._plot_diff_raw_data()
        self._plot_zero_line()
        self._tweak_axes()
        self._save()
        self._show()

    def _plot_diff_mean_ci(self):
        self._plot_mean_ci(self.info.mean_diff, self.info.ci_diff)

    def _plot_diff_raw_data(self):
        if self._plot_raw_diff():
            self._plot_raw_data(self.info.raw_diff)

    def _plot_raw_diff(self):
        return (self.info.raw_diff.data is not None) and self.info.plot_raw_diff

    def _plot_zero_line(self):
        self.ax.plot([0, 0.5], [0, 0], "--", color="grey", linewidth=1)

    def _tweak_axes(self):
        self.ax.tick_params(
            axis="y",
            which="both",
            left=False,
            right=True,
            labelleft=False,
            labelright=True,
        )
        self._remove_ax_spine("top")
        self._remove_ax_spine("bottom")
        self._remove_ax_spine("left")
        self._set_xticks(parser.Xticks())

    def _save(self):
        if self.save.yes_no:
            name = self.save.name + "." + self.save.name
            fig_path = Path(self.save.path) / name
            plt.savefig(fig_path, dpi=600)

    def _show(self):
        plt.show()
