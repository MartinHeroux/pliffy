import pytest
import random

import numpy as np

from pliffy import utils
from pliffy.estimate import Estimates
from pliffy.utils import ABD


@pytest.fixture()
def mock_data(n_values=(30, 30), means=(100, 100), standard_deviations=(10, 10)):
    data_a = np.random.default_rng().normal(
        means[0], standard_deviations[0], n_values[0]
    )
    data_b = np.random.default_rng().normal(
        means[1], standard_deviations[1], n_values[1]
    )
    return data_a, data_b


@pytest.fixture()
def data_a():
    random.seed(42)
    return _make_random_data(30)


def _make_random_data(num_samples):
    return [random.random() * 100 for _ in range(num_samples)]


@pytest.fixture()
def pliffy_data_paired():
    random.seed(42)
    data = _make_random_data(60)
    return utils.PliffyInfoABD(data_a=data[:30], data_b=data[30:], design="paired",)


@pytest.fixture()
def pliffy_data_paired_short():
    random.seed(42)
    data = _make_random_data(10)
    return utils.PliffyInfoABD(data_a=data[:5], data_b=data[5:], design="paired",)


@pytest.fixture()
def pliffy_data_unpaired():
    random.seed(73)
    data = _make_random_data(50)
    return utils.PliffyInfoABD(data_a=data[:30], data_b=data[30:],)


@pytest.fixture()
def estimates_a():
    return Estimates(mean=55.194, ci=(50.333, 61.001))


@pytest.fixture()
def estimates_b():
    return Estimates(mean=48.324, ci=(41.234, 57.451))


@pytest.fixture()
def pliffy_data_bad_design():
    return utils.PliffyInfoABD(data_a=[3], data_b=[6], design="not_possible")


@pytest.fixture()
def pliffy_data_unpaired_data_paired_design():
    random.seed(73)
    return utils.PliffyInfoABD(
        data_a=_make_random_data(30), data_b=_make_random_data(20), design="paired"
    )


@pytest.fixture()
def pliffy_info_abd_default_asdict():
    return {
        "data_a": None,
        "data_b": None,
        "ci_percentage": 95,
        "design": "unpaired",
        "measure_units": "Amplitude (a.u.)",
        "xtick_labels": ABD(a="a", b="b", diff="diff"),
        "decimals": 2,
        "plot_name": "figure",
        "save": False,
        "save_path": None,
        "save_type": "png",
        "dpi": 180,
        "marker": ABD(a="o", b="o", diff="^"),
        "marker_color": ABD(a="black", b="black", diff="black"),
        "summary_marker_size": ABD(a=5, b=5, diff=6),
        "raw_marker_size": ABD(a=3, b=3, diff=3),
        "raw_marker_transparency": 0.2,
        "paired_data_joining_lines": True,
        "paired_data_line_color": "gainsboro",
        "paired_data_line_width": 1,
        "paired_line_transparency": 0.2,
        "paired_data_plot_raw_diff": True,
        "ci_line_width": 1,
        "fontsize": 9,
        "show": True,
    }


def _pliffy_info_abd_custom():
    return {
        "data_a": [1, 2, 3, 4, 5],
        "data_b": [1, 4, 6, 7, 9],
        "ci_percentage": 99,
        "design": "paired",
        "measure_units": "Amplitude (Volts)",
        "xtick_labels": ABD(a="Biceps", b="Triceps", diff="Effect"),
        "decimals": 4,
        "plot_name": "arm",
        "save": True,
        "save_path": "/home/martin/Desktop/",
        "save_type": "svg",
        "dpi": 600,
        "marker": ABD(a="*", b="v", diff="."),
        "marker_color": ABD(a="tab:red", b="tab:blue", diff="tab:green"),
        "summary_marker_size": ABD(a=6, b=4, diff=2),
        "raw_marker_size": ABD(a=6, b=5, diff=3),
        "raw_marker_transparency": 0.1,
        "paired_data_joining_lines": False,
        "paired_data_line_color": "grey",
        "paired_data_line_width": 2,
        "paired_line_transparency": 0.3,
        "paired_data_plot_raw_diff": False,
        "ci_line_width": 2,
        "fontsize": 12,
        "show": False,
    }


@pytest.fixture()
def pliffy_info_abd_custom_asdict():
    return _pliffy_info_abd_custom()


@pytest.fixture()
def pliffy_info_abd_custom_asnamedtuple():
    return utils.PliffyInfoABD(**_pliffy_info_abd_custom())


def _pliffy_info_abd_custom_neg_unpaired():
    return {
        "data_a": [-11, -22, -32, -43, -52],
        "data_b": [-11, -43, -61, -71, -92],
        "ci_percentage": 95,
        "design": "unpaired",
        "measure_units": "Amplitude (Volts)",
        "xtick_labels": ABD(a="Biceps", b="Triceps", diff="Effect"),
        "decimals": 4,
        "plot_name": "arm",
        "save": True,
        "save_path": "/home/martin/Desktop/",
        "save_type": "svg",
        "dpi": 600,
        "marker": ABD(a="*", b="v", diff="."),
        "marker_color": ABD(a="tab:red", b="tab:blue", diff="tab:green"),
        "summary_marker_size": ABD(a=6, b=4, diff=2),
        "raw_marker_size": ABD(a=6, b=5, diff=3),
        "raw_marker_transparency": 0.1,
        "paired_data_joining_lines": False,
        "paired_data_line_color": "grey",
        "paired_data_line_width": 2,
        "paired_line_transparency": 0.3,
        "paired_data_plot_raw_diff": False,
        "ci_line_width": 2,
        "fontsize": 12,
        "show": False,
    }


@pytest.fixture()
def pliffy_info_abd_custom_neg_unpaired_asdict():
    return _pliffy_info_abd_custom()


@pytest.fixture()
def pliffy_info_abd_custom_neg_unpaired_asnamedtuple():
    return utils.PliffyInfoABD(**_pliffy_info_abd_custom_neg_unpaired())

@pytest.fixture()
def pliffy_estimates():
    return ABD(
        a=Estimates(mean=5, ci=(3.5, 6.5)),
        b=Estimates(mean=6, ci=(3.2, 8.8)),
        diff=Estimates(mean=1, ci=(0.1, 1.9)),
    )
