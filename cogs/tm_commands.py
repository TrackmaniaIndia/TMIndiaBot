import discord
from discord.ext import commands
import json
import logging
import datetime
from dotenv import load_dotenv
import requests
import os
import asyncio

try:
    import cogs.convert_logging as cl
    import cogs.common_functions as cf
except ModuleNotFoundError:
    import common_functions as cf
    import convert_logging as cl

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


async def record_usage(self, ctx):
    log.info(
        f"{ctx.author} used {ctx.command} at {ctx.message.created_at} in {ctx.guild}"
    )

    log_check = ""

    with open("./config.json") as file:
        data = json.load(file)
        log_check = data["log_function_usage"]
        file.close()

    if not log_check:
        log.debug(f"log_check is False, Returning")
        return
    log.debug(f"log_check is True, Sending Message")

    log.debug(f"Sending Message to Error Channel")
    channel = self.client.get_channel(876442289382248468)

    log.debug(f"Creating Embed")
    embed = discord.Embed(title=":clapper: Command Used", color=0x23FFFF)

    embed.add_field(name="Author Username", value=ctx.author, inline=False)
    embed.add_field(name="Author ID", value=ctx.author.id, inline=False)
    embed.add_field(name="Guild Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Guild ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Message content", value=ctx.message.content, inline=False)
    embed.set_footer(text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url)

    log.debug(f"Created Embed")

    log.debug(f"Sending Embed")
    await channel.send(embed=embed)
    log.debug(f"Embed Sent, Error Handler Quit")


async def finish_usage(self, ctx: commands.Context):
    log.info(f"{ctx.author} finished using {ctx.command} in {ctx.guild}")

    log_check = ""

    with open("./config.json") as file:
        data = json.load(file)
        log_check = data["log_function_usage"]
        file.close()

    if not log_check:
        log.debug(f"log_check is False, Returning")
        return
    log.debug(f"log_check is True, Sending Message")

    log.debug(f"Sending Message to Error Channel")
    channel = self.client.get_channel(876442289382248468)

    log.debug(f"Creating Embed")
    embed = discord.Embed(title=":medal: Command Finished", color=0x00FF00)

    embed.add_field(name="Author Username", value=ctx.author, inline=False)
    embed.add_field(name="Author ID", value=ctx.author.id, inline=False)
    embed.add_field(name="Guild Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Guild ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Message content", value=ctx.message.content, inline=False)

    embed.set_footer(text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url)

    log.debug(f"Created Embed")
    log.debug(f"Sending Embed")
    await channel.send(embed=embed)
    log.debug(f"Embed Sent, Error Handler Quit")


class TMCommands(commands.Cog, description="Commands for Trackmania"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="viewmap", help="Views Track/Map Details By ID Given")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def view_map(self, ctx: commands.Context, game_flag: str) -> None:
        valid_flags = ["tmnf", 'tm2020']

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

        if game_flag.lower() == 'tmnf':
            tmx_id_message = ''

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            log.debug(f'Requesting TMX ID from User')

            try:
                await ctx.send(embed=discord.Embed(title='Please Enter a TMX ID', color=0x00ff00))
                tmx_id_message = await self.client.wait_for('message', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(title='Bot Timed Out', color=0xff0000))
                return

            log.debug(f'Received TMX ID from User')

            await ctx.send(embed=get_tmnf_map(tmx_id=tmx_id_message.content))

        if game_flag.lower() == 'tm2020':
            await ctx.send(embed=discord.Embed(title='Under Construction', color=0xff0000))

    @view_map.error
    async def error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            log.error('Missing required arguments')

            log.debug(f'Creating Error Embed')
            await ctx.send(embed=discord.Embed(title=":warning: Missing required argument: Game Flag", description='**Game Flag is a required argument that is missing**,\n\nUsage: viewmap {TMNF/TM2020}', color=0xff0000))
            log.debug(f'Sent Error Embed')
def setup(client):
    client.add_cog(TMCommands(client))


def get_tmnf_map(tmx_id: str) -> discord.Embed:
    if not tmx_id.isnumeric():
        log.error(f"TMX ID is not Numeric")

        return discord.Embed(
            title=":warning: TMX ID must be a number",
            description="Example: 2233",
            color=0xFF0000,
        )

    BASE_API_URL = os.getenv("BASE_API_URL")
    LEADERBOARD_URL = f"{BASE_API_URL}/tmnf-x/trackinfo/{tmx_id}"

    log.debug(f"Requesting Response from API")
    response = requests.get(LEADERBOARD_URL)
    log.debug(f"Received Response From Api")

    log.debug(f"Checking API Response")
    if int(response.status_code) == 400:
        if response.json["error"] == "INVALID_TMX_ID":
            log.error("Invalid TMX ID given")
            return discord.Embed(
                title=":warning: Invalid TMX Id",
                description="The TMX ID provided is invalid",
                color=0xFF0000,
            )
    log.debug(f"API Response Checked")

    api_data = response.json()

    log.debug(f'Creating Embed')
    embed = discord.Embed(
        title=api_data["name"],
        description=api_data["authorComments"],
        color=cf.get_random_color(),
        url="https://tmnforever.tm-exchange.com/trackshow/" + tmx_id,
    )

    embed.set_thumbnail(
        url=f"https://tmnforever.tm-exchange.com/getclean.aspx?action=trackscreenscreens&id={tmx_id}&screentype=0"
    )

    embed.add_field(name="Author", value=api_data["author"], inline=True)
    embed.add_field(name="Version", value=api_data["version"], inline=True)
    embed.add_field(name="Released", value=api_data["releaseDate"], inline=True)
    embed.add_field(name="LB Rating", value=api_data["LBRating"], inline=True)
    embed.add_field(name="Game version", value=api_data["gameVersion"], inline=True)
    embed.add_field(name="Map type", value=api_data["type"], inline=True)
    embed.add_field(name="Map style", value=api_data["style"], inline=True)
    embed.add_field(name="Environment", value=api_data["environment"], inline=True)
    embed.add_field(name="Routes", value=api_data["routes"], inline=True)
    embed.add_field(name="Length", value=api_data["length"], inline=True)
    embed.add_field(name="Difficulty", value=api_data["difficulty"], inline=True)
    embed.add_field(name="Mood", value=api_data["mood"], inline=True)
    log.debug(f'Embed Created, Returning')

    return embed
