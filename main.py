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

import cogs.convert_logging as cl
import cogs.common_functions as cf

# Importing Fields from .env
load_dotenv()
BOTTOKEN = os.getenv("BOTTOKEN")
# log_level = os.getenv("LOG_LEVEL")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")
# testing_server_id = os.getenv("TESTING_SERVER_ID")
# version = os.getenv("VERSION")

log_level, discord_log_level, testing_server_id, version = "", "", "", ""

with open("./config.json") as file:
    config = json.load(file)

    log_level = config["log_level"]
    discord_log_level = config["discord_log_level"]
    testing_server_id = config["testing_server_id"]
    version = config["bot_version"]

# Constants
DEFAULT_PREFIX = "*"

log = logging.getLogger(__name__)
log = cl.get_logging(log_level, discord_log_level)

log.info("Logging Setup")

"""
log.info()
log.debug()
log.warning()
log.critical()
log.error()
"""

if not os.path.exists("./prefixes.json"):
    log.critical(
        "Prefixes.json Doesn't Exist, Creating and Dumping Testing Server Stuff"
    )
    log.critical("Edit Prefixes.json to add your own Testing Server ID")

    prefixes = {"876042400005505066": DEFAULT_PREFIX}

    with open("./prefixes.json", "w") as file:
        json.dump(prefixes, file, indent=4)
        file.close()

    log.critical("Prefixes.json Created, Please Restart the Program")
    exit()


def get_prefix(client, message):
    with open("prefixes.json", "r") as file:
        prefixes = json.load(file)
        file.close()

    return prefixes[str(message.guild.id)]


# Making the Client
client = commands.Bot(command_prefix=get_prefix)


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


# Catch all command errors, send them to developers.
@client.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        emb = discord.Embed(
            title=":warning: Command not found", color=cf.get_random_color()
        )
        await ctx.send(embed=emb)

        # Stop further execution
        return None

    log.debug(f"Reading Config File for Devs")
    with open("config.json", "r") as file:
        config = json.loads(file.read())
        file.close()
    log.debug(f"Found Devs")

    pingStr = ""

    log.debug(f"Checking for Ping")
    for dev in config["developers"]:
        if dev["error_ping"]:
            pingStr += f"<@!{dev['id']}> "
        log.debug(f"Ping for {dev['id']} set to {dev['error_ping']}")
    log.debug(f"Created Ping String")

    log.debug(f"Receiving Error Channel")
    channel = client.get_channel(876069587140087828)
    log.debug(f"Found Error Channel")

    log.debug(f"Creating Embed")
    embed = discord.Embed(title=":warning: " + str(error), color=0xFF0000)

    embed.add_field(name="Author Username", value=ctx.author, inline=False)
    embed.add_field(name="Author ID", value=ctx.author.id, inline=False)
    embed.add_field(name="Guild Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Guild ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Message content", value=ctx.message.content, inline=False)
    log.debug(f"Created Embed")

    log.debug(f"Sending Embed")
    await channel.send(pingStr, embed=embed)
    log.debug(f"Embed Sent, Error Handler Quit")


# Loading Cogs
log.info("Loading Cogs")
for filename in os.listdir("./cogs"):
    SKIP_FILES = [
        "convert_logging.py",
        "common_functions.py",
        "community_content_promoter.py",
    ]

    if filename.endswith(".py"):
        if filename in SKIP_FILES:
            log.debug(f"Skipping {filename}")
            continue

        log.debug(f"Loading {filename[:-3]}")
        client.load_extension(f"cogs.{filename[:-3]}")

log.info("Loaded Cogs")

# Running Client
client.run(BOTTOKEN)
