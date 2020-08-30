from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib

from pliffy import estimate, blocks

matplotlib.rcParams.update({"font.size": 9})


class Figure:
    def __init__(self, pliffy_data, plot_info, estimates, ax):
        self.pliffy_data = pliffy_data
        self.plot_info = plot_info
        # Adjust diff values by adding a.mean to simplify plotting diff axis
        estimates_diff = estimate.Estimates(
            mean=estimates.diff.mean + estimates.a.mean,
            ci=(
                estimates.diff.ci[0] + estimates.a.mean,
                estimates.diff.ci[1] + estimates.a.mean,
            ),
        )
        estimates = blocks.ABD(a=estimates.a, b=estimates.b, diff=estimates_diff)
        self.estimates = estimates
        if pliffy_data.design == 'paired':
            raw_data_diffs = estimate._paired_diffs(self.pliffy_data)
            # Adjust raw diff values by adding a.mean to simplify plotting diff axis
            self.raw_data_diffs_corrected = [value + self.estimates.a.mean for value in raw_data_diffs]
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
        self._tweak_x_axis()
        self._add_labels()
        self._tweak_y_ticks()
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
        x_val = self.plot_info.x_values.diff - (self.ba_spacing * 0.1)
        for raw_data_diff in self.raw_data_diffs_corrected:
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
            self.axes[0].plot(
                x_val_a,
                a,
                color=self.plot_info.symbol_color.a,
                marker=self.plot_info.summary_symbol.a,
                markeredgewidth=0,
                markersize=self.plot_info.raw_data_symbol_size.a,
                alpha=self.plot_info.alpha,
            )
            self.axes[0].plot(
                x_val_b,
                b,
                color=self.plot_info.symbol_color.b,
                marker=self.plot_info.summary_symbol.b,
                markeredgewidth=0,
                markersize=self.plot_info.raw_data_symbol_size.b,
                alpha=self.plot_info.alpha,
            )
            x_val_a += self.jitter
            x_val_b -= self.jitter

    def _tweak_x_axis(self):
        for ax in self.axes:
            ax.spines["top"].set_visible(False)
            # ax.spines["bottom"].set_visible(False)
            # ax.tick_params(axis="x", which="both", bottom=True, top=False, labelbottom=False)
            ax.set_xlim(
                (
                    self.plot_info.x_values.a - self.ba_spacing / 4,
                    self.plot_info.x_values.diff + self.ba_spacing / 4,
                )
            )

    def _add_labels(self):
        self.axes[0].set_ylabel(self.plot_info.measure_units)
        self.axes[0].set_xticks(
            [
                self.plot_info.x_values.a,
                self.plot_info.x_values.b,
                self.plot_info.x_values.diff,
            ]
        )
        self.axes[0].set_xticklabels(
            [
                self.plot_info.x_tick_labels.a,
                self.plot_info.x_tick_labels.b,
                self.plot_info.x_tick_labels.diff,
            ]
        )

    def _tweak_y_ticks(self):
        y_ticks = self.axes[0].get_yticks()
        y_tick_step = y_ticks[1] - y_ticks[0]
        y_ticks_adjusted = [y_ticks[0] - y_tick_step] + list(y_ticks) + [y_ticks[-1] + y_tick_step]
        self.axes[0].set_yticks(y_ticks_adjusted)
        self.axes[1].set_yticks(y_ticks_adjusted)
        self.axes[0].set_ylim([y_ticks_adjusted[0], y_ticks_adjusted[-1]])
        self.axes[1].set_ylim([y_ticks_adjusted[0], y_ticks_adjusted[-1]])
