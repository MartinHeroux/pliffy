from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from pliffy import estimate, blocks

matplotlib.rcParams.update({"font.size": 9})


X_VALS = blocks.ABD(a=1, b=2, diff=2.8)


class Figure:
    def __init__(self, pliffy_data, plot_info, estimates, ax_ab):
        self.pliffy_data = pliffy_data
        self.plot_info = plot_info
        self.estimates = estimates
        if ax_ab is None:
            ax_ab = self._make_figure_axis()
        self.ax_ab = ax_ab
        self.jitter = 0.05 / max([len(self.pliffy_data.a), len(self.pliffy_data.b)])
        self._plot_ab()
        self._plot_diff()
        if self.plot_info.save:
            plot_name = self.plot_info.plot_name + ".png"
            fig_path = Path(self.plot_info.save_path) / plot_name
            plt.savefig(fig_path)
        plt.show()

    def _make_figure_axis(self):
        width_height_in_inches = (8.2 / 2.54, 8.2 / 2.54)
        _, ax = plt.subplots(figsize=width_height_in_inches, dpi=600)
        return ax

    def _create_diff_axis(self):
        pass

    def _plot_ab(self):
        self._plot_raw_data()
        self._plot_ab_means()
        self._plot_ab_cis()
        self._tweak_ab_xaxis()
        self._tweak_ab_yaxis()

    def _plot_raw_data(self):
        if (
            self.pliffy_data.design == "paired"
        ) and self.plot_info.paired_data_joining_lines:
            self._plot_paired_lines()
        else:
            self._plot_ab_raw_data()

    def _plot_ab_means(self):
        self.ax_ab.plot(
            X_VALS.a,
            self.estimates.a.mean,
            marker=self.plot_info.summary_symbol.a,
            color=self.plot_info.symbol_color.a,
            markersize=self.plot_info.summary_symbol_size.a,
        )
        self.ax_ab.plot(
            X_VALS.b,
            self.estimates.b.mean,
            marker=self.plot_info.summary_symbol.b,
            color=self.plot_info.symbol_color.b,
            markersize=self.plot_info.summary_symbol_size.b,
        )

    def _plot_ab_cis(self):
        self.ax_ab.plot(
            [X_VALS.a, X_VALS.a],
            self.estimates.a.ci,
            color=self.plot_info.symbol_color.a,
            linewidth=self.plot_info.ci_line_width.a,
        )
        self.ax_ab.plot(
            [X_VALS.b, X_VALS.b],
            self.estimates.b.ci,
            color=self.plot_info.symbol_color.b,
            linewidth=self.plot_info.ci_line_width.b,
        )

    def _plot_paired_lines(self):
        x_vals = [X_VALS.a, X_VALS.b]
        for a, b in zip(self.pliffy_data.a, self.pliffy_data.b):
            self.ax_ab.plot(
                x_vals,
                [a, b],
                color=self.plot_info.paired_data_line_color,
                linewidth=self.plot_info.paired_data_line_width,
                alpha=self.plot_info.alpha,
            )
            x_vals[0] += self.jitter
            x_vals[1] -= self.jitter

    def _plot_ab_raw_data(self):
        x_val_a = X_VALS.a + 0.1
        x_val_b = X_VALS.b - 0.1
        for a, b in zip(self.pliffy_data.a, self.pliffy_data.b):
            self.ax_ab.plot(
                x_val_a,
                a,
                color=self.plot_info.symbol_color.a,
                marker=self.plot_info.summary_symbol.a,
                markeredgewidth=0,
                markersize=self.plot_info.raw_data_symbol_size.a,
                alpha=self.plot_info.alpha,
            )
            self.ax_ab.plot(
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

    def _tweak_ab_xaxis(self):
        self.ax_ab.spines["top"].set_visible(False)
        self.ax_ab.set_xlim((0.8, 3))
        self.ax_ab.set_xticks([X_VALS.a, X_VALS.b, X_VALS.diff])
        self.ax_ab.set_xticklabels(
            [
                self.plot_info.x_tick_labels.a,
                self.plot_info.x_tick_labels.b,
                self.plot_info.x_tick_labels.diff,
            ]
        )

    def _tweak_ab_yaxis(self):
        self.ax_ab.spines["right"].set_visible(False)
        self.ax_ab.set_ylabel(self.plot_info.measure_units)
        ab_yticks = self.ax_ab.get_yticks()
        self.ab_ytick_step = ab_yticks[1] - ab_yticks[0]
        min_past_lowest_ytick = ab_yticks[0] > min(
            min(self.pliffy_data.a), min(self.pliffy_data.b)
        )
        max_past_highest_ytick = ab_yticks[-1] < max(
            max(self.pliffy_data.a), max(self.pliffy_data.b)
        )
        y_ticks_adjusted = list()
        if min_past_lowest_ytick and max_past_highest_ytick:
            y_ticks_adjusted = (
                [ab_yticks[0] - self.ab_ytick_step]
                + list(ab_yticks)
                + [ab_yticks[-1] + self.ab_ytick_step]
            )
        if min_past_lowest_ytick and not max_past_highest_ytick:
            y_ticks_adjusted = [ab_yticks[0] - self.ab_ytick_step] + list(ab_yticks)
        if not min_past_lowest_ytick and max_past_highest_ytick:
            y_ticks_adjusted = list(ab_yticks) + [ab_yticks[-1] + self.ab_ytick_step]
        if not min_past_lowest_ytick and not max_past_highest_ytick:
            y_ticks_adjusted = list(ab_yticks)
        self.y_ticks_adjusted = y_ticks_adjusted
        self.ax_ab.set_yticks(self.y_ticks_adjusted)

    def _plot_diff(self):
        # Currently for summary_data only

        if self.estimates.diff.mean <= 0:
            bottom_limit = self.estimates.diff.ci[0]
            bottom_included = True
            y_tick_count_bottom = 1
            while bottom_included:
                if (y_tick_count_bottom * -self.ab_ytick_step) > bottom_limit:
                    y_tick_count_bottom += 1
                else:
                    break

            top_limit = self.estimates.diff.ci[1]
            top_included = True
            y_tick_count_top = 0
            while top_included:
                if (y_tick_count_top * self.ab_ytick_step) < top_limit:
                    y_tick_count_top += 1
                else:
                    break
            y_tick_count_top += 1

        diff_axis_y_bottom_left_corner = self.y_ticks_adjusted[0] + (
            (self.estimates.a.mean - (y_tick_count_bottom * self.ab_ytick_step))
            - self.y_ticks_adjusted[0]
        )

        y_ticks = list(np.arange(-y_tick_count_bottom*self.ab_ytick_step, self.ab_ytick_step*y_tick_count_top, self.ab_ytick_step))
        self.ax_diff = self.ax_ab.inset_axes(
            [2.5, diff_axis_y_bottom_left_corner, 0.5, y_ticks[-1] - y_ticks[0]],
            transform=self.ax_ab.transData,
        )
        self.ax_diff.set_yticks(y_ticks)
        self.ax_diff.set_ylim((y_ticks[0], y_ticks[-1]))
        self.ax_diff.plot(0.3, self.estimates.diff.mean, "^k", markersize=6)
        self.ax_diff.plot([0.3, 0.3], [self.estimates.diff.ci[0], self.estimates.diff.ci[1]], "-k", linewidth=1)
        self.ax_diff.plot([0, 0.5], [0, 0], '--', color='grey', linewidth=1)
        self.ax_diff.tick_params(
            axis="y",
            which="both",
            left=False,
            right=True,
            labelleft=False,
            labelright=True,
        )
        self.ax_diff.spines["top"].set_visible(False)
        self.ax_diff.spines["bottom"].set_visible(False)
        self.ax_diff.spines["left"].set_visible(False)
        self.ax_diff.xaxis.set_ticks([])
        self.ax_diff.xaxis.set_ticklabels([])
