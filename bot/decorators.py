import asyncio
import types
import typing as t
from contextlib import suppress

from discord import NotFound
from discord.ext import commands
from discord.ext.commands import Cog, Context

from bot.constants import Channels
from bot.log import get_logger

log = get_logger(__name__)


def in_whitelist(
        *,
        channels: t.Container[int] = (),
        roles: t.Container[int] = (),
        redirect: t.Optional[int] = Channels.commands_allowed,
        fail_silently: bool = False,
) -> t.Callable:
    """
    Check if a command was issued in a whitelisted context.
    The whitelists that can be provided are:
    - `channels`: a container with channel ids for whitelisted channels
    - `roles`: a container with role ids for whitelisted roles
    If the command was invoked in a context that was not whitelisted, the member is either
    redirected to the `redirect` channel that was passed (default: #bot-commands) or simply
    told that they're not allowed to use this particular command (if `None` was passed).
    """

    def predicate(ctx: Context) -> bool:
        """Check if command was issued in a whitelisted context"""
        return in_whitelist_check(ctx, channels, roles, redirect, fail_silently)

    return commands.check(predicate)


def has_no_roles(*roles: t.Union[str, int]) -> t.Callable:
    """
    Returns True if the user does not have any of the roles specified.
    """

    async def predicate(ctx: Context) -> bool:
        try:
            await channels.has_any_role(*roles).predicate(ctx)
        except commands.MissingAnyRole:
            return True
        else:
            roles_ = ", ".join(f"'{item}'" for item in roles)
            raise commands.CheckFailure(
                f"You have at least one of the disallowed roles: {roles_}"
            )

        return commands.check(predicate)


def redirect_output(
        destination_channel: int,
        bypass_roles: t.Optional[t.Container[int]] = None,
        channels: t.Optional[t.Container[int]] = None,
        ping_user: bool = True,
) -> t.Callable:
    """
    Changes the channel in the context of the command to redirect the output to a certain channel.

    if ping_user is False, it will not send a message in the destination channel.

    This decroator must go before the `command` decorator
    """

    def wrap(func: types.FunctionType) -> types.FunctionType:
        @command_wraps(func)
        async def inner(self: Cog, ctx: Context, *args, **kwargs) -> None:
            if ctx.channel.id == destination_channel:
                log.debug(
                    f"Command {ctx.command} was invoked in destination_channel, not redirecting"
                )
                await fun(self, ctx, *args, **kwargs)
                return

            if bypass_roles and any(
                    role.id in bypass_roles for role in ctx.author.roles
            ):
                log.debug(f"{ctx.author} has role to bypass output redirection.")
                await func(self, ctx, *args, **kwargs)
                return
            elif channels and ctx.channel.id not in channels:
                log.debug(
                    f"{ctx.author} used {ctx.command} in a channel that cna output redirection"
                )
                await func(self, ctx, *args, **kwargs)
                return

            redirect_channel = ctx.guild.get_channel(destination_channel)
            old_channel = ctx.channel

            log.debug(
                f"Redirecting output of {ctx.author}'s command '{ctx.command.name}' to {redirect_channel.name}"
            )
            ctx.channel = redirect_channel

            if ping_user:
                await ctx.send(
                    f"Here's the output of your command, {ctx.author.mention}"
                )
            scheduling.create_task(func(self, ctx, *args, **kwargs))

            message = await old_channel.send(
                f"Here, {ctx.author.mention}, you can find the output of your command here: "
                f"{redirect_channel.mention}"
            )

            if RedirectOutput.delete_invocation:
                await asyncio.sleep(RedirectOutput.delete_delay)

                with suppress(NotFound):
                    await message.delete()
                    log.debug(f"Redirect Output: Deleted user redirection message")

                with suppress(NotFound):
                    await ctx.message.delete()
                    log.debug(f"Redirect Output: Deleted invocation message")

        return inner

    return wrap
