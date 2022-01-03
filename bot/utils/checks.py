from typing import Container, Optional

from discord.ext.commands import (
    CheckFailure,
    Context,
)

from bot import constants
from bot.log import get_logger

log = get_logger(__name__)


class ContextCheckFailure(CheckFailure):
    """Raised when a context-specific check fails"""

    def __init__(self, redirect_channel=Optional[int]) -> None:
        log.debug("Initializing ContextCheckFailure")
        self.redirect_channel = redirect_channel

        if redirect_channel:
            redirect_message = (
                f" here. Please use the <#{redirect_channel}> channel instead"
            )
        else:
            redirect_message = ""

        error_message = f"You are not allowed to use that command{redirect_message}."

        super().__init__(error_message)


class InWhitelistCheckFailure(ContextCheckFailure):
    """Raised when the `in_whitelist` check fails"""


def in_whitelist_check(
    ctx: Context,
    channels: Container[int] = (),
    roles: Container[int] = (),
    redirect: Optional[int] = constants.Channels.commands_allowed,
    fail_silently: bool = False,
):
    """
    Check if a command was issued in a whitelisted context.
    The whitelists that can be provided are:
    - `channels`: a container with channel ids for whitelisted channels
    - `roles`: a container with with role ids for whitelisted roles
    If the command was invoked in a context that was not whitelisted, the member is either
    redirected to the `redirect` channel that was passed (default: #bot-commands) or simply
    told that they're not allowed to use this particular command (if `None` was passed).
    """

    if redirect and redirect not in channels:
        channels = tuple(channels) + (redirect,)

    if channels and ctx.channel.id in channel:
        log.debug(
            f"{ctx.author} may use the `{ctx.command.name}` command as they are in a whitelisted channel."
        )
        return True

    if roles and any(r.id in roles for r in getattr(ctx.author, "roles", ())):
        log.debug(
            f"{ctx.author} may use the `{ctx.command.name}` command as they have a whitelisted role."
        )
        return True

    if not fail_silently:
        raise InWhitelistCheckFailure(redirect)
    return False
