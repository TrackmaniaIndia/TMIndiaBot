import discord
from discord.ext import commands
from discord.utils import get

import util.logging.convert_logging as convert_logging
from util.cog_helpers.generic_helper import get_version
from util.logging.usage import record_usage, finish_usage
from util.guild_ids import guild_ids
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
    @commands.before_invoke(
        record_usage
    )  # Doesn't Work With Slash Commands, Must Check or Change
    @commands.after_invoke(finish_usage)
    async def _ping(self, ctx: commands.Context):
        await ctx.respond("Pong! {}ms".format(round(self.client.latency * 1000, 2)))

    @commands.slash_command(
        guild_ids=guild_ids, name="version", description="Displays bot version"
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def _version(self, ctx: commands.Context):
        await ctx.respond(f"Bot Version is {self.version}")

    @commands.slash_command(
        guild_ids=guild_ids, name="source", description="Displays Github Source Code"
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def _source(self, ctx: commands.Context):
        embed = ezembed.create_embed(
            title="Source Code",
            description="https://github.com/NottCurious/TMIndiaBot",
            color=discord.Colour.random(),
        )
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(GenericSlash(client))
