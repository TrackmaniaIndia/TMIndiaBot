import discord
from discord.ext import commands

import bot.utils.quote as quote_functions
from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command

log = get_logger(__name__)


class RandomQuote(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="randquote",
        description="Gets a random saved quote",
    )
    @discord.ext.commands.cooldown(1, 5, commands.BucketType.user)
    async def _rand_quote_slash(self, ctx: commands.Context):
        log_command(ctx, "rand_quote_slash")

        log.debug("Getting a random quote")
        quote_embed = quote_functions._quote_dict_to_embed(
            quote_functions._get_random_quote_dict(ctx.guild.id)
        )

        await ctx.respond(embed=quote_embed)

    @commands.command(name="randquote", description="Gets a random saved quote")
    @discord.ext.commands.cooldown(1, 5, commands.BucketType.user)
    async def _rand_quote(self, ctx: commands.Context):
        log_command(ctx, "rand_quote")

        log.debug("Getting a random quote")
        await ctx.send(
            embed=quote_functions._quote_dict_to_embed(
                quote_functions._get_random_quote_dict(ctx.guild.id)
            )
        )


def setup(bot: Bot):
    """Add RandomQuote Cog"""
    bot.add_cog(RandomQuote(bot))
