from discord import Embed
from discord.ext import commands

from bot import constants
from bot.bot import Bot


class BotVersion(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(name="version", description="Get the Bot Version")
    async def _version(self, ctx: Context):
        await ctx.respond(f"Bot version is {constants.Bot.version}")

    @commands.command(name="version", help="Gets the bot version")
    async def version(self, ctx: Context):
        await ctx.send(f"Bot version is {constants.Bot.version}")


def setup(bot: Bot) -> None:
    """Load the BotVersions cog."""
    bot.add_cog(BotVersion(bot))
