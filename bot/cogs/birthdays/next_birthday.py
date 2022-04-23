from discord import ApplicationContext
from discord.ext import commands

import bot.utils.birthdays as birthday
from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command

log = get_logger(__name__)


class NextBirthday(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="next-birthday",
        description="Gets the person who's birthday is the closest",
    )
    async def _next_birthday(self, ctx: ApplicationContext):
        log_command(ctx, "next_birthday")
        await ctx.respond(embed=birthday.next_birthday())

    @commands.command(
        name="next-birthday",
        description="Gets the person who's birthday is the closest",
    )
    async def _next_birthday(self, ctx: commands.Context):
        log_command(ctx, "next_birthday")
        await ctx.send(embed=birthday.next_birthday())


def setup(bot: Bot):
    bot.add_cog(NextBirthday(bot))
