import discord
from discord import ApplicationContext
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import ViewAdder

log = get_logger(__name__)


class GetHallOfFame(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._msg = "Please click the button to be redirected to the hall of fame"
        self._hall_of_fame_button = discord.ui.Button(
            label="TMI Hall of Fame (Github)",
            style=discord.ButtonStyle.url,
            url="https://github.com/NottCurious/TMIndiaBot",
        )

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="halloffame",
        description="Gives a link for the TMI Hall of Fame",
    )
    async def _hall_of_fame(self, ctx: ApplicationContext):
        log_command(ctx, "hall_of_fame")
        await ctx.respond(
            content=self._msg,
            view=ViewAdder([self._hall_of_fame_button]),
            ephemeral=True,
        )


def setup(bot: Bot) -> None:
    """Setup the SourceCode Cog"""
    bot.add_cog(GetHallOfFame(bot))
