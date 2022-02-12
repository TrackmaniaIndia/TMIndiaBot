from contextlib import suppress
from typing import Optional

from discord import Embed, Forbidden, TextChannel, Thread
from discord.ext import commands

from bot.bot import Bot
from bot.constants import Guild
from bot.log import get_logger
from bot.utils.discord import EZEmbed

log = get_logger(__name__)


class BotCog(commands.Cog, name="Bot"):
    """Bot information commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_join(self, thread: Thread) -> None:
        """
        Try to join newly created threads.
        Despite the event name being misleading, this is dispatched when new threads are created.
        """
        if thread.me:
            # We have already joined this thread
            return

        with suppress(Forbidden):
            await thread.join()


def setup(bot: Bot) -> None:
    """Load the Bot cog."""
    bot.add_cog(BotCog(bot))
