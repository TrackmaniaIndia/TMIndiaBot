from discord import ApplicationContext
from discord.commands import Option, permissions
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger
from bot.utils.birthdays import Birthday

log = get_logger(__name__)


class RemoveBirthday(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="remove_username",
        description="Remove a user's birthday with their discord id",
    )
    @permissions.has_any_role("Moderator", "Admin", "Bot Developer", "Developer")
    async def _remove_username(
        self, ctx: ApplicationContext, id: Option(int, "The user's id", required=True)
    ):
        log.info(f"{ctx.author.name} is requesting removal of {id}")

        log.debug("Sending message to #mod-logs")
        mod_log_channel = self.bot.get_channel(constants.Channels.mod_logs)

        if mod_log_channel is not None:
            await mod_log_channel.send(
                f"Requestor: `{ctx.author.name}` is requesting removal of `{id}`'s birthday"
            )

        log.debug("Removing Birthday")
        success_flag = Birthday.remove_birthday(id)

        if success_flag:
            log.debug(f"{id}'s birthday was removed successfully")
            await ctx.respond(
                f"Successfully removed birthday of `{id}`", ephemeral=True
            )
        if not success_flag:
            log.debug(f"This user {id} did not have a birthday saved")
            await ctx.respond(
                f"This User `{id}` does not have a birthday saved", ephemeral=True
            )


def setup(bot: Bot):
    bot.add_cog(RemoveBirthday(bot))
