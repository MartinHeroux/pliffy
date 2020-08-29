from pathlib import Path

import matplotlib.pyplot as plt

from pliffy import estimate


class Figure:
    def __init__(self, pliffy_data, plot_info, estimates, ax):
        self.pliffy_data = pliffy_data
        self.plot_info = plot_info
        self.estimates = estimates
        if ax is None:
            ax = self._make_figure_axis()
        self.axes = [ax, ax.twinx()]
        self.ba_spacing = plot_info.x_values.b - plot_info.x_values.a
        self.jitter = (self.ba_spacing * 0.05) / max(
            [len(self.pliffy_data.a), len(self.pliffy_data.b)]
        )
        self._plot()

    def _make_figure_axis(self):
        width_height_in_inches = (8.2 / 2.54, 8.2 / 2.54)
        _, ax = plt.subplots(figsize=width_height_in_inches, dpi=600)
        return ax

    def _plot(self):
        self._plot_raw_data()
        self._plot_means()
        self._plot_cis()
        if self.plot_info.save:
            plot_name = self.plot_info.plot_name + ".png"
            fig_path = Path(self.plot_info.save_path) / plot_name
            plt.savefig(fig_path)
        plt.show()

    def _plot_means(self):  # TODO: Make more pythonic
        self.axes[0].plot(
            self.plot_info.x_values.a,
            self.estimates.a.mean,
            marker=self.plot_info.summary_symbol.a,
            color=self.plot_info.symbol_color.a,
            markersize=self.plot_info.summary_symbol_size.a,
        )
        self.axes[0].plot(
            self.plot_info.x_values.b,
            self.estimates.b.mean,
            marker=self.plot_info.summary_symbol.b,
            color=self.plot_info.symbol_color.b,
            markersize=self.plot_info.summary_symbol_size.b,
        )
        self.axes[1].plot(
            self.plot_info.x_values.diff,
            self.estimates.diff.mean,
            marker=self.plot_info.summary_symbol.diff,
            color=self.plot_info.symbol_color.diff,
            markersize=self.plot_info.summary_symbol_size.diff,
        )

    def _plot_cis(self):  # TODO: Make more pythonic
        self.axes[0].plot(
            [self.plot_info.x_values.a, self.plot_info.x_values.a],
            self.estimates.a.ci,
            color=self.plot_info.symbol_color.a,
            linewidth=self.plot_info.ci_line_width.a,
        )
        self.axes[0].plot(
            [self.plot_info.x_values.b, self.plot_info.x_values.b],
            self.estimates.b.ci,
            color=self.plot_info.symbol_color.b,
            linewidth=self.plot_info.ci_line_width.b,
        )
        self.axes[1].plot(
            [self.plot_info.x_values.diff, self.plot_info.x_values.diff],
            self.estimates.diff.ci,
            color=self.plot_info.symbol_color.diff,
            linewidth=self.plot_info.ci_line_width.diff,
        )

    def _plot_raw_data(self):
        if (
            self.pliffy_data.design == "paired"
        ) and self.plot_info.paired_data_joining_lines:
            self._plot_paired_lines()
        elif (
            self.pliffy_data.design == "paired"
        ) and not self.plot_info.paired_data_joining_lines:
            self._plot_paired_diff_raw_data()
            self._plot_ab_raw_data()
        else:
            self._plot_ab_raw_data()

    def _plot_paired_lines(self):
        x_vals = [self.plot_info.x_values.a, self.plot_info.x_values.b]
        for a, b in zip(self.pliffy_data.a, self.pliffy_data.b):
            self.axes[0].plot(
                x_vals,
                [a, b],
                color=self.plot_info.paired_data_line_color,
                linewidth=self.plot_info.paired_data_line_width,
                alpha=self.plot_info.alpha,
            )
            x_vals[0] += self.jitter
            x_vals[1] -= self.jitter

    def _plot_paired_diff_raw_data(self):
        raw_data_diffs = estimate._paired_diffs(self.pliffy_data)
        x_val = self.plot_info.x_values.diff - (self.ba_spacing * 0.1)
        for raw_data_diff in raw_data_diffs:
            self.axes[1].plot(
                x_val,
                raw_data_diff,
                color=self.plot_info.symbol_color.diff,
                marker=self.plot_info.summary_symbol.diff,
                markeredgewidth=0,
                markersize=self.plot_info.raw_data_symbol_size.diff,
                alpha=self.plot_info.alpha,
            )
            x_val -= self.jitter

    def _plot_ab_raw_data(self):
        x_val_a = self.plot_info.x_values.a + (self.ba_spacing * 0.1)
        x_val_b = self.plot_info.x_values.b - (self.ba_spacing * 0.1)
        for a, b in zip(self.pliffy_data.a, self.pliffy_data.b):
            self.axes[0].plot(x_val_a, a,
                              color=self.plot_info.symbol_color.a,
                              marker=self.plot_info.summary_symbol.a,
                              markeredgewidth=0,
                              markersize=self.plot_info.raw_data_symbol_size.a,
                              alpha=self.plot_info.alpha,
                              )
            self.axes[0].plot(x_val_b, b,
                              color=self.plot_info.symbol_color.b,
                              marker=self.plot_info.summary_symbol.b,
                              markeredgewidth=0,
                              markersize=self.plot_info.raw_data_symbol_size.b,
                              alpha=self.plot_info.alpha,
                              )
            x_val_a += self.jitter
            x_val_b -= self.jitter
