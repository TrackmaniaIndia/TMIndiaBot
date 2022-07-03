import discord.ext.commands as commands
from discord import ApplicationContext

from bot.bot import Bot
from bot.log import get_logger, log_command

log = get_logger(__name__)


class SupportServer(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.support_server = "https://discord.gg/uFgjx5rEgr"
        self._msg = f"Hey!\nYou can join the support server for TMIndiaBot and py-tmio here!\n{self.support_server}"

    @commands.slash_command(
        name="support-server",
        description=f"Get a link to the Support Server for TMIndiaBot",
    )
    async def _support_server(self, ctx: ApplicationContext):
        log_command(ctx, "support_server")
        await ctx.respond(
            content=self._msg,
            ephemeral=True,
        )


def setup(bot: Bot):
    bot.add_cog(SupportServer(bot))
