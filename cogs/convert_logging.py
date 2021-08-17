import logging
import coloredlogs
import discord


def get_logging(normlog, discordlog):
    logdict = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "critical": logging.CRITICAL,
        "warning": logging.WARNING,
        "error": logging.ERROR,
    }
    log_level = logdict[normlog]
    discord_log_level = logdict[discordlog]

    DiscordLogger = logging.getLogger("discord")
    DiscordLogger.setLevel(discord_log_level)
    handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    DiscordLogger.addHandler(handler)

    log = logging.getLogger(__name__)

    fieldstyle = {
        "asctime": {"color": "green"},
        "levelname": {"bold": True, "color": "black"},
        "filename": {"color": "cyan"},
        "funcName": {"color": "blue"},
    }

    levelstyles = {
        "critical": {"bold": True, "color": "red"},
        "debug": {"color": "green"},
        "error": {"color": "red"},
        "info": {"color": "magenta"},
        "warning": {"color": "yellow"},
    }

    coloredlogs.install(
        level=log_level,
        logger=log,
        fmt="%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - %(message)s",
        datefmt="%H:%M:%S",
        field_styles=fieldstyle,
        level_styles=levelstyles,
    )

    return log
