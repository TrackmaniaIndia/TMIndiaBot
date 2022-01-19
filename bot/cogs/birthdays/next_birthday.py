import os
import json

import discord
from discord.ext import commands
from discord.commands import Option

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot import constants
from bot.utils.birthdays import Birthday

log = get_logger(__name__)


class NextBirthday(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = Bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="nextbirthday",
        description="Gets the person who's birthday is the closest",
    )
    async def _next_birthday(self, ctx: commands.Context):
        await ctx.respond(embed=Birthday.next_birthday())


def setup(bot: Bot):
    bot.add_cog(NextBirthday(bot))
