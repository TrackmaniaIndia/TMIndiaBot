import json
import logging
import coloredlogs


def get_logging() -> logging.Logger:
    """Makes a Logging.Logger to Avoid Copy Paste in Files

    Returns:
        logging.Logger: The Logger
    """
    # Getting the verbose level for the loggers
    with open("./data/config.json", encoding="UTF-8") as file:
        config = json.load(file)

        normal_logging_level = config["log_level"]
        discord_logging_level = config["discord_log_level"]

    log = logging.getLogger(__name__)

    logdict = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "critical": logging.CRITICAL,
        "warning": logging.WARNING,
        "error": logging.ERROR,
    }
    log_level = logdict[normal_logging_level]
    discord_log_level = logdict[discord_logging_level]

    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(discord_log_level)
    handler = logging.FileHandler(
        filename="./logs/discord.log", encoding="utf-8", mode="w"
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    discord_logger.addHandler(handler)

    field_style = {
        "asctime": {"color": "green"},
        "levelname": {"bold": True, "color": "black"},
        "filename": {"color": "cyan"},
        "funcName": {"color": "blue"},
    }

    level_styles = {
        "critical": {"bold": True, "color": "red"},
        "debug": {"color": "green"},
        "error": {"color": "red"},
        "info": {"bold": True, "color": "magenta"},
        "warning": {"bold": True, "color": "yellow"},
    }

    coloredlogs.install(
        level=log_level,
        logger=log,
        fmt="%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - %(message)s",
        datefmt="%H:%M:%S",
        field_styles=field_style,
        level_styles=level_styles,
    )

    return log
