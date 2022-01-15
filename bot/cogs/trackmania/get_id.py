from discord.commands import Option
from discord.ext import commands

import bot.utils.discord.easy_embed as ezembed
from bot import constants
from bot.bot import Bot
from bot.log import get_logger
from bot.log import log_command
from bot.utils.trackmania import TrackmaniaUtils

log = get_logger(__name__)


class GetID(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="getid",
        description="Gets an ID for a specific username",
    )
    async def _get_id_slash(
        self,
        ctx: commands.Context,
        username: Option(str, "The username of the player", required=True),
    ):
        log_command(ctx, "get_id_slash")

        await ctx.defer()

        log.debug(f"Creating TrackmaniaUtil object for {username}")
        username_obj = TrackmaniaUtils(username)
        log.debug(f"Created TrackmaniaUtil object for {username}")

        log.info(f"Getting ID for {username}")
        id = await username_obj.get_id()

        await username_obj.close()
        del username_obj

        await ctx.respond(
            embed=ezembed.create_embed(
                title=f"Here is the ID for {username}", description=id
            ),
            ephemeral=True,
        )

    @commands.command(name="getid", description="Gets an ID for a specific username")
    async def _get_id(self, ctx: commands.Context, username: str):
        log_command(ctx, "get_id")

        log.debug(f"Creating TrackmaniaUtil object for {username}")
        username_obj = TrackmaniaUtils(username)
        log.debug(f"Created TrackmaniaUtil object for {username}")

        log.info(f"Getting ID for {username}")
        id = await username_obj.get_id()

        await username_obj.close()
        del username_obj

        await ctx.send(
            embed=ezembed.create_embed(
                title=f"Here is the ID for {username}", description=id
            ),
        )

    @_get_id.error
    async def error(self, ctx: commands.Context, error: Exception):
        log.error(error)

        if isinstance(error, commands.MissingRequiredArgument):
            log.error("Missing required arguments")

            log.debug("Creating Error Embed")
            await ctx.send(
                embed=ezembed.create_embed(
                    title=":warning: Missing required argument: Username",
                    description="**Username is a required argument that is missing**, \n\nUsage: playerdetails {Username}",
                    color=0xFF0000,
                )
            )

            log.debug("Sent error Embed")
            return None


def setup(bot: Bot):
    """Add the GetID Cog"""
    bot.add_cog(GetID(bot))
