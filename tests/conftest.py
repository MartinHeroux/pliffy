import pytest
import random

import numpy as np

from pliffy import plot
from pliffy.estimate import Estimates


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
    return [random.random() * 100 for _ in range(30)]


@pytest.fixture()
def pliffy_data_paired():
    random.seed(42)
    return plot.PliffyData(
        a=[random.random() * 100 for _ in range(30)],
        b=[random.random() * 100 for _ in range(30)],
        design="paired",
    )


@pytest.fixture()
def pliffy_data_paired_short():
    random.seed(42)
    return plot.PliffyData(
        a=[random.random() * 100 for _ in range(5)],
        b=[random.random() * 100 for _ in range(5)],
        design="paired",
    )


@pytest.fixture()
def pliffy_data_unpaired():
    random.seed(73)
    return plot.PliffyData(
        a=[random.random() * 100 for _ in range(30)],
        b=[random.random() * 100 for _ in range(20)],
    )


@pytest.fixture()
def estimates_a():
    return Estimates(mean=55.194, ci=(50.333, 61.001))


@pytest.fixture()
def estimates_b():
    return Estimates(mean=48.324, ci=(41.234, 57.451))


@pytest.fixture()
def pliffy_data_bad_design():
    return plot.PliffyData(a=[3], b=[6], design='not_possible')


@pytest.fixture()
def pliffy_data_unpaired_data_paired_design():
    random.seed(73)
    return plot.PliffyData(
        a=[random.random() * 100 for _ in range(30)],
        b=[random.random() * 100 for _ in range(20)],
        design='paired'
    )
