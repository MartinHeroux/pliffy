from typing import NamedTuple, Tuple, Union, Literal
from pathlib import Path

from pliffy import estimate


class ABD(NamedTuple):
    """Helper namedtuple"""

    a: Union[str, int, float, "estimate.Estimates"] = None
    b: Union[str, int, float, "estimate.Estimates"] = None
    diff: Union[str, int, float, "estimate.Estimates"] = None


class PlotInfo(NamedTuple):
    """Information used to generate plot

    Includes sensible defaults to reduce need for user input
    """

    x_tick_labels: ABD = ABD(a="a", b="b", diff="diff")
    measure_units: str = "Amplitude (a.u.)"
    plot_name: str = "figure"
    save: Literal[True, False] = False
    save_path: Path = None

    summary_symbol: ABD = ABD(a="o", b="o", diff="^")
    symbol_color: ABD = ABD(a="black", b="black", diff="black")
    summary_symbol_size: ABD = ABD(a=5, b=5, diff=6)
    raw_data_symbol_size: ABD = ABD(a=3, b=3, diff=3)
    paired_data_joining_lines: bool = True
    paired_data_line_width: int = 1
    paired_data_line_color: str = "gainsboro"
    ci_line_width: ABD = ABD(a=1, b=1, diff=1)
    horiz_line_to_diffs: bool = False
    join_ab_means: bool = True
    ax1_y_range: Tuple = None
    ax2_y_range: Tuple = None
    ax1_y_ticks: Tuple = None
    ax2_y_ticks: Tuple = None
    ab_sub_label: str = None
    bottom_box: bool = False
    alpha: float = 0.2


class PliffyData(NamedTuple):
    """Data and details required from user

    See :function:`pliffy.estimates.calc` parameters for details.
    """

    a: list = None
    b: list = None
    design: Literal["paired", "unpaired"] = "unpaired"
    ci_percentage: int = 95
