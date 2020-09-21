from typing import NamedTuple, Union, Literal
from pathlib import Path

from pliffy import estimate


class ABD(NamedTuple):
    """Helper namedtuple"""

    a: Union[str, int, float, "estimate.Estimates"] = None
    b: Union[str, int, float, "estimate.Estimates"] = None
    diff: Union[str, int, float, "estimate.Estimates"] = None

    def __repr__(self):
        return f"ABD(a={repr(self.a)}, b={repr(self.b)}, diff={repr(self.diff)})"


class PliffyInfoABD(NamedTuple):
    """Information used to generate ABD plot

    Sensible defaults reduce need for user input
    """

    data_a: list = None
    data_b: list = None
    ci_percentage: int = 95
    design: Literal["paired", "unpaired"] = "unpaired"
    measure_units: str = "Amplitude (a.u.)"
    xtick_labels: ABD = ABD(a="a", b="b", diff="diff")
    decimals: int = 2
    plot_name: str = "figure"
    save: Literal[True, False] = False
    save_path: Path = None
    save_type: Literal["png", "svg", "pdf"] = "png"
    dpi: int = 180
    marker: ABD = ABD(a="o", b="o", diff="^")
    marker_color: ABD = ABD(a="black", b="black", diff="black")
    summary_marker_size: ABD = ABD(a=5, b=5, diff=6)
    raw_marker_size: ABD = ABD(a=3, b=3, diff=3)
    raw_marker_transparency: float = 0.2
    paired_data_joining_lines: Literal[True, False] = True
    paired_data_line_color: str = "gainsboro"
    paired_data_line_width: int = 1
    paired_line_transparency: float = 0.3
    paired_data_plot_raw_diff: Literal[True, False] = True
    ci_line_width: int = 1
    fontsize: int = 11
    zero_line_color: str = "grey"
    zero_line_width: int = 1
    show: Literal[True, False] = True

    def __repr__(self):
        return (
            f"PliffyInfoABD(\n"
            f"\tdata_a={repr(self.data_a)},\n"
            f"\tdata_b={repr(self.data_b)},\n"
            f"\tci_percentage={repr(self.ci_percentage)},\n"
            f"\tdesign={repr(self.design)},\n"
            f"\tmeasure_units={repr(self.measure_units)},\n"
            f"\txtick_labels={repr(self.xtick_labels)},\n"
            f"\tdecimals={repr(self.decimals)},\n"
            f"\tplot_name={repr(self.plot_name)},\n"
            f"\tsave={repr(self.save)},\n"
            f"\tsave_path={repr(self.save_path)},\n"
            f"\tsave_type={repr(self.save_type)},\n"
            f"\tdpi={repr(self.dpi)},\n"
            f"\tmarker={repr(self.marker)},\n"
            f"\tmarker_color={repr(self.marker_color)},\n"
            f"\tsummary_marker_size={repr(self.summary_marker_size)},\n"
            f"\traw_marker_size={repr(self.raw_marker_size)},\n"
            f"\traw_marker_transparency={repr(self.raw_marker_transparency)},\n"
            f"\tpaired_data_joining_lines={repr(self.paired_data_joining_lines)},\n"
            f"\tpaired_data_line_color={repr(self.paired_data_line_color)},\n"
            f"\tpaired_line_transparency={repr(self.paired_line_transparency)},\n"
            f"\tpaired_data_plot_raw_diff={repr(self.paired_data_plot_raw_diff)},\n"
            f"\tci_line_width={repr(self.ci_line_width)},\n"
            f"\tfontsize={repr(self.fontsize)},\n"
            f"\tzero_line_color={repr(self.zero_line_color)},\n"
            f"\tzero_line_width={repr(self.zero_line_width)},\n"
            f"\tshow={repr(self.show)},\n"
            ")"
        )
