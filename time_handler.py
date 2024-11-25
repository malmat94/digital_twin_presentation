# Internal imports
from db_handler import DBHandler
from settings import Settings


def get_timestamps():
    # Load settings
    """
    Retrieves the timestamps for the next calculations batch.

    Returns
    -------
    tuple[int, int, int]
        A tuple containing the start timestamp of the sensors data, the
        minimum timestamp of the results data, and the maximum timestamp of the
        results data.
    """

    (
        server_name,
        settings,
        sensors_db_settings,
        results_db_settings,
        _
    ) = Settings().get_db_settings()

    # Get the objects of dbs
    sensors_db = DBHandler(
        server_name=server_name,
        database_name=sensors_db_settings['database']
    )
    results_db = DBHandler(
        server_name=server_name,
        database_name=results_db_settings['database']
    )

    # Get The latest results timestamp -> sensors timestamps for new calcs
    max_min_results_timestamps = results_db.get_max_and_min_time(
        table_name=results_db_settings['table'],
        schema_name=results_db_settings['schema']
    )
    max_results_timestamp = max_min_results_timestamps.loc[0, 'max_timestamp']
    min_results_timestamp = max_min_results_timestamps.loc[0, 'min_timestamp']
    if max_results_timestamp is None:
        start_sensors_timestamp = sensors_db.get_max_and_min_time(
            table_name=sensors_db_settings['table'],
            schema_name=sensors_db_settings['schema']
        ).loc[0, 'min_timestamp']
    else:
        start_sensors_timestamp = max_results_timestamp + 1

    return (
        start_sensors_timestamp,
        min_results_timestamp,
        max_results_timestamp
    )
