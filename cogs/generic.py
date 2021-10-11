import discord
from discord.ext import commands, tasks
import json
import logging
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from itertools import cycle
import platform
import psutil

import functions.logging.convert_logging as convert_logging
import functions.common_functions.common_functions as common_functions
import functions.cog_helpers.generic_functions
from functions.logging.usage import record_usage, finish_usage
from functions.task_helpers.pingapi import ping_api
from functions.other_functions.get_data import get_version
from functions.other_functions.timestamp import curr_time


load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")


log = logging.getLogger(__name__)
log = convert_logging.get_logging()

version = get_version()

DEFAULT_PREFIX = "--"
guild_ids = [876042400005505066, 805313762663333919]

# Generic Class
class Generic(commands.Cog, description="Generic Functions"):
    first_time = True
    statuses = []

    def __init__(self, client):
        self.client = client
        self.first_time = True

        log.debug(f"Getting Statuses")
        self.statuses = cycle([])
        with open("./data/json_data/statuses.json", "r") as file:
            log.debug(f"Status Loading File")
            self.statuses = json.load(file)["statuses"]
            self.statuses.append(f"Version: {version}! Online and Ready")
            self.statuses = cycle(self.statuses)
            log.debug(f"Status File Loaded")
            file.close()
        log.debug(f"Received Statuses")

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        """What the bot does when it connects to discord servers"""
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"Version: {version}! Online and Ready"),
        )
        log.critical("Bot Logged In")

        log.debug(f"Checking for Times Run File")
        functions.cog_helpers.generic_functions.check_for_times_run()
        times_run = 0

        log.debug(f"Reading Value from Times Run File")
        with open("./data/times_run.txt", "r") as file:
            times_run = int(file.readline())

        times_run += 1

        time_started = curr_time()
        time_started = time_started.strftime("%c %z")

        log.info(f"Starting Keep Alive Loop")
        self.keep_alive.start()

        log.info(f"Starting Change Status Loop")
        self.change_status.start()

        log.debug(f"Sending Message to Bot Channel")

        log.debug(f"Getting Announcement Channels")
        with open("./data/json_data//announcement_channels.json", "r") as file:
            channels = json.load(file)

        architecture = platform.machine()
        hostname = "tmindiabot@" + platform.node()
        platform_details = platform.platform()
        processor = platform.processor()
        # python_build = platform.python_build()
        system = str(platform.system()) + " " + str(platform.release())
        avail_ram = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"

        full_system_info = (
            "------------------------------\n"
            + f"Hostname: {hostname}\n"
            + f"Platform: {platform_details}\n"
            + f"Processor: {processor}\n"
            + f"System: {system}\n"
            + f"Architecture: {architecture}\n"
            + f"Available Ram: {avail_ram}\n"
            + f"------------------------------"
        )

        log.info("------------------------------")
        log.info(f"Hostname: {hostname}")
        log.info(f"Platform: {platform_details}")
        log.info(f"Processor: {processor}")
        log.info(f"System: {system}")
        log.info(f"Architecture: {architecture}")
        log.info(f"Available Ram: {avail_ram}")
        log.info("------------------------------")

        log.debug(f"Creating Machine Details Embed")
        machine_details = discord.Embed(
            title="Machine Details", colour=discord.Colour.random()
        )
        log.debug(f"Created Machine Details Embed")

        for announcement_channel in channels["announcement_channels"]:
            log.debug(f"Sending Message in {announcement_channel}")

            channel = self.client.get_channel(int(announcement_channel))
            try:
                await channel.send(
                    f"Bot is Ready, Version: {version} - Times Run: {times_run} - Time of Start: {time_started}"
                )
                log.debug(f"Sent Message to {announcement_channel}")
                if (
                    int(announcement_channel) == 880771916099641364
                    or int(announcement_channel) == 880628511512096778
                ):
                    continue
                await channel.send(full_system_info)

            except:
                log.debug(f"Can't Send Message to {announcement_channel}")
                continue
        log.debug(f"Writing TimesRun to File")
        with open("./data/times_run.txt", "w") as file:
            print(times_run, file=file)

        log.info(f"Bot now Usable")

    # Tasks
    @tasks.loop(minutes=30)
    async def keep_alive(self):
        log.debug(f"30 Minutes have passed, Task activated - at {datetime.utcnow()}")
        log.debug(f"Pinging API")
        try:
            ping_api()
            log.debug(f"API Ping Successful")
        except:
            log.error("API is Offline")
        log.debug(f"Sending Message to Channel to Keep This Damned Thing Alive")
        log.debug(f"Got Channel Successfully")
        channel = self.client.get_channel(881732050451849216)
        log.debug(f"Sending Message to Channel")
        await channel.send(f"Bot is still alive at {datetime.utcnow()}")
        log.debug(f"Sent Message to Channel")

    @tasks.loop(minutes=10)
    async def change_status(self):
        log.debug(f"10 Minutes have Passed, Changing Status at - {datetime.utcnow()}")
        log.debug(f"Checking for First Time")
        if self.first_time:
            log.debug(f"First Time is True, returning")
            self.first_time = False
            return None

        log.debug(f"Changing Status")

        await self.client.change_presence(activity=discord.Game(next(self.statuses)))

        log.debug(f"Changed Status")

    # Commands
    @commands.command(
        aliases=["latency", "pong", "connection"],
        help="Shows the Ping/Latency of the Bot in milliseconds.",
        brief="Shows Bot Ping.",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def ping(self, ctx):
        """Ping Command

        Args:
            ctx ([type]): [description]
        """
        await ctx.send("Pong! {}ms".format(round(self.client.latency * 1000, 2)))

    @commands.command(help="Changes Prefix to Given prefix", brief="Changes Prefix")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_any_role("admin", "Moderator", "Bot Developer")
    @commands.guild_only()
    async def prefix(self, ctx, prefix: str):
        """Changes the Prefix for the Current Server the Bot is In

        Args:
            ctx ([type]): [description]
            prefix (str): [description]
        """
        log.info(f"Changing Prefix in {ctx.guild}")

        with open("./data/json_data/prefixes.json", "r") as file:
            log.debug("Opening Prefixes JSON")
            prefixes = json.load(file)
            file.close()

        log.debug(f"Changing Prefix")
        prefixes[str(ctx.guild.id)] = [prefix, DEFAULT_PREFIX]
        log.debug(f"Changed Prefix")

        with open("./data/json_data/prefixes.json", "w") as file:
            log.debug("Dumping Prefixes to File")
            json.dump(prefixes, file, indent=4)
            file.close()

        await ctx.send("Prefix Changed to {}".format(prefix))

    @commands.command(help="Displays Bot Version", brief="Bot Version")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def version(self, ctx):
        """Returns Version of Bot

        Args:
            ctx ([type]): [description]
        """
        await ctx.send(f"Bot Version is {version}")

    @commands.command(help="Sends Github Source Code Link", brief="Github Source Code")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def source(self, ctx):
        """Returns Source Code of Bot

        Args:
            ctx ([type]): [description]
        """
        embed = discord.Embed(
            title="Source Code",
            description="https://github.com/NottCurious/TMIndiaBot",
            color=common_functions.get_random_color(),
        )
        embed.timestamp = curr_time()
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.is_owner()
    async def causeError(self, ctx):
        """Causes an Error, Mostly only for Testing Purposes

        Args:
            ctx ([type]): [description]

        Raises:
            commands.CommandError: [description]
        """
        await ctx.send("Causing error")

        raise commands.CommandError(message="Caused error")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def kill(self, ctx):
        """Kills the Bot

        Args:
            ctx ([type]): [description]
        """
        log.error("KILLING")
        await ctx.send("***KILLING***")
        exit()

    @commands.command()
    async def joindevs(self, ctx):
        """Sends the Requirements to Join the Dev Team

        Args:
            ctx ([type]): [description]
        """
        embed = discord.Embed(
            title=f"Are you sure you want to join the dev team?",
            description=f"If you want to join the dev team, you must\n**1. Have knowledge in either Python/Javascript**\n**2. Be a known and trustworthy member of the Trackmania India scene**\n**3. Know x86 Assembly (Required)**\n**4. Know how to build a CPU from scratch (Optional)**\n**5. Know how to build a mini electro magnet which fits inside your chest using tools that you can find inside a cave with a doctor who becomes a friend but dies during your escape**\n**6. 70 Years of Experience in Python**\n\nPlease contact NottCurious#4351 if you want to apply.\n\nYou may also see the source code by using *source",
            colour=common_functions.get_random_color(),
        )
        embed.timestamp = curr_time()
        await ctx.send(embed=embed)

    # Error Management
    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            log.error(f"{ctx.author.name} tried to use prefix in a private message")

            embed = discord.Embed(
                title="This command cannot be used in a DM, please use a server",
                colour=discord.Colour.red(),
            )
            embed.timestamp = curr_time()

            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            log.error("Prefix Not Given")

            embed = discord.Embed(
                title=":warning: Prefix not given",
                description="Usage: prefix <new-prefix>\nExample: !prefix $",
                color=discord.Colour.red(),
            )
            embed.timestamp = curr_time()
            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingAnyRole):
            log.error("Caller Doesn't Have A Required Role")
            embed = discord.Embed(
                title=":warning: You dont have a required role: Admin, Moderator, Bot Developer",
                color=discord.Colour.red(),
            )
            embed.timestamp = curr_time()
            await ctx.send(embed=embed)

    @causeError.error
    async def cause_error_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            log.error(f"{ctx.author} Tried to Cause an Error")
            embed = discord.Embed(
                title="You need to be the owner of the bot to do that",
                description="This commands is only used in testing",
                color=discord.Colour.red(),
            )
            embed.timestamp = curr_time()
            await ctx.send(embed=embed)

            return None

    @kill.error
    async def kill_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            log.error(f"{ctx.author} Tried to CauseError")
            embed = discord.Embed(
                title="You need to be the owner of the bot to do that",
                description="Please contact NottCurious#4351 or Artifex#0690 if it's an emergency that requires them to kill the bot",
                color=discord.Colour.red(),
            )
            embed.timestamp = curr_time()
            await ctx.send(embed=embed)

            return None


def setup(client):
    client.add_cog(Generic(client))
