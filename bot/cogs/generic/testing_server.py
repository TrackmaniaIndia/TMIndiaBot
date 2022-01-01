import discord
from discord import Embed
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord.view_adder import ViewAdder

log = get_logger(__name__)


class GetHallOfFame(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._msg = (
            "Here is an invite to the testing server\nhttps://discord.gg/REEUs3CPND"
        )

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="testingserver",
        description="Get an invite to the TMI Bot Testing Server",
    )
    async def _testing_server_invite_slash(self, ctx: commands.Context):
        log_command(ctx, "testing_server_slash")

        await ctx.respond(
            content=self._msg,
            ephemeral=True,
        )

    @commands.command(
        name="testingserver",
        description="Gives a link for the TMI Hall of Fame",
    )
    async def _testing_server_invite(self, ctx: commands.Context):
        log_command(ctx, "testing_server")
        await ctx.send(
            content=self._msg,
        )


def setup(bot: Bot) -> None:
    """Setup the SourceCode Cog"""
    bot.add_cog(GetHallOfFame(bot))
