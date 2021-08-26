import discord
from discord.ext import commands
import json
import logging
import os
import datetime
from dotenv import load_dotenv
from datetime import datetime

import functions.convert_logging as cl
import functions.common_functions as cf
import functions.generic_functions
from functions.usage import record_usage, finish_usage

load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log_level, discord_log_level, version = "", "", ""

with open("./config.json") as file:
    config = json.load(file)

    log_level = config["log_level"]
    discord_log_level = config["discord_log_level"]
    version = config["bot_version"]

log = logging.getLogger(__name__)
log = cl.get_logging(log_level, discord_log_level)

DEFAULT_PREFIX = "*"

# Generic Class
class Generic(commands.Cog, description="Generic Functions"):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"Version: {version}! Online and Ready"),
        )
        log.critical("Bot Logged In")

        log.debug(f"Checking for Times Run File")
        functions.generic_functions.check_for_times_run()
        times_run = 0

        log.debug(f"Reading Value from Times Run File")
        with open("./Data/times_run.txt", "r") as file:
            times_run = int(file.readline())

        times_run += 1

        time_started = datetime.now()
        time_started = time_started.strftime("%c %z")

        log.debug(f"Sending Message to Bot Channel")
        channel = self.client.get_channel(876335103146623016)
        await channel.send(f"Bot is Ready, Version: {version} - Times Run: {times_run} - Time of Start: {time_started}")
        log.debug(f"Sent Message to Bot Channel")

        log.debug(f"Writing TimesRun to File")
        with open("./Data/times_run.txt", "w") as file:
            print(times_run, file=file)

    # Commands
    @commands.command(
        aliases=["latency", "pong", "connection"],
        help="Shows the Ping/Latency of the Bot in milliseconds.",
        brief="Shows Bot Ping.",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def ping(self, ctx):
        await ctx.send("Pong! {}ms".format(round(self.client.latency * 1000, 2)))

    @commands.command(help="Changes Prefix to Given prefix", brief="Changes Prefix")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix: str):
        log.info(f"Changing Prefix in {ctx.guild}")

        with open("prefixes.json", "r") as file:
            log.debug("Opening Prefixes JSON")
            prefixes = json.load(file)
            file.close()

        log.debug(f"Changing Prefix")
        prefixes[str(ctx.guild.id)] = [prefix, DEFAULT_PREFIX]
        log.debug(f"Changed Prefix")

        with open("prefixes.json", "w") as file:
            log.debug("Dumping Prefixes to File")
            json.dump(prefixes, file, indent=4)
            file.close()

        await ctx.send("Prefix Changed to {}".format(prefix))

    @commands.command(help="Displays Bot Version", brief="Bot Version")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def version(self, ctx):
        await ctx.send(f"Bot Version is {version}")

    @commands.command(help="Sends Github Source Code Link", brief="Github Source Code")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def source(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Source Code",
                description="https://github.com/NottCurious/TMIndiaBot",
                color=cf.get_random_color(),
            )
        )

    @commands.command(hidden=True)
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def causeError(self, ctx):
        await ctx.send("Causing error")

        raise commands.CommandError(message="Caused error")

    @commands.command(hidden=True)
    async def kill(self, ctx):
        if str(ctx.author.id) not in ["623085987442196503", "250257390643970059"]:
            log.error(f'{ctx.author} Tried to Kill')
            await ctx.send(embed=discord.Embed(title='You\'re Not Allowed To Do That', color=discord.Colour.red()))
            return None
        else:
            log.error('KILLING')
            await ctx.send('***KILLING***')
            exit()

    # Error Management
    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            log.error("Prefix Not Given")

            emb = discord.Embed(
                title=":warning: Prefix not given",
                description="Usage: prefix <new-prefix>\nExample: !prefix $",
                color=0xff0000(),
            )
            await ctx.send(embed=emb)

        if isinstance(error, commands.MissingPermissions):
            log.error("Caller Doesn't Have Required Permissions")
            emb = discord.Embed(
                title=":warning: You dont have the required permissions: Administrator",
                color=0xff0000(),
            )
            await ctx.send(embed=emb)


def setup(client):
    client.add_cog(Generic(client))



