import subprocess
import threading

import aiohttp

import bot
from bot import constants
from bot.bot import Bot, StartupError
from bot.log import get_logger

try:
    log = get_logger()

    log.info("Creating NPM Module for the API")
    npm_module = threading.Thread(
        target=subprocess.run, args=("npm run start",), kwargs={"shell": True}
    )
    log.info("Created NPM Module for API")

    # Asking if Dev Wants to Start API
    api_flag = input("Do you want to start the API? (y/n) ")

    if api_flag.lower() == "y" or api_flag.lower() == "yes":
        # Starting NPM Module
        log.critical("Starting API")
        npm_module.start()
    else:
        log.critical("Not Starting API")
        print("temp")

    log.critical("Starting Bot Instance")
    bot.instance = Bot.create()

    log.critical("Loading Extensions")
    bot.instance.load_extensions()

    log.critical("Running Bot")
    bot.instance.run(constants.Bot.token)
except StartupError as e:
    message = "Unknown Startup Error has Occured"
    if isinstance(
        e.exception, (aiohttp.ClientConnectionError, aiohttp.ServerDisconnectedError)
    ):
        message = "Could not Connect to the API"

    log = get_logger("bot")
    log.fatal("", exc_info=e.exception)
    log.fatal(message)

    exit(-1)
