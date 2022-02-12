from discord import ApplicationContext
from discord.commands import Option
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import EZEmbed
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
        ctx: ApplicationContext,
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
            embed=EZEmbed.create_embed(
                title=f"Here is the ID for {username}",
                description=id if id is not None else "Invalid Username.",
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
            embed=EZEmbed.create_embed(
                title=f"Here is the ID for {username}",
                description=id if id is not None else "Invalid Username Given.",
            ),
        )


def setup(bot: Bot):
    """Add the GetID Cog"""
    bot.add_cog(GetID(bot))
