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


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        """Initalizing the Bot"""
        log.debug("Initializing commands.Bot class")
        super().__init__(*args, **kwargs)

        log.debug("Creating Optional Api Client")
        self.api_client: Optional[api.APIClient] = None

        self._connector = None
        self._resolver = None
        self._guild_available = asyncio.Event()

    async def ping_services(self) -> None:
        """A helper to make sure all the services the bot relies on are available on startup."""
        # Connect to Bot API
        attempts = 0

        try:
            log.info(f"Attempting site connection to Localhost")
            await self.api_client.get("")
        except:
            attempts += 1

    @classmethod
    def create(cls) -> "Bot":
        """Create and return an instance of the Bot."""
        log.debug(
            f"Creating a bot with default intents and default guild -> {constants.Bot.debug_guild}"
        )
        loop = asyncio.get_event_loop()
        intents = discord.Intents.default()

        return cls(
            loop=loop,
            command_prefix=commands.when_mentioned_or(constants.Bot.prefix),
            help_command=None,
            intents=intents,
            debug_guild=constants.Bot.debug_guild,
        )

    def load_extensions(self) -> None:
        """Load all Enabled Extensions"""
        log.debug("Loading Extensions")

        # Must be done to avoid circular import
        from bot.utils.cogs import EXTENSIONS

        extensions = set(EXTENSIONS)  # Mutable Copy

        for extension in extensions:
            log.info(f"Loading {extension}")
            self.load_extension(extension)

    def add_cog(self, cog: commands.Cog) -> None:
        """Adds a "cog" to the bot and logs the operation."""
        super().add_cog(cog)
        log.info(f"Cog loaded: {cog.qualified_name}")

    def add_command(self, command: commands.Command) -> None:
        """Add `command` as normal and then add its root aliases to the bot."""
        super().add_command(command)
        self._add_root_aliases(command)
        log.info(f"Added {command.name}")

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
        log.info(f"Removed {command.name}")
        return command

    async def close(self) -> None:
        """Close the Discord connection and the aiohttp session, connector, statsd client, and resolver."""
        # Done before super().close() to allow tasks finish before the HTTP session closes.
        for ext in list(self.extensions):
            with suppress(Exception):
                self.unload_extension(ext)

        for cog in list(self.cogs):
            with suppress(Exception):
                log.debug(f"Removing {cog.name}")
                self.remove_cog(cog)

        # Now actually do full close of bot
        await super().close()

        log.info("Closing the API Client")
        if self.api_client:
            await self.api_client.close()

        log.info("Closing the Connector")
        if self._connector:
            await self._connector.close()

        log.info("Closing the Resolver")
        if self._resolver:
            await self._resolver.close()

    async def login(self, *args, **kwargs) -> None:
        """Re-create the connector and set up sessions before logging into Discord."""
        # Use asyncio for DNS resolution instead of threads so threads aren't spammed.
        log.info("Creating a resolver")
        self._resolver = aiohttp.AsyncResolver()

        # Use AF_INET as its socket family to prevent HTTPS related problems both locally
        # and in production.
        log.info("Creating a connector")
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

    async def on_guild_available(self, guild: discord.Guild) -> None:
        """
        Set the internal guild available event when constants.Guild.id becomes available.
        If the cache appears to still be empty (no members, no channels, or no roles), the event
        will not be set.
        """

        if (
            guild.id != constants.Guild.tmi_server
            and guild.id != constants.Guild.testing_server
        ):
            return

        if not guild.roles or not guild.members or not guild.channels:
            msg = "Guild available event was dispatched but cache is empty"
            log.warning(msg)

            return

        log.info(f"{guild.name} is available")
        self._guild_available.set()

    async def on_guild_unavailable(self, guild: discord.Guild) -> None:
        """Clear the internal guild available event when constants.Guild.id becomes unavailable."""
        if (
            guild.id != constants.Guild.tmi_server
            and guild.id != constants.Guild.testing_server
        ):
            return

        log.info(f"{guild.name} is unavailable")
        self._guild_available.clear()

    async def wait_until_guild_available(self) -> None:
        """
        Wait until the constants.Guild.id guild is available (and the cache is ready).
        The on_ready event is inadequate because it only waits 2 seconds for a GUILD_CREATE
        gateway event before giving up and thus not populating the cache for unavailable guilds.
        """
        await self._guild_available.wait()

    # async def on_error(self, event: str, *args, **kwargs) -> None:
    #     """Log errors raised in event listeners rather than printing them to stderr."""
    #     # self.stats.incr(f"errors.event.{event}")

    #     # with push_scope() as scope:
    #     #     scope.set_tag("event", event)
    #     #     scope.set_extra("args", args)
    #     #     scope.set_extra("kwargs", kwargs)

    #     #     log.exception(f"Unhandled exception in {event}.")
    #     log.exception(f"Unhandled exception in {event}.")

    def _add_root_aliases(self, command: commands.Command) -> None:
        """Recursively add root aliases for `command` and any of its subcommand"""
        if isinstance(command, commands.Group):
            for subcommand in command.commands:
                self._add_root_aliases(subcommand)
        for alias in getattr(command, "root_aliases", ()):
            if alias in self.all_commands:
                raise commands.CommandRegistrationError(alias, alias_conflict=True)

            self.all_commands[alias] = command

    def _remove_root_aliases(self, command: commands.Command) -> None:
        """Recursively remove root aliases for `command` and any of its subcommands."""
        if isinstance(command, commands.Group):
            for subcommand in command.commands:
                self._remove_root_aliases(subcommand)

        for alias in getattr(command, "root_aliases", ()):
            self.all_commands.pop(alias, None)
