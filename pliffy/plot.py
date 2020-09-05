from pliffy import estimate, parser
from pliffy.utils import PliffyInfoABD
from pliffy.figure import FigureAB, FigureDiff, DiffAxCreator

# TODO: Test plotting when a pre-generated axis is generated (e.g. a subplot)
# TODO: Add output of computed estimates for means and confidence intervals
#       - If plot is saved, include a .txt file of the output in same folder


def plot_abd(info: "PliffyInfoABD", ax=None):
    """Main user interface to generate ABD plot"""
    estimates = estimate.calc_abd(info)
    save, ab_fig_info, diff_fig_info = parser.abd(info, estimates)
    ab_ax = FigureAB(ab_fig_info, ax)
    diff_ax = DiffAxCreator(ab_ax, info, diff_fig_info).diff_ax()
    FigureDiff(diff_fig_info, diff_ax, save)

