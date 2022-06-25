from datetime import datetime

import discord
from discord import ApplicationContext, Option, SlashCommandOptionType
from discord.ext import commands
from trackmania import TOTD, InvalidTOTDDate, TMXMap

import bot.utils.commons as commons
from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import ViewAdder, create_embed
from bot.utils.totd import MAP_TYPE_ENUMS, parse_totd_data

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
        page, buttons = await parse_totd_data(totd_data, None)

        log.debug("Sending Embed")
        await ctx.respond(embed=page, view=ViewAdder(buttons))

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
        page, buttons = await parse_totd_data(totd_data, month - 1)

        log.debug("Sending Embed")
        await ctx.respond(embed=page, view=ViewAdder(buttons))


def setup(bot: Bot):
    bot.add_cog(LatestTOTD(bot))
