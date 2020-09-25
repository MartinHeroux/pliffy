from typing import NamedTuple, Union, Literal, Tuple
from pathlib import Path

from pliffy import estimate


class ABD(NamedTuple):
    """Namedtuple to store info/data for `a`, `b`, `diff`

    Examples
    --------

    >>> xtick_labels=ABD(a='a', b='b', diff='diff')
    >>> marker=ABD(a='o', b='o', diff='^')

    """

    a: Union[str, int, float, "estimate.Estimates"] = None
    b: Union[str, int, float, "estimate.Estimates"] = None
    diff: Union[str, int, float, "estimate.Estimates"] = None

    def __repr__(self):
        return f"ABD(a={repr(self.a)}, b={repr(self.b)}, diff={repr(self.diff)})"


class PliffyInfoABD(NamedTuple):
    """Information used to generate ABD plot

    `data_a` and `data_b` are the only two required parameters. Other values will be set
    to default values if not specified.

    Parameters
    ----------
    data_a: list = None
        Data to be plotted and used to compute difference
    data_b: list = None
        Data to be plotted and used to compute difference
    ci_percentage: int = 95
        Value used to compute confidence intervals
    design: Literal["paired", "unpaired"] = "unpaired"
        Specify whether `data_a` and `data_b` are paired or unpaired
    measure_units: str = "Amplitude (a.u.)"
        Label applied to left y-axis
    xtick_labels: ABD = ABD(a="a", b="b", diff="diff")
        Labels applied for `data_a`, `data_b` and `diff`. If `diff=""`, tick will be removed
    decimals: int = 2
        Precision with which to report estimates printed to console
    plot_name: str = "figure"
        Name given to plot when saved
    save: Literal[True, False] = False
        Flag whether or not to save figure
    save_path: Path = None
        Path where to save figure
    save_type: Literal["png", "svg", "pdf"] = "png"
        What type of figure to save
    dpi: int = 180
        If bitmap format, what dpi to use
    marker: ABD = ABD(a="o", b="o", diff="^")
        Marker style to use for plotted data (raw and summary)
    marker_color: ABD = ABD(a="black", b="black", diff="black")
        Color of plotted markers
    summary_marker_size: ABD = ABD(a=5, b=5, diff=6)
        Size of markers for mean values
    raw_marker_size: ABD = ABD(a=3, b=3, diff=3)
        Size of markers for raw data
    raw_marker_transparency: float = 0.2
        Transparency of raw data markers, value between 0.1 (very transparent) to 1 (opaque)
    paired_data_joining_lines: Literal[True, False] = True
        Indicate whether or not to plot joining lines between paired raw data points.
        If `False`, raw data points plotted
    paired_data_line_color: str = "gainsboro"
        Color of paired joining lines
    paired_data_line_width: int = 1
        Width of paired joining lines
    paired_line_transparency: float = 0.3
        Transparency of paired joining lines
    paired_data_plot_raw_diff: Literal[True, False] = True
        Indicate whether or not to plot raw difference values
    ci_line_width: int = 1
        Width of confidence interval error bars
    fontsize: int = 11
        Font of all labels and tick-values
    zero_line_color: str = "grey"
        Color of dotted line indicating zero on the floating difference axis
    zero_line_width: int = 1
        Width of zero line
    show: Literal[True, False] = True
        Indicate whether or not to show plot after generation. Set to `False` if want to save but
        not show figure. Also set to `False` if current figure is a subplot of a larger figure
    width_height_in_inches: Tuple[float, float] = (8.2, 8.2)
        Width and height of pliffy plot (in inches). Default is set to a one-column figure in
        a two-column journal format
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
    width_height_in_inches: Tuple[float, float] = (3.23, 3.23)

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
            f"\twidth_height_in_inches={repr(self.width_height_in_inches)},\n"
            ")"
        )
