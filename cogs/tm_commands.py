import discord
from discord.ext import commands
import json
import logging
import datetime
from discord.utils import valid_icon_size
from dotenv import load_dotenv
import requests
import os
import asyncio
from disputils import pagination
from disputils.pagination import BotEmbedPaginator

import functions.tm_commands_functions
import functions.convert_logging as cl
import functions.common_functions as cf
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


class TMCommands(commands.Cog, description="Commands for Trackmania"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="viewmap", help="Views Track/Map Details By ID Given")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def view_map(self, ctx: commands.Context, game_flag: str) -> None:
        valid_flags = ["tmnf", "tm2020"]

        if game_flag.lower() not in valid_flags:
            log.error(f"Not a Valid Flag, Returning")
            await ctx.send(
                embed=discord.Embed(
                    title="Not A Valid Flag",
                    description="Valid Flags are: TMNF, TM2020\nUsage ```viewmap <game_flag>```",
                    color=0xFF0000,
                )
            )
            return None

        if game_flag.lower() == "tmnf":
            log.debug(f"TMNF Flag Given")
            tmx_id_message = ""

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            log.debug(f"Requesting TMX ID from User")

            try:
                await ctx.send(
                    embed=discord.Embed(title="Please Enter a TMX ID", color=0x00FF00)
                )
                tmx_id_message = await self.client.wait_for(
                    "message", check=check, timeout=30.0
                )
            except asyncio.TimeoutError:
                await ctx.send(
                    embed=discord.Embed(title="Bot Timed Out", color=0xFF0000)
                )
                return

            log.debug(f"Received TMX ID from User")

            await ctx.send(
                embed=functions.tm_commands_functions.get_tmnf_map(
                    tmx_id=tmx_id_message.content
                )
            )

        if game_flag.lower() == "tm2020":
            await ctx.send(
                embed=discord.Embed(title="Under Construction", color=0xFF0000)
            )

    @commands.command(
        name="leaderboards",
        aliases=["lb", "ld"],
        help="Leaderboards for a Specific Map",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def get_leaderboards(self, ctx: commands.Context, game_flag: str) -> None:
        valid_flags = ["tmnf", "tm2020"]

        if game_flag.lower() not in valid_flags:
            log.error(f"Not a Valid Flag, Returning")
            await ctx.send(
                embed=discord.Embed(
                    title="Not a Valid Flag",
                    description="Valid Flags are: TMNF, TM2020\nUsage: ```leaderboards <game_flag>```",
                ),
                color=0xFF0000,
            )
            return None

        if game_flag.lower() == "tmnf":
            log.debug(f"TMNF Flag Given")
            tmx_id_message = ""

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            log.debug(f"Requesting TMX ID from User")

            try:
                await ctx.send(
                    embed=discord.Embed(
                        title="Please Enter Map ID", color=cf.get_random_color()
                    )
                )
                tmx_id_message = await self.client.wait_for(
                    "message", check=check, timeout=30
                )
            except asyncio.TimeoutError:
                await ctx.send(
                    embed=discord.Embed(title="Bot Timed Out", color=0xFF0000)
                )
                return None

            log.debug(f"Received TMX ID from User")

            log.debug(f"Asking for Embeds")
            embeds = functions.tm_commands_functions.get_leaderboards(
                tmx_id=tmx_id_message.content
            )
            log.debug(f"Received Embeds")

            log.debug(f"Creating Paginator")
            paginator = BotEmbedPaginator(ctx, embeds)
            log.debug(f"Created Paginator")

            log.debug(f"Running Paginator")
            await paginator.run()

        if game_flag.lower() == "tm2020":
            await ctx.send(
                embed=discord.Embed(title="Under Construction", color=0xFF0000)
            )

    @view_map.error
    async def error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            log.error("Missing required arguments")

            log.debug(f"Creating Error Embed")
            await ctx.send(
                embed=discord.Embed(
                    title=":warning: Missing required argument: Game Flag",
                    description="**Game Flag is a required argument that is missing**,\n\nUsage: viewmap {TMNF/TM2020}",
                    color=0xFF0000,
                )
            )
            log.debug(f"Sent Error Embed")

    @get_leaderboards.error
    async def error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            log.error("Missing required argument")

            log.debug(f"Sending Error Embed")
            await ctx.send(
                embed=discord.Embed(
                    title=":warning: Missing required argument: Game Flag",
                    description="**Game Flag is a required argument that is missing**,\n\nUsage: leaderboards {TMNF/TM2020}",
                    color=0xFF0000,
                )
            )


def setup(client):
    client.add_cog(TMCommands(client))
