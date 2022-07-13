import discord.ext.commands as commands
from discord import ApplicationContext, SlashCommandOptionType
from discord.commands import Option

import bot.utils.birthdays as birthday
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import get_mod_logs_channel
from bot.utils.moderation import send_in_mod_logs

log = get_logger(__name__)


class RemoveBirthday(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="remove-birthday",
        description="Remove your birthday from the list",
    )
    async def _remove_birthday(
        self,
        ctx: ApplicationContext,
    ):
        log_command(ctx, "remove-birthday")

        log.info(f"Removing {ctx.author.name}'s birthday from {ctx.guild.name}")

        success_flag = birthday.remove_birthday(ctx.author.id, ctx.guild.id)

        if success_flag:
            log.info(f"{ctx.author.name}'s birthday removed successfully")
            await ctx.respond(
                "Your birthday has been removed from the list.", ephemeral=True
            )
        else:
            log.info(f"{ctx.author.name}'s birthday could not be removed")
            await ctx.respond(
                "Your birthday is not stored in the list.", ephemeral=True
            )

    # TODO: Permissions. ManageServer.
    @commands.slash_command(
        name="remove-user-birthday",
        description="Remove a user's birthday with their discord id",
    )
    @commands.has_permissions(manage_guild=True)
    async def _remove_user_birthday(
        self,
        ctx: ApplicationContext,
        id: Option(SlashCommandOptionType.string, "The user's id", required=True),
    ):
        log_command(ctx, "remove-user-birthday")

        try:
            id = int(id)
        except ValueError:
            await ctx.respond("Invalid ID Given.", ephemeral=True)
            return

        log.info(f"{ctx.author.name} is requesting removal of {id}")

        await send_in_mod_logs(
            self.bot,
            ctx.guild.id,
            msg=f"Requestor: {ctx.author.mention} is removing {id}'s birthday.",
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
