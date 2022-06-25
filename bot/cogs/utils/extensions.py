import functools
import typing as t
from enum import Enum

import discord.ext.commands as commands
from discord import Colour, Embed
from discord.ext.commands import Context, group
from discord.ext.pages import Paginator

from bot import cogs
from bot.bot import Bot
from bot.constants import Emojis
from bot.converters import Extension
from bot.log import get_logger
from bot.utils.extensions import EXTENSIONS

log = get_logger(__name__)

UNLOAD_BLACKLIST = {f"{cogs.__name__}.utils.extensions"}
BASE_PATH_LEN = len(cogs.__name__.split("."))


class Action(Enum):
    """Represents an action to perform on an extension"""

    LOAD = functools.partial(Bot.load_extension)
    UNLOAD = functools.partial(Bot.unload_extension)
    RELOAD = functools.partial(Bot.reload_extension)


class Extensions(commands.Cog):
    """Extension management commands"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @group(
        name="extensions",
        aliases=("cogs", "cog"),
        invoke_without_command=True,
    )
    async def extensions_group(self, ctx: Context) -> None:
        await ctx.send_help(ctx.command)

    @extensions_group.command(name="load", aliases=("l",), root_aliases=("load",))
    async def load_command(self, ctx: Context, *extensions: Extension) -> None:
        r"""
        Load extensions given their fully qualified or unqualified names.
        If '\*' or '\*\*' is given as the name, all unloaded extensions will be loaded.
        """  # noqa: W605

        log.info(f"Loading {extensions}")
        if not extensions:
            await ctx.send_help(ctx.command)
            return

        log.debug("Checking if All Extensions Should be Loaded")
        if "*" in extensions or "**" in extensions:
            log.debug("All Extensions should be loaded")
            extensions = set(EXTENSIONS) - set(self.bot.extensions.keys())

        log.debug("Loading Extensions")
        msg = self.batch_manage(Action.LOAD, *extensions)
        log.debug("Loaded Extensions")
        await ctx.send(msg)

    @extensions_group.command(name="unload", aliases=("ul",), root_aliases=("unload",))
    async def unload_command(self, ctx: Context, *extensions: Extension) -> None:
        r"""
        Unload currently loaded extensions given their fully qualified or unqualified names.
        If '\*' or '\*\*' is given as the name, all loaded extensions will be unloaded.
        """  # noqa: W605
        log.debug(f"Unloading {extensions}")
        if not extensions:
            await ctx.send_help(ctx.command)
            return

        log.debug("Checking if Extension is Blacklisted")
        blacklisted = "\n".join(UNLOAD_BLACKLIST & set(extensions))

        if blacklisted:
            log.debug(f"{extensions} is blacklisted")
            msg = f":x: The following extension(s) may not be unloaded:```\n{blacklisted}```"
        else:
            log.debug("Checking if all extensions should be unloaded")
            if "*" in extensions or "**" in extensions:
                log.debug("All Extensions should be unloaded")
                extensions = set(self.bot.extensions.keys()) - UNLOAD_BLACKLIST

            log.debug("Unloading Extensions")
            msg = self.batch_manage(Action.UNLOAD, *extensions)

        await ctx.send(msg)

    @extensions_group.command(name="reload", aliases=("r",), root_aliases=("reload",))
    async def reload_command(self, ctx: Context, *extensions: Extension) -> None:
        r"""
        Reload extensions given their fully qualified or unqualified names.
        If an extension fails to be reloaded, it will be rolled-back to the prior working state.
        If '\*' is given as the name, all currently loaded extensions will be reloaded.
        If '\*\*' is given as the name, all extensions, including unloaded ones, will be reloaded.
        """  # noqa: W605
        log.info("Reloading Extensions")
        if not extensions:
            await ctx.send_help(ctx.command)
            return

        if "**" in extensions:
            log.debug("All Extensions (including unloaded) should be reloaded")
            extensions = EXTENSIONS
        elif "*" in extensions:
            log.debug("All Extensions (excluding unloaded) should be reloaded")
            extensions = set(self.bot.extensions.keys()) | set(extensions)
            extensions.remove("*")

        log.debug("Reloading Extensions")
        msg = self.batch_manage(Action.RELOAD, *extensions)

        await ctx.send(msg)

    @extensions_group.command(name="list", aliases=("all",), root_aliases=("list",))
    async def list_command(self, ctx: Context) -> None:
        """
        Get a list of all extensions, including their loaded status.
        Grey indicates that the extension is unloaded.
        Green indicates that the extension is currently loaded.
        """
        log.info("Listing Extensions")
        embed = Embed(colour=Colour.og_blurple())
        # embed.set_author(
        #     name="Extensions List", url=URLs.github_bot_repo, icon_url=URLs.bot_avatar
        # )

        lines = []
        categories = self.group_extension_statuses()
        for category, extensions in sorted(categories.items()):
            # Treat each category as a single line by concatenating everything.
            # This ensures the paginator will not cut off a page in the middle
            # of a category.
            category = category.replace("_", " ").title()
            extensions = "\n".join(sorted(extensions))
            lines.append(f"**{category}**\n{extensions}\n")
        log.debug(
            f"{ctx.author} requested a list of all cogs. Returning a paginated list."
        )

        log.debug("Creating Paginator")
        cogs_list_paginator = Paginator(pages=lines, show_disabled=True, timeout=30.0)

        log.debug("Running Paginator")
        await cogs_list_paginator.send(ctx, ephemeral=False)

    def group_extension_statuses(self) -> t.Mapping[str, str]:
        """Return a mapping of extension names and statuses to their categories."""
        categories = {}

        for ext in EXTENSIONS:
            if ext in self.bot.extensions:
                status = Emojis.status_online
            else:
                status = Emojis.status_offline

            path = ext.split(".")
            if len(path) > BASE_PATH_LEN + 1:
                category = " - ".join(path[BASE_PATH_LEN:-1])
            else:
                category = "uncategorised"

            categories.setdefault(category, []).append(f"{status}  {path[-1]}")

        return categories

    def batch_manage(self, action: Action, *extensions: str) -> str:
        """
        Apply an action to multiple extensions and return a message with the results.
        If only one extension is given, it is deferred to `manage()`.
        """
        if len(extensions) == 1:
            msg, _ = self.manage(action, extensions[0])
            return msg

        verb = action.name.lower()
        failures = {}

        for extension in extensions:
            _, error = self.manage(action, extension)
            if error:
                failures[extension] = error

        emoji = ":x:" if failures else ":ok_hand:"
        msg = f"{emoji} {len(extensions) - len(failures)} / {len(extensions)} extensions {verb}ed."

        if failures:
            failures = "\n".join(f"{ext}\n    {err}" for ext, err in failures.items())
            msg += f"\nFailures:```\n{failures}```"

        log.debug(f"Batch {verb}ed extensions.")

        return msg

    def manage(self, action: Action, ext: str) -> t.Tuple[str, t.Optional[str]]:
        """Apply an action to an extension and return the status message and any error message."""
        verb = action.name.lower()
        error_msg = None

        try:
            action.value(self.bot, ext)
        except (commands.ExtensionAlreadyLoaded, commands.ExtensionNotLoaded):
            if action is Action.RELOAD:
                # When reloading, just load the extension if it was not loaded.
                return self.manage(Action.LOAD, ext)

            msg = f":x: Extension `{ext}` is already {verb}ed."
            log.debug(msg[4:])
        except Exception as e:
            if hasattr(e, "original"):
                e = e.original

            log.exception(f"Extension '{ext}' failed to {verb}.")

            error_msg = f"{e.__class__.__name__}: {e}"
            msg = f":x: Failed to {verb} extension `{ext}`:\n```\n{error_msg}```"
        else:
            msg = f":ok_hand: Extension successfully {verb}ed: `{ext}`."
            log.debug(msg[10:])

        return msg, error_msg

    # This cannot be static (must have a __func__ attribute).
    async def cog_check(self, ctx: Context) -> bool:
        """Only allow moderators and core developers to invoke the commands in this cog."""
        return ctx.author.id == 250257390643970059

    # This cannot be static (must have a __func__ attribute).
    async def cog_command_error(self, ctx: Context, error: Exception) -> None:
        """Handle BadArgument errors locally to prevent the help command from showing."""
        if isinstance(error, commands.BadArgument):
            await ctx.send(str(error))
            error.handled = True


def setup(bot: Bot) -> None:
    """Load the Extensions cog."""
    bot.add_cog(Extensions(bot))
