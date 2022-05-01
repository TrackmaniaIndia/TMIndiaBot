import discord
from discord import ApplicationContext
from discord.ext import commands

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import ViewAdder

log = get_logger(__name__)


class GetSourceCode(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._msg = "Hey!\nHere is the source code. The bot is open source and licensed under the MIT License. It is currently developed and maintained by NottCurious and Artifex.\nAll Issues/Feature Requests/Bug Reports and Pull Requests are welcome and appreciated!"
        self._source_code_button = discord.ui.Button(
            label="Source Code (Github)",
            style=discord.ButtonStyle.url,
            url="https://github.com/TrackmaniaIndia/TMIndiaBot",
        )

    @commands.slash_command(
        name="source-code",
        description="Gives a link for the github source code",
    )
    async def _source_code(self, ctx: ApplicationContext):
        log_command(ctx, "source_code")
        await ctx.respond(
            content=self._msg,
            view=ViewAdder([self._source_code_button]),
            ephemeral=True,
        )


def setup(bot: Bot) -> None:
    """Setup the SourceCode Cog"""
    bot.add_cog(GetSourceCode(bot))
