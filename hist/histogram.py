#!/usr/bin/env python3

from typing import Iterator, Sequence, Callable
from math import floor

VBAR = "\u2502"
HBAR = "\u2500"
CORNER = "\u253c"
BLOCK = "\u2588"

def bin_iter(average_value: float, bin_width: int, bins: int) -> Iterator[int]:
    """Iterate over lower bounds of bins that are evenly distributed around the
    average value.
    """
    lower_bound = int(average_value - (bin_width * (bins // 2)))
    cursor = 0
    while cursor < bins:
        yield lower_bound
        lower_bound += bin_width
        cursor += 1

def positive_bin_iter(highest_value: float, bin_width: int, bins: int) -> Iterator[int]:
    """Iterate over lower bounds of bins that start at zero."""
    lower_bound = 0
    cursor = 0
    while cursor < bins:
        yield lower_bound
        lower_bound += bin_width
        cursor += 1

def spaces(count: int) -> str:
    return " " * count

def bars(count: int) -> str:
    return HBAR * count

def build_inclusion_func(low: int, high: int) -> Callable[[float], bool]:
    def inclusion_func(n: float) -> bool:
        return n >= low and n < high
    return inclusion_func

def format_tower(count_values: int, average_value: float) -> str:
    """Handle edge case where all values are in the same bin."""
    # Besides handling an edge case, this is an excellent documentation of the
    # desired layout. Each step is carefully explained in comments.

    # get the wider of 'all' or the count of values;
    # this is the 'column width'
    count_width = len(str(count_values))
    if count_width < 3: #len('all')
        col_width = 3
    else:
        col_width = count_width

    # draw y-axis, border space, and count of values right-aligned with the bar
    buf = f"{VBAR} {str(count_values).rjust(col_width)}\n"

    # draw y-axis, border space, and bar at right edge of the 'column width'
    for _ in range(count_values - 1):
        buf += f"{VBAR} {BLOCK.rjust(col_width)}\n"

    # draw x-axis the full length of the border space and the 'column width'
    buf += f"{CORNER}{bars(1 + col_width)}\n"

    # draw x-axis label right-aligned with the bar
    buf += f"  {'all'.rjust(col_width)}\n"

    # draw summary statistics
    buf += f"Avg. = {average_value:.2f}\n"

    return buf

def format(values: Sequence[float], bins: int, positive: bool) -> str:
    """Creates a histogram."""
    count_values = len(values)
    average_value = sum(values) / count_values

    # handle edge cases where there is a single bin
    if bins == 1:
        return format_tower(count_values, average_value)

    # determine the floored bin range
    ordered_values = sorted(values)
    value_range = ordered_values[-1] - ordered_values[0]
    bin_range = floor(value_range // bins)

    # handle edge cases where floored bin range is less than 1;
    # force to 1 and accept that there will be empty trailing bins
    if bin_range == 0:
        bin_range = 1

    # determine the bin lower bounds
    bin_lower_bounds = [n for n in bin_iter(average_value, bin_range, bins)]

    # if positive is True and the lowest bound is negative, redraw bin lower
    # bounds starting at zero
    if positive and bin_lower_bounds[0] < 0:
        bin_lower_bounds = [n for n in positive_bin_iter(ordered_values[-1], bin_range, bins)]

    # handle outlier values that cannot be drawn;
    # flooring the bin ranges causes values (esp. lower outliers) to be cut
    check_inclusion = build_inclusion_func(bin_lower_bounds[0], bin_lower_bounds[-1] + bin_range)
    included_values = list(filter(check_inclusion, values))
    excluded_count = count_values - len(included_values)

    # count values within a bin range
    bin_counts = [0] * bins
    for i in range(bins):
        bin_counter = build_inclusion_func(bin_lower_bounds[i], bin_lower_bounds[i] + bin_range)
        bin_values = list(filter(bin_counter, included_values))
        bin_counts[i] = len(bin_values)

    # get the widest column, either a bin label or a bar count
    col_width = max(len(str(n)) for n in bin_lower_bounds)
    widest_bin_count = max(len(str(n)) for n in bin_counts)
    if col_width < widest_bin_count:
        col_width = widest_bin_count

    # draw y-axis, border space, and a column and border space for each bin
    buf = ""
    cursor = max(bin_counts)
    while cursor > 0:
        buf += VBAR
        for bin_count in bin_counts:
            if bin_count == cursor:
                buf += f" {str(bin_count).rjust(col_width)}"
            elif bin_count > cursor:
                buf += f" {BLOCK.rjust(col_width)}"
            else:
                buf += spaces(col_width + 1)
        buf += "\n"
        cursor -= 1

    # draw x-axis labels that will be right-aligned with the bars;
    # cannot push to buffer yet
    x_axis_labels = " "
    for bin_label in bin_lower_bounds:
        x_axis_labels += f" {str(bin_label).rjust(col_width)}"
    chart_width = len(x_axis_labels)

    # draw x-axis the full length of the chart
    buf += f"{CORNER}{bars(chart_width - 1)}\n"

    # now push x-axis labels
    buf += f"{x_axis_labels}\n"

    # draw statistics
    buf += f"Avg. = {average_value:.2f}\n"
    if excluded_count != 0:
        buf += f"excluded {excluded_count} values\n"

    return buf

def draw(values: Sequence[float], bins: int, positive: bool):
    print(format(values, bins, positive))

