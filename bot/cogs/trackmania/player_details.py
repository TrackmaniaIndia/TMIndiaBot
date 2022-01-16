from discord.commands import Option
from discord.ext import commands
from discord.ext.pages import Paginator

from bot.utils.discord.easy_embed import EZEmbed
from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.trackmania import TrackmaniaUtils

log = get_logger(__name__)


class PlayerDetails(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="playerdetails",
        description="Gets the player details of a sepcific username",
    )
    async def _player_details_slash(
        self,
        ctx: commands.Context,
        username: Option(str, "The username of the player", required=True),
    ):
        log_command(ctx, "player_details_slash")

        await ctx.defer()

        player_obj = TrackmaniaUtils(username)
        player_id = await player_obj.get_id()

        if player_id is None:
            # An Invalid Username was given, sending a message to the user
            log.critical("Invalid Player Username Received, Sending Error Message")
            await ctx.respond(
                embed=EZEmbed.create_embed(
                    title="Invalid Username Given",
                    description=f"Username Given: {username}",
                    color=common_functions.get_random_color(),
                ),
                delete_after=5,
                ephemeral=False,
            )
            return

        log.info("Getting Player Data")
        data_pages = await player_obj.get_player_data(player_id)

        if len(data_pages) == 1:
            log.info("Only 1 Page was Returned")
            await ctx.respond(embed=data_pages[0])
            return

        log.info("Received Data Pages")
        log.info("Creating Paginator")
        player_detail_paginator = Paginator(
            pages=data_pages,
            show_disabled=True,
            show_indicator=True,
            author_check=True,
            disable_on_timeout=True,
            loop_pages=False,
            timeout=120.0,
        )

        await player_obj.close()
        del player_obj

        await player_detail_paginator.respond(ctx.interaction)

    @commands.command(
        name="playerdetails",
        description="Gets the player details of a sepcific username",
    )
    async def _player_details(
        self,
        ctx: commands.Context,
        username: str,
    ):
        log_command(ctx, "player_details")

        player_obj = TrackmaniaUtils(username)
        player_id = await player_obj.get_id()

        if player_id is None:
            # An Invalid Username was given, sending a message to the user
            log.critical("Invalid Player Username Received, Sending Error Message")
            await ctx.send(
                embed=EZEmbed.create_embed(
                    title="Invalid Username Given",
                    description=f"Username Given: {username}",
                    color=common_functions.get_random_color(),
                ),
                delete_after=5,
                ephemeral=False,
            )
            return

        log.info("Getting Player Data")
        data_pages = await player_obj.get_player_data(player_id)

        if len(data_pages) == 1:
            log.info("Only 1 Page was Returned")
            await ctx.send(embed=data_pages[0])
            return

        log.info("Received Data Pages")
        log.info("Creating Paginator")
        player_detail_paginator = Paginator(
            pages=data_pages,
            show_disabled=True,
            show_indicator=True,
            author_check=True,
            disable_on_timeout=True,
            loop_pages=False,
            timeout=120.0,
        )

        await player_obj.close()
        del player_obj

        await player_detail_paginator.send(ctx)


def setup(bot: Bot):
    """Adds the PlayerDetails cog"""
    bot.add_cog(PlayerDetails(bot))
