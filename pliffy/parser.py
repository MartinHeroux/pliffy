from typing import NamedTuple, Literal, Tuple, List
from pathlib import Path

from pliffy import estimate
from pliffy import utils

ABD_XVALS = utils.ABD(a=1, b=2, diff=2.8)
ABD_XVALS_RAW = utils.ABD(a=ABD_XVALS.a + 0.1, b=ABD_XVALS.b - 0.2)
DIFF_XVAL = 0.3
DIFF_XVAL_RAW = 0.15
AB_XLIM = (0.8, 3)
DIFF_XLIM = (0.0, 0.5)
JITTER_RANGE = 0.1


def abd(info: "utils.PliffyInfoABD", estimates: "utils.ABD"):
    """Parse pliffy data and information to simplify plotting ABD figure"""
    jitter = _calc_jitter(info)
    raw_a, raw_b, raw_diff = _parse_raw_abd(info, jitter)
    mean_a, mean_b, mean_diff = _parse_mean_abd(info, estimates)
    ci_a, ci_b, ci_diff = _parse_ci_abd(info, estimates)
    plot_paired_lines = info.paired_data_joining_lines
    paired_lines = _parse_paired_lines(info, jitter)
    plot_raw_diff = info.paired_data_plot_raw_diff
    xticks = _parse_xticks(info)
    ab_xlim = AB_XLIM
    diff_xlim = DIFF_XLIM
    ylabel = info.measure_units
    fontsize = info.fontsize
    design = info.design
    zero_line = _parse_zero_line(info)
    show = info.show
    width_height_in_inches = info.width_height_in_inches

    save = _parse_save(info)

    ab_figure_info = FigureInfoAB(
        raw_a=raw_a,
        raw_b=raw_b,
        mean_a=mean_a,
        mean_b=mean_b,
        ci_a=ci_a,
        ci_b=ci_b,
        plot_paired_lines=plot_paired_lines,
        paired_lines=paired_lines,
        xticks=xticks,
        xlim=ab_xlim,
        ylabel=ylabel,
        design=design,
        fontsize=fontsize,
        width_height_in_inches=width_height_in_inches,
    )
    diff_figure_info = FigureInfoDiff(
        raw_diff=raw_diff,
        mean_diff=mean_diff,
        plot_raw_diff=plot_raw_diff,
        ci_diff=ci_diff,
        xlim=diff_xlim,
        zero_line=zero_line,
        show=show,
    )
    return save, ab_figure_info, diff_figure_info


def _calc_jitter(info: "utils.PliffyInfoABD") -> float:
    """Calculate offset to add to each raw data point (i.e. jitter)"""
    return JITTER_RANGE / max([len(info.data_a), len(info.data_b)])


class Save(NamedTuple):
    """Helper namedtuple to store save-related details"""

    name: str
    yes_no: Literal[True, False]
    path: Path
    type_: Literal["png", "svg", "pdf"] = "png"
    dpi: int = 180


def _parse_save(info: "utils.PliffyInfoABD") -> Save:
    """Parse save-related details"""
    return Save(
        name=info.plot_name,
        yes_no=info.save,
        path=info.save_path,
        type_=info.save_type,
        dpi=info.dpi,
    )


class Xticks(NamedTuple):
    """Helper namedtuple to store xtick details"""

    vals: Tuple[float, float, float] = tuple()
    labels: Tuple[str, str, str] = tuple()


def _parse_xticks(info: "utils.PliffyInfoABD") -> Xticks:
    """Parse details related to xticks"""
    return Xticks(
        vals=(ABD_XVALS.a, ABD_XVALS.b, ABD_XVALS.diff),
        labels=(info.xtick_labels.a, info.xtick_labels.b, info.xtick_labels.diff),
    )


def _raw_format(color: str, marker: str, markersize: int, alpha: float) -> dict:
    """Plotting format details for raw data in format that allows **kwargs call"""
    return {
        "color": color,
        "marker": marker,
        "markeredgewidth": 0,
        "markersize": markersize,
        "alpha": alpha,
    }


class Raw(NamedTuple):
    """Helper nametuple to store details for plotting raw data"""

    data: List[float]
    xval: float
    jitter: float
    format_: dict


def _parse_raw_abd(info: "utils.PliffyInfoABD", jitter: float) -> Tuple[Raw, Raw, Raw]:
    """Parse details and data to plot raw data"""
    raw_a = Raw(
        data=info.data_a,
        xval=ABD_XVALS_RAW.a,
        jitter=jitter,
        format_=_raw_format(
            info.marker_color.a,
            info.marker.a,
            info.raw_marker_size.a,
            info.raw_marker_transparency,
        ),
    )
    raw_b = Raw(
        data=info.data_b,
        xval=ABD_XVALS_RAW.b,
        jitter=jitter,
        format_=_raw_format(
            info.marker_color.b,
            info.marker.b,
            info.raw_marker_size.b,
            info.raw_marker_transparency,
        ),
    )
    raw_diff = Raw(
        data=estimate._calc_paired_diffs(info) if info.design == "paired" else None,
        xval=DIFF_XVAL_RAW,
        jitter=jitter,
        format_=_raw_format(
            info.marker_color.diff,
            info.marker.diff,
            info.raw_marker_size.diff,
            info.raw_marker_transparency,
        ),
    )
    return raw_a, raw_b, raw_diff


