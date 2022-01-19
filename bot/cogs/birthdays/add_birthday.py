import os
import json

import discord
from discord.ext import commands
from discord.commands import Option

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot import constants
from bot.utils.birthdays import Birthday

log = get_logger(__name__)


class AddBirthday(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        if not os.path.exists("./bot/resources/json/birthdays.json"):
            log.critical("birthdays.json file does not exist, creating")
            with open(
                "./bot/resources/json/birthdays.json", "w", encoding="UTF-8"
            ) as file:
                json.dump({"birthdays": []}, file, indent=4)

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="addbirthday",
        description="Adds your birthday to the server list!",
    )
    async def _add_birthday_slash(
        self,
        ctx: commands.Context,
        year: Option(int, "The year you were born!", required=True),
        month: Option(
            str,
            "The month you were born in!",
            choices=constants.Consts.months,
            required=True,
        ),
        day: Option(int, "The day you were born on", required=True),
    ):
        log_command(ctx, "add_birthday_slash")

        # Checks
        if day <= 0 or day >= 32:
            await ctx.respond("Invalid Date Given", ephemeral=True)
            return
        if month.lower() == "february" and day >= 30:
            log.error("30+ Days in February")
            await ctx.respond(
                "February does not have more than 30 days", ephemeral=True
            )
            return
        if year % 4 != 0 and day == 29:
            log.error("Not a Leap Year")
            await ctx.respond(f"{year} is not a leap year", ephemeral=True)
            return
        if year > 2022 or year < 1970:
            log.error("Invalid Year (>2022, <1970)")
            await ctx.respond("When the fuck were you born", ephemeral=True)
            return
        if constants.Consts.months.index(month) % 2 == 1 and day == 31:
            log.error("31 days in a month that does not have 31 days")
            await ctx.respond(f"{month} does not have 31 Days", ephemeral=True)
            return

        log.debug("All date checks passed, Saving")
        Birthday(ctx, year, month, day).save()

        await ctx.respond(
            f"Successfully Saved:\nDate: {day} {month}, {year}", ephemeral=True
        )


def setup(bot: Bot):
    bot.add_cog(AddBirthday(bot))
