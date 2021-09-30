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
        # if username is None:
        #     log.debug(f'No Username is Given, Getting Username from File')
        #     username = username_functions.get_trackmania_username(str(ctx.author.id))

        log.debug(f"Getting ID for {username}")
        user_id = username_functions.get_id(username)

        if user_id is None:
            raise NotAValidTrackmaniaUsername("A Valid Username was not Given")

        log.debug(f"Getting COTD Data")
        PLAYER_URL = BASE_API_URL + "/tm2020/player/" + user_id + "/cotd"
        cotd_data = requests.get(PLAYER_URL).json()
        log.debug(f"Got COTD Data")

        # print(user_id)

        print(cotd_data)


def setup(client):
    client.add_cog(COTD(client))
