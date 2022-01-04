import discord
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord.view_adder import ViewAdder

log = get_logger(__name__)


class GetSourceCode(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._msg = "Hey!\nHere is the source code. The bot is open source and licensed under the MIT License. It is currently developed and maintained by NottCurious and Artifex.\nAll Issues/Feature Requests/Bug Reports and Pull Requests are welcome and appreciated!"
        self._source_code_button = discord.ui.Button(
            label="Source Code (Github)",
            style=discord.ButtonStyle.url,
            url="https://github.com/NottCurious/TMIndiaBot",
        )

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="sourcecode",
        description="Gives a link for the github source code",
    )
    async def _source_code_slash(self, ctx: commands.Context):
        log_command(ctx, "source_code_slash")
        await ctx.respond(
            content=self._msg,
            view=ViewAdder([self._source_code_button]),
            ephemeral=True,
        )

    @commands.command(
        name="sourcecode",
        description="Gives a link for the github source code",
    )
    async def _source_code(self, ctx: commands.Context):
        log_command(ctx, "source_code")

        await ctx.send(
            content=self._msg,
            view=ViewAdder([self._source_code_button]),
        )


def setup(bot: Bot) -> None:
    """Setup the SourceCode Cog"""
    bot.add_cog(GetSourceCode(bot))
