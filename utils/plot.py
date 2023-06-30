import os

import matplotlib.pyplot as plt
import numpy as np

parameters = {
    "figure.figsize": [15, 10],
    "axes.labelsize": 25,
    "xtick.labelsize": 25,
    "ytick.labelsize": 25,
    "legend.fontsize": 25,
    "lines.markersize": 24,
    "lines.linewidth": 5,
    # "font.family": "arial",
    "font.size": 30,
}
plt.rcParams.update(parameters)
mcolor = [
    # from dark to white
    (97 / 255, 30 / 255, 30 / 255),
    (205 / 255, 68 / 255, 50 / 255),
    (239 / 255, 145 / 255, 99 / 255),
    (236 / 255, 194 / 255, 155 / 255),
    (243 / 255, 217 / 255, 190 / 255),
]
mmarker = [".", "v", "^", "*", "d", "p", "x", "s"]


def plot_lines(
    fig_name: str,
    xticks: np.ndarray,
    xiticklabels: np.ndarray,
    xlabel: str,
    ylim: tuple,
    ylabel: str,
    values_list: list,
    labels: list,
    path: str,
):
    fig, ax = plt.subplots()
    # There are 8 ticks in the x-axis, change the value if wanting more or less.
    ax.set_xticks(xticks)
    ax.set_xticklabels(xiticklabels)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(ylim)

    for i in range(len(values_list)):
        ax.plot(
            np.arange(values_list[i].size),
            values_list[i],
            linewidth=5,
            ms=24,
            color=mcolor[i],
            label=labels[i],
            marker=mmarker[i],
        )

    ax.legend(loc="upper left")

    plt.grid(axis="y")
    if not os.path.exists(path):
        os.makedirs(path)
    plt.tight_layout()
    plt.savefig(f"{path}/{fig_name}.pdf")


def plot_two_lines(
    fig_name: str,
    xrange: int,
    xlabel: str,
    y1lim: tuple,
    y1label: str,
    y2lim: tuple,
    y2label: str,
    values1: list,
    label1: str,
    values2: list,
    label2: str,
    path: str,
):
    """
    A function that plots two lines with different y-axes on a single figure using 'subplot()' function and saves the
    resulting figure as a PDF file.

    Args:
    fig_name (string):  the name of the saved PDF file.
    xrange   (integer): indicating the maximum value of the x-axis.
    xlabel   (string):  the label of the x-axis.
    y1lim    (tuple):   (min, max), indicating the range of the y1-axis.
    y1label  (string):  the label of the y1-axis.
    y2lim    (tuple):   (min, max), indicating the range of the y2-axis.
    y2label  (string):  the label of the y2-axis.
    values1  (ndarray): [data], an array of values representing the y1-axis coordinates of the data points for line 1.
    values2  (ndarray): [data], an array of values representing the y2-axis coordinates of the data points for line 2.

    Returns:
    None.
    """

    # create the subplots with shared x-axis
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # set x-axis properties
    ax1.set_xlabel(xlabel)
    ax1.set_xticks(np.arange(0, xrange))  # , xrange // 8))

    # set y1-axis properties
    ax1.set_ylabel(y1label)
    ax1.set_ylim(y1lim)

    # set y2-axis properties
    ax2.set_ylabel(y2label)
    ax2.set_ylim(y2lim)

    # plot line 1
    ax1.plot(
        np.arange(len(values1)),
        values1,
        color=mcolor[0],
        label=label1,
        marker=mmarker[0],
    )

    # plot line 2
    ax2.plot(
        np.arange(len(values2)),
        values2,
        color=mcolor[2],
        label=label2,
        marker=mmarker[3],
    )

    # set legend and grid
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    plt.grid(axis="y")

    # save the plot
    if not os.path.exists(path):
        os.makedirs(path)
    plt.tight_layout()
    plt.savefig(f"{path}/{fig_name}.pdf")


