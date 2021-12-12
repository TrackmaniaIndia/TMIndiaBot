import discord
import json
import datetime

import util.logging.convert_logging as convert_logging

from discord.ext import commands

log = convert_logging.get_logging()


def log_command(ctx: commands.Context, command: str):
    """
    Logs a command to a file.
    """
    file_flag = False
    debug_or_info = "info"

    with open("./data/config.json", "r") as f:
        config = json.load(f)
        debug_or_info = config["log_level"]

    if debug_or_info == "info":
        log.info(f"{ctx.author} used {command} in {ctx.guild.name}")
    elif debug_or_info == "debug":
        log.debug(
            f"{ctx.author.id}|{ctx.author.name}|{ctx.author.discriminator}|{ctx.guild.id}|{ctx.guild.name}|{ctx.channel.id}|{ctx.channel.name}|{command}\n"
        )

    with open("logs/commands.log", "a") as f:
        f.write(
            f"{datetime.datetime.now()}|{ctx.author.id}|{ctx.author.name}|{ctx.author.discriminator}|{ctx.guild.id}|{ctx.guild.name}|{ctx.channel.id}|{ctx.channel.name}|{command}\n"
        )
