from datetime import datetime

import discord.ext.commands as commands
from discord import ApplicationContext, Option, SlashCommandOptionType
from discord.ext.pages import Page, PageGroup, Paginator
from trackmania import TOTD, InvalidTOTDDate

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import ViewAdder
from bot.utils.totd import get_totd_leaderboards, parse_totd_data

log = get_logger(__name__)


class LatestTOTD(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="latest-totd",
        description="Gets the data about the latest totd",
    )
    async def _latest_totd(self, ctx: ApplicationContext):
        log_command(ctx, "latest_totd")

        await ctx.defer()

        log.debug("Getting TOTD Data")
        totd_data = await TOTD.latest_totd()
        log.debug("Parsing Data")
        totd_page, buttons = await parse_totd_data(totd_data, None)

        _todays_date = datetime.now()
        year = _todays_date.year
        month = _todays_date.month
        day = _todays_date.day - 1

        log.debug("Getting TOTD leaderboards")
        totd_leaderboard = await get_totd_leaderboards(
            year, constants.Consts.months[month - 1], day
        )

        if totd_leaderboard is not None:
            log.debug("Creating a Paginator")
            totd_page = Page(embeds=[totd_page], custom_view=ViewAdder(buttons))

            page_groups = [
                PageGroup(pages=[totd_page], label="TOTD Data"),
                PageGroup(pages=totd_leaderboard, label="TOTD Leaderboard"),
            ]

            paginator = Paginator(pages=page_groups, show_menu=True)
            await paginator.respond(ctx.interaction)
        else:
            await ctx.respond(embed=totd_page, view=ViewAdder(buttons))

        # log.debug("Sending Embed")
        # await ctx.respond(embed=page, view=ViewAdder(buttons))

    @commands.slash_command(
        name="totd",
        description="Gets the TOTD Data of a certain date.",
    )
    async def _totd(
        self,
        ctx: ApplicationContext,
        year: Option(
            SlashCommandOptionType.integer,
            description="The year of the TOTD",
            required=True,
        ),
        month: Option(
            SlashCommandOptionType.integer,
            description="The month of the TOTD (1-12)",
            required=True,
        ),
        day: Option(
            SlashCommandOptionType.integer,
            description="The day of the TOTD",
            required=True,
        ),
    ):
        log_command(ctx, "totd")

        await ctx.defer()

        log.debug("Doing Initial Basic Checks")
        if month < 1 or month > 12:
            await ctx.respond("Invalid Month")
            return
        if day < 1 or day > 31:
            await ctx.respond("Invalid Date")
            return
        if year < 2020:
            await ctx.respond("Invalid year")
            return
        log.debug("Passed Initial Basic Checks")

        thedate = datetime(year, month, day)
        log.debug("Getting TOTD Data for %s", str(thedate))

        try:
            totd_data = await TOTD.get_totd(thedate)
        except InvalidTOTDDate:
            log.error("Invalid Date was given")
            await ctx.respond("TOTD Not found. Date given %s %s %s", day, month, year)
            return

        log.debug("Parsing Data")
        totd_page, buttons = await parse_totd_data(totd_data, month - 1)

        log.debug("Getting TOTD leaderboards")
        totd_leaderboard = await get_totd_leaderboards(
            year, constants.Consts.months[month - 1], day
        )

        if totd_leaderboard is not None:
            log.debug("Creating a Paginator")

            totd_page = Page(embeds=[totd_page], custom_view=ViewAdder(buttons))

            page_groups = [
                PageGroup(pages=[totd_page], label="TOTD Data"),
                PageGroup(pages=totd_leaderboard, label="TOTD Leaderboard"),
            ]

            paginator = Paginator(pages=page_groups, show_menu=True)
            await paginator.respond(ctx.interaction)
        else:
            await ctx.respond(embed=totd_page, view=ViewAdder(buttons))


def setup(bot: Bot):
    bot.add_cog(LatestTOTD(bot))
