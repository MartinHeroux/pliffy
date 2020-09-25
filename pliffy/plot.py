from pliffy import estimate, parser, utils, figure


def plot_abd(info: "utils.PliffyInfoABD", ax=None):
    """Main user interface to generate ABD plot

    Examples
    --------

    >>> from pliffy import PliffyInfoABD, plot_abd
    >>> info = PliffyInfoABD(data_a=data_a, data_b=data_b)
    >>> plot_abd(info)
    """
    estimates = estimate.calc_abd(info)
    save, ab_info, diff_info = parser.abd(info, estimates)
    ab_ax = figure.FigureAB(ab_info, ax)
    diff_ax = figure.DiffAxCreator(ab_ax, info, diff_info).diff_ax()
    figure.FigureDiff(diff_info, diff_ax, save)
