import discord
from discord.ext import commands
import logging
import json
from dotenv import load_dotenv
from datetime import datetime

import functions.logging.convert_logging as convert_logging

load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")


log = logging.getLogger(__name__)
log = convert_logging.get_logging()

DEFAULT_PREFIX = "*"


async def record_usage(self, ctx: commands.Context) -> None:
    log.info(
        f"{ctx.author} used {ctx.command} at {ctx.message.created_at} in {ctx.guild}"
    )

    log_check = ""

    with open("./data/json_data/config.json") as file:
        data = json.load(file)
        log_check = data["log_function_usage"]
        file.close()

    if not log_check:
        log.debug(f"log_check is False, Returning")
        return
    log.debug(f"log_check is True, Sending Message")

    log.debug(f"Sending Message to Error Channel")
    channel = self.client.get_channel(876442289382248468)

    log.debug(f"Creating Embed")
    embed = discord.Embed(title=":clapper: Command Used", color=0x23FFFF)

    embed.add_field(name="Author Username", value=ctx.author, inline=False)
    embed.add_field(name="Author ID", value=ctx.author.id, inline=False)
    embed.add_field(name="Guild Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Guild ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Message content", value=ctx.message.content, inline=False)
    embed.set_footer(text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url)

    log.debug(f"Created Embed")

    log.debug(f"Sending Embed")
    await channel.send(embed=embed)
    log.debug(f"Embed Sent, Error Handler Quit")


async def finish_usage(self, ctx: commands.Context) -> None:
    log.info(f"{ctx.author} finished using {ctx.command} in {ctx.guild}")

    log_check = ""

    with open("./data/json_data/config.json") as file:
        data = json.load(file)
        log_check = data["log_function_usage"]
        file.close()

    if not log_check:
        log.debug(f"log_check is False, Returning")
        return
    log.debug(f"log_check is True, Sending Message")

    log.debug(f"Sending Message to Error Channel")
    channel = self.client.get_channel(876442289382248468)

    log.debug(f"Creating Embed")
    embed = discord.Embed(title=":medal: Command Finished", color=0x00FF00)

    embed.add_field(name="Author Username", value=ctx.author, inline=False)
    embed.add_field(name="Author ID", value=ctx.author.id, inline=False)
    embed.add_field(name="Guild Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Guild ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Message content", value=ctx.message.content, inline=False)

    embed.set_footer(text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url)

    log.debug(f"Created Embed")
    log.debug(f"Sending Embed")
    await channel.send(embed=embed)
    log.debug(f"Embed Sent, Error Handler Quit")
