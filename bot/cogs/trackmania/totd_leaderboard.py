from datetime import datetime

from discord import ApplicationContext, Option
from discord.ext import commands
from discord.ext.pages import Paginator
from prettytable import PrettyTable
from trackmania import TOTD, InvalidTOTDDate, TMIOException
from trackmania.config import cache_flush_key

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.commons import format_seconds, format_time_split, split_list_of_lists
from bot.utils.discord import create_embed
from bot.utils.totd import get_totd_leaderboards

log = get_logger(__name__)


class TOTDLeaderboards(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        name="totd-leaderboards",
        description="Get a certain TOTD's leaderboard",
    )
    async def _totd_lb(
        self,
        ctx: ApplicationContext,
        year: Option(int, "The year", required=True),
        month: Option(str, "The month", choices=constants.Consts.months, required=True),
        day: Option(int, "The day", required=True),
    ):
        log_command(ctx, "totd-lb")
        await ctx.defer()

        log.debug("Doing Initial Basic Checks")
        if day < 1 or day > 31:
            await ctx.respond("Invalid Date")
            return
        if year < 2020:
            await ctx.respond("Invalid year")
            return
        log.debug("Passed Initial Basic Checks")

        log.debug("Getting Leaderboard Pages")
        leaderboard_pages = await get_totd_leaderboards(year, month, day)

        if leaderboard_pages is None:
            await ctx.respond("An unexpected error occured.")
            return

        log.debug("Creating Paginator")
        totd_paginator = Paginator(pages=leaderboard_pages, timeout=60)
        await totd_paginator.respond(ctx.interaction)


def setup(bot: Bot) -> None:
    """Load the TOTDLeaderboards cog."""
    bot.add_cog(TOTDLeaderboards(bot))
