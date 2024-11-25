# Python/third-party imports
from pathlib import Path
import math
import json
import pandas as pd

# Internal imports
from settings import Settings
from logger_handler import logger_handler
from time_handler import get_timestamps
from calculation_runner import calculation_runner
from model_trainer import model_trainer
from destruction_predictor import destruction_predictor
from check_the_predictions import check_the_predictions


# Pipeline:
# 1. Get the timestamp
# 2. Calculate the destruction
# 3. If we have 1 day of results - train the model
# 4. If we have 1 day of results - make a prediction
# 5. Check the predictions
# 6. When the predictions are bad, train the model after next day

# Load settings and prediction scheduler
calculation_batch_size, training_batch_size, predictions_batch_size =(
    Settings().get_batch_settings()
)
with (
    open(
        Path('prediction_models/prediction_schedule.json'),
        'r'
    ) as schedule_json
):
    prediction_schedule = json.load(schedule_json)

# Get the timestamps and start calcualtion.
(
    sensor_initial_timestamp,
    very_first_results_timestamp,
    last_results_timestamp
 ) = (
    get_timestamps()
)
sensor_final_timestamp = sensor_initial_timestamp + calculation_batch_size
logger_handler().info(
    '------------------------------------------'
    '------------------------------------------'
)
logger_handler().info('Pipeline started!')
logger_handler().info(f'Stage 1: calculating the destruction...')
logger_handler().info(
    f"Calculating the destruction for the batch: "
    f"{pd.to_datetime(sensor_initial_timestamp, unit='s')} - "
    f"{pd.to_datetime(sensor_final_timestamp, unit='s')}"
)
(
    latest_destruction,
    calculations_saving_message,
    first_results_timestamp,
    last_results_timestamp
) = (
    calculation_runner(
        start_timestamp=sensor_initial_timestamp,
        stop_timestamp=sensor_final_timestamp,
        last_results_timestamp=last_results_timestamp
    )
)
if type(latest_destruction) == float:
    logger_handler().info('Calculations performed successfully!')
    logger_handler().info(
        f'Actual destruction: '
        f'{round(latest_destruction, 3)}%'
    )
    logger_handler().info(calculations_saving_message)
else:
    logger_handler().error('Calculations failed!')
    raise EOFError

# Stage 2
logger_handler().info(f'Stage 2: training the model...')
if very_first_results_timestamp is None:
    results_time_amount = 0
else:
    results_time_amount = last_results_timestamp - very_first_results_timestamp
if results_time_amount >= training_batch_size:

    # Training the model
    full_days = math.floor(results_time_amount / training_batch_size)
    training_start = very_first_results_timestamp
    training_stop = training_start + full_days * training_batch_size
    if training_stop not in prediction_schedule["model_trainings"]:
        logger_handler().info(
            f"Training the model for the batch: "
            f"{pd.to_datetime(training_start, unit='s')} - "
            f"{pd.to_datetime(training_stop, unit='s')}"
        )
        model_message = model_trainer(
            start_results_timestamp=very_first_results_timestamp,
            stop_results_timestamp=last_results_timestamp
        )
        logger_handler().info(model_message)
        prediction_schedule["model_trainings"].append(int(training_stop))
        with (
            open(
                Path('prediction_models/prediction_schedule.json'),
                'w'
            ) as schedule_json
        ):
            json.dump(prediction_schedule, schedule_json, indent=4)
    else:
        logger_handler().info(
            'Model will be trained only for the full days '
            'of processed results.'
        )

    # Predicting the destruction
    prediction_start = last_results_timestamp + 1
    prediction_stop = prediction_start + predictions_batch_size
    try:
        last_performed_prediction = prediction_schedule["predictions"][-1]
        latest_results_destruction = None
    except IndexError:
        last_performed_prediction = 0
        latest_results_destruction = latest_destruction
    if (
            prediction_stop not in prediction_schedule["predictions"]
            and prediction_stop - last_performed_prediction
            > predictions_batch_size
    ):
        logger_handler().info(
            f"Predicting the destruction for: "
            f"{pd.to_datetime(prediction_start, unit='s')} - "
            f"{pd.to_datetime(prediction_stop,unit='s')}"
        )
        prediction_saving_message = destruction_predictor(
            prediction_start=prediction_start,
            prediction_stop=prediction_stop,
            latest_results_destruction=latest_results_destruction
        )
        if type(prediction_saving_message) == str:
            logger_handler().info('Predictions performed successfully!')
            logger_handler().info(prediction_saving_message)
        else:
            logger_handler().error('Predictions failed!')
            raise EOFError
        prediction_schedule["predictions"].append(int(prediction_stop))
        with (
            open(
                Path('prediction_models/prediction_schedule.json'),
                'w'
            ) as schedule_json
        ):
            json.dump(prediction_schedule, schedule_json, indent=4)
    else:
        logger_handler().info(
            'Predictions will be performed only for full hours '
            'of processed results.'
        )

    # Check the predictions
    if results_time_amount - training_batch_size >= calculation_batch_size:
        check_start = first_results_timestamp
        check_stop = check_start + predictions_batch_size
        logger_handler().info(
            f"Checking the destruction prediction for: "
            f"{pd.to_datetime(check_start, unit='s')} - "
            f"{pd.to_datetime(check_stop, unit='s')}"
        )
        result = check_the_predictions(
            start_timestamp=check_start,
            stop_timestamp=check_stop
        )
        if result is not None:
            logger_handler().info(
                "Model performance check results:"
                f"\n - Mean square error value = {result[0]}"
                f"\n - Root square mean error value = {result[1]}"
                f"\n - Mean absolute error value = {result[2]}"
                f"\n - Coefficient of determination value = {result[3]}"
            )
        else:
            logger_handler().info(
                f"Predictions was not performed, there's nothing to check."
            )
else:
    logger_handler().info("There's not enough data for predictions...")
