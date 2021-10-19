import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import logging
from datetime import datetime
import jishaku

import util.logging.convert_logging as cl
import util.discord.easy_embed as ezembed
from util.logging.usage import record_usage, finish_usage
from util.before_launch.file_check import file_check
from util.discord.get_prefix import get_prefix

log = cl.get_logging()
log.info(f"Logging Setup for main.py")

log.info(f"Reading Bot Token")
load_dotenv()
BOT_TOKEN = os.getenv('BOTTOKEN')
log.info(f"Got Bot Token")

log.info(f'Creating Client')
client = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.default())
log.info(f'Created Client')

if __name__ == '__main__':
    file_check()

    # Loading Cogs
    log.info("Loading Cogs")
    for filename in os.listdir("./cogs"):
        SKIP_FILES = [
            "convert_logging.py",
            "common_functions.py",
        ]

        if filename.endswith(".py"):
            if filename in SKIP_FILES:
                log.debug(f"Skipping {filename}")
                continue

            log.debug(f"Loading {filename[:-3]}")
            client.load_extension(f"cogs.{filename[:-3]}")

    log.info("Loaded Cogs")
    
    log.debug("Loading JISHAKU")
    client.load_extension('jishaku')
    log.debug("Loaded JISHAKU")

    # Running Client
    client.run(BOT_TOKEN)