from discord import ApplicationContext, SlashCommandOptionType
from discord.commands import Option
from discord.ext import commands

import bot.utils.quote as quote_functions
from bot.bot import Bot
from bot.log import get_logger, log_command

log = get_logger(__name__)


class ShowQuote(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="show-quote", description="Gets a quote of a specific number."
    )
    async def _show_quote(
        self,
        ctx: ApplicationContext,
        quote_number: Option(
            SlashCommandOptionType.integer, "The quote number to get", required=True
        ),
    ):
        log_command(ctx, "show_quote")

        await ctx.defer()

        log.debug("Getting the quote")
        quote = quote_functions.get_quote(ctx.guild.id, quote_number)

        if quote is None:
            await ctx.respond("That quote number does not exist.", ephemeral=True)
        else:
            await ctx.respond(embed=quote)


def setup(bot: Bot):
    bot.add_cog(ShowQuote(bot))
