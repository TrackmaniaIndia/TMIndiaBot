import discord
from discord import ApplicationContext, SlashCommandOptionType
from discord.commands import Option
from discord.ext import commands

import bot.utils.birthdays as birthday
from bot import constants
from bot.bot import Bot
from bot.log import get_logger
from bot.utils.discord import get_mod_logs_channel

log = get_logger(__name__)


class RemoveBirthday(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # TODO: Permissions. ManageServer.
    @commands.slash_command(
        name="remove-username",
        description="Remove a user's birthday with their discord id",
    )
    @commands.has_permissions(manage_guild=True)
    async def _remove_username(
        self,
        ctx: ApplicationContext,
        id: Option(SlashCommandOptionType.integer, "The user's id", required=True),
    ):
        log.info(f"{ctx.author.name} is requesting removal of {id}")

        log.debug("Sending message to #mod-logs")
        mod_log_channel = get_mod_logs_channel(self.bot, ctx.guild.id)

        if mod_log_channel is not None:
            await mod_log_channel.send(
                f"Requestor: `{ctx.author.name}` is requesting removal of `{id}`'s birthday"
            )

        log.debug("Removing Birthday")
        success_flag = birthday.remove_birthday(id, ctx.guild.id)

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
