import discord
from discord.ext import commands
from discord.commands.commands import Option
import json
from datetime import datetime
from dotenv import load_dotenv
from itertools import cycle

import util.logging.convert_logging as convert_logging
from util.cog_helpers.generic_helper import *
from util.logging.usage import record_usage, finish_usage
from util.tasks.keep_alive import keep_alive
from util.tasks.status_change import change_status
from util.guild_ids import guild_ids
import util.discord.easy_embed as ezembed

log = convert_logging.get_logging()
version = get_version()

DEFAULT_PREFIX = "--"


class GenericSlash(commands.Cog, description="Generic Functions"):
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

    @commands.slash_command(
        guild_ids=guild_ids,
        name="ping",
        description="Get ping of bot to discord api in milliseconds",
    )
    @commands.before_invoke(
        record_usage
    )  # Doesn't Work With Slash Commands, Must Check or Change
    @commands.after_invoke(finish_usage)
    async def _ping(self, ctx: commands.Context):
        await ctx.respond("Pong! {}ms".format(round(self.client.latency * 1000, 2)))

    @commands.slash_command(
        guild_ids=guild_ids, name="version", description="Displays bot version"
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def _version(self, ctx: commands.Context):
        await ctx.respond(f"Bot Version is {version}")

    @commands.slash_command(
        guild_ids=guild_ids, name="source", description="Displays Github Source Code"
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def _source(self, ctx):
        embed = ezembed.create_embed(
            title="Source Code",
            description="https://github.com/NottCurious/TMIndiaBot",
            color=discord.Colour.random(),
        )
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(GenericSlash(client))
