"""Class gotten from python-discord/bot which is licensed under MIT License"""
import logging
import os
import sys
from logging import Logger, handlers
from pathlib import Path
from typing import Optional, TYPE_CHECKING, cast

import coloredlogs

from bot import constants

TRACE_LEVEL = 5

if TYPE_CHECKING:
    LoggerClass = Logger
else:
    LoggerClass = logging.getLoggerClass()


def get_logger(name: Optional[str] = None) -> Logger:
    """Utility to make mypy recognise that logger is of type `CustomLogger`."""
    return cast(Logger, logging.getLogger(name))


def setup() -> None:
    """Setup Loggers."""
    root_log = get_logger()

    format_string = "%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - %(message)s"
    datefmt = "%H:%M:%S"
    log_format = logging.Formatter(format_string)

    if constants.FILE_LOGS:
        log_file = Path("logs", "bot.log")
        log_file.parent.mkdir(exist_ok=True)
        file_handler = handlers.RotatingFileHandler(
            log_file, maxBytes=5242880, backupCount=7, encoding="utf8"
        )
        file_handler.setFormatter(log_format)
        root_log.addHandler(file_handler)

    if "COLOREDLOGS_LEVEL_STYLES" not in os.environ:
        coloredlogs.DEFAULT_LEVEL_STYLES = {
            **coloredlogs.DEFAULT_LEVEL_STYLES,
            "critical": {"bold": True, "color": "red"},
            "debug": {"color": "green"},
            "error": {"color": "red"},
            "info": {"bold": True, "color": "green"},
            "warning": {"bold": True, "color": "yellow"},
        }

    if "COLOREDLOGS_LOG_FORMAT" not in os.environ:
        coloredlogs.DEFAULT_LOG_FORMAT = format_string

    FIELD_STYLE = {
        "asctime": {"color": "green"},
        "levelname": {"bold": True, "color": "black"},
        "filename": {"color": "cyan"},
        "funcName": {"color": "blue"},
    }

    coloredlogs.install(
        level=logging.INFO,
        logger=root_log,
        stream=sys.stdout,
        fmt=format_string,
        datefmt=datefmt,
        field_styles=FIELD_STYLE,
    )

    root_log.setLevel(logging.DEBUG if constants.DEBUG_MODE else logging.INFO)
    get_logger("discord").setLevel(logging.WARNING)

    get_logger("asyncio").setLevel(logging.INFO)
