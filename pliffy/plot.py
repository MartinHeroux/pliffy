from pliffy import estimate, parse
from pliffy.blocks import PliffyInfoABD
from pliffy.figure import FigureAB, FigureDiff, DiffAxCreator


def plot_abd(info: "PliffyInfoABD", ax=None):
    """Main user interface to generate plot"""
    estimates = estimate.calc_abd(info)
    save, ab_fig_info, diff_fig_info = parse.abd(info, estimates)
    fig_ab = FigureAB(ab_fig_info, ax)
    diff_ax = DiffAxCreator(fig_ab, info, diff_fig_info).diff_ax()
    FigureDiff(diff_fig_info, diff_ax, save)

