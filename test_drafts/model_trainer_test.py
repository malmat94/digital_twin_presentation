"""Script to test the model trainer."""
# Python/third-party imports
from pathlib import Path

# Internal imports
from model_trainer import model_trainer
from settings import Settings

# Get the batch settings
calculation_batch_size, training_batch_size, predictions_batch_size =(
    Settings(
        settings_path=Path('../settings/settings.json')
    ).get_batch_settings()
)

# Determine the timestamps and train the models
start_timestamp = 1704067201
stop_timestamp = 1704074400
model_trainer(
    start_results_timestamp=start_timestamp,
    stop_results_timestamp=stop_timestamp
)
