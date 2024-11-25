# Python/third-party imports
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    root_mean_squared_error
)

# Internal imports
from plotter_seaborn import two_mutual_subplots
from db_handler import DBHandler
from settings import Settings


def check_the_predictions(
    start_timestamp: int,
    stop_timestamp: int,
    plot: bool = True
) -> tuple[float, float, float, float] | None:
    """
    Retrieves the predictions and results data from the databases in the given
    timestamp range and calculates the metrics of model performance.

    Parameters
    ----------
    start_timestamp : int
        The start timestamp of the data to be processed.
    stop_timestamp : int
        The end timestamp of the data to be processed.
    plot : bool, optional
        If True, plots the input data and results. Defaults to True.

    Returns
    -------
    tuple
        A tuple containing the mean squared error, root mean squared error,
        mean absolute error, and the R^2 score of the model predictions.
    """

    # Load settings
    server_name, _, _, results_db_settings, predictions_db_settings = (
        Settings().get_db_settings()
    )

    # Get the objects of dbs
    results_db = DBHandler(
        server_name=server_name,
        database_name=results_db_settings['database']
    )
    predictions_db = DBHandler(
        server_name=server_name,
        database_name=predictions_db_settings['database']
    )

    # Get the prediction and results data
    predictions_data = predictions_db.load_data(
        table_name=predictions_db_settings['table'],
        schema_name=predictions_db_settings['schema'],
        timestamps_list=[start_timestamp, stop_timestamp]
    )
    predictions_data.sort_values('timestamp', inplace=True)
    if predictions_data.empty:
        return None
    results_data = results_db.load_data(
        table_name=results_db_settings['table'],
        schema_name=results_db_settings['schema'],
        timestamps_list=[start_timestamp, stop_timestamp]
    )
    results_data.sort_values('timestamp', inplace=True)
    if len(predictions_data) != len(results_data):
        raise ValueError("Prediction and results lengths does not match!")

    # Calculate and display the metrics of model performance
    mse = mean_squared_error(
        results_data['accumulated_destruction'],
        predictions_data['accumulated_destruction']
    )
    rmse = root_mean_squared_error(
        results_data['accumulated_destruction'],
        predictions_data['accumulated_destruction']
    )
    mae = mean_absolute_error(
        results_data['accumulated_destruction'],
        predictions_data['accumulated_destruction']
    )
    r2 = r2_score(
        results_data['accumulated_destruction'],
        predictions_data['accumulated_destruction']
    )

    # Plot if requested and return
    if plot:
        two_mutual_subplots(
            x=results_data['timestamp'],
            y1=results_data['accumulated_destruction'],
            y2=predictions_data['accumulated_destruction'],
            title='Destruction',
            y_axis_name='destruction',
            save=True,
            show=False
        )
    return mse, rmse, mae, r2