def plot_bar(
    fig_name: str,
    xlabel: list,
    xticks: list,
    ylabel: str,
    ylim: tuple,
    values: list,
    label: list,
    bar_width: float,
    path: str,
):
    """
    Plots a bar chart.

    Args:
        fig_name (str): Name of the output PDF file.
        xlabel  (list): List of x-axis labels.
        xticks  (list): List of x-axis tick locations.
        ylabel  (str): Label for the y-axis.
        ylim   (tuple): (min, max), indicating the range of the y-axis.
        values  (list): List of values to be plotted.
        bar_width (float): Width of each bar.
        label    (list): list of labels.
        Note that the size of the xlabel, the xticks, and the values are the same.

    Returns:
        None
    """
    # Create a new figure and axis object
    fig, ax = plt.subplots()

    # Set the x-axis labels and tick locations
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabel)

    # Set the y-axis label and lim
    ax.set_ylabel(ylabel)
    ax.set_ylim(ylim)

    # Plot the bar chart
    ax.bar(xticks, values, width=bar_width, color=mcolor, label=label)
    ax.legend(loc="upper right")

    if not os.path.exists(path):
        os.makedirs(path)
    plt.tight_layout()
    plt.savefig(f"{path}/{fig_name}.pdf")


def plot_comparison_bar(
    fig_name: str,
    xlabel: list,
    xticks: list,
    ylabel: str,
    ylim: tuple,
    values1: list,
    values2: list,
    label1: str,
    label2: str,
    bar_width: float,
    path: str,
):
    """
    Plots a comparison bar chart with two objects.

    Args:
        fig_name (str): Name of the output PDF file.
        xlabel (list): List of x-axis labels.
        xticks (list): List of x-axis tick locations.
        ylabel (str): Label for the y-axis.
        ylim   (tuple): (min, max), indicating the range of the y-axis.
        values1 (list): List of values to be plotted.
        values2 (list): List of values to be plotted.
        label1 (str): The label of the first bar.
        label2 (str): The label of the second bar.
        bar_width (float): Width of each bar.

        Note that the size of the xlabel, the xticks, and the values should be the same.

    Returns:
        None
    """
    # Create a new figure and axis object
    fig, ax = plt.subplots()

    # Set the x-axis labels and tick locations
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabel)

    # Set the y-axis label and lim
    ax.set_ylabel(ylabel)
    ax.set_ylim(ylim)

    # Set x1 and x2
    x1 = [i - bar_width / 2 for i in xticks]
    x2 = [i + bar_width / 2 for i in xticks]

    # Plot the bar chart
    ax.bar(x1, values1, width=bar_width, color=mcolor[0], label=label1)
    ax.bar(x2, values2, width=bar_width, color=mcolor[1], label=label2)

    ax.legend(loc="upper left")

    # Create the 'plots' directory if it does not exist
    if not os.path.exists(path):
        os.makedirs(path)
    plt.tight_layout()
    plt.savefig(f"{path}/{fig_name}.pdf")


def plot_horizontal_bar(
    fig_name: str,
    value_label: list,
    values: list,
    part_name: list,
    height: float,
    path: str,
):
    """
    plot a horizontal bar.

    Args:
        fig_name: the name of this figure.
        value_label: the label of each bar.
        values: [[data],[data]], each [data] represents a bar.
        part_name: the name of each part of the bar.
        height: the width of the bar.
    """
    # Create a new figure and axis object
    fig, ax = plt.subplots()

    values = np.array(values)
    values_cum = values.cumsum(axis=1)

    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(values, axis=1).max())

    for i, (colname, color) in enumerate(zip(part_name, mcolor[: len(part_name)])):
        width = values[:, i]
        starts = values_cum[:, i] - width
        rects = ax.barh(
            value_label, width, left=starts, height=height, label=colname, color=color
        )

        r, g, b = color
        text_color = "white" if r * g * b < 0.5 else "darkgrey"
        ax.bar_label(rects, label_type="center", color=text_color)

    ax.legend(ncols=len(part_name), bbox_to_anchor=(0, 1), loc="lower left")

    if not os.path.exists(path):
        os.makedirs(path)
    plt.tight_layout()
    plt.savefig(f"{path}/{fig_name}.pdf")
