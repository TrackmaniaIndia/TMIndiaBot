from re import T
import discord
from discord import colour
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
guild_ids=[876042400005505066, 805313762663333919]

class Quote(commands.Cog, description="Quoting Functions"):
    def __init__(self, client):
        self.client = client

    @commands.command(
        aliases=["q"], help='Quotes a Message -> Format "Message" - Author'
    )
    @commands.has_any_role("admin", "Bot Developer")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def quote(self, ctx: commands.Context, *, message):
        message, author = message.split(" - ")

        quote_functions.save(message, author, ctx.author.id)
        await ctx.send('done', delete_after=3)

    @commands.command(help="Quotes a Random Quote")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def randquote(self, ctx: commands.Context):
        log.debug(f'Getting Random Quote')
        randQuote = quote_functions.get_random_quote_dict()

        log.debug(f'Getting Quote Embed')
        embed = quote_functions.get_random_quote_dict_to_embed(randQuote)

        log.debug(f'Sending Random Quote')
        await ctx.send(embed=embed)

    @commands.command(help='View all your quotes, or someone else\'s by pinging them')
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def viewquotes(self, ctx: commands.Context, mention: discord.User = None):
        if mention != None:
            userId = mention.id
            user = mention
        else: 
            userId = ctx.author.id
            user = ctx.message.author

        userQuotes = quote_functions.getQuotesById(userId)

        if not userQuotes:
            embed = discord.Embed(title="No quotes for " + user.name, description="Add one by using `$quote`")
            await ctx.send(embed=embed)
            return None

        embed=discord.Embed(title=f"Quotes by {user.name}", description=f"{user.name} Has uploaded {len(userQuotes)} Quotes", colour=discord.Colour.random())

        if len(userQuotes) > 1:
            loopAmount = 2 
        else:
            loopAmount = len(userQuotes)

        for i in range(loopAmount):
            quote = userQuotes[i]
            embed.add_field(name=f'{quote["Message"]}', value=f' - {quote["Author"]}', inline=True)
        
        if len(userQuotes) > 1:
            embed.set_footer(text=f"{len(userQuotes) - loopAmount} More...")

        await ctx.send(embed=embed)

    @quote.error
    async def quote_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingAnyRole):
            log.error("Missing Required Role")
            await ctx.send(embed=discord.Embed(title='You do not have the required role to use this command', description=f'You need the following roles: bot developer, admin',colour=discord.Colour.red()))
        

def setup(client):
    client.add_cog(Quote(client))
