from discord.commands import Option
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.trackmania import TrackmaniaUtils

log = get_logger(__name__)


class COTDDetails(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        default_guilds=constants.Bot.default_guilds,
        name="cotddetails",
        description="COTD Details of a player including 2 graphs with and without reruns",
    )
    async def _cotd_details_slash(
        self,
        ctx: commands.Cog,
        username: Option(str, "Username of the player", required=True),
    ):
        log_command(ctx, "cotd_details_slash")

        await ctx.defer()

        log.debug(f"Creating a TrackmaniaUtils object with username -> {username}")
        player_obj = TrackmaniaUtils(username)
        log.debug(f"Created a TrackmaniaUtils object with username -> {username}")

        log.debug("Getting player id")
        player_id = await player_obj.get_id()
        log.debug(f"Got player id -> {player_id}")

        if player_id is None:
            await ctx.respond(
                f"Invalid Username Given\nUsername Given: {username}", ephemeral=True
            )
            return

        cotd_data, image = await player_obj.get_cotd_data(player_id)

        if image is not None:
            await ctx.respond(file=image, embed=cotd_data)
        else:
            await ctx.respond(embed=cotd_data)

        await player_obj.close()


def setup(bot: Bot):
    bot.add_cog(COTDDetails(bot))
