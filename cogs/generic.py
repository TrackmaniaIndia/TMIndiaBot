import discord
from discord.ext import commands
import json
from datetime import datetime
from dotenv import load_dotenv
from itertools import cycle

import util.logging.convert_logging as convert_logging
from util.cog_helpers.generic_helper import *
from util.logging.usage import record_usage, finish_usage
from util.tasks.keep_alive import keep_alive
from util.tasks.status_change import change_status
from util.guild_ids import guild_ids

log = convert_logging.get_logging()
version = get_version()

DEFAULT_PREFIX = "--"


class Generic(commands.Cog, description="Generic Functions"):
    def __init__(self, client):
        self.client = client

    @commands.command(
        # guild_ids=guild_ids,
        name="ping",
        aliases=["latency", "pong", "connection"],
        help="Shows the Ping/Latency of the Bot in milliseconds.",
        brief="Shows Bot Ping.",
    )
    # @commands.slash_command(guild_ids=guild_ids, name='ping', description='Get ping of bot to discord api in milliseconds')
    @commands.before_invoke(
        record_usage
    )  # Doesn't Work With Slash Commands, Must Check or Change
    @commands.after_invoke(finish_usage)
    async def _ping(self, ctx: commands.Context):
        await ctx.reply(
            "Pong! {}ms".format(round(self.client.latency * 1000, 2)),
            mention_author=False,
        )

    @commands.command(
        name="prefix", help="Changes Prefix to Given prefix", brief="Changes Prefix"
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_any_role("admin", "Moderator", "Bot Developer")
    @commands.guild_only()
    async def _prefix(self, ctx: commands.Context, prefix: str):
        change_prefix(ctx, prefix)
        await ctx.reply("Prefix Changed to {}".format(prefix), mention_author=False)
        log.info(f"prefix successfully changed to {prefix} for {ctx.guild.name}")


def setup(client):
    client.add_cog(Generic(client))
