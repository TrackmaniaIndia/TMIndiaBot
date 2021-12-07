import discord
import json

import util.logging.convert_logging as convert_logging

from discord.ext import commands
from datetime import datetime
from itertools import cycle
from util.cog_helpers.generic_helper import *
from util.cog_helpers.listener_helper import _get_statuses
from util.tasks.keep_alive import keep_alive
from util.tasks.status_change import change_status

# Creating logger
log = convert_logging.get_logging()
version = get_version()


class Listeners(commands.Cog, description="Generic Functions"):
    statuses = cycle([])

    def __init__(self, client):
        self.client = client

        # Adding Statuses to the List
        log.debug(f"Adding Statuses")
        self.statuses = cycle(_get_statuses())
        log.debug(f"Received Statuses")
        log.info(f"cogs.listeners has finished initializing")

    @commands.Cog.listener()
    async def on_ready(self):
        # Changes Precense to the default status
        # Default Status is:
        #    Version: VERSION! Online and Ready!
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"Version: {version}! Online and Ready"),
        )
        log.critical("Bot Logged In")

        # Getting number of times bot was run on this computer
        times_run = 0
        log.debug(f"Reading Value from Times Run File")
        with open("./data/times_run.txt", "r") as file:
            times_run = int(file.readline())

        # Adding one to the times run
        times_run += 1

        # Starting the Keep Alive loop that periodically sends a message to a designated channel and pings the API every 30 minutes
        log.debug(f"Starting Keep Alive Loop")
        keep_alive.start(self.client)
        log.debug(f"Started Keep Alive Loop")

        # Starting the Change Status Loop that Changes the Bot's Status Every 10 Minutes
        log.debug(f"Start Change Status Loop")
        change_status.start(self.client, self.statuses)
        log.debug(f"Started Change Status Loop")

        # Getting the Announcement Channels for where the bot should send that it is ready
        # Channels taken from ./data/json/announcement_channels.json
        log.debug(f"Getting Announcement Channels")
        with open("./data/json/announcement_channels.json", "r") as file:
            channels = json.load(file)

        # Printing System Info to the Screen
        print_system_info()

        # Looping Through Announcement Channels
        for announcement_channel in channels["announcement_channels"]:
            log.debug(f"Sending Message in {announcement_channel}")

            # Sending Message to the Channel
            channel = self.client.get_channel(int(announcement_channel))
            try:
                # Inside a TryExcept to prevent the bot from crashing if the channel is deleted or permissions to send messages are removed
                await channel.send(
                    f"Bot is Ready, Version: {version} - Times Run: {times_run} - Time of Start: {datetime.now()}"
                )
                log.debug(f"Sent Message to {announcement_channel}")
                if (
                    int(announcement_channel) == 880771916099641364
                    or int(announcement_channel) == 880628511512096778
                ):
                    continue
            except:
                log.debug(f"Can't Send Message to {announcement_channel}")
                continue

        # Printing out the new timesrun value to the file
        log.debug(f"Writing TimesRun to File")
        with open("./data/times_run.txt", "w") as file:
            print(times_run, file=file)

        log.info(f"Bot now Usable")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # Bot prints a message when it joins a Guild
        log.critical(f"The Bot has Joined {guild.name} with id {guild.id}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # Bot prints a message when it leaves or is removed from a Guild
        log.critical(
            f"The bot has left/been kicked/been banned from {guild.name} with id {guild.id}"
        )


def setup(client: discord.Bot):
    client.add_cog(Listeners(client))
