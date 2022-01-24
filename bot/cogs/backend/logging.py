from discord import Embed
from discord.ext.commands import Cog

from bot.bot import Bot
from bot.utils.commons import Commons
from bot import constants
from bot.log import get_logger
from bot.utils import scheduling

log = get_logger(__name__)


class Logging(Cog):
    """Debug logging module"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.times_run = Commons.get_times_run()

        scheduling.create_task(self.startup_greeting(), event_loop=self.bot.loop)

    async def startup_greeting(self) -> None:
        await self.bot.wait_until_guild_available()
        log.info("Bot Connected")

        # embed = Embed(description="Connected!")
        # embed.set_author(
        #     name="TMI Bot", url="https://github.com/NottCurious/TMIndiaBot"
        # )

        description = f"Connected!\nLatency: {self.bot.latency * 1000:.2f}ms\nTimes Run: {self.bot.times_run}"

        embed = Embed(
            title=f"TMIndiaBot {constants.Bot.version}",
            description=description,
        )

        if not constants.DEBUG_MODE:
            await self.bot.get_channel(constants.Channels.bot_updates).send(embed=embed)


def setup(bot: Bot) -> None:
    """Load the Logging cog."""
    bot.add_cog(Logging(bot))
