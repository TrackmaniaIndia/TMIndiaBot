import json
import os

import discord
from discord import ApplicationContext
from discord.commands import Option, permissions
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.birthdays import Birthday
from bot.utils.discord import EZEmbed

log = get_logger(__name__)


class SetBirthday(commands.Cog):
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
        name="setbirthday",
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
        if month.capitalize() not in constants.Consts.months:
            log.error("Invalid Month Given")
            await ctx.respond(
                f"Thats not even a valid month ({month}) dumbo", ephemeral=True
            )
            return

        log.debug("All date checks passed, Saving")

        # # Jank Solution
        # log.debug("Changing fields of context")
        # ctx.__setattr__("author.name", user.name)
        # # ctx.author.discriminator = user.discriminator
        # # ctx.author.id = user.id

        Birthday(user.name, user.discriminator, user.id, year, month, day).save()

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


def setup(bot: Bot):
    bot.add_cog(SetBirthday(bot))
