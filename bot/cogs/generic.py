import os

import discord
from discord.commands import permissions
from discord.ext import commands

from bot.log import get_logger

# Creating Logger
log = get_logger()


class Generic(commands.Cog, description="Generic Functions"):
    # Statuses for the bot, will be gotten by a function.

    # Init Generic Cog
    def __init__(self, client: commands.Bot):
        self.client = client

        log.info("cogs.generic has finished initializing")

    @commands.slash_command(
        name="ping",
        description="Get ping of bot in ms",
    )
    async def _ping(self, ctx: commands.Context):
        await ctx.respond(f"Pong! {round(self.client.latency * 1000, 2)}ms")


def setup(client: discord.Bot):
    client.add_cog(Generic(client))
