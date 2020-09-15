import numpy as np
import matplotlib.pyplot as plt

from pliffy.utils import PliffyInfoABD, ABD
from pliffy.plot import plot_abd


def gen_paired_data():
    sample_size = 60
    mean_a, standard_deviation_a = 100, 25
    data_a = np.random.default_rng().normal(mean_a, standard_deviation_a, sample_size)

    mean_b, standard_deviation_b = 30, 15
    effect = np.random.default_rng().normal(mean_b, standard_deviation_b, sample_size)
    data_b = data_a - effect
    return data_a, data_b


data_a, data_b = gen_paired_data()

info = PliffyInfoABD(
    data_a=data_b,
    data_b=data_a,
    ci_percentage=95,
    design="paired",
    measure_units="Amplitude (a.u.)",
    xtick_labels=ABD(a="control", b="Treatment", diff="effect"),
    decimals=4,
    plot_name='Great_stuff',
    save=True,
    save_path="/home/martin/Desktop/",
    save_type="png",
    dpi=600,
    marker=ABD(a="o", b="o", diff="^"),
    marker_color=ABD(a="tab:blue", b="tab:red", diff="tab:green"),
    summary_marker_size=ABD(a=5, b=5, diff=6),
    raw_marker_size=ABD(a=3, b=3, diff=3),
    raw_marker_transparency=0.2,
    paired_data_joining_lines=False,
    paired_data_line_color="gainsboro",
    paired_line_transparency=0.2,
    paired_data_plot_raw_diff=True,
    ci_line_width=1,
    fontsize=9,
    show=True,
)


plot_abd(info)


# fig, axes = plt.subplots(nrows=4, figsize=(3, 8))
# last_subplot = len(axes) - 1
# for i, ax in enumerate(axes):
#     data_a, data_b = gen_paired_data()
#     if i != last_subplot:
#         info = PliffyInfoABD(data_a=data_a, data_b=data_b, show=False)
#     else:
#         info = PliffyInfoABD(data_a=data_a, data_b=data_b)
#     plot_abd(info, ax)
