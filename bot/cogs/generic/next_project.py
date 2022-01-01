import discord
from discord import Embed
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord.view_adder import ViewAdder

log = get_logger(__name__)


class GetNextProject(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._msg = "Here is the link to the next project"
        self._next_project_button = discord.ui.Button(
            label="Next Project - v2.1 (Github)",
            style=discord.ButtonStyle.url,
            url="https://github.com/NottCurious/TMIndiaBot/projects/8",
        )

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="nextproject",
        description="Gives a link for the TMI Hall of Fame",
    )
    async def _next_project_slash(self, ctx: commands.Context):
        log_command(ctx, "next_project_slash")
        await ctx.respond(
            content=self._msg,
            view=ViewAdder([self._next_project_button]),
            ephemeral=True,
        )

    @commands.command(
        name="nextproject",
        description="Gives a link for the TMI Hall of Fame",
    )
    async def _next_project(self, ctx: commands.Context):
        log_command(ctx, "next_project")
        await ctx.send(
            content=self._msg,
            view=ViewAdder([self._next_project_button]),
        )


def setup(bot: Bot) -> None:
    """Setup the SourceCode Cog"""
    bot.add_cog(GetHallOfFame(bot))
