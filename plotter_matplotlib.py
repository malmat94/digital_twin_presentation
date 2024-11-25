# Python/third-party imports
import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def two_separate_subplots(
    x: tuple | list | pd.DataFrame | pd.Series| np.ndarray,
    y1: tuple | list | pd.DataFrame | pd.Series| np.ndarray,
    y2: tuple | list | pd.DataFrame | pd.Series| np.ndarray,
    y1_title: str,
    y2_title: str,
    y1_axis_title: str,
    y2_axis_title: str
):
    # Creating the subplots area
    """
    Function to create two subplots in one figure, each with their own y-axis
    titles and axis titles.

    Parameters
    ----------
    x : tuple | list | pd.DataFrame | pd.Series| np.ndarray
        The x-values data for the both subplots.
    y1 : tuple | list | pd.DataFrame | pd.Series| np.ndarray
        The y-values data for the first subplot.
    y2 : tuple | list | pd.DataFrame | pd.Series| np.ndarray
        The y-values data for the second subplot.
    y1_title : str
        The title of the first subplot.
    y2_title : str
        The title of the second subplot.
    y1_axis_title : str
        The title of the y-axis of the first subplot.
    y2_axis_title : str
        The title of the y-axis of the second subplot.
    """
    # Creating matplotlib figure
    plt.figure(figsize=(18, 12))

    # Definition of first subplot
    plt.subplot(1, 2, 1)    # Coordinates: 1st row, 2 columns, 1st column
    plt.plot(x, y1, color='darkblue')
    plt.title(y1_title)
    plt.xlabel('time')
    plt.ylabel(y1_axis_title)
    plt.grid(True)

    # Definition of second plot
    plt.subplot(1, 2, 2)    # Coordinates: 1st row, 2 columns, 2nd column
    plt.plot(x, y2, color='lightblue')
    plt.title(y2_title)
    plt.xlabel('time')
    plt.ylabel(y2_axis_title)
    plt.grid(True)

    # tight_layout is for getting beautiful labels
    plt.tight_layout()
    plt.show()


def two_mutual_subplots(
    x: tuple | list | pd.DataFrame | pd.Series| np.ndarray,
    y1: tuple | list | pd.DataFrame | pd.Series| np.ndarray,
    y2: tuple | list | pd.DataFrame | pd.Series| np.ndarray,
    title: str,
    y_axis_name: str
):
    """
    Function to create two mutual subplots.

    Parameters
    ----------
    x : tuple | list | pd.DataFrame | pd.Series| np.ndarray
        The x-values data for both subplots.
    y1 : tuple | list | pd.DataFrame | pd.Series| np.ndarray
        The y-values data for the first subplot.
    y2 : tuple | list | pd.DataFrame | pd.Series| np.ndarray
        The y-values data for the second subplot.
    title : str
        The title of the entire figure.
    y_axis_name : str
        The title of the y-axis of the first subplot.
    """

    fig, ax1 = plt.subplots(figsize=(18, 12))
    ax1.plot(x, y1, color='darkblue', label='actual damage')
    ax1.set_xlabel('time')
    ax1.set_ylabel(y_axis_name)
    ax1.set_title(title)
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(x, y2, color='lightblue', label='predicted damage')
    ax2.set_ylabel('predicted damage')
    ax1.set_title(title)
    ax2.grid(True)

    plt.legend()
    plt.show()


def one_plot(
    x: tuple | list | pd.DataFrame | pd.Series| np.ndarray,
    y: tuple | list | pd.DataFrame | pd.Series| np.ndarray,
    title: str,
    y_axis_name: str,
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
    save : bool, optional
        Whether to save the plot as an image file. Default is False.
    """
    plt.figure(figsize=(18, 12))
    plt.plot(x, y, color='darkblue')
    plt.xlabel('time [s]')
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
    plt.show()


