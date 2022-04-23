import json
import os
from typing import TYPE_CHECKING

import discord
from discord import ApplicationContext
from discord.commands import Option
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import EZEmbed

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
        name="add-birthday",
        description="Adds your birthday to the server list!",
    )
    async def _add_birthday(
        self,
        ctx: ApplicationContext,
        year: Option(int, "The year you were born!", required=True),
        month: Option(
            str,
            "The month you were born in!",
            choices=constants.Consts.months,
            required=True,
        ),
        day: Option(int, "The day you were born on", required=True),
    ):
        log_command(ctx, "add_birthday")

        check_flag, msg = self.__check_date(year, month, day)
        if not check_flag:
            await ctx.respond(content=msg)
            return

        log.debug("All date checks passed, Saving")
        self.__save_birthday(
            ctx.author.name, ctx.author.discriminator, ctx.author.id, year, month, day
        )

        await ctx.respond(
            f"Successfully Saved:\nDate: {day} {month}, {year}", ephemeral=True
        )

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="set-birthday",
        description="Adds your birthday to the server list!",
    )
    @discord.has_any_role(
        805318382441988096, 858620171334057994, guild_id=constants.Guild.tmi_server
    )
    @discord.has_any_role(
        940194181731725373, 941215148222341181, guild_id=constants.Guild.testing_server
    )
    async def _set_birthday(
        self,
        ctx: ApplicationContext,
        user: Option(
            discord.User,
            description="The user you want to set the birthday for",
            required=True,
        ),
        year: Option(int, "The year you were born!", required=True),
        month: Option(
            str,
            "The month you were born in!",
            choices=constants.Consts.months,
            required=True,
        ),
        day: Option(int, "The day you were born on", required=True),
    ):
        log_command(ctx, "set_birthday")

        user: discord.User = user

        # Checks
        checks_flag, msg = self.__check_date(year, month, day)

        if not checks_flag:
            await ctx.respond(msg, ephemeral=True)
            return

        log.debug("All date checks passed, Saving")

        self.__save_birthday(user.name, user.discriminator, user.id, year, month, day)

        log.debug("Sending the message to the #mod-logs channel")
        try:
            channel = self.bot.get_channel(constants.Channels.mod_logs)

            log.debug("Creating embed")
            description = f"Requestor: {ctx.author.name}#{ctx.author.discriminator} set birthday of `{user.name}#{user.discriminator}` to `{day} {month}, {year}`"

            await channel.send(embed=EZEmbed.create_embed(description=description))
        except:
            log.debug("Testing Bot is being run, sending message")
            pass
        await ctx.respond(
            f"Successfully Saved:\nName: {user.name}\nID: {user.id}\nDate: {day} {month}, {year}",
            ephemeral=True,
        )

    def __check_date(self, year: int, month: str, day: int) -> tuple[bool, str]:
        # Checks
        if day <= 0 or day >= 32:
            return False, "Invalid Date Given"
        if month.lower() == "february" and day >= 30:
            log.error("30+ Days in February")
            return False, "February does not have more than 30 days"
        if year % 4 != 0 and month.lower() == "february" and day == 29:
            log.error("Not a Leap Year")
            return False, f"{year} is not a leap year"
        if year > 2022 or year < 1970:
            log.error("Invalid Year (>2022, <1970)")
            return False, "Invalid Years"
        if (constants.Consts.months.index(month)) % 2 == 1 and day == 31:
            log.error("31 days in a month that does not have 31 days")
            return False, f"{month} does not have 31 days"
        if month.capitalize() not in constants.Consts.months:
            log.error("Invalid Month Given")
            return False, "That's not a valid month"

        return True, ""

    def __save_birthday(
        self,
        username: str,
        discriminator: str,
        id: str,
        year: int,
        month: str,
        day: int,
    ):
        log.debug("Opening Birthday List")
        birthdays: dict[list] = {}

        with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
            birthdays = json.load(file)

        # Checking if person already has a saved birthday
        for person in birthdays.get("birthdays", []):
            if person.get("ID") == id:
                log.critical("Player already has a saved birthday, popping")
                birthdays.get("birthdays", []).pop(
                    birthdays.get("birthdays", []).index(person)
                )

        birthdays["birthdays"].append(
            {
                "Name": username,
                "Discriminator": discriminator,
                "ID": id,
                "Year": year,
                "Month": month,
                "Day": day,
            }
        )

        log.debug("Dumping birthdays data to file.")
        with open("./bot/resources/json/birthdays.json", "w", encoding="UTF-8") as file:
            json.dump(birthdays, file, index=4)


def setup(bot: Bot):
    bot.add_cog(AddBirthday(bot))
