import json
from itertools import zip_longest

from discord import ApplicationContext
from discord.ext import commands
from discord.ext.pages import Paginator
from prettytable import PrettyTable

import bot.utils.commons as commons
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import create_embed

log = get_logger(__name__)


class ShowTrophies(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="show-trophies",
        description="Shows the current TMI Trophy Leaderboards",
    )
    async def _show_trophy_leaderboards(
        self,
        ctx: ApplicationContext,
    ):
        log_command(ctx, "add_player_tracking")

        await ctx.defer()

        log.debug("Opening Trophy File")
        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/trophy_tracking.json", "r"
        ) as file:
            trophy_leaderboards = json.load(file)

        log.debug("Splitting List")
        split_list = list(
            zip_longest(*(iter(trophy_leaderboards.get("tracking")),) * 10)
        )
        pages_needed = len(split_list)
        embeds = [
            create_embed(f"Trophy Leaderboard for TMI - Page {i + 1}")
            for i in range(pages_needed)
        ]
        count = 0

        log.debug("Creating Tables for Embeds")
        for j, plist in enumerate(split_list):
            trophy_table = PrettyTable(["Rank", "Name", "Score"])

            for player in plist:
                if player is None:
                    # List has run out of players
                    break

                log.debug(player)

                # Updating table
                trophy_table.add_row(
                    [
                        count + 1,
                        player.get("username"),
                        commons.add_commas(player.get("score")),
                    ]
                )

                # Update player count
                count += 1

            embeds[j].description = f"```{trophy_table}```"

        log.debug("Sending Embed")
        if len(embeds) == 0:
            await ctx.respond("No player is set up for trophy tracking in this server")
        elif len(embeds) == 1:
            await ctx.respond(embed=embeds[0])
        else:
            paginator = Paginator(embeds)
            await paginator.respond(ctx.interaction)


def setup(bot: Bot):
    bot.add_cog(ShowTrophies(bot))
