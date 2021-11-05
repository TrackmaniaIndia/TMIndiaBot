import discord
from discord.ext import commands
import json
from datetime import datetime
from itertools import cycle
import util.logging.convert_logging as convert_logging
from util.cog_helpers.generic_helper import *
from util.tasks.keep_alive import keep_alive
from util.tasks.status_change import change_status
import time

log = convert_logging.get_logging()
version = get_version()

DEFAULT_PREFIX = "--"
role_ids = [905321194071416872, 905321269451427840, 905321297146441729]


class Listeners(commands.Cog, description="Generic Functions"):
    first_time = True
    statuses = []

    def __init__(self, client):
        self.client = client
        self.first_time = True

        log.debug(f"Getting Statuses")
        self.statuses = cycle([])
        with open("./data/json/statuses.json", "r") as file:
            log.debug(f"Status Loading File")
            self.statuses = json.load(file)["statuses"]
            self.statuses.append(f"Version: {version}! Online and Ready")
            self.statuses = cycle(self.statuses)
            log.debug(f"Status File Loaded")
            file.close()
        log.debug(f"Received Statuses")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"Version: {version}! Online and Ready"),
        )
        log.critical("Bot Logged In")

        times_run = 0
        log.debug(f"Reading Value from Times Run File")
        with open("./data/times_run.txt", "r") as file:
            times_run = int(file.readline())

        times_run += 1

        log.debug(f"Starting Keep Alive Loop")
        keep_alive.start(self.client)
        log.debug(f"Started Keep Alive Loop")
        log.debug(f"Start Change Status Loop")
        change_status.start(self.client, self.first_time, self.statuses)
        log.debug(f"Started Change Status Loop")

        log.info(f"Starting Loop to Wait for a correct time")
        curr_time = str(datetime.now().strftime("%M"))
        while curr_time != "36" and curr_time != "00":
            time.sleep(0.5)
            curr_time = str(datetime.now().strftime("%M"))
        log.info(f"Current Time is {datetime.now()}, continuing bot init")

        log.debug(f"Getting Announcement Channels")
        with open("./data/json/announcement_channels.json", "r") as file:
            channels = json.load(file)

        print_system_info()

        for announcement_channel in channels["announcement_channels"]:
            log.debug(f"Sending Message in {announcement_channel}")

            channel = self.client.get_channel(int(announcement_channel))
            try:
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
        log.debug(f"Writing TimesRun to File")
        with open("./data/times_run.txt", "w") as file:
            print(times_run, file=file)

        log.info(f"Bot now Usable")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        log.critical(f"The Bot has Joined {guild.name} with id {guild.id}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        log.critical(
            f"The bot has left/been kicked/been banned from {guild.name} with id {guild.id}"
        )


def setup(client):
    client.add_cog(Listeners(client))
