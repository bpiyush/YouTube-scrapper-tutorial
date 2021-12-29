"""Utility functions for plotting."""

# NOTE: this script is not tested yet

from typing import Any
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mc
from matplotlib import rc
import colorsys
import seaborn as sns


def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


def fig2data(fig: plt.Figure):
    """Convert a Matplotlib figure to a numpy array with RGBA channels"""
    # draw the renderer
    fig.canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = fig.canvas.get_width_height()
    buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the
    # ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis=2)
    return buf.reshape(h, w, 4)


def fig2im(fig: plt.Figure):
    """Convert figure to ndarray

    Args:
        fig (plt.Figure): plt figure object

    Returns:
        np.ndarray: figure converted to np.ndarray
    """
    img_data = fig2data(fig).astype(np.int32)
    plt.close()
    return img_data[:, :, :3] / 255.


def plot_categorical_attribute(
        df: pd.DataFrame,
        attribute: str,
        hue: str = None,
        title: str = None,
        ax: plt.axis = None,
        figsize: tuple = (8, 6),
        show: bool = False,
        kwargs: dict = dict(),
    ):
    """Plots a count plot for a categorical attribute (column) in a dataframe.

    Args:
        df (pd.DataFrame): input dataframe
        attribute (str): attribute (df column) to be plotted
        hue (str, optional): hue. Defaults to None.
        title (str, optional): plot title. Defaults to None.
        ax (plt.axis, optional): plt axis. Defaults to None.
        figsize (tuple, optional): size of figure. Defaults to (8, 6).
        show (bool, optional): whether to render. Defaults to False.
        kwargs (dict, optional): additional keyword args. Defaults to dict().
    """
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)

    sns.countplot(data=df, x=attribute, ax=ax, hue=hue, **kwargs)
    ax.grid()
    if title is None:
        title = f'Countplot of {attribute}'
    ax.set_title(title)
    ax.set_xlabel('')

    patches = ax.patches
    for patch in patches:
        x, _ = patch.xy
        counts = patch.get_height()
        ax.text(x + 0.1, counts + 25, counts)

    if show:
        plt.show()
