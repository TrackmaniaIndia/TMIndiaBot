import discord
import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed

from discord.commands.commands import Option
from discord.commands import permissions
from discord.ext import commands
from util.constants import guild_ids
from util.trackmania.tm2020.player import *
from util.discord.confirmation import Confirmer

log = convert_logging.get_logging()


class Trackmania(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        guild_ids=guild_ids,
        name="player_details",
        description="player details for a specific player",
    )
    async def _player_details(
        self,
        ctx: commands.Context,
        username: Option(str, "The Trackmania2020 Username", required=True),
    ):
        data = get_player_data(username)

        if data == None:
            error_embed = ezembed.create_embed(
                title="This user does not exist",
                description=f"Username given: {username}",
                color=discord.Colour.red(),
            )
            await ctx.respond(embed=error_embed)
            log.error(f"{username} is not a valid username")
        else:
            await ctx.respond(embed=data)


def setup(client):
    client.add_cog(Trackmania(client))
