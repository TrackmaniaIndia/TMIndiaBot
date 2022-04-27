from discord import ApplicationContext, SlashCommandOptionType
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
        name="next-birthday",
        description="Gets the person who's birthday is the closest",
    )
    async def _next_birthday(self, ctx: ApplicationContext):
        log_command(ctx, "next_birthday_slash")
        await ctx.respond(embed=birthday.next_birthday(ctx.guild.id))

    @commands.command(
        name="next-birthday",
        description="Gets the person who's birthday is the closest",
    )
    async def _next_birthday_normal(self, ctx: commands.Context):
        log_command(ctx, "next_birthday")
        await ctx.reply(
            embed=birthday.next_birthday(ctx.guild.id), mention_author=False
        )


def setup(bot: Bot):
    bot.add_cog(NextBirthday(bot))
