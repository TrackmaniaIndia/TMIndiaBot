import discord
from discord.commands import permissions
from discord.commands.commands import Option
from discord.ext import commands

import util.discord.easy_embed as ezembed
from util.logging import convert_logging
from util.logging.command_log import log_command
from util.trackmania.tm2020.player import get_player_id

# Creating Logger
log = convert_logging.get_logging()


class Username(commands.Cog):
    def __init__(self, client):
        self.client = client
        log.info("cogs.username has finished initializing")

    @commands.slash_command(
        name="getid",
        description="Gets the Trackmania ID of A Player",
    )
    @permissions.is_owner()
    async def _get_id(
        self,
        ctx: commands.Context,
        username: Option(str, "The Trackmania2020 Username", required=True),
    ):
        log_command(ctx, ctx.command.name)
        log.info(f"Getting Data of {username}")
        embed = ezembed.create_embed(
            title="ID",
            description=get_player_id(username),
            color=discord.Color.random(),
        )
        log.debug("Got Data and Created Embed, Sending")
        # await ctx.respond(get_player_id(username))
        await ctx.respond(embed=embed, ephemeral=True)
        log.debug("Sent Embed")


def setup(client: discord.Bot):
    client.add_cog(Username(client))
