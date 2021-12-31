import discord
from discord import Embed
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord.view_adder import ViewAdder

log = get_logger(__name__)


class GetSourceCode(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="sourcecode",
        description="Gives a link for the github source code",
    )
    async def _source_code_slash(self, ctx: commands.Context):
        log_command(ctx, "Source Code Slash")
        log.info("Creating button for source code")

        source_code_button = discord.ui.Button(
            label="Source Code (Github)",
            style=discord.ButtonStyle.url,
            url="https://github.com/NottCurious/TMIndiaBot",
        )

        log.debug("Created a button for Source Code, Sending a message")

        await ctx.respond(
            content="Hey!\nHere is the source code. The bot is open source and licensed under the MIT License. It is currently developed and maintained by NottCurious and Artifex.\nAll Issues/Feature Requests/Bug Reports and Pull Requests are welcome and appreciated!",
            view=ViewAdder([source_code_button]),
        )

    @commands.command(
        name="sourcecode",
        description="Gives a link for the github source code",
    )
    async def _source_code(self, ctx: commands.Context):
        log_command(ctx, "Source Code")
        log.info("Creating button for source code")

        source_code_button = discord.ui.Button(
            label="Source Code (Github)",
            style=discord.ButtonStyle.url,
            url="https://github.com/NottCurious/TMIndiaBot",
        )

        log.debug("Created a button for Source Code, Sending a message")

        await ctx.send(
            content="Hey!\nHere is the source code. The bot is open source and licensed under the MIT License. It is currently developed and maintained by NottCurious and Artifex.\nAll Issues/Feature Requests/Bug Reports and Pull Requests are welcome and appreciated!",
            view=ViewAdder([source_code_button]),
        )


def setup(bot: Bot) -> None:
    """Setup the SourceCode Cog"""
    bot.add_cog(GetSourceCode(bot))
