import discord
import os
import subprocess
import threading

import util.logging.convert_logging as convert_logging

from dotenv import load_dotenv
from util.before_launch.file_check import file_check
from discord.ext import commands

# Setting up logging
log = convert_logging.get_logging()
log.info(f"Logging Setup for main.py")

# Getting Bot Token
log.info(f"Reading Bot Token")
load_dotenv()
BOT_TOKEN = os.getenv("BOTTOKEN")
log.info(f"Got Bot Token")

# Creating Bot with the following intents:
#   bans
#   dm_messages
#   dm_reactions
#   dm_typing
#   emojis
#   emojis_and_stickers
#   guild_messages
#   guild_reactions
#   guild_typing
#   integrations
#   invites
#   members
#   messages
#   reactions
#   typing
#   value
#   voice_states
#   webhooks
log.info(f"Creating Client")
client = commands.Bot(
    prefix="!!", intents=discord.Intents.default(), debug_guild="876042400005505066"
)
log.info(f"Created Client")

# This Thread runs the TMIndiaBotApi, clone from https://github.com/artifexdevstuff/TMIndiaBotApi
log.info("Creating Thread for NPM Module")
npm_module = threading.Thread(
    target=subprocess.run, args=("npm run start",), kwargs={"shell": True}
)

log.info("Thread Created for NPM Module")

# Starting Bot
log.info("Starting Bot Startup")
if __name__ == "__main__":
    # Checking for Important Files
    file_check()

    # Asking if Dev Wants to Start API
    api_flag = input("Do you want to start the API? (y/n) ")

    if api_flag.lower() == "y" or api_flag.lower() == "yes":
        # Starting NPM Module
        log.info("Starting NPM Module thread")
        npm_module.start()
        log.info("NPM Module Thread Started")
        log.info("NPM Module Initialized, Resuming Bot INIT")
    else:
        log.critical("API will not be started, Resuming Bot INIT")

    # Loading Cogs
    log.info("Loading Slash Cogs")
    log.debug(f"Loading listeners.py")
    client.load_extension("cogs.listeners")
    log.debug(f"Loading generic.py")
    client.load_extension(f"cogs.generic")
    log.debug(f"Loading quote.py")
    client.load_extension(f"cogs.quote")
    log.debug(f"Loading trackmania.py")
    client.load_extension(f"cogs.trackmania")
    log.debug(f"Loading username.py")
    client.load_extension(f"cogs.username")
    log.info("Loaded Slash Cogs")

    # Running Bot Client
    client.run(BOT_TOKEN)
