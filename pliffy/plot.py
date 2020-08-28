from typing import NamedTuple, Tuple, Union, Literal


from pliffy import blocks, estimate


def plot(pliffy_data: blocks.PliffyData, plot_info: blocks.PlotInfo = blocks.PlotInfo(), ax=None):
    """Main user interface to generate plot
    """
    estimates_diff = estimate.calc(pliffy_data)
    pliffy = blocks.Pliffy(pliffy_data, plot_info, estimates_diff, ax)
    pliffy.plot()


