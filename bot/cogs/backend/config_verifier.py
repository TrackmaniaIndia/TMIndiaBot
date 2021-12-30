from discord.ext.commands import Cog

from bot import constants
from bot.bot import Bot
from bot.log import get_logger
from bot.utils import scheduling

log = get_logger(__name__)


class ConfigVerifier(Cog):
    """Verify config on startup."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.channel_verify_task = scheduling.create_task(
            self.verify_channels(), event_loop=self.bot.loop
        )

    async def verify_channels(self) -> None:
        """
        Verify channels.
        If any channels in config aren't present in server, log them in a warning.
        """
        await self.bot.wait_until_guild_available()
        log.info("Guild available starting channel verification")

        server = self.bot.get_guild(constants.Guild.tmi_server)
        server = (
            self.bot.get_guild(constants.Guild.testing_server)
            if server is None
            else server
        )

        server_channel_ids = []

        for channel in server.channels:
            server_channel_ids.append(channel.id)
        invalid_channels = [
            channel_name
            for channel_name, channel_id in constants.Channels
            if channel_id not in server_channel_ids
        ]

        if invalid_channels:
            log.warning(
                f"Configured channels do not exist in server: {', '.join(invalid_channels)}."
            )


def setup(bot: Bot) -> None:
    """Load the ConfigVerifier cog."""
    bot.add_cog(ConfigVerifier(bot))
