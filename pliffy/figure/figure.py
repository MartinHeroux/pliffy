from typing import Literal, Tuple

from pliffy.parser import Xticks, Raw, Mean, CI, Paired


class Figure:
    """Mixin class to add low-level plotting ability"""

    def _remove_ax_spine(self, spine: Literal["top", "bottom", "left", "right"] = None):
        self.ax.spines[spine].set_visible(False)

    def _set_xlim(self, xlim: Tuple[float, float]):
        self.ax.set_xlim(xlim)

    def _set_ylim(self, ylim: Tuple[float, float]):
        self.ax.set_ylim(ylim)

    def _set_xticks(self, xticks: "Xticks"):
        if xticks.labels[2] == "":
            self.ax.set_xticks(xticks.vals[:2])
            self.ax.set_xticklabels(xticks.labels[:2])
        else:
            self.ax.set_xticks(xticks.vals)
            self.ax.set_xticklabels(xticks.labels)

    def _set_yticks(self, yticks: Tuple[float]):
        self.ax.set_yticks(yticks)

    def _set_ylabel(self, ylabel: str):
        self.ax.set_ylabel(ylabel)

    def _plot_raw_data(self, raw: "Raw"):
        xval = raw.xval
        for datum in raw.data:
            self.ax.plot(xval, datum, clip_on=False, **raw.format_)
            xval += raw.jitter

    def _plot_mean_ci(self, mean_: "Mean", ci: "CI"):
        self.ax.plot(*mean_.data, **mean_.format_)
        self.ax.plot(*ci.data, **ci.format_)

    def _plot_paired_lines(self, paired: "Paired"):
        xvals = list(paired.xvals)
        for a, b in zip(paired.a, paired.b):
            self.ax.plot(xvals, [a, b], **paired.format_)
            xvals[0] += paired.jitter
            xvals[1] -= paired.jitter
