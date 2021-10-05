import discord
from discord.ext import commands
import json
import logging
import datetime
from dotenv import load_dotenv
import asyncio
import os
import requests

from functions.custom_errors.custom_errors import NotAValidTrackmaniaUsername
import functions.logging.convert_logging as convert_logging
from functions.logging.usage import record_usage, finish_usage
import functions.tm_username_functions.username_functions as username_functions
from functions.cog_helpers.cotd_functions import get_average_data

load_dotenv()
BASE_API_URL = os.getenv("BASE_API_URL")

log = logging.getLogger(__name__)
log = convert_logging.get_logging()

guild_ids = [876042400005505066, 805313762663333919]


class COTD(commands.Cog, description="Commands related to COTD Standings"):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="COTD",
        aliases=["cotd", "totd", "stats", "cotdstats"],
        help="COTD Stats for a given player, if none is given it will use your stored username",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def cotd(self, ctx: commands.Command, username: str = None) -> None:
        if username is None:
            log.debug(f'No Username is Given, Getting Username from File')
            username = username_functions.get_trackmania_username(str(ctx.author.id))

        log.debug(f"Getting ID for {username}")
        user_id = username_functions.get_id(username)

        if user_id is None:
            log.error('A Valid Username was Not Given')
            raise NotAValidTrackmaniaUsername("A Valid Username was not Given")

        log.debug(f"Getting COTD Data")
        PLAYER_URL = BASE_API_URL + "/tm2020/player/" + user_id + "/cotd"
        cotd_data = requests.get(PLAYER_URL).json()
        log.debug(f"Got COTD Data")

        log.debug(f'Parsing through the data and getting average values')
        avg_global_rank, avg_server_rank, avg_div, total_cotds = get_average_data(cotd_data)

    
    @cotd.error
    async def cotd_error(self, ctx: commands.Context, error):
        if isinstance(error, NotAValidTrackmaniaUsername):
            embed = discord.Embed(title="Not a Valid Trackmania Username/Your Username is not stored in the file", description='If your username is not in the file, please use `--storeusername \{tm2020_username\}`', color=discord.Colour.red())
            embed.timestamp = 
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(COTD(client))
