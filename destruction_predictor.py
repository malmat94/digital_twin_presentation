# Python/third-party imports
import os.path
from pathlib import Path
import pandas as pd
import joblib

# Internal imports
from db_handler import DBHandler
from settings import Settings


def destruction_predictor(
    prediction_start: int,
    prediction_stop: int,
    latest_results_destruction: int| None = None,
    model_path: Path = Path('prediction_models/rfr_destruction_model.joblib')
) -> str:
    """
    Predicts the destruction and accumulated destruction over a given time
    period using a pre-trained machine learning model, and saves the
    predictions to the database.

    Parameters
    ----------
    prediction_start : int
        The start timestamp for the prediction data.
    prediction_stop : int
        The end timestamp for the prediction data.
    latest_results_destruction : int | None, optional
        The latest destruction value from the results database to be added to
        the cumulative predictions. If None, the latest prediction destruction
        is used. Defaults to None.
    model_path : Path, optional
        Path to the pre-trained machine learning model file.
        Defaults to 'prediction_models/rfr_destruction_model.joblib'.

    Returns
    -------
    str
        A message indicating the success of the data insertion into the
        database.

    Raises
    ------
    FileNotFoundError
        If the specified model file does not exist.
    """

    # Load settings
    (
        server_name,
        _,
        sensors_db_settings,
        results_db_settings,
        predictions_db_settings
    ) = Settings().get_db_settings()

    # Get the objects of dbs
    sensors_db = DBHandler(
        server_name=server_name,
        database_name=sensors_db_settings['database']
    )
    predictions_db = DBHandler(
        server_name=server_name,
        database_name=predictions_db_settings['database']
    )

    # Load the sensor data for predictions
    sensor_data = sensors_db.load_data(
        table_name=sensors_db_settings['table'],
        schema_name=sensors_db_settings['schema'],
        timestamps_list=[prediction_start, prediction_stop]
    )
    sensor_data.sort_values(by='timestamp', inplace=True)
    input_prediction_data = sensor_data[[
        'torque',
        'speed',
        'oli_temperature']
    ]

    # Load the model and predict the destruction
    if os.path.isfile(model_path):
        model = joblib.load(model_path)
    else:
        raise FileNotFoundError('Model not found')
    predictions = model.predict(input_prediction_data)
    predictions_df = pd.DataFrame(
        data=predictions,
        columns=['destruction']
    )

    # Calculate predicted accumulated destruction
    if latest_results_destruction is not None:
        predictions_df['accumulated_destruction'] = (
                predictions_df['destruction'].cumsum() +
                latest_results_destruction
        )
    else:
        last_prediction_timestamp = predictions_db.get_max_and_min_time(
            table_name=predictions_db_settings['table'],
            schema_name=predictions_db_settings['schema']
        ).loc[0, 'max_timestamp']
        latest_predicted_destruction = predictions_db.load_data(
            table_name=predictions_db_settings['table'],
            schema_name=predictions_db_settings['schema'],
            columns=['accumulated_destruction'],
            timestamps_list=[
                last_prediction_timestamp,
                last_prediction_timestamp
            ]
        ).loc[0, 'accumulated_destruction']
        predictions_df['accumulated_destruction'] = (
            predictions_df['destruction'].cumsum() + latest_predicted_destruction
        )
    predictions_df['timestamp'] = sensor_data['timestamp']
    predictions_df.sort_values(by='timestamp', inplace=True)

    # Save the predictions and return the message
    saving_message = predictions_db.insert_data(
        table_name=predictions_db_settings['table'],
        schema_name=predictions_db_settings['schema'],
        data=predictions_df
    )
    return saving_message
