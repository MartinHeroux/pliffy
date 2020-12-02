import pliffy


def plot_abd(info: "utils.PliffyInfoABD", ax=None):
    """Main user interface to generate ABD plot

    Examples
    --------

    >>> from pliffy import PliffyInfoABD, plot_abd
    >>> info = PliffyInfoABD(data_a=data_a, data_b=data_b)
    >>> plot_abd(info)
    """
    estimates = pliffy.estimate.calc_abd(info)
    save, ab_info, diff_info = pliffy.parser.abd(info, estimates)
    ab_ax = pliffy.figure.FigureAB(ab_info, ax)
    diff_ax = pliffy.figure.DiffAxCreator(ab_ax, info, diff_info).diff_ax()
    pliffy.figure.FigureDiff(diff_info, diff_ax, save)
