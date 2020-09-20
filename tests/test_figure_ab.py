from pliffy import estimate, parser, figure


def test_figure_ab_paired_data(pliffy_info_abd_custom_asnamedtuple):
    info = pliffy_info_abd_custom_asnamedtuple
    estimates = estimate.calc_abd(info)
    save, ab_info, diff_info = parser.abd(info, estimates)
    ab_ax = figure.FigureAB(ab_info)
    assert ab_ax.yticks == (0.0, 2.0, 4.0, 6.0, 8.0, 10.0)
    assert ab_ax.max_raw_data == 9
    assert ab_ax.min_raw_data == 1
    assert ab_ax.ax.get_ylim() == (0.0, 10.0)
    assert ab_ax.ax.get_xlim() == (0.8, 3.0)
    assert list(ab_ax.ax.get_yticks()) == [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]
    assert list(ab_ax.ax.get_xticks()) == [1.0, 2.0, 2.8]
    assert ab_ax.ax.get_xticklabels()[0].get_text() == "Biceps"
    assert ab_ax.ax.get_xticklabels()[1].get_text() == "Triceps"
    assert ab_ax.ax.get_xticklabels()[2].get_text() == "Effect"


def test_figure_ab_unpaired_data(pliffy_info_abd_custom_neg_unpaired_asnamedtuple):
    info = pliffy_info_abd_custom_neg_unpaired_asnamedtuple
    estimates = estimate.calc_abd(info)
    save, ab_info, diff_info = parser.abd(info, estimates)
    ab_ax = figure.FigureAB(ab_info)
    assert ab_ax.yticks == (-100.0, -80.0, -60.0, -40.0, -20.0, 0.0)
    assert ab_ax.max_raw_data == -11
    assert ab_ax.min_raw_data == -92
    assert ab_ax.ax.get_ylim() == (-100.0, 0.0)
    assert ab_ax.ax.get_xlim() == (0.8, 3.0)
    assert list(ab_ax.ax.get_yticks()) == [-100.0, -80.0, -60.0, -40.0, -20.0, 0.0]
    assert list(ab_ax.ax.get_xticks()) == [1.0, 2.0, 2.8]
    assert ab_ax.ax.get_xticklabels()[0].get_text() == "Biceps"
    assert ab_ax.ax.get_xticklabels()[1].get_text() == "Triceps"
    assert ab_ax.ax.get_xticklabels()[2].get_text() == "Effect"
