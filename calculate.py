# Python/third-party imports
import pandas as pd


def calculate_destruction(
    column_names: list,
    sensor_data: pd.DataFrame,
    latest_destruction: float = 0
) -> pd.DataFrame:
    """
    Calculates the destruction percentage based on sensor data and returns
    the result as a DataFrame.

    Parameters
    ----------
    column_names : list
        A list containing the column names for the resulting DataFrame.
    sensor_data : DataFrame
        A DataFrame containing the sensor data with columns 'torque', 'speed',
        'oli_temperature', and 'timestamp'.
    latest_destruction : float, optional
        The initial destruction value to be added to the cumulative destruction.
        Default is 0.

    Returns
    -------
    result : DataFrame
        A DataFrame with columns for timestamps, destruction percentage, and
        cumulative destruction.
    """

    torque = sensor_data['torque'] / 1_000_000  # [MNm]
    speed = sensor_data['speed'] / 60   # [RPS]
    oli_temperature = sensor_data['oli_temperature']
    destruction = (torque * speed + oli_temperature)/ 5_000_000 # [%]

    result = pd.DataFrame(
        {
            column_names[0]: sensor_data['timestamp'],
            column_names[1]: destruction
        }
    )
    result[column_names[2]] = (
            result[column_names[1]].cumsum() + latest_destruction
    )
    return result
