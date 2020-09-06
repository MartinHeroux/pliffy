import pytest
import random

import numpy as np

from pliffy import utils
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
    return _make_random_data(30)


def _make_random_data(num_samples):
    return [random.random() * 100 for _ in range(num_samples)]


@pytest.fixture()
def pliffy_data_paired():
    random.seed(42)
    data = _make_random_data(60)
    return utils.PliffyInfoABD(
        data_a=data[:30],
        data_b=data[30:],
        design="paired",
    )


@pytest.fixture()
def pliffy_data_paired_short():
    random.seed(42)
    data = _make_random_data(10)
    return utils.PliffyInfoABD(
        data_a=data[:5],
        data_b=data[5:],
        design="paired",
    )


@pytest.fixture()
def pliffy_data_unpaired():
    random.seed(73)
    data = _make_random_data(50)
    return utils.PliffyInfoABD(
        data_a=data[:30],
        data_b=data[30:],
    )


@pytest.fixture()
def estimates_a():
    return Estimates(mean=55.194, ci=(50.333, 61.001))


@pytest.fixture()
def estimates_b():
    return Estimates(mean=48.324, ci=(41.234, 57.451))


@pytest.fixture()
def pliffy_data_bad_design():
    return utils.PliffyInfoABD(data_a=[3], data_b=[6], design='not_possible')


@pytest.fixture()
def pliffy_data_unpaired_data_paired_design():
    random.seed(73)
    return utils.PliffyInfoABD(
        data_a=_make_random_data(30),
        data_b=_make_random_data(20),
        design='paired'
    )
