from discord.commands import Option
from discord.commands import permissions
from discord.ext import commands

import bot.utils.quote as quote_functions
from bot import constants
from bot.bot import Bot
from bot.log import get_logger
from bot.log import log_command
from bot.utils.commons import Commons
from bot.utils.discord.easy_embed import EZEmbed

log = get_logger(__name__)


class SaveQuote(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="quote",
        description="Saves a Quote, Only Usable by Mods",
        default_permissions=False,
    )
    @permissions.has_any_role("Moderator", "Admin", "Bot Developer", "Developer")
    async def _save_quote_slash(
        self,
        ctx: commands.Context,
        *,
        message: Option(str, "Message to Quote", required=True),
        author: Option(str, "The author of the message", required=True),
        message_link: Option(
            str, "The Link to the Message you want to quote", required=True
        ),
    ):
        log_command(ctx, "save_quote_slash")

        log.info(f"Saving {message} by {author} from guild {ctx.guild.name}")

        log.debug("Deferring Response")
        await ctx.defer()
        log.debug("Deferred Response")

        quote_functions.save(message, author, message_link, ctx.guild.id)

        embed = EZEmbed.create_embed(
            title=":white_check_mark: Saved",
            description=f'Saved "{message}" by {author} with [Jump!]({message_link})',
            color=Commons.get_random_color(),
        )

        await ctx.send_followup(embed=embed)


def setup(bot: Bot):
    """Add the SaveQuote cog"""
    bot.add_cog(SaveQuote(bot))
