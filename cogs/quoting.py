import discord
from discord.ext import commands, tasks
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from itertools import cycle

import functions.logging.convert_logging as convert_logging
import functions.common_functions.common_functions as common_functions
import functions.cog_helpers.generic_functions
from functions.logging.usage import record_usage, finish_usage
from functions.task_helpers.pingapi import ping_api
from functions.other_functions.get_data import get_version
import functions.cog_helpers.quote_functions as quote_functions

load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")


log = logging.getLogger(__name__)
log = convert_logging.get_logging()

version = get_version()

class Quote(commands.Cog, description='Quoting Functions'):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['q'], help='Quotes a Message -> Format "Message" - Author')
    @commands.has_any_role('admin', 'Bot Developer')
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def quote(self, ctx: commands.Context, *, message):
        message, author = message.split(' - ')

        quote_functions.save(message, author)
        await ctx.send('done', delete_after=3)

    @commands.command(help='Quotes a Random Quote')
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def randquote(self, ctx: commands.Context):
        pass

def setup(client):
    client.add_cog(Quote(client))