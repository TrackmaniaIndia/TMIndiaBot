"""Launches the Bot"""
import sys

import aiohttp

import bot
from bot import constants
from bot.bot import Bot, StartupError
from bot.log import get_logger

try:
    log = get_logger()

    log.critical("Starting Bot Instance")
    bot.instance = Bot.create()

    log.critical("Loading Extensions")
    bot.instance.load_extensions()

    log.critical("Running Bot")
    bot.instance.run(constants.Bot.token)
except StartupError as e:
    MESSAGE = "Unknown Startup Error has Occured"
    if isinstance(
        e.exception, (aiohttp.ClientConnectionError, aiohttp.ServerDisconnectedError)
    ):
        MESSAGE = "Could not Connect to the API"

    log = get_logger("bot")
    log.fatal("", exc_info=e.exception)
    log.fatal(MESSAGE)

    sys.exit(-1)
