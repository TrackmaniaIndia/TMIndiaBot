from datetime import datetime

from discord import ApplicationContext, Option, SlashCommandOptionType
from discord.ext import commands
from discord.ext.pages import Paginator
from prettytable import PrettyTable
from trackmania import Campaign
from trackmania.config import cache_flush_key

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.commons import (
    add_commas,
    format_seconds,
    format_time_split,
    split_list_of_lists,
)
from bot.utils.discord import create_embed

log = get_logger(__name__)


class TopCampaign(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="top-campaign",
        description="Gets the top players of the current campaign based on score.",
    )
    async def _top_campaign(
        self,
        ctx: ApplicationContext,
        position: Option(
            SlashCommandOptionType.integer,
            "From which position to start at.",
            default=0,
        ),
    ):
        log_command(ctx, "top_command")
        await ctx.defer()

        log.debug("Getting current campaign data")
        current = await Campaign.current_season()

        log.debug(
            "Getting top players of current campaign with starting position %s",
            position,
        )
        top = await current.leaderboards(offset=position)
        split_list = split_list_of_lists(top, 20)
        embeds = []

        log.debug("Creating Embeds")
        for group in split_list:
            scores = []

            for player in group:
                pos_data = {}

                pos_data["position"] = player.position
                pos_data["name"] = player.player_name
                pos_data["points"] = add_commas(player.points)

                scores.append(pos_data)

            table = PrettyTable(["Position", "Name", "Score"])

            for score in scores:
                table.add_row([score["position"], score["name"], score["points"]])

            embed = create_embed(
                title=f"{position}->{position + 100} of Current Campaign",
                description=f"```{table}```",
            )
            embeds.append(embed)

        log.debug("Running Top Campaigns paginator")
        paginator = Paginator(embeds, timeout=60)
        await paginator.respond(ctx.interaction)


def setup(bot: Bot):
    bot.add_cog(TopCampaign(bot))
