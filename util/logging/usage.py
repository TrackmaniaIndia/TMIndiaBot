import discord
from discord.ext import commands

import json
from dotenv import load_dotenv
from datetime import datetime

import util.logging.convert_logging as cl

load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")


log = cl.get_logging()

DEFAULT_PREFIX = "*"


async def record_usage(self, ctx: commands.Context) -> None:
    """Records Usage of Commands

    Args:
        ctx (commands.Context): The Message Context
    """
    log.info(
        f"{ctx.author} used {ctx.command} at {ctx.message.created_at} in {ctx.guild}"
    )


async def finish_usage(self, ctx: commands.Context) -> None:
    """Records Finish Usage of Commands

    Args:
        ctx (commands.Context): Message Context
    """
    log.info(f"{ctx.author} finished using {ctx.command} in {ctx.guild}")


async def record_usage_slash(self, ctx: commands.Context) -> None:
    """Records Usage of Slash Commands

    Args:
        ctx (commands.Context): Message Context
    """
    log.info(
        f"{ctx.author.name} used slash command -> {ctx.command} at {ctx.message.created_at} in {ctx.guild}"
    )


async def finish_usage_slash(self, ctx: commands.Context) -> None:
    """Records Finish Usage of Commands

    Args:
        ctx (commands.Context): Message Context
    """
    log.info(f"{ctx.author} finished using slash command: {ctx.command} in {ctx.guild}")
