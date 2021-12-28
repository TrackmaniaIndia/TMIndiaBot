"""Class gotten from python-discord/bot which is licensed under MIT License"""
import asyncio
import socket
from contextlib import suppress
from typing import Optional

import aiohttp
import discord
from discord.ext import commands

from bot import api, constants
from bot.log import get_logger

log = get_logger()


class StartupError(Exception):
    """Exception raised when the bot fails to start up."""

    def __init__(self, base: Exception):
        super().__init__()
        self.exception = base


class Bot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api_client: Optional[api.APIClient] = None

        self._connector = None
        self._resolver = None

    async def ping_services(self) -> None:
        """A helper to make sure all the services the bot relies on are available on startup."""
        # Connect to Bot API
        attempts = 0

        while True:
            try:
                log.info(f"Attempting site connection: {attempts + 1}")
                await self.api_client.get("")
                break
            except:
                attempts += 1

    @classmethod
    def create(cls) -> "Bot":
        """Create and return an instance of the Bot."""
        intents = discord.Intents.default()

        return cls(
            intents=intents,
            debug_guild=constants.Bot.debug_guild,
        )

    def load_extensions(self) -> None:
        """Load all Enabled Extensions"""

        # Must be done to avoid circular import
        from TMIBot.utils.cogs import EXTENSIONS

        extensions = set(EXTENSIONS)  # Mutable Copy

        for extension in extensions:
            self.load_extension(extension)

    def add_cog(self, cog: commands.Cog) -> None:
        """Adds a "cog" to the bot and logs the operation."""
        super().add_cog(cog)
        log.info(f"Cog loaded: {cog.qualified_name}")

    def add_command(self, command: commands.Command) -> None:
        """Add `command` as normal and then add its root aliases to the bot."""
        super().add_command(command)
        self._add_root_aliases(command)

    def remove_command(self, name: str) -> Optional[commands.Command]:
        """
        Remove a command/alias as normal and then remove its root aliases from the bot.
        Individual root aliases cannot be removed by this function.
        To remove them, either remove the entire command or manually edit `bot.all_commands`.
        """
        command = super().remove_command(name)
        if command is None:
            # Even if it's a root alias, there's no way to get the Bot instance to remove the alias.
            return

        self._remove_root_aliases(command)
        return command

    async def close(self) -> None:
        """Close the Discord connection and the aiohttp session, connector, statsd client, and resolver."""
        # Done before super().close() to allow tasks finish before the HTTP session closes.
        for ext in list(self.extensions):
            with suppress(Exception):
                self.unload_extension(ext)

        for cog in list(self.cogs):
            with suppress(Exception):
                self.remove_cog(cog)

        # Wait until all tasks that have to be completed before bot is closing is done
        log.trace("Waiting for tasks before closing.")
        await asyncio.gather(*self.closing_tasks)

        # Now actually do full close of bot
        await super().close()

        if self.api_client:
            await self.api_client.close()

        if self._connector:
            await self._connector.close()

        if self._resolver:
            await self._resolver.close()

    async def login(self, *args, **kwargs) -> None:
        """Re-create the connector and set up sessions before logging into Discord."""
        # Use asyncio for DNS resolution instead of threads so threads aren't spammed.
        self._resolver = aiohttp.AsyncResolver()

        # Use AF_INET as its socket family to prevent HTTPS related problems both locally
        # and in production.
        self._connector = aiohttp.TCPConnector(
            resolver=self._resolver,
            family=socket.AF_INET,
        )

        # Client.login() will call HTTPClient.static_login() which will create a session using
        # this connector attribute.
        self.http.connector = self._connector

        self.http_session = aiohttp.ClientSession(connector=self._connector)
        self.api_client = api.APIClient(connector=self._connector)

        try:
            await self.ping_services()
        except Exception as e:
            raise StartupError(e)

        await super().login(*args, **kwargs)
