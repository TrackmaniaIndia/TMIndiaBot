import json
from itertools import zip_longest
from typing import Dict

import discord
from discord import ApplicationContext
from discord.commands import Option, permissions
from discord.ext import commands
from discord.ext.pages import Paginator
from trackmania import Player

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.commons import Commons
from bot.utils.discord import EZEmbed

log = get_logger(__name__)


class ShowTrophies(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="showtrophies",
        description="Shows the current TMI Trophy Leaderboards",
    )
    async def _show_trophy_leaderboards(
        self,
        ctx: ApplicationContext,
    ):
        log_command(ctx, "add_player_tracking")

        await ctx.defer()

        log.debug("Opening Trophy File")
        with open("./bot/resources/json/trophy_tracking.json", "r") as file:
            trophy_leaderboards = json.load(file)

        split_list = list(
            zip_longest(*(iter(trophy_leaderboards.get("tracking")),) * 10)
        )
        pages_needed = len(split_list)
        embeds = [
            EZEmbed.create_embed(f"Trophy Leaderboard for TMI - Page {i + 1}")
            for i in range(pages_needed)
        ]
        count = 0
        for j, plist in enumerate(split_list):
            player_str = ""
            for player in plist:
                if player is None:
                    break
                player_str = (
                    player_str
                    + f"\n{count + 1}. {player.get('username')} - {Commons.add_commas(player.get('score'))}"
                )
                count += 1

            embeds[j].add_field(
                name="Trophies", value=f"```{player_str}```", inline=False
            )

        log.debug("Sending Embed")
        if len(embeds) == 1:
            await ctx.respond(embed=embeds[0])
        else:
            paginator = Paginator(embeds)
            await paginator.respond(ctx.interaction)


def setup(bot: Bot):
    bot.add_cog(ShowTrophies(bot))
