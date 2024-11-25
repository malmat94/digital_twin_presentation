# Python/third-party imports
import os
from pathlib import Path
import logging


def logger_handler(
        logger_name: str = "TwinLogger",
        log_file_path: Path = 'logs/twin_logs.log'
) -> logging.Logger:
    # Logger configuration
    """
    Returns a logger object.

    Parameters
    ----------
    logger_name : str, optional
        The name of the logger object. Defaults to "TwinLogger".
    log_file_path : Path, optional
        The path to save the log file. Defaults to 'logs/twin_logs.log'.

    Returns
    -------
    logging.Logger
        The logger object.
    """

    if not os.path.isfile(log_file_path):
        log_dir = log_file_path.parent
        log_dir.mkdir(parents=True, exist_ok=True)
        Path(log_file_path).touch()

    logging.basicConfig(
        level=logging.INFO,  # Minimal display level
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log formats
        handlers=[
            logging.FileHandler(log_file_path),  # Saving logs to a file
            logging.StreamHandler()  # Displaying logs in the console
        ]
    )

    return logging.getLogger(logger_name)
