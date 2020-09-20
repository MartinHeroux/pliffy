from pathlib import Path

import pytest
import matplotlib
import matplotlib.pyplot as plt

from pliffy.plot import plot_abd

matplotlib.use('Qt5Agg')


@pytest.mark.mpl_image_compare(savefig_kwargs={'dpi': 600}, baseline_dir=str(Path(".") / "baseline"))
def test_example1(pliffy_info_example1):
    plot_abd(pliffy_info_example1)
    return plt.gcf()


@pytest.mark.mpl_image_compare(savefig_kwargs={'dpi': 600}, baseline_dir=str(Path(".") / "baseline"))
def test_example2(pliffy_info_example2):
    plot_abd(pliffy_info_example2)
    return plt.gcf()


@pytest.mark.mpl_image_compare(savefig_kwargs={'dpi': 600}, baseline_dir=str(Path(".") / "baseline"))
def test_example3(pliffy_info_example3):
    plot_abd(pliffy_info_example3)
    return plt.gcf()
