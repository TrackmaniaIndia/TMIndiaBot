# Importing Packages
import discord
from discord.enums import DefaultAvatar
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import coloredlogs
import logging
import datetime

import cogs.convertLogging as cl

# Importing Fields from .env
load_dotenv()
BOTTOKEN = os.getenv("BOTTOKEN")
log_level = os.getenv("LOG_LEVEL")
discord_log_level = os.getenv("DISCORD_LOG_LEVEL")
testing_server_id = os.getenv("TESTING_SERVER_ID")
version = os.getenv("VERSION")

# Constants
DEFAULT_PREFIX = "*"

log = logging.getLogger(__name__)
log = cl.getLogging(log_level, discord_log_level)

log.info("Logging Setup")

"""
log.info()
log.debug()
log.warning()
log.critical()
log.error()
"""

if not os.path.exists("./prefixes.json"):
    log.critical('Prefixes.json Doesn\'t Exist, Creating and Dumping Testing Server Stuff')
    log.critical('Edit Prefixes.json to add your own Testing Server ID')

    prefixes = {
        "876042400005505066": "*"
    }

    with open("./prefixes.json", "w") as file:
        json.dump(prefixes, file, indent=4)
        file.close()

    log.critical('Prefixes.json Created, Please Restart the Program')
    exit()

def get_prefix(client, message):
    with open("prefixes.json", "r") as file:
        prefixes = json.load(file)
        file.close()

    return prefixes[str(message.guild.id)]

# Making the Client
client = commands.Bot(command_prefix=get_prefix)

async def record_usage(ctx):
    print(ctx.author, "used", ctx.command, "at", ctx.message.created_at)

# Events

# Assigning Prefix to Guild Upon Join
# Bot has to Be Active Upon Time of Joining for This to Work
@client.event
async def on_guild_join(guild):
    log.critical("Joined {}".format(guild.id))

    with open("prefixes.json", "r") as file:
        log.debug("Loading Prefixes File")
        prefixes = json.load(file)
        file.close()

    log.info(f"Setting Guild Prefix ({guild.id} -> {DEFAULT_PREFIX})")
    prefixes[str(guild.id)] = DEFAULT_PREFIX

    with open("prefixes.json", "w") as file:
        log.debug("Dumping Prefix Into Json File")
        json.dump(prefixes, file, indent=4)
        file.close()

# Removing Assigned Prefix if Bot is Kicked/Banned from Server
# Bot has to stay online as usual
@client.event
async def on_guild_remove(guild):
    log.critical("Removed from {}".format(guild.id))

    with open("prefixes.json", "r") as file:
        log.debug("Loading Prefixes File")
        prefixes = json.load(file)
        file.close()

    log.info("Removing Guild Prefix")
    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as file:
        log.debug("Dumping Prefix Into Json File")
        json.dump(prefixes, file, indent=4)
        file.close()

# Loading Cogs
log.info("Loading Cogs")
for filename in os.listdir("./cogs"):
    skip_files = ["convertLogging.py", "commonFunctions.py"]

    if filename.endswith('.py'):
        if filename in skip_files:
            continue

        log.debug(f"Loading {filename[:-3]}")
        client.load_extension(f"cogs.{filename[:-3]}")

log.info("Loaded Cogs")

# Running Client
client.run(BOTTOKEN)