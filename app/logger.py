import os
import logging
import colorlog
from datetime import datetime


def setup_logger():
    """Return a logger with a default ColoredFormatter."""
    # Formatter for the stream handler with color codes
    stream_formatter = colorlog.ColoredFormatter(
        "%(cyan)s%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        reset=True,
        log_colors={
            "DEBUG": "blue",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style='%',
    )

    # Formatter for the file handler without color codes
    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    logger = colorlog.getLogger("example_logger")

    # Stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    # File handler
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = os.path.join(log_dir, f'{current_time}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    logger.setLevel(logging.INFO)

    return logger


logger = setup_logger()
