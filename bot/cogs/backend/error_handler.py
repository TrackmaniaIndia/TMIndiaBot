import difflib

from discord import Embed
from discord.ext.commands import (
    Cog,
    Context,
    errors,
)

from bot.api import ResponseCodeError
from bot.bot import Bot
from bot.constants import Colours
from bot.log import get_logger
from bot.utils.checks import ContextCheckFailure

log = get_logger(__name__)


class ErrorHandler(Cog):
    """Handles errors emitted from commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_error_embed(self, title: str, body: str) -> Embed:
        """Return an Embed that Contains the exception."""

        return Embed(title=title, color=Colours.soft_red, description=body)

    @Cog.listener()
    async def on_command_error(self, ctx: Context, e: errors.CommandError) -> None:
        """
        Provide generic command error handling.
        Error handling is deferred to any local error handler, if present. This is done by
        checking for the presence of a `handled` attribute on the error.
        Error handling emits a single error message in the invoking context `ctx` and a log message,
        prioritised as follows:
        1. If the name fails to match a command:
            * If it matches shh+ or unshh+, the channel is silenced or unsilenced respectively.
              Otherwise if it matches a tag, the tag is invoked
            * If CommandNotFound is raised when invoking the tag (determined by the presence of the
              `invoked_from_error_handler` attribute), this error is treated as being unexpected
              and therefore sends an error message
        2. UserInputError: see `handle_user_input_error`
        3. CheckFailure: see `handle_check_failure`
        4. CommandOnCooldown: send an error message in the invoking context
        5. ResponseCodeError: see `handle_api_error`
        6. Otherwise, if not a DisabledCommand, handling is deferred to `handle_unexpected_error`
        """

        if hasattr(e, "handled"):
            log.debug(
                f"Command {command} had its error already handled locally; ignoring"
            )
            return

        debug_message = (
            f"Command {command} invoked by {ctx.message.author} with error "
            f"{e.__class__.__name__}: {e}"
        )

        if isinstance(e, errors.CommandNotFound) and not getattr(
                ctx, "invoked_from_error_handler", False
        ):
            await self.try_get_tag(ctx)
        elif isinstance(e, errors.UserInputError):
            log.debug(debug_message)
            await self.handle_user_input_error(ctx, e)
        elif isinstance(e, errors.CheckFailure):
            log.debug(debug_message)
            await self.handle_check_failure(ctx, e)
        elif isinstance(e, errors.CommandOnCooldown):
            log.debug(debug_message)
            await ctx.send(e)
        elif isinstance(e, errors.CommandInvokeError):
            if isinstance(e.original, ResponseCodeError):
                await self.handle_api_error(ctx, e.original)
            elif isinstance(e.original, LockedResourceError):
                await ctx.send(
                    f"{e.original} Please wait for it to finish and try again later."
                )
            elif isinstance(e.original, InvalidInfractedUserError):
                await ctx.send(f"Cannot infract that user. {e.original.reason}")
            else:
                await self.handle_unexpected_error(ctx, e.original)
        elif isinstance(e, errors.ConversionError):
            if isinstance(e.original, ResponseCodeError):
                await self.handle_api_error(ctx, e.original)
            else:
                await self.handle_unexpected_error(ctx, e.original)
        elif isinstance(e, errors.DisabledCommand):
            log.debug(debug_message)
        else:
            # MaxConcurrencyReached, ExtensionError
            await self.handle_unexpected_error(ctx, e)

    async def send_command_help(self, ctx: Context) -> None:
        """Return a prepared `help` command invocation coroutine."""
        if ctx.command:
            self.bot.help_command.context = ctx
            await ctx.send_help(ctx.command)
            return

        await ctx.send_help()

    async def try_get_tag(self, ctx: Context) -> None:
        """
        Attempt to display a tag by interpreting the command name as a tag name.
        The invocation of tags get respects its checks. Any CommandErrors raised will be handled
        by `on_command_error`, but the `invoked_from_error_handler` attribute will be added to
        the context to prevent infinite recursion in the case of a CommandNotFound exception.
        """
        tags_get_command = self.bot.get_command("tags get")
        ctx.invoked_from_error_handler = True

        log_msg = "Cancelling attempt to fall back to a tag due to failed checks."
        try:
            if not await tags_get_command.can_run(ctx):
                log.debug(log_msg)
                return
        except errors.CommandError as tag_error:
            log.debug(log_msg)
            await self.on_command_error(ctx, tag_error)
            return

        if await ctx.invoke(tags_get_command, argument_string=ctx.message.content):
            return

        if not any(role.id in MODERATION_ROLES for role in ctx.author.roles):
            await self.send_command_suggestion(ctx, ctx.invoked_with)

    async def send_command_suggestion(self, ctx: Context, command_name: str) -> None:
        """Sends user similar commands if any can be found."""
        # No similar tag found, or tag on cooldown -
        # searching for a similar command
        raw_commands = []
        for cmd in self.bot.walk_commands():
            if not cmd.hidden:
                raw_commands += (cmd.name, *cmd.aliases)
        if similar_command_data := difflib.get_close_matches(
                command_name, raw_commands, 1
        ):
            similar_command_name = similar_command_data[0]
            similar_command = self.bot.get_command(similar_command_name)

            if not similar_command:
                return

            log_msg = "Cancelling attempt to suggest a command due to failed checks."
            try:
                if not await similar_command.can_run(ctx):
                    log.debug(log_msg)
                    return
            except errors.CommandError as cmd_error:
                log.debug(log_msg)
                await self.on_command_error(ctx, cmd_error)
                return

            misspelled_content = ctx.message.content
            e = Embed()
            e.set_author(name="Did you mean:", icon_url=Icons.questionmark)
            e.description = (
                f"{misspelled_content.replace(command_name, similar_command_name, 1)}"
            )
            await ctx.send(embed=e, delete_after=10.0)

    async def handle_user_input_error(
            self, ctx: Context, e: errors.UserInputError
    ) -> None:
        """
        Send an error message in `ctx` for UserInputError, sometimes invoking the help command too.
        * MissingRequiredArgument: send an error message with arg name and the help command
        * TooManyArguments: send an error message and the help command
        * BadArgument: send an error message and the help command
        * BadUnionArgument: send an error message including the error produced by the last converter
        * ArgumentParsingError: send an error message
        * Other: send an error message and the help command
        """
        if isinstance(e, errors.MissingRequiredArgument):
            embed = self._get_error_embed("Missing required argument", e.param.name)
            self.bot.stats.incr("errors.missing_required_argument")
        elif isinstance(e, errors.TooManyArguments):
            embed = self._get_error_embed("Too many arguments", str(e))
            self.bot.stats.incr("errors.too_many_arguments")
        elif isinstance(e, errors.BadArgument):
            embed = self._get_error_embed("Bad argument", str(e))
            self.bot.stats.incr("errors.bad_argument")
        elif isinstance(e, errors.BadUnionArgument):
            embed = self._get_error_embed("Bad argument", f"{e}\n{e.errors[-1]}")
            self.bot.stats.incr("errors.bad_union_argument")
        elif isinstance(e, errors.ArgumentParsingError):
            embed = self._get_error_embed("Argument parsing error", str(e))
            await ctx.send(embed=embed)
            self.bot.stats.incr("errors.argument_parsing_error")
            return
        else:
            embed = self._get_error_embed(
                "Input error",
                "Something about your input seems off. Check the arguments and try again.",
            )
            self.bot.stats.incr("errors.other_user_input_error")

        await ctx.send(embed=embed)
        await self.send_command_help(ctx)

    @staticmethod
    async def handle_check_failure(ctx: Context, e: errors.CheckFailure) -> None:
        """
        Send an error message in `ctx` for certain types of CheckFailure.
        The following types are handled:
        * BotMissingPermissions
        * BotMissingRole
        * BotMissingAnyRole
        * NoPrivateMessage
        * InWhitelistCheckFailure
        """
        bot_missing_errors = (
            errors.BotMissingPermissions,
            errors.BotMissingRole,
            errors.BotMissingAnyRole,
        )

        if isinstance(e, bot_missing_errors):
            ctx.bot.stats.incr("errors.bot_permission_error")
            await ctx.send(
                "Sorry, it looks like I don't have the permissions or roles I need to do that."
            )
        elif isinstance(e, (ContextCheckFailure, errors.NoPrivateMessage)):
            ctx.bot.stats.incr("errors.wrong_channel_or_dm_error")
            await ctx.send(e)

    @staticmethod
    async def handle_api_error(ctx: Context, e: ResponseCodeError) -> None:
        """Send an error message in `ctx` for ResponseCodeError and log it."""
        if e.status == 404:
            log.debug(f"API responded with 404 for command {ctx.command}")
            await ctx.send("There does not seem to be anything matching your query.")
            ctx.bot.stats.incr("errors.api_error_404")
        elif e.status == 400:
            content = await e.response.json()
            log.debug(f"API responded with 400 for command {ctx.command}: %r.", content)
            await ctx.send("According to the API, your request is malformed.")
            ctx.bot.stats.incr("errors.api_error_400")
        elif 500 <= e.status < 600:
            log.warning(f"API responded with {e.status} for command {ctx.command}")
            await ctx.send("Sorry, there seems to be an internal issue with the API.")
            ctx.bot.stats.incr("errors.api_internal_server_error")
        else:
            log.warning(
                f"Unexpected API response for command {ctx.command}: {e.status}"
            )
            await ctx.send(
                f"Got an unexpected status code from the API (`{e.status}`)."
            )
            ctx.bot.stats.incr(f"errors.api_error_{e.status}")

    @staticmethod
    async def handle_unexpected_error(ctx: Context, e: errors.CommandError) -> None:
        """Send a generic error message in `ctx` and log the exception as an error with exc_info."""
        await ctx.send(
            f"Sorry, an unexpected error occurred. Please let us know!\n\n"
            f"```{e.__class__.__name__}: {e}```"
        )

        ctx.bot.stats.incr("errors.unexpected")

        with push_scope() as scope:
            scope.user = {"id": ctx.author.id, "username": str(ctx.author)}

            scope.set_tag("command", ctx.command.qualified_name)
            scope.set_tag("message_id", ctx.message.id)
            scope.set_tag("channel_id", ctx.channel.id)

            scope.set_extra("full_message", ctx.message.content)

            if ctx.guild is not None:
                scope.set_extra(
                    "jump_to",
                    f"https://discordapp.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}",
                )

            log.error(
                f"Error executing command invoked by {ctx.message.author}: {ctx.message.content}",
                exc_info=e,
            )


def setup(bot: Bot) -> None:
    """Load the ErrorHandler cog."""
    bot.add_cog(ErrorHandler(bot))
