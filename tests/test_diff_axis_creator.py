import pytest

from pliffy import estimate, parser, figure


def test_diff_ax_creator_paired(pliffy_info_abd_custom_asnamedtuple):
    info = pliffy_info_abd_custom_asnamedtuple
    estimates = estimate.calc_abd(info)
    save, ab_info, diff_info = parser.abd(info, estimates)
    ab_ax = figure.FigureAB(ab_info)
    diff_ax = figure.DiffAxCreator(ab_ax, info, diff_info)
    assert diff_ax.ytick_step == 2.0
    assert diff_ax.height == 8.0
    assert diff_ax.y == 1.0
    assert diff_ax.max_diff == pytest.approx(4.8460190413538555)
    assert diff_ax.min_diff == pytest.approx(-0.04601904135385615)
    assert diff_ax.yticks == (-2.0, 0.0, 2.0, 4.0, 6.0)
    assert diff_ax.width == 0.5
    assert diff_ax.x == 2.5


def test_diff_ax_creator_paired_created_ax(pliffy_info_abd_custom_asnamedtuple):
    info = pliffy_info_abd_custom_asnamedtuple
    estimates = estimate.calc_abd(info)
    save, ab_info, diff_info = parser.abd(info, estimates)
    ab_ax = figure.FigureAB(ab_info)
    diff_ax = figure.DiffAxCreator(ab_ax, info, diff_info).diff_ax()
    assert diff_ax.get_ylim() == (-2.0, 6.0)
    assert list(diff_ax.get_yticks()) == [-2.0, 0.0, 2.0, 4.0, 6.0]


def test_diff_ax_creator_unpaired(pliffy_info_abd_custom_neg_unpaired_asnamedtuple):
    info = pliffy_info_abd_custom_neg_unpaired_asnamedtuple
    estimates = estimate.calc_abd(info)
    save, ab_info, diff_info = parser.abd(info, estimates)
    ab_ax = figure.FigureAB(ab_info)
    diff_ax = figure.DiffAxCreator(ab_ax, info, diff_info)
    assert diff_ax.ytick_step == 20.0
    assert diff_ax.height == 80.0
    assert diff_ax.y == -92.0
    assert diff_ax.max_diff == pytest.approx(8.356924461457027)
    assert diff_ax.min_diff == pytest.approx(-55.55692446145703)
    assert diff_ax.yticks == (-60.0, -40.0, -20.0, 0.0, 20.0)
    assert diff_ax.width == 0.5
    assert diff_ax.x == 2.5


def test_diff_ax_creator_unpaired_created_ax(
    pliffy_info_abd_custom_neg_unpaired_asnamedtuple,
):
    info = pliffy_info_abd_custom_neg_unpaired_asnamedtuple
    estimates = estimate.calc_abd(info)
    save, ab_info, diff_info = parser.abd(info, estimates)
    ab_ax = figure.FigureAB(ab_info)
    diff_ax = figure.DiffAxCreator(ab_ax, info, diff_info).diff_ax()
    assert diff_ax.get_ylim() == (-60.0, 20.0)
    assert list(diff_ax.get_yticks()) == [-60.0, -40.0, -20.0, 0.0, 20.0]
