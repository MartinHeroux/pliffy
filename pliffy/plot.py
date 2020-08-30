from typing import NamedTuple, Tuple, Union, Literal


from pliffy import blocks, estimate, figure


def plot(pliffy_data: blocks.PliffyData, plot_info: blocks.PlotInfo = blocks.PlotInfo(), ax=None):
    """Main user interface to generate plot
    """
    estimates_a, estimates_b, estimates_diff = estimate.calc(pliffy_data)
    estimates = blocks.ABD(a=estimates_a, b=estimates_b, diff=estimates_diff)
    #TODO: print to screen and save to file all estimates
    figure.Figure(pliffy_data, plot_info, estimates, ax)


