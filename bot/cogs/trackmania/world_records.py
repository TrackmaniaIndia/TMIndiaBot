from discord import ApplicationContext
from discord.commands import Option
from discord.ext import commands
from discord.ext.pages import Paginator

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.leaderboard import Leaderboards

log = get_logger(__name__)


class CampaignWRs(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="worldrecords",
        description="Gets the world records for campaign maps",
    )
    async def _world_records_slash(
        self,
        ctx: ApplicationContext,
        year: Option(
            str, description="Year of Season", choices=["2020", "2021", "2022"]
        ),
        season: Option(
            str, "The season", choices=["Winter", "Spring", "Summer", "Fall"]
        ),
    ):
        log_command(ctx, "world_records_slash")
        illegal_combinations = [
            ("2020", "Winter"),
            ("2020", "Spring"),
            ("2022", "Spring"),
            ("2022", "Summer"),
            ("2022", "Fall"),
        ]

        if (year, season) in illegal_combinations:
            await ctx.respond("Illegal Combination")
            return

        maps = Leaderboards.get_world_records(year, season)
        maps_pag = Paginator(pages=maps)
        await maps_pag.respond(ctx.interaction)

    @commands.command(
        name="worldrecords",
        description="Gets the world records for campaign maps",
    )
    async def _world_records(
        self,
        ctx: commands.Context,
        year: str,
        season: str,
    ):
        log_command(ctx, "world_records")
        if str(year) not in ("2020", "2021", "2022"):
            raise commands.BadArgument("Invalid year")

        if season.capitalize() not in ("Winter", "Spring", "Summer", "Fall"):
            raise commands.BadArgument("Invalid season")

        illegal_combinations = [
            ("2020", "Winter"),
            ("2020", "Spring"),
            ("2022", "Spring"),
            ("2022", "Summer"),
            ("2022", "Fall"),
        ]

        if (year, season.capitalize()) in illegal_combinations:
            await ctx.send(f"Illegal Combination\nCombination Given: {year} {season}")
            return

        maps = Leaderboards.get_world_records(year, season)
        maps_pag = Paginator(pages=maps)
        await maps_pag.send(ctx)


def setup(bot: Bot):
    bot.add_cog(CampaignWRs(bot))
