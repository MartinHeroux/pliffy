from typing import NamedTuple, Tuple, Union, Literal
from pathlib import Path

import matplotlib.pyplot as plt


class _ABD(NamedTuple):
    """Helper namedtuple used by PlotInfo"""

    a: Union[str, int] = None
    b: Union[str, int] = None
    diff: Union[str, int] = None


class PlotInfo(NamedTuple):
    """Information used to generate plot

    Includes sensible defaults to reduce need for user input
    """

    x_tick_labels: _ABD = _ABD(a='a', b='b', diff='diff')
    measure_units: str = "Amplitude (a.u.)"
    plot_name: str = None
    save: Literal[True, False] = False
    save_path: Path = None

    colors: _ABD = _ABD(a="black", b="black", diff="black")
    symbol_size_summary: _ABD = _ABD(a=3, b=3, diff=3)
    symbol_size_subject: _ABD = _ABD(a=1, b=1, diff=1)
    symbols: _ABD = _ABD(a="o", b="o", diff="^")
    x_values: _ABD = _ABD(a=1, b=2, diff=3)
    horiz_line_to_diffs: bool = False
    join_ab_means: bool = True
    ax1_y_range: Tuple = None
    ax2_y_range: Tuple = None
    ax1_y_ticks: Tuple = None
    ax2_y_ticks: Tuple = None
    ab_sub_label: str = None
    bottom_box: bool = False
    alpha: float = 0.7


class PliffyData(NamedTuple):
    """Data and details required from user

    See :function:`pliffy.estimates.calc` parameters for details.
    """

    a: list = None
    b: list = None
    design: Literal["paired", "unpaired"] = "unpaired"
    ci_percentage: int = 95


class Pliffy:
    def __init__(self, pliffy_data, plot_info, estimates_diff, ax):
        self.pliffy_data = pliffy_data
        self.plot_info = plot_info
        self.estimates_diff = estimates_diff
        if ax is None:
            ax = self._make_figure_axis()
        self.ax = [ax, ax.twinx()]
        self.plot()

    def _make_figure_axis(self):
        width_height_in_inches = (8.2 / 2.54, 8.2 / 2.54)
        _, ax = plt.subplots(figsize=width_height_in_inches)
        return ax

    def plot(self):
        pass

