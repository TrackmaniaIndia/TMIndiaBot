import discord
from discord.ext import commands

import util.logging.convert_logging as convert_logging
from util.cog_helpers.generic_helper import get_version
from util.logging.usage import record_usage, finish_usage
from util.constants import guild_ids
import util.discord.easy_embed as ezembed

log = convert_logging.get_logging()


class GenericSlash(commands.Cog, description="Generic Functions"):
    statuses = []
    version = ""

    def __init__(self, client):
        self.client = client
        self.version = get_version()

    @commands.slash_command(
        guild_ids=guild_ids,
        name="ping",
        description="Get ping of bot to discord api in milliseconds",
    )
    async def _ping(self, ctx: commands.Context):
        await ctx.respond("Pong! {}ms".format(round(self.client.latency * 1000, 2)))

    @commands.slash_command(
        guild_ids=guild_ids, name="version", description="Displays bot version"
    )
    async def _version(self, ctx: commands.Context):
        await ctx.respond(f"Bot Version is {self.version}", ephemeral=True)

    @commands.slash_command(
        guild_ids=guild_ids, name="source", description="Displays Github Source Code"
    )
    async def _source(self, ctx: commands.Context):
        await ctx.respond(
            "Here is the source code\nhttps://github.com/NottCurious/TMIndiaBot",
            ephemeral=True,
        )

    @commands.slash_command(
        guild_ids=guild_ids,
        name="invite",
        description="Gives you an invite link for the server",
    )
    async def _invite(self, ctx: commands.Context):
        await ctx.respond(
            "Here is an invite for you to share with your friends\nhttps://discord.gg/yvgFYsTKNr",
            ephemeral=True,
        )


def setup(client):
    client.add_cog(GenericSlash(client))
