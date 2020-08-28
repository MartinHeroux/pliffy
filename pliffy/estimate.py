from typing import NamedTuple, Tuple, Union, List

from scipy.stats import t
import numpy as np

from pliffy import blocks


def calc(pliffy_data: blocks.PliffyData) -> "Estmates":
    """Calculate mean difference and confidence interval

    Parameters
    ----------
    pliffy_data
        a
            First set of data
        b
            Second set of data
        design
            Flag to identify if data `a` and `b` are `paired` or `unpaired`
        ci_percentage
            Desired confidence interval.
            Example: 95 or 99
    """
    if pliffy_data.design not in ("unpaired", "paired"):
        raise ValueError(
            "`PliffyData.design` must be set to either 'paired' or 'unpaired'"
        )
    estimates_a, estimates_b = _calc_means_and_confidence_intervals(pliffy_data)
    estimates_diff = None
    if pliffy_data.design == "unpaired":
        estimates_diff = _unpaired_diff_mean_and_confidence_interval(
            pliffy_data, estimates_a, estimates_b
        )
    if pliffy_data.design == "paired":
        estimates_diff = _paired_diff_mean_and_confidence_interval(
            pliffy_data
        )
    return estimates_diff


class Estimates(NamedTuple):
    """Calculated mean and confidence interval"""

    mean: float = None
    ci: Tuple[float] = None


def _calc_means_and_confidence_intervals(pliffy_data) -> Tuple["Estimates"]:
    """Calculate means and confidence intervals for data `a` and `b`"""
    estimates_a = _calc_mean_and_confidence_interval(
        pliffy_data.a, pliffy_data.ci_percentage
    )
    estimates_b = _calc_mean_and_confidence_interval(
        pliffy_data.b, pliffy_data.ci_percentage
    )
    return estimates_a, estimates_b


def _calc_mean_and_confidence_interval(
    data: List[float], ci_percentage: int
) -> "Estimate":
    """Calculate mean and confidence interval for single set of data"""
    data_len = len(data)
    data_sem = np.std(data) / np.sqrt(data_len)
    data_mean = np.mean(data)
    t_value = _t_value(ci_percentage, data_len)
    margin_of_error = data_sem * t_value
    ci_vals = (data_mean - margin_of_error, data_mean + margin_of_error)
    return Estimates(mean=data_mean, ci=ci_vals)


def _sem(data: List[float]) -> float:
    return np.std(data) / (np.sqrt(len(data)))


def _t_value(ci: int, degrees_of_freedom: int):
    """Calculate Student t-value based on degrees-of-freedom and desired confidence interval"""
    one_sided_conf_int = (100 - (100 - ci) / 2) / 100
    return t.ppf(one_sided_conf_int, degrees_of_freedom)


def _unpaired_diff_mean_and_confidence_interval(
    pliffy_data: blocks.PliffyData, estimates_a: "Estimates", estimates_b: "Estimates"
) -> "Estimates":
    """Calculate mean difference of confidence interval of the mean difference

    Equation from: Cumming G, Calin-Jageman R (2017). Introduction to the New Statistics:
                   Estimation, Open Science, and Beyond. Routledge, New York
    """
    len_a, len_b = _data_len(pliffy_data)
    degrees_of_freedom = len_a + len_b - 2
    t_component = _t_value(pliffy_data.ci_percentage, degrees_of_freedom)
    weighted_sd_a = _weighted_sd(pliffy_data.a)
    weighted_sd_b = _weighted_sd(pliffy_data.b)
    variabilility_component = np.sqrt(
        (weighted_sd_a + weighted_sd_b) / degrees_of_freedom
    )
    sample_size_component = np.sqrt(1 / len_a + 1 / len_b)
    margin_of_error = t_component * variabilility_component * sample_size_component
    diff_mean = estimates_b.mean - estimates_a.mean
    diff_ci_vals = (diff_mean - margin_of_error, diff_mean + margin_of_error)
    return Estimates(mean=diff_mean, ci=diff_ci_vals)


def _data_len(pliffy_data: blocks.PliffyData) -> Tuple[int, int]:
    """Determine length of data `a` and `b`"""
    return len(pliffy_data.a), len(pliffy_data.b)


def _weighted_sd(data: List[float]) -> float:
    """Calculate weighted standard deviation"""
    return (len(data) - 1) * (np.std(data)) ** 2


def _paired_diff_mean_and_confidence_interval(
    pliffy_data: blocks.PliffyData,
) -> Tuple["Estimates", List[float]]:
    """Calculate mean difference of confidence interval of the mean difference"""
    len_a, len_b = _data_len(pliffy_data)
    if len_a != len_b:
        raise UnequalLength(
            "`pliffy_data.a` and `pliffy_data.b` must have the same length."
        )
    diff_vals = _paired_diffs(pliffy_data)
    estimates_diff = _calc_mean_and_confidence_interval(
        diff_vals, pliffy_data.ci_percentage
    )
    return estimates_diff


def _paired_diffs(pliffy_data):
    """Calculate paired difference for data in `a` and `b`"""
    return [b - a for a, b in zip(pliffy_data.a, pliffy_data.b)]


class UnequalLength(Exception):
    """Custom exception for paired analysis when data_a/data_b not same length"""

    pass
