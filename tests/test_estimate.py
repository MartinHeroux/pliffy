from pytest import approx
import pytest
import numpy as np

from pliffy import estimate


def test_weighted_sd(data_a):
    actual = estimate._weighted_sd(data_a)
    expected = 25646.059030
    assert actual == approx(expected)


def test_data_len_paired(pliffy_data_paired):
    len_a, len_b = estimate._data_len(pliffy_data_paired)
    assert (len_a, len_b) == (30, 30)


def test_data_len_unpaired(pliffy_data_unpaired):
    len_a, len_b = estimate._data_len(pliffy_data_unpaired)
    assert (len_a, len_b) == (30, 20)


def test_sem(data_a):
    actual = np.std(data_a) / (np.sqrt(len(data_a)))
    assert actual == approx(5.429385)


@pytest.mark.parametrize(
    "ci, degrees_of_freedom, expected", [(95, 30, 2.042272), (99, 5, 4.032142)]
)
def test_t_value(ci, degrees_of_freedom, expected):
    actual = estimate._t_value(ci, degrees_of_freedom)
    assert actual == approx(expected)


@pytest.mark.parametrize(
    "ci, expected",
    [(95, (42.368976, 31.280691, 53.457261)), (99, (42.368976, 27.438189, 57.299763))],
)
def test_calc_mean_and_confidence_interval(data_a, ci, expected):
    actual = estimate._calc_mean_and_confidence_interval(data_a, ci)
    assert (actual.mean, actual.ci[0], actual.ci[1]) == approx(expected)


def test_unpaired_diff_mean_and_confidence_interval(
    pliffy_data_unpaired, estimates_a, estimates_b
):
    estimates_diff = estimate._unpaired_mean_diff_and_confidence_interval(
        pliffy_data_unpaired, estimates_a, estimates_b
    )
    assert (estimates_diff.mean, estimates_diff.ci[0], estimates_diff.ci[1]) == approx(
        (-6.870000, -22.916868, 9.176868)
    )


def test_calc_means_and_confidence_intervals_paired(pliffy_data_paired):
    estimate_a, estimate_b = estimate._calc_means_and_confidence_intervals(
        pliffy_data_paired
    )
    assert (
        estimate_a.mean,
        estimate_a.ci[0],
        estimate_a.ci[1],
        estimate_b.mean,
        estimate_b.ci[0],
        estimate_b.ci[1],
    ) == approx((42.368976, 31.280691, 53.457261, 47.690431, 37.682449, 57.698414))


def test_calc_means_and_confidence_intervals_unpaired(pliffy_data_unpaired):
    estimate_a, estimate_b = estimate._calc_means_and_confidence_intervals(
        pliffy_data_unpaired
    )
    assert (
        estimate_a.mean,
        estimate_a.ci[0],
        estimate_a.ci[1],
        estimate_b.mean,
        estimate_b.ci[0],
        estimate_b.ci[1],
    ) == approx((51.483584, 41.592262, 61.374905, 42.197593, 28.543706, 55.851479))


def test_paired_diff_mean_and_confidence_interval(pliffy_data_paired_short):
    estimates_diff = estimate._paired_mean_diff_and_confidence_interval(
        pliffy_data_paired_short
    )
    assert (estimates_diff.mean, estimates_diff.ci[0], estimates_diff.ci[1]) == approx(
        (4.167762, -54.875948, 63.211472)
    )


def test_paired_diffs(pliffy_data_paired_short):
    actual = estimate._calc_paired_diffs(pliffy_data_paired_short)
    assert actual == approx([3.727268, 86.716881, -18.809048, 19.871108, -70.667399])


def test_ValueError_PliffyData_invalid_design(capfd, pliffy_data_bad_design):
    with pytest.raises(
        ValueError,
        match="`PliffyData.design` must be set to either 'paired' or 'unpaired'",
    ):
        estimates = estimate.calc_abd(pliffy_data_bad_design)


def test_ValueError_PliffyData_unequal_length_data(
    capfd, pliffy_data_unpaired_data_paired_design
):
    with pytest.raises(
        estimate.UnequalLength,
        match="`PliffyInfoABD.data_a` and `PliffyInfoABD.data_b` must have the "
        "same length in paired design.",
    ):
        estimates_diff = estimate.calc_abd(pliffy_data_unpaired_data_paired_design)
