from discord import ApplicationContext
from discord.commands import Option
from discord.ext import commands

import bot.utils.commons as commons
from bot import constants
from bot.bot import Bot
from bot.log import get_logger

log = get_logger(__name__)


class TimeSince(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="time-since",
        description="time since a specific date",
    )
    async def _time_since(
        self,
        ctx: ApplicationContext,
        year: Option(int, "The year", required=True),
        month: Option(str, "The month", choices=constants.Consts.months, required=True),
        day: Option(int, "The day", required=True),
    ):
        # Checks
        if day <= 0 or day >= 32:
            await ctx.respond(
                "Invalid Date Given. I wasn't born yesterday... well I was... you know what I mean.",
                ephemeral=True,
            )
            return
        if month.lower() == "february" and day >= 30:
            log.error("30+ Days in February")
            await ctx.respond(
                "February does not have more than 30 days\nYou think I am stupid?",
                ephemeral=True,
            )
            return
        if year % 4 != 0 and day == 29:
            log.error("Not a Leap Year")
            await ctx.respond(f"{year} is not a leap year... dumbass", ephemeral=True)
            return
        if year > 2022 or year < 1970:
            log.error("Invalid Year (>2022, <1970)")
            await ctx.respond("When the fuck were you born", ephemeral=True)
            return
        if (constants.Consts.months.index(month)) % 2 == 1 and day == 31:
            log.error("31 days in a month that does not have 31 days")
            await ctx.respond(f"{month} does not have 31 Days", ephemeral=True)
            return

        timestamp = commons.timestamp_date(
            year, constants.Consts.months.index(month) + 1, day
        )

        log.debug(f"Sending Time Since {year} {month} {day}")
        await ctx.respond(content=commons.time_since(timestamp), ephemeral=True)


def setup(bot: Bot):
    bot.add_cog(TimeSince(bot))
