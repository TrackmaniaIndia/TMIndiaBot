from discord import Embed
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command


class BotVersion(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._version = constants.Bot.version

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="version",
        description="Get the Bot Version",
    )
    async def _version_slash(self, ctx: commands.Context):
        log_command(ctx, "version_slash")
        await ctx.respond(f"Bot version is {self._version}", ephemeral=True)

    @commands.command(name="version", help="Gets the bot version")
    async def _version(self, ctx: commands.Context):
        log_command(ctx, "version")
        await ctx.send(f"Bot version is {self._version}")


def setup(bot: Bot) -> None:
    """Load the BotVersions cog."""
    bot.add_cog(BotVersion(bot))
