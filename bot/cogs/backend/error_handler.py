from discord import Embed
from discord.ext.commands import Cog, Context, errors

from bot.api import ResponseCodeError
from bot.bot import Bot
from bot.constants import Channels, Colours
from bot.log import get_logger
from bot.utils.discord import create_embed

log = get_logger(__name__)


class ErrorHandler(Cog):
    """Handles errors emitted from commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_error_embed(self, title: str, body: str) -> Embed:
        """Return an Embed that Contains the exception."""

        return create_embed(title=title, color=Colours.soft_red, description=body)

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
                f"Command {ctx.command} had its error already handled locally; ignoring"
            )
            return

        try:
            debug_message = (
                f"Command {ctx.command} invoked by {ctx.message.author} with error "
                f"{e.__class__.__name__}: {e}"
            )
        except AttributeError:
            debug_message = (
                f"Command {ctx.command} invoked by {ctx.author.name} with error "
                f"{e.__class__.__name__}: {e}"
            )
        if isinstance(e, errors.UserInputError):
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

    @Cog.listener()
    async def on_application_command_error(
        self, ctx: Context, e: errors.CommandError
    ) -> None:
        if hasattr(e, "handled"):
            log.debug(
                f"Command {ctx.command} had its error already handled locally; ignoring"
            )
            return

        try:
            debug_message = (
                f"Command {ctx.command} invoked by {ctx.message.author} with error "
                f"{e.__class__.__name__}: {e}"
            )
        except AttributeError:
            debug_message = (
                f"Command {ctx.command} invoked by {ctx.author.name} with error "
                f"{e.__class__.__name__}: {e}"
            )

        if isinstance(e, errors.CommandOnCooldown):
            log.debug(debug_message)
            await ctx.respond(e, ephemeral=True)
            return
        elif isinstance(e, errors.MissingPermissions):
            log.debug(debug_message)
            await ctx.respond(e, ephemeral=True)
            return
        else:
            log.error(e)

        log.debug("Sending Error Message to the Channel")
        error_channel = self.bot.get_channel(Channels.error_channel)

        error_embed = create_embed(description=debug_message)
        error_embed.add_field(name="Command", value=ctx.command.name, inline=False)
        error_embed.add_field(name="Requestor", value=ctx.author.name, inline=False)
        error_embed.add_field(name="Guild", value=ctx.guild.name, inline=False)
        error_embed.add_field(name="Channel", value=ctx.channel.name, inline=False)
        error_embed.add_field(name="Error", value=f"```{e}```", inline=False)
        await error_channel.send(embed=error_embed)

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
            embed = self._get_error_embed(
                f"Missing required argument: {e.param.name}", e.param.name
            )
            log.debug("Missing Required Argument")
        elif isinstance(e, errors.TooManyArguments):
            embed = self._get_error_embed("Too many arguments", str(e))
            log.debug("Too Many Arguements")
        elif isinstance(e, errors.BadArgument):
            embed = self._get_error_embed("Bad argument", str(e))
            log.debug("Bad Argument")
        elif isinstance(e, errors.BadUnionArgument):
            embed = self._get_error_embed("Bad argument", f"{e}\n{e.errors[-1]}")
            log.debug("Bad (Union) Argument")
        elif isinstance(e, errors.ArgumentParsingError):
            embed = self._get_error_embed("Argument parsing error", str(e))
            log.debug("Argument Parsing Error")
            await ctx.send(embed=embed)
            return
        else:
            embed = self._get_error_embed(
                "Input error",
                "Something about your input seems off. Check the arguments and try again.",
            )
            # self.bot.stats.incr("errors.other_user_input_error")
            log.debug(
                "Input Error: Something about your input seems off. Check the arguments and try again."
            )

        await ctx.send(embed=embed)

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
            log.debug("errors.bot_permission_error")
            await ctx.send(
                "Sorry, it looks like I don't have the permissions or roles I need to do that."
            )

    @staticmethod
    async def handle_api_error(ctx: Context, e: ResponseCodeError) -> None:
        """Send an error message in `ctx` for ResponseCodeError and log it."""
        if e.status == 404:
            log.debug(f"API responded with 404 for command {ctx.command}")
            await ctx.send("There does not seem to be anything matching your query.")
            log.debug("errors.api_error_404")
        elif e.status == 400:
            content = await e.response.json()
            log.debug(f"API responded with 400 for command {ctx.command}: %r.", content)
            await ctx.send("According to the API, your request is malformed.")
            log.debug("errors.api_error_400")
        elif 500 <= e.status < 600:
            log.warning(f"API responded with {e.status} for command {ctx.command}")
            await ctx.send("Sorry, there seems to be an internal issue with the API.")
            log.debug("errors.api_internal_server_error")
        else:
            log.warning(
                f"Unexpected API response for command {ctx.command}: {e.status}"
            )
            await ctx.send(
                f"Got an unexpected status code from the API (`{e.status}`)."
            )
            log.debug(f"errors.api_error_{e.status}")

    @staticmethod
    async def handle_unexpected_error(ctx: Context, e: errors.CommandError) -> None:
        """Send a generic error message in `ctx` and log the exception as an error with exc_info."""
        await ctx.send(
            f"Sorry, an unexpected error occurred. Please let us know!\n\n"
            f"```{e.__class__.__name__}: {e}```"
        )

        log.debug("errors.unexpected")

        # with push_scope() as scope:
        #     scope.user = {"id": ctx.author.id, "username": str(ctx.author)}

        #     scope.set_tag("command", ctx.command.qualified_name)
        #     scope.set_tag("message_id", ctx.message.id)
        #     scope.set_tag("channel_id", ctx.channel.id)

        #     scope.set_extra("full_message", ctx.message.content)

        #     if ctx.guild is not None:
        #         scope.set_extra(
        #             "jump_to",
        #             f"https://discordapp.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}",
        #         )

        log.error(
            f"Error executing command invoked by {ctx.message.author}: {ctx.message.content}",
            exc_info=e,
        )


def setup(bot: Bot) -> None:
    """Load the ErrorHandler cog."""
    bot.add_cog(ErrorHandler(bot))
