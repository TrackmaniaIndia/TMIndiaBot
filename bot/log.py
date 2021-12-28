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


class CustomLogger(LoggerClass):
    """Custom Implementation of the `Logger` class with an added `trace` method"""

    def trace(self, msg: str, *args, **kwargs) -> None:
        """
        Log 'msg % args' with severity 'TRACE'.
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
        logger.trace("Houston, we have an %s", "interesting problem", exc_info=1)
        """
        if self.isEnabledFor(TRACE_LEVEL):
            self.log(TRACE_LEVEL, msg, *args, **kwargs)


def get_logger(name: Optional[str] = None) -> CustomLogger:
    """Utility to make mypy recognise that logger is of type `CustomLogger`."""
    return cast(CustomLogger, logging.getLogger(name))


def setup() -> None:
    """Setup Loggers."""
    logging.TRACE = TRACE_LEVEL
    logging.addLevelName(TRACE_LEVEL, "TRACE")
    logging.setLoggerClass(CustomLogger)

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
        level=TRACE_LEVEL,
        logger=root_log,
        stream=sys.stdout,
        fmt=format_string,
        datefmt=datefmt,
        field_styles=FIELD_STYLE,
    )

    root_log.setLevel(logging.DEBUG if constants.DEBUG_MODE else logging.INFO)
    get_logger("discord").setLevel(logging.WARNING)

    get_logger("asyncio").setLevel(logging.INFO)
