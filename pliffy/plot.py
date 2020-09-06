from pliffy import estimate, parser, utils, figure

# TODO: Test plotting when a pre-generated axis is generated (e.g. a subplot)
# TODO: Add output of computed estimates for means and confidence intervals
#       - If plot is saved, include a .txt file of the output in same folder


def plot_abd(info: "utils.PliffyInfoABD", ax=None):
    """Main user interface to generate ABD plot"""
    estimates = estimate.calc_abd(info)
    save, ab_info, diff_info = parser.abd(info, estimates)
    ab_ax = figure.FigureAB(ab_info, ax)
    diff_ax = figure.DiffAxCreator(ab_ax, info, diff_info).diff_ax()
    figure.FigureDiff(diff_info, diff_ax, save)

