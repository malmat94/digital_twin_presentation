# Python/third-party imports
from decimal import Decimal
from pathlib import Path
import os
import joblib
from sklearn.ensemble import RandomForestRegressor

# Internal imports
from db_handler import DBHandler
from settings import Settings


def model_trainer(
    start_results_timestamp: int,
    stop_results_timestamp: int,
    model_type: str = 'RandomForestRegressor',
    save_model: bool = True,
    save_path: Path = Path('prediction_models')
) -> str:
    """
    Trains machine learning models on sensor and results data and optionally
    saves them.

    Parameters
    ----------
    start_results_timestamp : int
        The start timestamp for retrieving results data.
    stop_results_timestamp : int
        The stop timestamp for retrieving results data.
    model_type : str, optional
        The type of model to train. Defaults to 'RandomForestRegressor'.
    save_model : bool, optional
        If True, saves the trained models to the specified path. Defaults to
        True.
    save_path : Path, optional
        The path where models should be saved. Defaults to 'prediction_models'.

    Returns
    -------
    str
        A message indicating the duration of data used for training and the
        save status of the models.

    Raises
    ------
    ValueError
        If an unknown model type is specified.

    Notes
    -----
    This function loads sensor and results data from databases, processes it,
    and trains two RandomForestRegressor models: one for destruction and one
    for accumulated destruction.
    """

    # Get the settings and db objects
    server_name, settings, sensors_db_settings, results_db_settings, _ = (
        Settings().get_db_settings()
    )
    sensors_db = DBHandler(
        server_name=server_name,
        database_name=sensors_db_settings['database']
    )
    results_db = DBHandler(
        server_name=server_name,
        database_name=results_db_settings['database']
    )
    days = (stop_results_timestamp - start_results_timestamp)/ (24*60*60)

    # Load the whole results
    results_data = results_db.load_data(
        table_name=results_db_settings['table'],
        schema_name=results_db_settings['schema'],
        timestamps_list=[start_results_timestamp, stop_results_timestamp]
    )
    results_data.sort_values('timestamp', inplace=True)
    results_data['destruction'] = (
        results_data['destruction'].apply(
            lambda x: Decimal(x).quantize(
            Decimal('1.000000000'))
        )
    )
    results_data['accumulated_destruction'] = (
        results_data['accumulated_destruction'].apply(
            lambda x: Decimal(x).quantize(
                Decimal('1.000000000'))
        )
    )

    # Load the corresponding sensors data for the loaded results
    sensors_data = sensors_db.load_data(
        table_name=sensors_db_settings['table'],
        schema_name=sensors_db_settings['schema'],
        timestamps_list=[start_results_timestamp, stop_results_timestamp]
    )
    sensors_data.sort_values('timestamp', inplace=True)

    # Prepare data for destruction model and acc destruction model
    training_features = sensors_data
    training_features['time_amount'] = (
            training_features['timestamp'] - training_features[
        'timestamp'].iloc[0])
    destruction_features = training_features[[
        'torque',
        'speed',
        'oli_temperature']
    ]
    destruction_results = results_data[['destruction']].values.ravel()
    acc_destruction_features = training_features[[
        'time_amount'
    ]]
    acc_destruction_results = (
        results_data[['accumulated_destruction']].values.ravel()
    )
    if model_type == 'RandomForestRegressor':
        destruction_model = RandomForestRegressor()
        acc_destruction_model = RandomForestRegressor()
    else:
        raise ValueError('Unknown model type')
    destruction_model.fit(destruction_features, destruction_results)
    acc_destruction_model.fit(acc_destruction_features, acc_destruction_results)

    # Save the models if necessary
    final_basic_message = (
        f"{model_type} models was trained based on "
        f"{int(days)} days of data."
    )
    if save_model:
        os.makedirs(save_path, exist_ok=True)
        destruction_model_path = os.path.join(
            save_path, Path('rfr_destruction_model.joblib')
        )
        acc_destruction_model_path = os.path.join(
            save_path, Path('rfr_acc_destruction_model.joblib')
        )
        joblib.dump(destruction_model, destruction_model_path )
        joblib.dump(acc_destruction_model, acc_destruction_model_path)
        additional_message = (
            f"\nModels were saved to:"
            f"\n - {destruction_model_path}"
            f"\n - {acc_destruction_model_path}"
        )
    else:
        additional_message = ""

    # Build the final message and return it
    final_message = final_basic_message + additional_message
    return final_message
