import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import logging
from datetime import datetime

import util.logging.convert_logging as cl
import util.discord.easy_embed as ezembed
from util.logging.usage import record_usage, finish_usage

log = cl.get_logging()
log.info(f"Logging Setup for main.py")

log.info(f"Reading Bot Token")
load_dotenv()
BOT_TOKEN = os.getenv('BOTTOKEN')
log.info(f"Got Bot Token")

