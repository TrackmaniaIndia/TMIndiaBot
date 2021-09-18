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
        hidden=True,
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def cotd(self, ctx: commands.Command, username: str = None) -> None:
        return None


def setup(client):
    client.add_cog(COTD(client))
