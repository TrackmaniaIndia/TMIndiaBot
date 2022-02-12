from discord import ApplicationContext
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import log_command


class BotVersion(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._version = constants.Bot.version

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="version",
        description="Get the Bot Version",
    )
    async def _version(self, ctx: ApplicationContext):
        log_command(ctx, "version")
        await ctx.respond(f"Bot version is {self._version}", ephemeral=True)


def setup(bot: Bot) -> None:
    """Load the BotVersions cog."""
    bot.add_cog(BotVersion(bot))
