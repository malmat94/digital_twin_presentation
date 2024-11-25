# Python/third-party imports
import os.path
from pathlib import Path
import json


class Settings:
    def __init__(self, settings_path: Path = 'settings/settings.json'):
        """
        Initialize Settings object with a specific settings file path.
        Settings should be build like this:
        {
          "server": "SERVER_NAME",
          "sensors": {
            "database": "Sensor_readings",
            "schema": "dbo",
            "table": "sensor_readings",
            "columns": ["timestamp", "torque", "speed", "oil_temperature"]
          },
          "results": {
            "database": "Results",
            "schema": "dbo",
            "table": "results",
            "columns": ["timestamp", "destruction", "accumulated_destruction"]
          },
          "predictions": {
            "database": "Results",
            "schema": "dbo",
            "table": "predictions",
            "columns": ["timestamp", "accumulated_destruction"]
          },
          "data_batches": {
            "calculations_batch_size": CALC_BATCH_SIZE (int),
            "training_batch_size": TRAINING_BATCH_SIZE (int),
            "predictions_batch_size": PREDICTIONS_BATCH_SIZE (int)
          }
        }

        Parameters
        ----------
        settings_path : Path
            Path to the settings JSON file.
            Defaults to 'settings/settings.json'.

        Notes
        -----
        This method opens the settings file and loads its content into
        the `settings` attribute.

        Raises
        ------
        FileNotFoundError
            If the settings file is not found at the specified path.
        """

        self.settings_path = settings_path
        if os.path.isfile(self.settings_path):
            with open(settings_path, "r") as settings_json:
                self.settings = json.load(settings_json)
        else:
            raise FileNotFoundError(
                f"Settings file not found at {settings_path} "
                "Make sure to create the file according to example in "
                "docstrings and try again."
            )


    def get_db_settings(self) -> tuple[str, dict, dict, dict, dict]:
        """
        Retrieve server name and specific database settings from self.settings.

        Returns
        -------
        tuple
            A tuple containing the server name, the entire settings dictionary,
            and settings for sensors, results, and predictions databases.
        """

        server_name = self.settings['server']
        sensors_db_settings = self.settings['sensors']
        results_db_settings = self.settings['results']
        predictions_db_settings = self.settings['predictions']
        return (
            server_name,
            self.settings,
            sensors_db_settings,
            results_db_settings,
            predictions_db_settings
        )


    def get_batch_settings(self) -> tuple[int, int, int]:
        """
        Retrieve settings for data batch sizes from self.settings.

        Returns
        -------
        tuple
            A tuple containing the sizes of data batches for calculations,
            training, and predictions.
        """

        calculation_batch_size = (
            self.settings["data_batches"]["calculations_batch_size"]
        )
        training_batch_size = (
            self.settings["data_batches"]["training_batch_size"]
        )
        predictions_batch_size = (
            self.settings["data_batches"]["predictions_batch_size"]
        )

        return (
            calculation_batch_size,
            training_batch_size,
            predictions_batch_size
        )
