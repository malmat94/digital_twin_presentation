# Python/third-party imports
import os
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def three_separate_subplots(
    x: tuple | list | pd.DataFrame | pd.Series | np.ndarray,
    y1: tuple | list | pd.DataFrame | pd.Series | np.ndarray,
    y2: tuple | list | pd.DataFrame | pd.Series | np.ndarray,
    y3: tuple | list | pd.DataFrame | pd.Series | np.ndarray,
    y1_title: str,
    y2_title: str,
    y3_title: str,
    y1_axis_title: str,
    y2_axis_title: str,
    y3_axis_title: str,
    show: bool = True,
    save: bool = False,
    save_title: str = None
):
    """
    Function to create three separate subplots in one figure, each with their
    own y-axis titles and axis titles.

    Parameters
    ----------
    x : tuple | list | pd.DataFrame | pd.Series | np.ndarray
        The x-values data for all subplots.
    y1 : tuple | list | pd.DataFrame | pd.Series | np.ndarray
        The y-values data for the first subplot.
    y2 : tuple | list | pd.DataFrame | pd.Series | np.ndarray
        The y-values data for the second subplot.
    y3 : tuple | list | pd.DataFrame | pd.Series | np.ndarray
        The y-values data for the third subplot.
    y1_title : str
        The title of the first subplot.
    y2_title : str
        The title of the second subplot.
    y3_title : str
        The title of the third subplot.
    y1_axis_title : str
        The title of the y-axis of the first subplot.
    y2_axis_title : str
        The title of the y-axis of the second subplot.
    y3_axis_title : str
        The title of the y-axis of the third subplot.
    show : bool, optional
        Whether to display the plot. Default is True.
    save : bool, optional
        Whether to save the plot as an image file. Default is False.
    save_title : str, optional
        The title used for saving the plot file. If not provided, defaults to
        'Untitled'.

    """

    data1 = pd.DataFrame({'x': x, 'y1': y1})
    data2 = pd.DataFrame({'x': x, 'y2': y2})
    data3 = pd.DataFrame({'x': x, 'y3': y3})

    # Setting the seaborn style
    sns.set_theme(style='whitegrid')

    # Creating the seaborn subplots
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(24, 8))

    # Definition of the first plot
    sns.lineplot(data=data1, x='x', y='y1', ax=axes[0], color='darkblue')
    axes[0].set_title(y1_title)
    axes[0].set_xlabel('time [s]')
    axes[0].set_ylabel(y1_axis_title)

    # Definition of the second plot
    sns.lineplot(data=data2, x='x', y='y2', ax=axes[1], color='lightblue')
    axes[1].set_title(y2_title)
    axes[1].set_xlabel('time [s]')
    axes[1].set_ylabel(y2_axis_title)

    # Definition of the third plot
    sns.lineplot(data=data3, x='x', y='y3', ax=axes[2], color='red')
    axes[2].set_title(y3_title)
    axes[2].set_xlabel('time [s]')
    axes[2].set_ylabel(y3_axis_title)

    # tight_layout is for getting beautiful labels
    plt.tight_layout()

    if save:
        if save_title is None:
            save_title = 'Untitled'
            raise Warning("No save title provided, using 'Untitled' as title.")

        plotting_path = Path("plots/")
        os.makedirs(plotting_path, exist_ok=True)
        title = save_title.replace(" ", "_")
        plt.savefig(
            os.path.join(plotting_path, f"{min(x)}_-_{max(x)}_{title}.png")
        )

    if show:
        plt.show()


def two_separate_subplots(
    x: tuple | list | pd.DataFrame | pd.Series | np.ndarray,
    y1: tuple | list | pd.DataFrame | pd.Series | np.ndarray,
    y2: tuple | list | pd.DataFrame | pd.Series | np.ndarray,
    y1_title: str,
    y2_title: str,
    y1_axis_title: str,
    y2_axis_title: str,
    show: bool = True,
    save: bool = False,
    save_title: str = None
):
    """
    Function to create two separate subplots in one figure, each with their
    own y-axis titles and axis titles.

    Parameters
    ----------
    x : tuple | list | pd.DataFrame | pd.Series | np.ndarray
        The x-values data for both subplots.
    y1 : tuple | list | pd.DataFrame | pd.Series | np.ndarray
        The y-values data for the first subplot.
    y2 : tuple | list | pd.DataFrame | pd.Series | np.ndarray
        The y-values data for the second subplot.
    y1_title : str
        The title of the first subplot.
    y2_title : str
        The title of the second subplot.
    y1_axis_title : str
        The title of the y-axis of the first subplot.
    y2_axis_title : str
        The title of the y-axis of the second subplot.
    show : bool, optional
        Whether to display the plot. Default is True.
    save : bool, optional
        Whether to save the plot as an image file. Default is False.
    save_title : str, optional
        The title used for saving the plot file. If not provided, defaults to
        'Untitled'.
    """
    data1 = pd.DataFrame({'x': x, 'y1': y1})
    data2 = pd.DataFrame({'x': x, 'y2': y2})

    # Setting the seaborn style
    sns.set_theme(style='whitegrid')

    # Creating the seaborn subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

    # Definition of the first plot
    sns.lineplot(data=data1, x='x', y='y1', ax=axes[0], color='darkblue')
    axes[0].set_title(y1_title)
    axes[0].set_xlabel('time')
    axes[0].set_ylabel(y1_axis_title)

    # Definition of the second plot
    sns.lineplot(data=data2, x='x', y='y2', ax=axes[1], color='lightblue')
    axes[1].set_title(y2_title)
    axes[1].set_xlabel('time')
    axes[1].set_ylabel(y2_axis_title)

    # tight_layout is for getting beautiful labels
    plt.tight_layout()
    if save:
        if save_title is None:
            save_title = 'Untitled'
            raise Warning("No save title provided, using 'Untitled' as title.")

        plotting_path = Path("plots/")
        os.makedirs(plotting_path, exist_ok=True)
        title = save_title.replace(" ", "_")
        plt.savefig(
            os.path.join(plotting_path, f"{min(x)}_-_{max(x)}_{title}.png")
        )

    if show:
        plt.show()


