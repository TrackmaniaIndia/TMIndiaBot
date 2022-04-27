import discord
from discord import ApplicationContext, SlashCommandOptionType
from discord.ext import commands

import bot.utils.quote as quote_functions
from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command

log = get_logger(__name__)


class LastQuote(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="last-quote",
        description="Gets the last quote saved",
    )
    @discord.ext.commands.cooldown(1, 5, commands.BucketType.user)
    async def _last_quote(self, ctx: ApplicationContext):
        log_command(ctx, "last_quote")

        log.debug("Getting the last quote saved")
        quote_embed = quote_functions.get_last_quote(ctx.guild.id)

        await ctx.respond(embed=quote_embed)


def setup(bot: Bot):
    """Add LastQuote Cog"""
    bot.add_cog(LastQuote(bot))