class Mean(NamedTuple):
    """Helper namedtuple to store xy data and format details for mean"""

    data: Tuple[float, float]
    format_: dict


def _mean_format(color: str, marker: str, markersize: int) -> dict:
    """Plotting format details for mean data in format that allows **kwargs call"""
    return {"color": color, "marker": marker, "markersize": markersize}


def _parse_mean_abd(
    info: "utils.PliffyInfoABD", estimates: "utils.ABD"
) -> Tuple[Mean, Mean, Mean]:
    """Parse details and data to plot mean value"""
    mean_a = Mean(
        data=(ABD_XVALS.a, estimates.a.mean),
        format_=_mean_format(
            info.marker_color.a, info.marker.a, info.summary_marker_size.a
        ),
    )
    mean_b = Mean(
        data=(ABD_XVALS.b, estimates.b.mean),
        format_=_mean_format(
            info.marker_color.b, info.marker.b, info.summary_marker_size.b
        ),
    )
    mean_diff = Mean(
        data=(DIFF_XVAL, estimates.diff.mean),
        format_=_mean_format(
            info.marker_color.diff, info.marker.diff, info.summary_marker_size.diff
        ),
    )
    return mean_a, mean_b, mean_diff


class CI(NamedTuple):
    """Helper namedtuple to store xy data and format details for CI"""

    data: Tuple[Tuple[float, float], Tuple[float, float]]
    format_: dict


def _ci_format(color: str, linewidth: int) -> dict:
    """Plotting format details for CI data in format that allows **kwargs call"""
    return {"color": color, "linewidth": linewidth}


def _parse_ci_abd(
    info: "utils.PliffyInfoABD", estimates: "utils.ABD"
) -> Tuple[CI, CI, CI]:
    """Parse details and data to plot CI values"""
    ci_a = CI(
        data=((ABD_XVALS.a, ABD_XVALS.a), estimates.a.ci),
        format_=_ci_format(info.marker_color.a, info.ci_line_width),
    )
    ci_b = CI(
        data=((ABD_XVALS.b, ABD_XVALS.b), estimates.b.ci),
        format_=_ci_format(info.marker_color.b, info.ci_line_width),
    )
    ci_diff = CI(
        data=((DIFF_XVAL, DIFF_XVAL), estimates.diff.ci),
        format_=_ci_format(info.marker_color.diff, info.ci_line_width),
    )
    return ci_a, ci_b, ci_diff


class Paired(NamedTuple):
    """Helper namedtuple to store data and format details to plot paired lines"""

    a: List[float]
    b: List[float]
    xvals: Tuple[float, float]
    jitter: float
    format_: dict


def _paired_line_format(color: str, linewidth: int, alpha: float) -> dict:
    """Plotting format details for paired lines data in format that allows **kwargs call"""
    return {"color": color, "linewidth": linewidth, "alpha": alpha}


def _parse_paired_lines(info: "utils.PliffyInfoABD", jitter: float) -> Paired:
    """Parse details and data to plot paired lines"""
    return Paired(
        a=info.data_a,
        b=info.data_b,
        xvals=(ABD_XVALS.a, ABD_XVALS.b),
        jitter=jitter,
        format_=_paired_line_format(
            info.paired_data_line_color,
            info.paired_data_line_width,
            info.paired_line_transparency,
        ),
    )


class ZeroLine(NamedTuple):
    """Helper namedtuple to store format details to plot zero line on diff plot"""

    color: str = "grey"
    width: int = 1


def _parse_zero_line(info: "utils.PliffyInfoABD") -> ZeroLine:
    return ZeroLine(color=info.zero_line_color, width=info.zero_line_width)


class FigureInfoAB(NamedTuple):
    """Helper namedtuple to hold data and details to plot AB part of figure"""

    raw_a: "Raw"
    raw_b: "Raw"
    mean_a: "Mean"
    mean_b: "Mean"
    ci_a: "CI"
    ci_b: "CI"
    paired_lines: "Paired"
    plot_paired_lines: Literal[True, False]
    xticks: "Xticks"
    xlim: Tuple[float, float]
    ylabel: str
    design: Literal["paired", "unpaired"]
    fontsize: int
    width_height_in_inches: Tuple[float, float]


class FigureInfoDiff(NamedTuple):
    """Helper namedtuple to hold data and details to plot diff part of figure"""

    raw_diff: "Raw"
    mean_diff: "Mean"
    plot_raw_diff: Literal[True, False]
    ci_diff: "CI"
    xlim: Tuple[float, float]
    zero_line: ZeroLine
    show: Literal[True, False]