def two_mutual_subplots(
    x: tuple | list | pd.DataFrame | pd.Series | np.ndarray,
    y1: tuple | list | pd.DataFrame | pd.Series | np.ndarray,
    y2: tuple | list | pd.DataFrame | pd.Series | np.ndarray,
    title: str,
    y_axis_name: str,
    show: bool = True,
    save: bool = False
):
    # Conversion to dataframes for easier data manipulation
    """
    Function to create two mutual subplots in one figure.

    Parameters
    ----------
    x : tuple | list | pd.DataFrame | pd.Series| np.ndarray
        The x-values data for the both subplots.
    y1 : tuple | list | pd.DataFrame | pd.Series| np.ndarray
        The y-values data for the first subplot.
    y2 : tuple | list | pd.DataFrame | pd.Series| np.ndarray
        The y-values data for the second subplot.
    title : str
        The title of the entire figure.
    y_axis_name : str
        The title of the y-axis of the first subplot.
    show : bool, optional
        Whether to display the plot. Default is True.
    save : bool, optional
        Whether to save the plot as an image file. Default is False.
    """

    data = pd.DataFrame({'x': x, 'y1': y1, 'y2': y2})

    # Setting the seaborn style
    sns.set_theme(style='whitegrid')

    # Creating the plot with double y-axis
    fig, ax1 = plt.subplots(figsize=(18, 6))
    sns.lineplot(
        data=data,
        x='x',
        y='y1',
        ax=ax1,
        color='darkblue',
        label='actual damage'
    )
    ax1.set_ylabel(y_axis_name)
    ax1.set_xlabel('time')
    ax1.set_title(title)

    # Tworzenie drugiej osi
    ax2 = ax1.twinx()
    sns.lineplot(
        data=data,
        x='x',
        y='y2',
        ax=ax2,
        color='lightblue',
        label='predicted damage'
    )
    ax2.set_ylabel('predicted damage')

    # Adding the legend
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # tight_layout is for getting beautiful labels
    plt.tight_layout()

    if save:
        plotting_path = Path("plots/")
        os.makedirs(plotting_path, exist_ok=True)
        title = title.replace(" ", "_")
        plt.savefig(
            os.path.join(plotting_path, f"{min(x)}_-_{max(x)}_{title}.png")
        )

    if show:
        plt.show()


def one_plot(
    x: tuple | list | pd.DataFrame | pd.Series | np.ndarray,
    y: tuple | list | pd.DataFrame | pd.Series | np.ndarray,
    title: str,
    y_axis_name: str,
    show: bool = True,
    save: bool = False
):
    """
    Function to create one plot.

    Parameters
    ----------
    x : tuple | list | pd.DataFrame | pd.Series| np.ndarray
        The x-values data for the plot.
    y : tuple | list | pd.DataFrame | pd.Series| np.ndarray
        The y-values data for the plot.
    title : str
        The title of the plot.
    y_axis_name : str
        The title of the y-axis of the plot.
    show : bool, optional
        Whether to display the plot. Default is True.
    save : bool, optional
        Whether to save the plot as an image file. Default is False.
    """

    data = pd.DataFrame({'x': x, 'y': y})

    # Setting the seaborn style
    sns.set_theme(style='whitegrid')

    # Creating the single plot
    plt.figure(figsize=(18, 6))
    sns.lineplot(data=data, x='x', y='y', color='darkblue')
    plt.xlabel('time')
    plt.ylabel(y_axis_name)
    plt.title(title)
    plt.grid(True)
    if save:
        plotting_path = Path("plots/")
        os.makedirs(plotting_path, exist_ok=True)
        title = title.replace(" ", "_")
        plt.savefig(
            os.path.join(plotting_path, f"{min(x)}_-_{max(x)}_{title}.png")
        )
    if show:
        plt.show()
