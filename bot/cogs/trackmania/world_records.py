import discord
from discord.commands import Option
from discord.ext import commands
from discord.ext.pages import Paginator

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import Confirmer
from bot.utils.discord import EZEmbed
from bot.utils.trackmania import Leaderboards

log = get_logger(__name__)


class CampaignWRs(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="world_records",
        description="Gets the world records for campaign maps",
    )
    async def _world_records_slash(
        self,
        ctx: commands.Context,
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


def setup(bot: Bot):
    bot.add_cog(CampaignWRs(bot))
