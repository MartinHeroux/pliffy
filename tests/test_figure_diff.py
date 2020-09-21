from pathlib import Path

import pytest
import matplotlib
import matplotlib.pyplot as plt

from pliffy.plot import plot_abd
from pliffy.utils import PliffyInfoABD

matplotlib.use("Qt5Agg")


@pytest.mark.mpl_image_compare(
    savefig_kwargs={"dpi": 600}, baseline_dir=str(Path(".") / "baseline")
)
def test_example1(pliffy_info_example1):
    plot_abd(pliffy_info_example1)
    return plt.gcf()


@pytest.mark.mpl_image_compare(
    savefig_kwargs={"dpi": 600}, baseline_dir=str(Path(".") / "baseline")
)
def test_example2(pliffy_info_example2):
    plot_abd(pliffy_info_example2)
    return plt.gcf()


@pytest.mark.mpl_image_compare(
    savefig_kwargs={"dpi": 600}, baseline_dir=str(Path(".") / "baseline")
)
def test_example3(pliffy_info_example3):
    plot_abd(pliffy_info_example3)
    return plt.gcf()


def test_example_save(tmpdir):
    pliffy_info = PliffyInfoABD(
        data_a=[1, 2, 3, 4],
        data_b=[3, 4, 5, 6],
        plot_name="test_figure",
        save=True,
        save_path=tmpdir,
        save_type="png",
        show=False,
    )
    plot_abd(pliffy_info)
    figure_path = Path(tmpdir) / (pliffy_info.plot_name + '.' + pliffy_info.save_type)
    assert figure_path.is_file()
