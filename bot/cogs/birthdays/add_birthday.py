import json
import os

import discord
from discord import ApplicationContext, SlashCommandOptionType
from discord.commands import Option
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import create_embed, get_mod_logs_channel

log = get_logger(__name__)


class AddBirthday(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="add-birthday",
        description="Adds your birthday to the server list!",
    )
    async def _add_birthday(
        self,
        ctx: ApplicationContext,
        year: Option(
            SlashCommandOptionType.integer, "The year you were born!", required=True
        ),
        month: Option(
            SlashCommandOptionType.string,
            "The month you were born in!",
            choices=constants.Consts.months,
            required=True,
        ),
        day: Option(
            SlashCommandOptionType.integer, "The day you were born on", required=True
        ),
    ):
        log_command(ctx, "add_birthday")

        check_flag, msg = self.__check_date(year, month, day)
        if not check_flag:
            await ctx.respond(content=msg)
            return

        log.debug("Checking if birthday channel was set")
        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/config.json",
            "r",
            encoding="UTF-8",
        ) as file:
            config_data = json.load(file)

            if config_data["birthdays_channel"] == 0:
                await ctx.send(
                    "WARNING: A birthday channel is not set to send birthday reminders. You can ask a person with the `manage_guild` permission to set one with the `/set-birthday-channel` command."
                )

        log.debug("All date checks passed, Saving")
        self.__save_birthday(
            ctx.author.name,
            ctx.author.discriminator,
            ctx.author.id,
            year,
            month,
            day,
            ctx.guild.id,
        )

        await ctx.respond(
            f"Successfully Saved:\nDate: {day} {month}, {year}", ephemeral=True
        )

    @commands.slash_command(
        name="set-birthday",
        description="Adds your birthday to the server list!",
    )
    @commands.has_permissions(manage_guild=True)
    async def _set_birthday(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            description="The user you want to set the birthday for",
            required=True,
        ),
        year: Option(
            SlashCommandOptionType.integer, "The year you were born!", required=True
        ),
        month: Option(
            SlashCommandOptionType.string,
            "The month you were born in!",
            choices=constants.Consts.months,
            required=True,
        ),
        day: Option(
            SlashCommandOptionType.integer, "The day you were born on", required=True
        ),
    ):
        log_command(ctx, "set_birthday")

        user: discord.User = user

        # Checks
        checks_flag, msg = self.__check_date(year, month, day)

        if not checks_flag:
            await ctx.respond(msg, ephemeral=True)
            return

        log.debug("All date checks passed, Saving")

        self.__save_birthday(
            user.name, user.discriminator, user.id, year, month, day, ctx.guild.id
        )

        log.debug("Sending the message to the #mod-logs channel")
        channel = get_mod_logs_channel(self.bot, ctx.guild.id)

        log.debug("Checking if birthday channel was set")
        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/config.json",
            "r",
            encoding="UTF-8",
        ) as file:
            config_data = json.load(file)

            if config_data["birthdays_channel"] == 0:
                await ctx.send(
                    "WARNING: A birthday channel is not set to send birthday reminders. You can ask a person with the `manage_guild` permission to set one with the `/set-birthday-channel` command."
                )

        log.debug("Creating embed")
        description = f"Requestor: {ctx.author.name}#{ctx.author.discriminator} set birthday of `{user.name}#{user.discriminator}` to `{day} {month}, {year}`"

        try:
            await channel.send(embed=create_embed(description=description))
        except AttributeError:
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
        guild_id: int,
    ):
        log.debug("Opening Birthday List")
        birthdays: dict[list] = {}

        with open(
            f"./bot/resources/guild_data/{guild_id}/birthdays.json",
            "r",
            encoding="UTF-8",
        ) as file:
            birthdays = json.load(file)

        # Checking if person already has a saved birthday
        for person in birthdays.get("birthdays", []):
            if person.get("ID") == id:
                log.critical("Player already has a saved birthday, popping")
                birthdays_arr = birthdays.get("birthdays", [])
                birthdays_arr.pop(birthdays_arr.index(person))
                birthdays["birthdays"] = birthdays_arr

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
        with open(
            f"./bot/resources/guild_data/{guild_id}/birthdays.json",
            "w",
            encoding="UTF-8",
        ) as file:
            json.dump(birthdays, file, indent=4)


def setup(bot: Bot):
    bot.add_cog(AddBirthday(bot))
