from trackmania import TOTD, totd

from datetime import datetime

from discord import Option, ApplicationContext
from discord.ext import commands
from discord.ext.pages import Paginator
from prettytable import PrettyTable

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.commons import format_seconds, split_list_of_lists
from bot.utils.discord import create_embed

log = get_logger(__name__)

class TOTDLeaderboards(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        name="totd-leaderboards",
        description="Get a certain TOTD's leaderboard",
    )
    async def _totd_lb(self, 
        ctx: ApplicationContext,
        year: Option(int, "The year", required=True),
        month: Option(str, "The month", choices=constants.Consts.months, required=True),
        day: Option(int, "The day", required=True),
    ):
        log_command(ctx, "totd-lb")
        await ctx.defer()

        log.debug("Doing Initial Basic Checks")
        if day < 1 or day > 31:
            await ctx.respond("Invalid Date")
            return
        if year < 2020:
            await ctx.respond("Invalid year")
            return
        log.debug("Passed Initial Basic Checks")

        month_int = constants.Consts.months.index(month) + 1
        the_date = datetime(year, month_int, day)
        
        totd_data: TOTD = await TOTD.get_totd(the_date)
        leaderboards = await totd_data.map.get_leaderboard(length=100)
        map_name = totd_data.map.name

        split_list = split_list_of_lists(leaderboards, 20)

        embeds = []
        for group in split_list:
            times = []
            for lb in group:
                # timestr = f"{lb.position}) {lb.player_name} -> {lb.time}"
                time_data = {}

                time_data['pl_name'] = lb.player_name
                time_data['position'] = lb.position
                time_data['time'] = format_seconds(lb.time)

                times.append(time_data)

            lb_table  = PrettyTable(["Position", "Username", "Time"])
            for time in times:
                lb_table .add_row([time['position'], time['pl_name'], time['time']])

            embed = create_embed(
                title=f"Top 100 Leaderboards for {map_name}",
                description=f"**Date**\n{day} {month} {year}\n```{lb_table }```"
            )
            embeds.append(embed)

        totd_paginator = Paginator(pages=embeds, timeout=60)
        await totd_paginator.respond(ctx.interaction)

def setup(bot: Bot) -> None:
    """Load the TOTDLeaderboards cog."""
    bot.add_cog(TOTDLeaderboards(bot))
