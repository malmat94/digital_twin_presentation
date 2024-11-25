# Internal imports
from settings import Settings
from db_handler import DBHandler
from calculate import calculate_destruction
from plotter_seaborn import three_separate_subplots, one_plot


def calculation_runner(
    start_timestamp: int,
    stop_timestamp: int,
    last_results_timestamp: int,
    plot_data:bool = True
) -> tuple[float, str, int, int]:
    """
    Runs the calculations and saves the results to the database.
    Optionally plots the input data and results.

    Parameters
    ----------
    start_timestamp : int
        The start timestamp of the data to be processed.
    stop_timestamp : int
        The end timestamp of the data to be processed.
    last_results_timestamp : int
        The latest timestamp of the results in the database.
    plot_data : bool, optional
        If True, plots the input data and results. Defaults to True.

    Returns
    -------
    tuple[float, str, int, int]
        A tuple containing the latest destruction, a saving message,
        the first timestamp of the results, and the last timestamp of the
        results.
    """
    # Load settings
    server_name, settings, sensors_db_settings, results_db_settings, _ = (
        Settings().get_db_settings()
    )

    # Get the objects of dbs
    sensors_db = DBHandler(
        server_name=server_name,
        database_name=sensors_db_settings['database']
    )
    results_db = DBHandler(
        server_name=server_name,
        database_name=results_db_settings['database']
    )

    # Load sensor data batch
    sensor_data = sensors_db.load_data(
        table_name=sensors_db_settings['table'],
        schema_name=sensors_db_settings['schema'],
        timestamps_list=[start_timestamp, stop_timestamp]
    )
    sensor_data.sort_values(by='timestamp', inplace=True)

    # Get the latest destruction
    latest_destruction = check_last_destruction(
        results_db=results_db,
        results_db_settings=results_db_settings,
        last_results_timestamp=last_results_timestamp
    )

    # Calculate the destruction and save it to db
    destruction = calculate_destruction(
        column_names=results_db_settings['columns'],
        sensor_data=sensor_data,
        latest_destruction=latest_destruction
    )
    destruction.sort_values(by='timestamp', inplace=True)
    latest_destruction = destruction["accumulated_destruction"].max()
    first_results_timestamp = destruction["timestamp"].min()
    latest_results_timestamp = destruction["timestamp"].max()
    saving_message = results_db.insert_data(
        table_name=results_db_settings['table'],
        schema_name=results_db_settings['schema'],
        data=destruction
    )

    # Plot the input data and results
    if plot_data:
        three_separate_subplots(
            x=sensor_data['timestamp'],
            y1=sensor_data['torque'],
            y2=sensor_data['speed'],
            y3=sensor_data['oli_temperature'],
            y1_title='Torque in time',
            y2_title='Speed in time',
            y3_title='Oli temperature in time',
            y1_axis_title='Torque [Nm]',
            y2_axis_title='Speed [RPM]',
            y3_axis_title='Oli temperature [C]',
            show=False,
            save=True,
            save_title='Input data'
        )
        one_plot(
            x=destruction['timestamp'],
            y=destruction['accumulated_destruction'],
            title='Destruction in time',
            y_axis_name='Destruction [%]',
            show=False,
            save=True
        )
    return (
        float(latest_destruction),
        saving_message,
        first_results_timestamp,
        latest_results_timestamp
    )


def check_last_destruction(
    results_db: DBHandler,
    results_db_settings: dict,
    last_results_timestamp: int = None
) -> float:
    """
    Retrieves the latest destruction value from the results database.

    Parameters
    ----------
    results_db : DBHandler
        Object for interacting with the results database.
    results_db_settings : dict
        Settings for the results database.
    last_results_timestamp : int
        The timestamp of the last recorded destruction value.
        Defaults to None.

    Returns
    -------
    float
        The latest destruction value.
    """
    if last_results_timestamp is None:
        # No data present, return 0
        return 0
    else:
        # Retrieve the latest destruction value
        last_destruction = results_db.load_data(
            table_name=results_db_settings['table'],
            schema_name=results_db_settings['schema'],
            columns=['accumulated_destruction'],
            timestamps_list=[last_results_timestamp, last_results_timestamp]
        )['accumulated_destruction'].values[0]
    return last_destruction
