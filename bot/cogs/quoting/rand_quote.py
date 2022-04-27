import discord
from discord import ApplicationContext, SlashCommandOptionType
from discord.ext import commands
from discord.ext.commands import Context

import bot.utils.quote as quote_functions
from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command

log = get_logger(__name__)


class RandomQuote(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="rand-quote",
        description="Gets a random saved quote",
    )
    @discord.ext.commands.cooldown(1, 5, commands.BucketType.user)
    async def _rand_quote(self, ctx: ApplicationContext):
        log_command(ctx, "rand_quote")

        try:
            log.debug("Getting a random quote")
            quote_embed = quote_functions._quote_dict_to_embed(
                quote_functions._get_random_quote_dict(ctx.guild.id)
            )
        except ValueError:
            await ctx.respond("There are no quotes saved for this server")
            return

        await ctx.respond(embed=quote_embed)


def setup(bot: Bot):
    """Add RandomQuote Cog"""
    bot.add_cog(RandomQuote(bot))
