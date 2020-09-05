import numpy as np

from pliffy.utils import PliffyInfoABD, ABD
from pliffy.plot import plot_abd

# TODO: Improve demo to generate series of figures to show off capabilities

n = 60
mu_a, sigma_a = 100, 25  # mean and standard deviation
a = np.random.default_rng().normal(mu_a, sigma_a, n)

mu_b, sigma_b = 30, 15  # mean and standard deviation
effect = np.random.default_rng().normal(mu_b, sigma_b, n)
b = a - effect

info = PliffyInfoABD(
    data_a=a,
    data_b=b,
    ci_percentage=95,
    design="paired",
    measure_units="Length (cm)",
    xtick_labels=ABD(a="Hand", b="Foot", diff="difference"),
    save=False,
    save_path=None,
    save_type="png",
    marker=ABD(a="o", b="o", diff="^"),
    marker_color=ABD(a="tab:red", b="tab:blue", diff="tab:green"),
    summary_marker_size=ABD(a=4, b=4, diff=5),
    raw_marker_size=ABD(a=3, b=3, diff=3),
    raw_marker_transparency=0.2,
    paired_data_joining_lines=False,
    paired_data_line_color="gainsboro",
    paired_line_transparency=0.3,
    paired_data_plot_raw_diff=True,
    ci_line_width=1,
    fontsize=9,
)

plot_abd(info)
