import json

import discord
from discord import Embed
from discord.ext.commands import Cog

import bot.utils.commons as commons
import bot.utils.scheduling as scheduling
from bot import constants
from bot.bot import Bot
from bot.log import get_logger

log = get_logger(__name__)


class Logging(Cog):
    """Debug logging module"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.times_run = commons.get_times_run()

        scheduling.create_task(self.startup_greeting(), event_loop=self.bot.loop)

    async def startup_greeting(self) -> None:
        await self.bot.wait_until_guild_available()
        log.info("Bot Connected")

        description = f"Connected!\nLatency: {self.bot.latency * 1000:.2f}ms\nTimes Run: {self.bot.times_run}"

        embed = Embed(
            title=f"TMIndiaBot {constants.Bot.version}",
            description=description,
            url="https://github.com/TrackmaniaIndia/TMIndiaBot",
        )

        if not constants.DEBUG_MODE:
            async for guild in self.bot.fetch_guilds():
                with open(
                    f"./bot/resources/guild_data/{guild.id}/config.json",
                    "r",
                    encoding="UTF-8",
                ) as file:
                    config_data = json.load(file)
                    achannel_id = config_data.get("announcement_channel", 0)
                    if achannel_id != 0:
                        try:
                            log.info(f"Sending message to {achannel_id}")
                            await self.bot.get_channel(achannel_id).send(embed=embed)
                        except discord.errors.Forbidden:
                            log.error("Can't send messages to %s", achannel_id)
                        except Exception as e:
                            log.error(f"Unexpected Error has occured. {e}")


def setup(bot: Bot) -> None:
    """Load the Logging cog."""
    bot.add_cog(Logging(bot))
