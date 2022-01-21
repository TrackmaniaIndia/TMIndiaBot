from discord.commands import Option, permissions
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.trackmania import TrackmaniaUtils, Leaderboards

log = get_logger(__name__)


class StalkPlayer(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(guild_ids=constants.Bot.default_guilds, name="stalkplayer")
    @permissions.has_any_role("TSCC", "Moderator", "Admin", "Developer")
    async def _stalk_player_slash(
        self,
        ctx: commands.Context,
        username: Option(str, "The username of the player", required=True),
    ):
        log_command(ctx, "stalk_player_slash")

        # Check if the Username is in the top 500 for any maps in the TSCC Map
        # Pool

        log.info("Deferring Response")
        await ctx.defer()
        log.info("Deferred Response")

        player_obj = TrackmaniaUtils(username)

        log.info(f"Checking Player username -> {username}")
        player_id = player_obj.get_id()
        log.info(f"Got Player Id -> {player_id}")

        await player_obj.close()

        if player_id is None:
            log.error(f"Invalid Username Given, Username -> {username}")
            await ctx.respond(
                content=f"Invalid Username\nUsername given: {username}", ephemeral=True
            )

            return

        log.info(f"Valid Username, Username -> {username}")
        log.info("Executing Function, Pray")
        await ctx.respond(embed=Leaderboards.get_player_good_maps(username))
        log.info("Player stalking was a success")


def setup(bot: Bot):
    bot.add_cog(StalkPlayer(bot))
