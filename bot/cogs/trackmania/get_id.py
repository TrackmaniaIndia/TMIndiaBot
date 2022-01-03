import discord
from discord.commands import permissions
from discord.commands.commands import Option
from discord.ext import commands

import bot.utils.discord.easy_embed as ezembed
import bot.utils.quote as quote_functions
from bot import constants
from bot.bot import Bot
from bot.log import get_logger
from bot.log import log_command
from bot.utils.commons import get_random_color
from bot.utils.trackmania import NotAValidUsername
from bot.utils.trackmania import TrackmaniaUtils

log = get_logger(__name__)


class GetID(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.id_url = "http://localhost:3000/tm2020/player/{}/id"

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="getid",
        description="Gets an ID for a specific username",
    )
    async def _get_id_slash(
        self,
        ctx: commands.Context,
        username: Option(str, "The username of the player", required=True),
    ):
        log_command(ctx, "get_id_slash")

        log.debug(f"Creating TrackmaniaUtil object for {username}")
        username_obj = TrackmaniaUtils(username)
        log.debug(f"Created TrackmaniaUtil object for {username}")

        log.info(f"Getting ID for {username}")
        id = username_obj.get_id()

        await ctx.respond(
            embed=ezembed.create_embed(
                title=f"Here is the ID for {username}", description=id
            ),
            ephemeral=True,
        )

    @commands.command(name="getid", description="Gets an ID for a specific username")
    async def _get_id(self, ctx: commands.Context, username: str):
        log_command(ctx, "get_id")

        log.debug(f"Creating TrackmaniaUtil object for {username}")
        username_obj = TrackmaniaUtils(username)
        log.debug(f"Created TrackmaniaUtil object for {username}")

        log.info(f"Getting ID for {username}")
        id = username_obj.get_id()

        await ctx.send(
            embed=ezembed.create_embed(
                title=f"Here is the ID for {username}", description=id
            ),
        )

    # @_get_id_slash.error
    # async def error(self, ctx: commands.Context, error: Exception):
    #     log.error(error)

    #     if isinstance(error, NotAValidUsername):
    #         log.error("Invalid Username")

    #         await ctx.send(
    #             embed=ezembed.create_embed(
    #                 title="That is not a valid username",
    #                 color=constants.Colours.soft_red,
    #             )
    #         )


def setup(bot: Bot):
    """Add the GetID Cog"""
    bot.add_cog(GetID(bot))
