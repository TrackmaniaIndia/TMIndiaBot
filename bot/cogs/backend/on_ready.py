import datetime
import json
import os
import random
from itertools import cycle

import discord
from discord.ext import commands, tasks

import bot.utils.birthdays as birthday
import bot.utils.checks as checks
import bot.utils.reminders as reminders
from bot import constants
from bot.bot import Bot
from bot.log import get_logger

log = get_logger(__name__)


class OnReady(
    commands.Cog,
    description="What the bot does when it's when it is connected and ready",
):
    def __init__(self, bot: Bot):
        self.bot = bot

        # Adding Statuses
        self.statuses = []

    @commands.Cog.listener()
    async def on_ready(self):
        self._set_statuses()

        # Changes Precense to the Default Status
        # Default Status is:
        #   Version: VERSION! Online and Ready!
        log.debug("Changing Presence")
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(
                f"Version: {constants.Bot.version}! Online and Ready"
            ),
        )

        # Getting number of times bot was run on this computer
        times_run = 0
        log.info("Reading value from Times Run file")
        with open("./bot/resources/times_run.txt", "r", encoding="UTF-8") as file:
            times_run = int(file.readline())

        times_run += 1

        # Starting ChangeStatus task
        if not self.change_status.is_running():
            log.info("Starting ChangeStatus")
            self.change_status.start()

        # Starting BirthdayReminder
        if not self.todays_birthday.is_running():
            log.info("Starting BirthdayReminder")
            self.todays_birthday.start()

        # Starting File Checker
        if not self.create_files.is_running():
            log.info("Starting FileChecker")
            self.create_files.start()

        # Starting QuoteNumbers task
        if not self.quote_numbers.is_running():
            log.info("Starting QuoteNumbers")
            self.quote_numbers.start()

        # Printing out the new timesrun value to the file
        log.info("Writing TimesRun to File")
        with open("./bot/resources/times_run.txt", "w", encoding="UTF-8") as file:
            print(times_run, file=file)

        # Checking configs to ensure all required fields are there.
        log.info("Verifying all Config Files for required fields")
        guilds = os.listdir("./bot/resources/guild_data/")

        # Starting Reminders
        log.info("Starting COTD Reminders")
        reminders.main_cotd_reminder.start(self.bot)
        reminders.first_rerun_cotd_reminder(self.bot)
        reminders.second_rerun_cotd_reminder(self.bot)

        log.info("Starting Royal Reminders")
        reminders.main_royal_reminder(self.bot)
        reminders.first_rerun_royal_reminder(self.bot)
        reminders.second_rerun_royal_reminder(self.bot)

        # Getting all required fields
        with open("./bot/resources/config_fields.txt", "r", encoding="UTF-8") as file:
            fields = file.readlines()

        for guild in guilds:
            with open(
                f"./bot/resources/guild_data/{guild}/config.json", "r", encoding="UTF-8"
            ) as file:
                config_data = json.load(file)

            for field in fields:
                field = field[:-1]
                if config_data.get(field, None) is None:
                    log.error(f"{field} is missing from {guild}")
                    if field.lower() == "prefix":
                        config_data[field] = ">>"
                    elif "channel" in field.lower():
                        config_data[field] = 0
                    elif (
                        "reminder" in field.lower()
                        or field.lower() == "totd_data"
                        or field.lower() == "trophy_tracking"
                    ):
                        config_data[field] = False
                    else:
                        config_data[field] = 0

            with open(
                f"./bot/resources/guild_data/{guild}/config.json", "w", encoding="UTF-8"
            ) as file:
                json.dump(config_data, file, indent=4)

        log.info("Config Verification Finished.")

        log.critical("Bot now Usable")

    @tasks.loop(minutes=10)
    async def change_status(self):
        """Changes Bot Status Every 10 Minutes"""
        log.debug("Changing Status")
        await self.bot.change_presence(activity=discord.Game(next(self.statuses)))

    @tasks.loop(minutes=15)
    async def create_files(self):
        async for guild in self.bot.fetch_guilds():
            if not os.path.exists(f"./bot/resources/guild_data/{guild.id}"):
                log.info("Creating folder for %s", guild.name)
                os.mkdir(f"./bot/resources/guild_data/{guild.id}")

            log.info("Checking for %s", guild.name)
            checks.create_config(guild.id)
            checks.create_quotes(guild.id)
            checks.create_trophy_tracking(guild.id)
            checks.create_birthdays(guild.id)

    @tasks.loop(hours=2, seconds=0)
    async def quote_numbers(self):
        async for guild in self.bot.fetch_guilds():
            log.debug("Checking %s (%s)", guild.name, guild.id)
            with open(
                f"./bot/resources/guild_data/{guild.id}/quotes.json",
                "r",
                encoding="UTF-8",
            ) as file:
                quotes = json.load(file)

            for i, _ in enumerate(quotes["quotes"]):
                quotes["quotes"][i]["Number"] = i + 1

            with open(
                f"./bot/resources/guild_data/{guild.id}/quotes.json",
                "w",
                encoding="UTF-8",
            ) as file:
                json.dump(quotes, file, indent=4)

    @tasks.loop(
        time=datetime.time(hour=1, minute=30, second=0, tzinfo=datetime.timezone.utc)
    )
    async def todays_birthday(self):
        log.info("Starting Today's Birthday Task.")

        async for guild in self.bot.fetch_guilds():
            guild_id = guild.id
            log.debug("Getting birthday channel for %s", guild_id)
            with open(
                f"./bot/resources/guild_data/{guild_id}/config.json",
                "r",
                encoding="UTF-8",
            ) as file:
                config_data = json.load(file)

                birthdays_channel_id = config_data.get("birthdays_channel", 0)

                if birthdays_channel_id == 0:
                    continue

            log.debug("Checking birthdays for %s", guild_id)
            birthdays_list = birthday.today_birthday(guild_id)

            if birthdays_list is not None:
                log.info("There is a birthday for %s today", guild_id)

                birthdays_channel = self.bot.get_channel(birthdays_channel_id)

                if birthdays_channel is None:
                    log.warn("Cannot get channel for %s", guild_id)
                    continue

                if len(birthdays_list) > 1:
                    log.debug("There is multiple birthdays for %s today", guild_id)

                    for birthday_embed in birthdays_list:
                        log.debug(f"Sending {birthday_embed}")

                        try:
                            await birthdays_channel.send(
                                content="Hey Everyone! We have a birthday today!",
                                embed=birthday_embed,
                            )
                        except Exception as e:
                            log.error(e)
                            continue
                else:
                    log.debug("Only one birthday today %s", guild_id)

                    try:
                        await birthdays_channel.send(
                            content="Hey Everyone! We have a birthday today!",
                            embed=birthdays_list[0],
                        )
                    except Exception as e:
                        log.error(e)

            else:
                log.debug("No birthday today for %s.", guild_id)

    def _set_statuses(self):
        # Read Static Statuses
        with open("./bot/resources/json/statuses.json", "r", encoding="UTF-8") as file:
            statuses = json.load(file).get("statuses", ["Default Status"])

        # Add Dynamically Generated Statuses
        statuses.append(f"Currently in {len(self.bot.guilds)} servers!")
        statuses.append(f"Currently Serving {len(self.bot.users)} users!")
        statuses.append(f"Version: {constants.Bot.version}")

        # Randomize statuses
        random.shuffle(statuses)

        self.statuses = cycle(statuses)


def setup(bot: Bot):
    """Setup OnReady Cog"""
    bot.add_cog(OnReady(bot))
