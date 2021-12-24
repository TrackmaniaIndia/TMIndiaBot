import datetime
import json

import discord
from discord.ext import commands

from util.logging import convert_logging

log = convert_logging.get_logging()


def log_command(ctx: commands.Context, command: str):
    """
    Logs a command to a file.
    """
    debug_or_info = "info"

    with open("./data/config.json", "r", encoding="UTF-8") as file:
        config = json.load(file)
        debug_or_info = config["log_level"]

    if debug_or_info == "info":
        log.info(f"{ctx.author} used {command} in {ctx.guild.name}")
    elif debug_or_info == "debug":
        log.debug(
            f"{ctx.author.id}|{ctx.author.name}|{ctx.author.discriminator}|{ctx.guild.id}|{ctx.guild.name}|{ctx.channel.id}|{ctx.channel.name}|{command}"
        )

    with open("logs/commands.log", "a", encoding="UTF-8") as file:
        file.write(
            f"{datetime.datetime.now()}|{ctx.author.id}|{ctx.author.name}|{ctx.author.discriminator}|{ctx.guild.id}|{ctx.guild.name}|{ctx.channel.id}|{ctx.channel.name}|{command}\n"
        )


def log_join_guild(guild: discord.Guild):
    log.info(f"{datetime.datetime.now()}|Joined {guild.name}|ID: {guild.id}")
    with open("logs/commands.log", "a", encoding="UTF-8") as file:
        file.write(f"{datetime.datetime.now()}|Joined {guild.name}|ID: {guild.id}")


def log_leave_guild(guild: discord.Guild):
    log.info(f"{datetime.datetime.now()}|Left {guild.name}|ID: {guild.id}")
    with open("logs/commands.log", "a", encoding="UTF-8") as file:
        file.write(f"{datetime.datetime.now()}|Left {guild.name}|ID: {guild.id}")
