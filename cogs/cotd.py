import discord
from discord.ext import commands
import json
import logging
import datetime
from dotenv import load_dotenv
import asyncio

import functions.logging.convert_logging as convert_logging
from functions.logging.usage import record_usage, finish_usage
import functions.tm_username_functions.username_functions as username_functions

load_dotenv()

log = logging.getLogger(__name__)
log = convert_logging.get_logging()


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
        log.debug(f"Checking Username")

        user_id = ""

        if username is None:
            log.debug(f"No Username Given, Checking if in file")
            if not username_functions.check_trackmania_username_in_file(ctx):
                log.error(f"Username not in File")
                return None
            else:
                log.debug(f"Username in File, Getting Id")
                user_id = username_functions.get_trackmania_id(ctx)

        else:
            log.debug(f"Username Given, Checking if Valid")

            if not username_functions.check_username(username):
                log.error(f"Not a Valid Username")
                return None
            else:
                log.debug(f"Valid Username, Getting ID from API")
                user_id = username_functions.get_trackmania_id_from_api(ctx, username)

        await ctx.send(user_id)


def setup(client):
    client.add_cog(COTD(client))
