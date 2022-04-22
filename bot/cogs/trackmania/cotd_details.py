from typing import List, Tuple

import discord
import matplotlib.pyplot as plt
from discord import ApplicationContext
from discord.commands import Option
from discord.ext import commands
from discord.ext.pages import Paginator
from trackmania import BestCOTDStats, Player, PlayerCOTD, PlayerCOTDResults

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import EZEmbed

log = get_logger(__name__)


class COTDDetails(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="cotd-details",
        description="Gets the COTD Details of a player along with a graph of the last 25 COTDs",
    )
    @discord.ext.commands.cooldown(1, 15, commands.BucketType.guild)
    async def _cotd_details(
        self,
        ctx: ApplicationContext,
        username: Option(str, "The username of the player", required=True),
    ):
        log_command(ctx, "cotd_details")

        await ctx.defer()

        player_id = await Player.get_id(username)
        page = 0
        pop_flag = True

        if player_id is None:
            log.error(f"Invalid Username was given -> {username} by {ctx.author.name}")
            await ctx.respond(
                embed=EZEmbed.create_embed(
                    "Invalid Username",
                    f"Username Given: {username}",
                    color=discord.Colour.red(),
                )
            )
            return

        log.debug("Getting COTD Stats")
        cotd_stats = await PlayerCOTD.get_page(player_id, page)

        log.debug("Creating Pages")
        pages = COTDDetails.__parse_pages(cotd_stats, username)

        log.debug("Popping COTDs")
        popped, original = COTDDetails.__pop_reruns(cotd_stats.recent_results)

        while (len(popped) <= 25 and page < 5) or pop_flag:
            page += 1
            cotd_stats_new = await PlayerCOTD.get_page(player_id, page)

            _new_popped, _new_original = COTDDetails.__pop_reruns(
                cotd_stats_new.recent_results
            )
            popped.extend(_new_popped)
            original.extend(_new_original)

            pop_flag = False

        if len(popped) > 25:
            popped = popped[:25]
        if len(original) > 25:
            original = original[:25]

        log.debug("Creating Graphs")
        COTDDetails.__create_graphs(popped, original)

        log.debug("Sending Images to Channel")
        channel = self.bot.get_channel(962961137924726834)
        image_message = await channel.send(
            files=[
                discord.File("./bot/resources/temp/overall.png"),
                discord.File("./bot/resources/temp/primary.png"),
            ]
        )

        log.debug("Getting Image URLs")
        url_one = image_message.attachments[0].url
        url_two = image_message.attachments[1].url

        pages[0].set_image(url=url_one)
        pages[1].set_image(url=url_two)

        log.debug("Sending Paginator")
        paginator = Paginator(pages=pages)
        await paginator.respond(ctx.interaction)
        log.debug("Paginator Finished")

    @staticmethod
    def __parse_pages(cotd_stats: PlayerCOTD, username: str):
        log.info(f"Parsing Pages for {cotd_stats.player_id}")

        log.debug("Creating 2 Embeds")
        page_one = EZEmbed.create_embed(title=f"Overall Data for {username}")
        page_two = EZEmbed.create_embed(title=f"Primary Data for {username}")

        log.debug("Adding Total COTDs Played")
        page_one.add_field(name="Total Played", value=cotd_stats.total, inline=False)
        page_two.add_field(name="Total Played", value=cotd_stats.total, inline=False)

        log.debug("Adding Average Data")
        average_data = COTDDetails.__create_avg_data_str(cotd_stats)
        page_one.add_field(name="Average Stats", value=average_data, inline=False)
        page_two.add_field(name="Average Stats", value=average_data, inline=False)

        log.debug("Adding Best Stats")
        page_one = COTDDetails.__parse_best_stats(
            page_one, cotd_stats.stats.best_overall
        )
        page_two = COTDDetails.__parse_best_stats(
            page_two, cotd_stats.stats.best_primary
        )

        log.debug("Returning Embed Pages")
        return (page_one, page_two)

    @staticmethod
    def __parse_best_stats(page: discord.Embed, stats: BestCOTDStats):
        log.debug("Parsing Best Stats")
        temp_str = f"Best Division - {stats.best_div}\nBest Division Time Achieved -> {stats.best_div_time}\n\nBest Rank -> {stats.best_rank}\nRank Achieved in Division of Best Rank -> {stats.best_rank_div_rank}\nBest Rank - Time Achieved -> {stats.best_rank_time}\n\nBest Rank in Division -> {stats.best_rank_in_div}\nBest Rank in Division - Division Achived -> {stats.best_rank_in_div_div}\nBest Rank in Division - Time Achieved -> {stats.best_rank_in_div_time}"

        page.add_field(name="Best Stats", value=f"```\n{temp_str}\n```")

        return page

    @staticmethod
    def __pop_reruns(cotds: List[PlayerCOTDResults]) -> Tuple[List[PlayerCOTDResults]]:
        popped = cotds
        temp = []

        for cotd in popped:
            if cotd.name.endswith("#1"):
                log.debug("Popping %s", cotd.name)
                temp.append(popped[popped.index(cotd)])

        return (temp, cotds)

    @staticmethod
    def __create_graphs(
        popped: List[PlayerCOTDResults], original: List[PlayerCOTDResults]
    ):
        popped_name_list, popped_rank_list = [], []
        original_name_list, original_rank_list = [], []

        log.debug("Adding Names and Ranks for Primary Data")
        for i, cotd in enumerate(popped):
            popped_name_list.append(cotd.name)
            popped_rank_list.append(cotd.rank)
        log.debug("Adding Names and Ranks for Original Data")
        for cotd in original:
            original_name_list.append(cotd.name)
            original_rank_list.append(cotd.rank)

        log.debug("Creating Loop Tuple")
        loop_tuple = (
            (popped_name_list, popped_rank_list, "Primary Rank Graph", "primary.png"),
            (
                original_name_list,
                original_rank_list,
                "Overall Rank Graph",
                "overall.png",
            ),
        )

        log.info("Creating the Graphs for COTD Details")
        for i in range(2):
            log.debug(f"{loop_tuple[i][2]} -> Clearing Graph")
            plt.clf()

            log.debug(f"{loop_tuple[i][2]} -> Plotting Graph")
            plt.plot(loop_tuple[i][0], loop_tuple[i][1], label=loop_tuple[i][2])
            plt.xlabel("COTD Names")

            log.debug(f"{loop_tuple[i][2]} -> Setting Plot Rotation to 90Deg")
            plt.xticks(rotation=90)

            log.debug(f"{loop_tuple[i][2]} -> Setting YLabel to Ranks")
            plt.ylabel("Ranks")

            log.debug(f"{loop_tuple[i][2]} -> Setting title to {loop_tuple[i][2]}")
            plt.title(f"{loop_tuple[i][2]}")

            log.debug(f"{loop_tuple[i][2]} -> Setting Tight Layout")
            plt.tight_layout()

            log.debug(f"{loop_tuple[i][2]} -> saving the Plot")
            plt.savefig(f"./bot/resources/temp/" + loop_tuple[i][3])

    @staticmethod
    def __create_avg_data_str(data: PlayerCOTD) -> str:
        log.debug("Creating Average Data String")
        average_rank = round(data.stats.average_rank, 4) * 100
        average_div = round(data.stats.average_div, 2)
        average_div_rank = round(data.stats.average_div_rank, 4) * 100

        return f"```Average Rank -> {average_rank}\nAverage Division -> {average_div}\nAverage Division Rank -> {average_div_rank}```"


def setup(bot: Bot):
    """Adds the COTDDetails cog"""
    bot.add_cog(COTDDetails(bot))
