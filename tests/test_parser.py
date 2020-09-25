from pliffy.parser import abd
from pliffy.utils import ABD
from pliffy.parser import Raw, CI, Xticks, Mean, Paired, ZeroLine


def test_abd_save(pliffy_info_abd_custom_asnamedtuple, pliffy_estimates):
    save = abd(pliffy_info_abd_custom_asnamedtuple, pliffy_estimates)[0]
    expected = {
        "name": "arm",
        "yes_no": True,
        "path": "/home/martin/Desktop/",
        "type_": "svg",
        "dpi": 600,
    }
    assert save._asdict() == expected


def test_abd_figure_info(pliffy_info_abd_custom_asnamedtuple, pliffy_estimates):
    abd_figure_info = abd(pliffy_info_abd_custom_asnamedtuple, pliffy_estimates)[1]
    assert abd_figure_info._asdict() == {
        "raw_a": Raw(
            data=[1, 2, 3, 4, 5],
            xval=1.1,
            jitter=0.02,
            format_={
                "color": "tab:red",
                "marker": "*",
                "markeredgewidth": 0,
                "markersize": 6,
                "alpha": 0.1,
            },
        ),
        "raw_b": Raw(
            data=[1, 4, 6, 7, 9],
            xval=1.8,
            jitter=0.02,
            format_={
                "color": "tab:blue",
                "marker": "v",
                "markeredgewidth": 0,
                "markersize": 5,
                "alpha": 0.1,
            },
        ),
        "mean_a": Mean(
            data=(1, 5), format_={"color": "tab:red", "marker": "*", "markersize": 6}
        ),
        "mean_b": Mean(
            data=(2, 6), format_={"color": "tab:blue", "marker": "v", "markersize": 4}
        ),
        "ci_a": CI(
            data=((1, 1), (3.5, 6.5)), format_={"color": "tab:red", "linewidth": 2}
        ),
        "ci_b": CI(
            data=((2, 2), (3.2, 8.8)), format_={"color": "tab:blue", "linewidth": 2}
        ),
        "paired_lines": Paired(
            a=[1, 2, 3, 4, 5],
            b=[1, 4, 6, 7, 9],
            xvals=(1, 2),
            jitter=0.02,
            format_={"color": "grey", "linewidth": 2, "alpha": 0.3},
        ),
        "plot_paired_lines": False,
        "xticks": Xticks(
            vals=(1, 2, 2.8), labels=ABD(a="Biceps", b="Triceps", diff="Effect")
        ),
        "xlim": (0.8, 3),
        "ylabel": "Amplitude (Volts)",
        "design": "paired",
        "fontsize": 12,
        "width_height_in_inches": (3.23, 3.23),
    }


def test_abd_diff_figure_info(pliffy_info_abd_custom_asnamedtuple, pliffy_estimates):
    diff_figure_info = abd(pliffy_info_abd_custom_asnamedtuple, pliffy_estimates)[2]
    assert diff_figure_info._asdict() == {
        "raw_diff": Raw(
            data=[0, 2, 3, 3, 4],
            xval=0.15,
            jitter=0.02,
            format_={
                "color": "tab:green",
                "marker": ".",
                "markeredgewidth": 0,
                "markersize": 3,
                "alpha": 0.1,
            },
        ),
        "mean_diff": Mean(
            data=(0.3, 1),
            format_={"color": "tab:green", "marker": ".", "markersize": 2},
        ),
        "plot_raw_diff": False,
        "ci_diff": CI(
            data=((0.3, 0.3), (0.1, 1.9)),
            format_={"color": "tab:green", "linewidth": 2},
        ),
        "xlim": (0.0, 0.5),
        "show": False,
        'zero_line': ZeroLine(color='grey', width=1),
    }
