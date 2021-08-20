# from common_functions import get_random_color
import discord
from discord.ext import commands
import json
import logging
import datetime
from dotenv import load_dotenv
import requests
import os

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
        response = requests.get(leaderboardUrl)

        if int(response.status_code) == 400:
            if response.json()['error'] == 'INVALID_TMX_ID':
                await ctx.send('invalid tmx id')
                return None        
        apiData = response.json()

        embed=discord.Embed(
            title=apiData['name'], 
            description=apiData['authorComments'], 
            color=cf.get_random_color(), 
            url="https://tmnforever.tm-exchange.com/trackshow/" + tmxId
        )
        
        embed.set_thumbnail(url=f"https://tmnforever.tm-exchange.com/getclean.aspx?action=trackscreenscreens&id={tmxId}&screentype=0")
        
        embed.add_field(name="Author",       value=apiData['author'],        inline=True)
        embed.add_field(name="Version",      value=apiData['version'],  inline=True)
        embed.add_field(name="Released",     value=apiData['releaseDate'],   inline=True)
        embed.add_field(name="LB Rating",    value=apiData['LBRating'],      inline=True)
        embed.add_field(name="Game version", value=apiData['gameVersion'],   inline=True)
        embed.add_field(name="Map type",     value=apiData['type'],          inline=True)
        embed.add_field(name="Map style",    value=apiData['style'],         inline=True)
        embed.add_field(name="Environment",  value=apiData['environment'],   inline=True)
        embed.add_field(name="Routes",       value=apiData['routes'],        inline=True)
        embed.add_field(name="Length",       value=apiData['length'],        inline=True)
        embed.add_field(name="Difficulty",   value=apiData['difficulty'],    inline=True)
        embed.add_field(name="Mood",         value=apiData['mood'],          inline=True)
        
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
            '**:first_place: {} by {}**'.format(leaderboards[0]['time'], leaderboards[0]['username']),
            ':second_place: {} by {}'.format(leaderboards[1]['time'], leaderboards[1]['username']),
            ':third_place: {} by {}'.format(leaderboards[2]['time'], leaderboards[2]['username']),
            '4) {} by {}'.format(leaderboards[3]['time'], leaderboards[3]['username']),
            '5) {} by {}'.format(leaderboards[4]['time'], leaderboards[4]['username']),
            '6) {} by {}'.format(leaderboards[5]['time'], leaderboards[5]['username']),
            '7) {} by {}'.format(leaderboards[6]['time'], leaderboards[6]['username']),
            '8) {} by {}'.format(leaderboards[7]['time'], leaderboards[7]['username']),
            '9) {} by {}'.format(leaderboards[8]['time'], leaderboards[8]['username']),
            '10) {} by {}'.format(leaderboards[9]['time'], leaderboards[9]['username']),
        ]

        descStr = "{}\n[View all replays](https://tmnforever.tm-exchange.com/trackreplayshow/{})".format('\n'.join(times), tmxId)

        embed = discord.Embed(
            title = "Leaderboard | " + mapName, 
            url = 'https://tmnforever.tm-exchange.com/trackshow/' + tmxId,
            description = descStr,
            color = cf.get_random_color()
        )

        await ctx.send(embed=embed)

    # Error handlers
    @viewtmnfmap.error
    async def error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            log.error('Missing required arguments')

            log.debug("Creating error embed")
            embed = discord.Embed(
                title=":warning: Missing required argument: TMX Id",
                description="**TMX Id is an required argument that is missing**,\n\nUsage: viewmap-tmnf <TMX-id>\nExample: viewmap-tmnf 2233",
                color=cf.get_random_color()
            )
            log.debug('Created error embed')
            log.debug('Sending error embed')

            await ctx.send(embed=embed)
            
            log.debug('Sent error embed')

def setup(client):
    client.add_cog(TMNFExchngeCommands(client))