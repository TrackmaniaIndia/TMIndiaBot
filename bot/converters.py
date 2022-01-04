from __future__ import annotations

import re
import typing as t
from datetime import datetime, timezone

import discord
from discord.ext.commands import (
    BadArgument,
    Context,
    Converter,
    IDConverter,
    MemberConverter,
    UserConverter,
)
from discord.utils import escape_markdown, snowflake_time

from bot import cogs
from bot.log import get_logger
from bot.utils.extensions import EXTENSIONS, unqualify

log = get_logger(__name__)

DISCORD_EPOCH_DT = snowflake_time(0)
RE_USER_MENTION = re.compile(r"<@!?([0-9]+)>$")


def allowed_strings(*values, preserve_case: bool = False) -> t.Callable[[str], str]:
    """
    Return a converter which only allows arguments equal to one of the given values.
    Unless preserve_case is True, the argument is converted to lowercase. All values are then
    expected to have already been given in lowercase too.
    """

    def converter(arg: str) -> str:
        if not preserve_case:
            arg = arg.lower()

        if arg not in values:
            raise BadArgument(
                f"Only the following values are allowed:\n```{', '.join(values)}```"
            )
        else:
            return arg

    return converter


class Extension(Converter):
    """
    Fully qualify the name of an extension and ensure it exists.
    The * and ** values bypass this when used with the reload command.
    """

    async def convert(self, ctx: Context, argument: str) -> str:
        """Fully qualify the name of an extension and ensure it exists."""
        # Special values to reload all extensions
        if argument == "*" or argument == "**":
            return argument

        argument = argument.lower()

        if argument in EXTENSIONS:
            return argument
        elif (qualified_arg := f"{cogs.__name__}.{argument}") in EXTENSIONS:
            return qualified_arg

        matches = []
        for ext in EXTENSIONS:
            if argument == unqualify(ext):
                matches.append(ext)

        if len(matches) > 1:
            matches.sort()
            names = "\n".join(matches)
            raise BadArgument(
                f":x: `{argument}` is an ambiguous extension name. "
                f"Please use one of the following fully-qualified names.```\n{names}```"
            )
        elif matches:
            return matches[0]
        else:
            raise BadArgument(f":x: Could not find the extension `{argument}`.")


class Snowflake(IDConverter):
    """
    Converts to an int if the argument is a valid Discord snowflake.
    A snowflake is valid if:
    * It consists of 15-21 digits (0-9)
    * Its parsed datetime is after the Discord epoch
    * Its parsed datetime is less than 1 day after the current time
    """

    async def convert(self, ctx: Context, arg: str) -> int:
        """
        Ensure `arg` matches the ID pattern and its timestamp is in range.
        Return `arg` as an int if it's a valid snowflake.
        """
        error = f"Invalid snowflake {arg!r}"

        if not self._get_id_match(arg):
            raise BadArgument(error)

        snowflake = int(arg)

        try:
            time = snowflake_time(snowflake)
        except (OverflowError, OSError) as e:
            # Not sure if this can ever even happen, but let's be safe.
            raise BadArgument(f"{error}: {e}")

        if time < DISCORD_EPOCH_DT:
            raise BadArgument(f"{error}: timestamp is before the Discord epoch.")
        elif (datetime.now(timezone.utc) - time).days < -1:
            raise BadArgument(f"{error}: timestamp is too far into the future.")

        return snowflake


class SourceConverter(Converter):
    """Convert an argument into a help command, tag, command, or cog."""

    @staticmethod
    async def convert(ctx: Context, argument: str) -> SourceType:
        """Convert argument into source object."""
        if argument.lower() == "help":
            return ctx.bot.help_command

        cog = ctx.bot.get_cog(argument)
        if cog:
            return cog

        cmd = ctx.bot.get_command(argument)
        if cmd:
            return cmd

        tags_cog = ctx.bot.get_cog("Tags")
        show_tag = True

        if not tags_cog:
            show_tag = False
        else:
            identifier = TagIdentifier.from_string(argument.lower())
            if identifier in tags_cog.tags:
                return identifier
        escaped_arg = escape_markdown(argument)

        raise BadArgument(
            f"Unable to convert '{escaped_arg}' to valid command{', tag,' if show_tag else ''} or Cog."
        )


AMBIGUOUS_ARGUMENT_MSG = (
    "`{argument}` is not a User mention, a User ID or a Username in the format"
    " `name#discriminator`."
)


class UnambiguousUser(UserConverter):
    """
    Converts to a `discord.User`, but only if a mention, userID or a username (name#discrim) is provided.
    Unlike the default `UserConverter`, it doesn't allow conversion from a name.
    This is useful in cases where that lookup strategy would lead to too much ambiguity.
    """

    async def convert(self, ctx: Context, argument: str) -> discord.User:
        """Convert the `argument` to a `discord.User`."""
        if _is_an_unambiguous_user_argument(argument):
            return await super().convert(ctx, argument)
        else:
            raise BadArgument(AMBIGUOUS_ARGUMENT_MSG.format(argument=argument))


class UnambiguousMember(MemberConverter):
    """
    Converts to a `discord.Member`, but only if a mention, userID or a username (name#discrim) is provided.
    Unlike the default `MemberConverter`, it doesn't allow conversion from a name or nickname.
    This is useful in cases where that lookup strategy would lead to too much ambiguity.
    """

    async def convert(self, ctx: Context, argument: str) -> discord.Member:
        """Convert the `argument` to a `discord.Member`."""
        if _is_an_unambiguous_user_argument(argument):
            return await super().convert(ctx, argument)
        else:
            raise BadArgument(AMBIGUOUS_ARGUMENT_MSG.format(argument=argument))


if t.TYPE_CHECKING:
    Extension = str  # noqa: F811
    Snowflake = int  # noqa: F811
    UnambiguousUser = discord.User  # noqa: F811
    UnambiguousMember = discord.Member  # noqa: F811

UnambiguousMemberOrUser = t.Union[UnambiguousMember, UnambiguousUser]
