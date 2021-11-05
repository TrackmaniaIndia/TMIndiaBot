import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import subprocess
import threading
import time

from datetime import datetime

# import jishaku

import util.logging.convert_logging as cl
import util.discord.easy_embed as ezembed
from util.logging.usage import record_usage, finish_usage
from util.before_launch.file_check import file_check
from util.discord.get_prefix import get_prefix

log = cl.get_logging()
log.info(f"Logging Setup for main.py")

log.info(f"Reading Bot Token")
load_dotenv()
BOT_TOKEN = os.getenv("BOTTOKEN")
log.info(f"Got Bot Token")

log.info(f"Creating Client")
client = commands.Bot(intents=discord.Intents.default())
log.info(f"Created Client")

log.info("Creating Thread for NPM Module")
# npm_module = threading.Thread(
#     target=subprocess.run, args=(["npm", "run", "start"],), kwargs={"shell": True}
# )
npm_module = threading.Thread(
    target=subprocess.run, args=("npm run start",), kwargs={"shell": True}
)

log.info("Thread Created for NPM Module")

log.info("Starting Bot Startup")
if __name__ == "__main__":
    file_check()

    log.info("Starting NPM Module thread")
    npm_module.start()
    log.info("NPM Module Thread Started")
    log.info("NPM Module Initialized, Resuming Bot INIT")

    # Loading Cogs
    log.info("Loading Slash Cogs")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            log.debug(f"Loading cogs.{filename[:-3]}")
            client.load_extension(f"cogs.{filename[:-3]}")
    log.info("Loaded Slash Cogs")

    Running Client
    client.run(BOT_TOKEN)
