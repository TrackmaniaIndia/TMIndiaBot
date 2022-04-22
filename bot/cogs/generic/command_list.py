import discord
from discord import ApplicationContext
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import ViewAdder

log = get_logger(__name__)


class GetCommandList(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._msg = "Here is the command list for this bot!"
        self._command_list_button = discord.ui.Button(
            label="Command List (Github)",
            style=discord.ButtonStyle.url,
            url="https://gist.github.com/NottCurious/f9b618bbfd8aa133d0de2655b94bfca6",
        )

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="command-list",
        description="Gives a link for the TMIBot Command List",
    )
    async def _command_list(self, ctx: ApplicationContext):
        log_command(ctx, "command_list")
        await ctx.respond(
            content=self._msg,
            view=ViewAdder([self._command_list_button]),
            ephemeral=True,
        )


def setup(bot: Bot) -> None:
    """Setup the SourceCode Cog"""
    bot.add_cog(GetCommandList(bot))
