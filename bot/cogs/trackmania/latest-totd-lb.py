from trackmania import TOTD, totd

from datetime import datetime, date

from discord import Option, ApplicationContext
from discord.ext import commands
from discord.ext.pages import Paginator
from prettytable import PrettyTable

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.commons import format_seconds, split_list_of_lists, format_time_split
from bot.utils.discord import create_embed

log = get_logger(__name__)

def remove_unnecessary_minutes(time: str) -> str:
    if time.startswith('0'):
        return time.split(':')[1]
    else:
        return time

class LatestTOTDLeaderboards(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        name="latest-totd-leaderboards",
        description="Get latest TOTD's leaderboard",
    )
    async def _latest_totd_lb(self, 
        ctx: ApplicationContext,
    ):
        log_command(ctx, "latest-totd-lb")
        await ctx.defer()
        
        totd_data: TOTD = await TOTD.latest_totd()
        leaderboards = await totd_data.map.get_leaderboard(length=100)
        map_name = totd_data.map.name
        first_time = leaderboards[0].time

        split_list = split_list_of_lists(leaderboards, 20)

        embeds = []
        time_format = '%M:%S.%f'
        for group in split_list:
            times = []
            for lb in group:
                # timestr = f"{lb.position}) {lb.player_name} -> {lb.time}"
                time_data = {}

                time_data['pl_name'] = lb.player_name
                time_data['position'] = lb.position

                time_formated = format_seconds(lb.time)
                time_formated_wihtout_zero = remove_unnecessary_minutes(time_formated)

                time_data['time'] = time_formated_wihtout_zero

                tdelta = datetime.strptime(time_formated, time_format) - datetime.strptime(format_seconds(first_time), time_format)
                
                split = format_time_split(tdelta.total_seconds())
                time_data['split'] = f"+{split}"

                times.append(time_data)

            lb_table  = PrettyTable(["Position", "Username", "Time", "Split"])
            for time in times:
                lb_table .add_row([time['position'], time['pl_name'], time['time'], time['split']])

            today = date.today()
            embed = create_embed(
                title=f"Top 100 Leaderboards for {map_name}",
                description=f"**Date**\n{today.day} {constants.Consts.months[today.month - 1]} {today.year}\n```{lb_table }```"
            )
            embeds.append(embed)

        totd_paginator = Paginator(pages=embeds, timeout=60)
        await totd_paginator.respond(ctx.interaction)

def setup(bot: Bot) -> None:
    """Load the LatestTOTDLeaderboards cog."""
    bot.add_cog(LatestTOTDLeaderboards(bot))
