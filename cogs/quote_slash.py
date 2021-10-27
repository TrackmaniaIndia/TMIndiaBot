from typing_extensions import Required
import discord
from discord import colour
from discord.ext import commands, tasks
from discord.commands.commands import Option
import json

from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from itertools import cycle

import util.logging.convert_logging as convert_logging
import util.cog_helpers.generic_helper as generic_functions
from util.logging.usage import record_usage, finish_usage
import util.quoting.quote as quote_functions
import util.discord.easy_embed as ezembed
from util.guild_ids import guild_ids

log = convert_logging.get_logging()

class QuoteSlash(commands.Cog, description="Quoting Functions"):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(guild_ids=guild_ids, name='quote', description='Saves a Quote, Only Usable By MODS')
    @commands.has_any_role("admin", "Bot Developer")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def _quote(self, ctx: commands.Context, *, message: Option(str, "Message you want to quote in format \"Message - Author\"", required=True)):
        message, author = message.split(" - ")

        log.debug(f'Saving {message} by {author}')

        quote_functions.save(message, author)
        embed = ezembed.create_embed(
            title=":white_check_mark: Saved",
            description=f"Saved {message} by {author}",
            color=discord.Colour.green(),
        )
        await ctx.respond(
            embed=embed
        )

    @commands.slash_command(guild_ids=guild_ids, name='randquote', description='Shows a random saved quote')
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def _rand_quote(self, ctx: commands.Context):
        log.debug(f"Getting Random Quote")
        rand_quote = quote_functions.get_random_quote_dict()

        log.debug(f"Getting Quote Embed")
        embed = quote_functions.quote_dict_to_embed(rand_quote)

        log.debug(f"Sending Random Quote")
        await ctx.respond(embed=embed)
        
    @commands.slash_command(guild_ids=guild_ids, name='lastquote', description='Displays the last quote saved')
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def _last_quote(self, ctx: commands.Context):
        log.debug(f'Getting the Last Quote Saved')
        quote_embed = quote_functions.get_last_quote()
        
        await ctx.respond(embed=quote_embed)

def setup(client):
    client.add_cog(QuoteSlash(client))
