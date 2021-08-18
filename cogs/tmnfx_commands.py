# from common_functions import get_random_color
import discord
from discord.ext import commands
import json
import logging
import datetime
from dotenv import load_dotenv
import requests
import os

from requests.models import Response

try:
    import cogs.convert_logging as cl
    import cogs.common_functions as cf
except:
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


class TMNFExchngeCommands(
    commands.Cog, description="Comamnds for Trackmania nations exchange"
):
    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command(
        name="viewmap-tmnf",
        help="View track/map details by TMX Id",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def viewtmnfmap(self, ctx: commands.Context, tmxId: str):
        if not tmxId.isnumeric(): # check if tmxId is an integer
            await ctx.send('TMX Id must be a number')

        baseApiUrl = os.getenv('BASE_API_URL')
        leaderboardUrl = f'{baseApiUrl}/tmnf-x/trackinfo/{tmxId}'
        response = requests.get(leaderboardUrl).json()

        embed=discord.Embed(
            title=response['name'], 
            description=response['authorComments'], 
            color=cf.get_random_color(), 
            url="https://tmnforever.tm-exchange.com/trackshow/" + tmxId
        )
        
        embed.set_thumbnail(url=f"https://tmnforever.tm-exchange.com/getclean.aspx?action=trackscreenscreens&id={tmxId}&screentype=0")
        
        embed.add_field(name="Author",       value=response['author'],        inline=True)
        embed.add_field(name="Version",      value=response['version'],  inline=True)
        embed.add_field(name="Released",     value=response['releaseDate'],   inline=True)
        embed.add_field(name="LB Rating",    value=response['LBRating'],      inline=True)
        embed.add_field(name="Game version", value=response['gameVersion'],   inline=True)
        embed.add_field(name="Map type",     value=response['type'],          inline=True)
        embed.add_field(name="Map style",    value=response['style'],         inline=True)
        embed.add_field(name="Environment",  value=response['environment'],   inline=True)
        embed.add_field(name="Routes",       value=response['routes'],        inline=True)
        embed.add_field(name="Length",       value=response['length'],        inline=True)
        embed.add_field(name="Difficulty",   value=response['difficulty'],    inline=True)
        embed.add_field(name="Mood",         value=response['mood'],          inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(
        name="leaderboards-tmnf",
        aliases=['rankings-tmnf', 'maptimes-tmnf'],
        help="View track/map leaderboards by TMX Id",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def leaderboardstmnf(self, ctx: commands.Context, tmxId: str):
        if not tmxId.isnumeric(): # check if tmxId is an integer
            await ctx.send('TMX Id must be a number')

        baseApiUrl = os.getenv('BASE_API_URL')
        leaderboardUrl = f'{baseApiUrl}/tmnf-x/leaderboard/{tmxId}'
        leaderboards = requests.get(leaderboardUrl).json()
        mapName = requests.get(f'{baseApiUrl}/tmnf-x/trackinfo/{tmxId}').json()['name']

        times = [
            '**:first_place: {} by {}**'.format(leaderboards[0]['time'], leaderboards[0]['username'])
        ]

        for i in range(2, 10):
            obj = leaderboards[i]
            placeStr = ""

            if i == 2:
                placeStr = ':second_place:'
            
            if i == 3:
                placeStr = ':third_place:'
            
            if i > 3:
                placeStr = f'{i}) '

            times.append('{} {} by {}'.format(placeStr, obj['time'], obj['username']))

        embed = discord.Embed(
            title="Leaderboard | " + mapName, 
            url='https://tmnforever.tm-exchange.com/trackshow/' + tmxId,
            description='\n'.join(times),
            color=cf.get_random_color()
        )

        await ctx.send(embed=embed)

    # Error handlers
    @viewtmnfmap.error
    async def error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            logging.error('Missing required arguments')
            await ctx.send('Missing required arguments: TMX Id')


def setup(client):
    client.add_cog(TMNFExchngeCommands(client))