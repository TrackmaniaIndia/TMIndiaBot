from discord import ApplicationContext, User, slash_command
from discord.commands import slash_command, user_command
from discord.ext import commands

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
        log_command(ctx, "user_birthday")
        log.debug(f"Getting the birthday of {ctx.author.name}")
        birthday_data = Birthday.user_birthday(user.id)
        await ctx.respond(embed=birthday_data, ephemeral=True)
        # if isinstance(type(birthday_data), str):
        #     await ctx.respond(content=birthday_data, ephemeral=True)
        # else:
        #     await ctx.respond(embed=birthday_data, ephemeral=True)

    @slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="user-birthday",
        description="Gets a player's birthday if it was stored with the bot.",
    )
    async def _user_birthday_slash(self, ctx: ApplicationContext, user: User):
        log_command(ctx, "user_birthday_slash")
        log.debug(f"Getting the birthday of {ctx.author.name}")
        birthday_data = Birthday.user_birthday(user.id)
        await ctx.respond(embed=birthday_data, ephemeral=True)


def setup(bot: Bot):
    bot.add_cog(UserBirthday(bot))
