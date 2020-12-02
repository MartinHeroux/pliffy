from typing import NamedTuple, Union

import numpy as np
import matplotlib.pyplot as plt

from pliffy.utils import PliffyInfoABD, ABD
from pliffy.plot import plot_abd


class DataSpecs(NamedTuple):
    """Helper namedtuple used to set parameters of data to be mocked"""
    sample_size_a: int = 30
    sample_size_b: int = 30
    mean_a: float = 100
    mean_b: float = 95
    sd_a: float = 5
    sd_b: float = 5
    design: Union["paired", "unpaired"] = "paired"


def _gen_data(data_specs: DataSpecs) -> Union[list, list]:
    """Create mock data based on data_specs"""
    data_a = np.random.default_rng().normal(
        data_specs.mean_a, data_specs.sd_a, data_specs.sample_size_a
    )
    if data_specs.design == "paired":
        effect = np.random.default_rng().normal(
            data_specs.mean_a - data_specs.mean_b,
            data_specs.sd_b,
            data_specs.sample_size_a,
        )
        data_b = data_a - effect
    if data_specs.design == "unpaired":
        data_b = np.random.default_rng().normal(
            data_specs.mean_b, data_specs.sd_b, data_specs.sample_size_b
        )
    return data_a, data_b


def _example1():
    data_specs = DataSpecs()
    data_a, data_b = _gen_data(data_specs)
    info = PliffyInfoABD(data_a=data_b, data_b=data_a, design="paired")
    plot_abd(info)


def _example2():
    data_specs = DataSpecs(
        sample_size_a=50,
        sample_size_b=10,
        mean_a=10,
        mean_b=4,
        sd_a=5,
        sd_b=3,
        design="unpaired",
    )
    data_a, data_b = _gen_data(data_specs)
    info = PliffyInfoABD(
        data_a=data_b,
        data_b=data_a,
        ci_percentage=95,
        design="unpaired",
        measure_units="Weight (Kg)",
        xtick_labels=ABD(a="fish", b="birds", diff="effect"),
        decimals=4,
        plot_name="figure",
        marker=ABD(a="s", b="s", diff="^"),
        marker_color=ABD(a="tab:blue", b="tab:red", diff="tab:green"),
        fontsize=12,
    )
    plot_abd(info)


def _example3():
    data_specs = DataSpecs(
        sample_size_a=70,
        sample_size_b=10,
        mean_a=0.234,
        mean_b=0.1031,
        sd_a=0.14,
        sd_b=0.1,
        design="unpaired",
    )
    data_a, data_b = _gen_data(data_specs)
    info = PliffyInfoABD(
        data_a=data_b,
        data_b=data_a,
        ci_percentage=90,
        design="unpaired",
        measure_units="Height (cm)",
        xtick_labels=ABD(a="ants", b="fleas", diff=""),
        decimals=8,
        marker_color=ABD(a="tab:brown", b="tab:pink", diff="tab:olive"),
        summary_marker_size=ABD(a=5, b=5, diff=6),
        raw_marker_size=ABD(a=3, b=3, diff=3),
        raw_marker_transparency=0.8,
        fontsize=10,
    )
    plot_abd(info)


def _example4():
    data_specs = DataSpecs(
        sample_size_a=10,
        sample_size_b=10,
        mean_a=15,
        mean_b=10,
        sd_a=5,
        sd_b=5,
        design="paired",
    )
    data_a, data_b = _gen_data(data_specs)
    info = PliffyInfoABD(
        data_a=data_b,
        data_b=data_a,
        ci_percentage=95,
        design="paired",
        measure_units="Anxiety (points)",
        xtick_labels=ABD(a="Control", b="Test", diff="Effect"),
        decimals=1,
        marker_color=ABD(a="tab:orange", b="tab:purple", diff="tab:cyan"),
        summary_marker_size=ABD(a=6, b=6, diff=8),
        raw_marker_size=ABD(a=4, b=4, diff=4),
        raw_marker_transparency=1,
        paired_data_joining_lines=False,
        paired_data_plot_raw_diff=True,
        ci_line_width=2,
        fontsize=12,
        zero_line_width=2,
        zero_line_color="tab:red",
    )
    plot_abd(info)


def _example5():
    fig, axes = plt.subplots(nrows=4, figsize=(3, 8))
    last_subplot = len(axes) - 1
    for i, ax in enumerate(axes):
        data_specs = DataSpecs(
            sample_size_a=(i + 1) * 10,
            sample_size_b=(i + 1) * 10,
            mean_a=100,
            mean_b=120,
            sd_a=30,
            sd_b=30,
            design="unpaired",
        )
        data_a, data_b = _gen_data(data_specs)
        show = i == last_subplot
        info = PliffyInfoABD(data_a=data_a, data_b=data_b,  show=show, fontsize=12)
        plot_abd(info, ax)


def demo():
    """Generate five different demo plots"""
    _example1()
    _example2()
    _example3()
    _example4()
    _example5()
