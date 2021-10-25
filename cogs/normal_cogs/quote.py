import discord
from discord import colour
from discord.ext import commands, tasks
import json

from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from itertools import cycle

import util.logging.convert_logging as convert_logging
import util.cog_helpers.generic_helper as generic_functions
from util.logging.usage import record_usage, finish_usage
import util.quoting.quote as quote_functions
import util.discord.easy_embed as ezembed

log = convert_logging.get_logging()

guild_ids = [876042400005505066, 805313762663333919]

class Quote(commands.Cog, description="Quoting Functions"):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='quote', aliases=["q"], help='Quotes a Message -> Format "Message" - Author'
    )
    @commands.has_any_role("admin", "Bot Developer")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def _quote(self, ctx: commands.Context, *, message):
        message, author = message.split(" - ")

        log.debug(f'Saving \"{message}\" by \"{author}\"')

        quote_functions.save(message, author)
        embed = ezembed.create_embed(
            title=":white_check_mark: Saved",
            description=f"Saved **\"{message}\"** by **\"{author}\"**",
            color=discord.Colour.green(),
        )
        await ctx.reply(
            embed=embed,
            mention_author=False
        )

    @commands.command(name="randquote", help="Quotes a Random Quote")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def _rand_quote(self, ctx: commands.Context):
        log.debug(f"Getting Random Quote")
        rand_quote = quote_functions.get_random_quote_dict()

        log.debug(f"Getting Quote Embed")
        embed = quote_functions.quote_dict_to_embed(rand_quote)

        log.debug(f"Sending Random Quote")
        await ctx.reply(embed=embed, mention_author=False)
        
    @commands.command(name='lastquote', help='Get the last quote saved')
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def _last_quote(self, ctx: commands.Context):
        log.debug(f'Getting the Last Quote Saved')
        quote_embed = quote_functions.get_last_quote()
        
        await ctx.reply(embed=quote_embed, mention_author=False)

    @_quote.error
    async def _quote_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingAnyRole):
            log.error("Missing Required Role")
            embed = ezembed.create_embed(
                title="You do not have the required role to use this command",
                description=f"You need the following roles: bot developer, admin",
                colour=discord.Colour.red(),
            )
            await ctx.reply(embed=embed, mention_author=False)


def setup(client):
    client.add_cog(Quote(client))
