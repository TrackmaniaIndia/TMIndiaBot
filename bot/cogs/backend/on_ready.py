import datetime
import json
import os
from itertools import cycle

import discord
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger
from bot.utils.tasks import (
    change_status,
    keep_alive,
    todays_birthday,
    totd_image_deleter,
)

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

        # Starting KeepAlive task
        log.info("Starting KeepAlive")
        keep_alive.start(self.bot)

        # Starting ChangeStatus task
        log.info("Starting ChangeStatus")
        change_status.start(self.bot, self.statuses)

        # Deleting the TOTD Image if it exists
        if os.path.exists("./bot/resources/temp/totd.png"):
            if int(datetime.datetime.now().hour) >= 23:
                log.critical("TOTD Image Exists, Deleting")
                os.remove("./bot/resources/temp/totd.png")
            else:
                log.critical("Time is not after 11pm, not deleting TOTD Image")
        # Starting TOTDImageDeleter
        log.info("Starting TOTDImageDeleter")
        totd_image_deleter.start(self.bot)

        # Starting BirthdayReminder
        log.info("Starting BirthdayReminder")
        todays_birthday.start(self.bot)

        # Looping Through Announcement Channels
        for announcement_channel in constants.Channels.announcement_channels:
            log.info(f"Sending Message in {announcement_channel}")

            # Sending Message to the Channel
            channel = self.bot.get_channel(int(announcement_channel))
            try:
                # Inside a TryExcept to prevent the bot from crashing if the
                # channel is deleted or permissions to send messages are
                # removed
                await channel.send(
                    f"Bot is Ready, Version: {constants.Bot.version} - Times Run: {times_run} - Time of Start: {datetime.now()}"
                )
                log.info(f"Sent Message to {announcement_channel}")
                if (
                    int(announcement_channel) == 880771916099641364
                    or int(announcement_channel) == 880628511512096778
                ):
                    continue
            except BaseException:
                log.info(f"Can't Send Message to {announcement_channel}")
                continue

        # Printing out the new timesrun value to the file
        log.info("Writing TimesRun to File")
        with open("./bot/resources/times_run.txt", "w", encoding="UTF-8") as file:
            print(times_run, file=file)

        log.critical("Bot now Usable")

    @staticmethod
    def _get_statuses(self) -> list:
        with open("./bot/resources/json/statuses.json", "r", encoding="UTF-8") as file:
            return json.load(file)["statuses"]

    def _set_statuses(self):
        self.statuses = cycle(self._get_statuses(self))


def setup(bot: Bot):
    """Setup OnReady Cog"""
    bot.add_cog(OnReady(bot))
