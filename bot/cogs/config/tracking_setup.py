import json

from discord import ApplicationContext
from discord.ext import commands

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import Confirmer

log = get_logger(__name__)


class SetupTracking(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Check if user has manage-server permission
    @commands.slash_command(
        name="setup-tracking",
        description="Start the setup process for tracking.",
    )
    @commands.has_permissions(manage_guild=True)
    async def _setup_tracking(self, ctx: ApplicationContext):
        log_command(ctx, "setup_tracking")

        log.info("Starting Setup Process for %s", ctx.guild.name)
        await ctx.defer()
        confirmer = Confirmer()
        confirmer.change_confirm_button(label="Yes!")
        confirmer.change_cancel_button(label="No!")

        message = await ctx.respond(
            "Is this the channel where you want your server's trophy leaderboard updates to be sent?",
            view=confirmer,
        )
        await confirmer.wait()
        await message.delete()

        if confirmer.value is None:
            log.info("Confirmation Timed Out")
            await ctx.send("Timed Out...", delete_after=10)
        elif not confirmer.value:
            log.info("Setup Declined")
            self.__save_settings(False, ctx.guild.id, 0)
            await ctx.send(
                f"Settings Saved!\nYou have unsubscribed from Trophy Tracking.\nGuild Name: {ctx.guild.name} Channel Name: {ctx.channel.name}",
                delete_after=10,
            )
        elif confirmer.value:
            log.info("Setup Accepted")
            self.__save_settings(True, ctx.guild.id, ctx.channel.id)
            await ctx.send(
                f"Settings Saved!\nYou have subscribed to Trophy Tracking.\nGuild Name: {ctx.guild.name} Channel Name: {ctx.channel.name}",
                delete_after=10,
            )

    def __save_settings(self, flag: bool, guild_id: int, channel_id: int):
        with open(
            f"./bot/resources/guild_data/{guild_id}/config.json", "r", encoding="UTF-8"
        ) as file:
            config_data = json.load(file)

        config_data["trophy_tracking"] = flag
        config_data["trophy_update_channel"] = channel_id

        with open(
            f"./bot/resources/guild_data/{guild_id}/config.json", "w", encoding="UTF-8"
        ) as file:
            json.dump(config_data, file, indent=4)


def setup(bot: Bot):
    bot.add_cog(SetupTracking(bot))
