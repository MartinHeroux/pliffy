import numpy as np
import pytest
import matplotlib

from pliffy import demo

matplotlib.use("Qt5Agg")


def test_demo_data_specs():
    data_specs = demo.DataSpecs()
    assert data_specs._asdict() == {
        "sample_size_a": 30,
        "sample_size_b": 30,
        "mean_a": 100,
        "mean_b": 95,
        "sd_a": 5,
        "sd_b": 5,
        "design": "paired",
    }


def test_demo_gen_data():
    data_specs = demo.DataSpecs(
        sample_size_a=60,
        sample_size_b=100,
        mean_a=100,
        mean_b=200,
        sd_a=1,
        sd_b=2,
        design="unpaired",
    )
    data_a, data_b = demo._gen_data(data_specs)
    assert len(data_a) == 60
    assert len(data_b) == 100
    assert np.mean(data_a) == pytest.approx(expected=100, rel=1)
    assert np.mean(data_b) == pytest.approx(expected=200, rel=2)
