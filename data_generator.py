# Python/third-party imports
import pandas as pd
import numpy as np


def generate_sinusoidal(
    start_timestamp: int,
    end_timestamp: int,
    data_type: str,
    max_val: float,
    min_val: float = 0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generates a sinusoidal curve of given amplitude and frequency,
    with a certain noise level.

    Parameters
    ----------
    start_timestamp : int
        The start timestamp of the generated array.
    end_timestamp : int
        The end timestamp of the generated array.
    max_val : float
        The maximum value of the generated array.
    min_val : float, default=0
        The minimum value of the generated array.
    data_type : string
        The type of data to generate.

    Returns
    -------
    timestamps : array
        An array of timestamps with 1 second interval
    sinus : array
        The generated sinusoidal curve
    """

    amplitude = max_val - min_val
    if data_type == "torque":
        frequency = 4 / (24 * 60 * 60)
        noise_level = 0.02 * (max_val - min_val)
    elif data_type == "speed":
        frequency = 4 / (24 * 60 * 60)
        noise_level = 0.02 * (max_val - min_val)
    elif data_type == "temperature":
        frequency = 1 / (24 * 60 * 60)
        noise_level = 0.005 * (max_val - min_val)
    else:
        raise ValueError(f'Wrong data type: {data_type}')
    phase = 200
    num_points = end_timestamp - start_timestamp

    timestamps = np.arange(start_timestamp, end_timestamp, 1)
    x = np.arange(0, num_points, 1)
    sinus = np.sin(2 * np.pi * frequency * x + phase)
    sinus = sinus * 0.5 * amplitude + 0.5 * amplitude
    sinus = sinus + np.random.normal(0.0, noise_level, num_points)
    return timestamps, sinus


def generate_data(
    start_timestamp: int,
    end_timestamp: int,
    max_torque: float,
    max_speed: float,
    min_temp: float,
    max_temp: float
) -> pd.DataFrame:
    """
    Generates a DataFrame with artificial data representing torque,
    speed, and oil temperature of a wind turbine.

    The data is generated using a sinusoidal curve with a certain
    noise level. The generated data is suitable for testing and
    development purposes.

    Parameters
    ----------
    start_timestamp : int
        The start timestamp of the generated data
    end_timestamp : int
        The end timestamp of the generated data
    max_torque : float
        The maximum torque value of the generated data
    max_speed : float
        The maximum speed value of the generated data
    min_temp : float
        The minimum oil temperature value of the generated data
    max_temp : float
        The maximum oil temperature value of the generated data

    Returns
    -------
    artificial_data : pd.DataFrame
        A DataFrame with four columns: timestamp, torque, speed, and
        oil_temperature. The data is indexed by timestamp and is
        suitable for plotting or further analysis.

    # Examples
    # --------
    # >>> artificial_data = generate_data(
    # ...     start_timestamp=1704067201,
    # ...     end_timestamp=1704067201 + 31 * 24 * 60 * 60,
    # ...     max_torque=3000,
    # ...     max_speed=300,
    # ...     min_temp=-20,
    # ...     max_temp=100
    # ... )
    # >>> artificial_data.head()
    #     timestamp     torque      speed         oli_temperature
    # 0  1704067201  1514.852113  151.933098        50.221012
    # 1  1704067202  1502.770991  156.332536        56.010039
    # 2  1704067203  1493.451980  140.106548        57.847200
    # 3  1704067204  1499.304553  153.293359        60.485997
    # 4  1704067205  1509.562148  136.744071        57.517079
    """

    timestamps, torque = generate_sinusoidal(
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        max_val=max_torque,
        data_type="torque"
    )
    _, speed = generate_sinusoidal(
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        max_val=max_speed,
        data_type="speed"
    )
    _, temp = generate_sinusoidal(
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        max_val=max_temp,
        min_val=min_temp,
        data_type="temperature"
    )
    artificial_data = pd.DataFrame(
        {
            "timestamp": timestamps,
            "torque": torque,
            "speed": speed,
            "oli_temperature": temp
        }
    )
    return artificial_data
