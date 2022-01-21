from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.birthdays import Birthday

log = get_logger(__name__)


class NextBirthday(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="nextbirthday",
        description="Gets the person who's birthday is the closest",
    )
    async def _next_birthday_slash(self, ctx: commands.Context):
        log_command(ctx, "next_birthday_slash")
        await ctx.respond(embed=Birthday.next_birthday())

    @commands.command(
        name="nextbirthday", description="Gets the person who's birthday is the closest"
    )
    async def _next_birthday(self, ctx: commands.Context):
        log_command(ctx, "next_birthday")
        await ctx.send(embed=Birthday.next_birthday())


def setup(bot: Bot):
    bot.add_cog(NextBirthday(bot))
