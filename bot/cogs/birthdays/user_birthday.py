import json
import os

from discord import ApplicationContext, User
from discord.commands import user_command
from discord.ext import commands
from discord.ext.pages import Paginator

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.birthdays import Birthday

log = get_logger(__name__)


class UserBirthday(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @user_command(guild_ids=constants.Bot.default_guilds, name="User Birthday")
    async def _user_birthday(self, ctx: ApplicationContext, user: User):
        log.debug(f"Getting the birthday of {ctx.author.name}")
        await ctx.respond(Birthday.user_birthday(user.id), ephemeral=True)


def setup(bot: Bot):
    bot.add_cog(UserBirthday(bot))
