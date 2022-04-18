import json
from typing import Dict

import discord
from discord import ApplicationContext, Bot
from discord.commands import Option, permissions
from discord.ext import commands
from trackmania import Player

from bot import constants
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

        log.debug("Creating Embed")
        embed = EZEmbed.create_embed(
            title="Trophy Leaderboard for TMI", color=discord.Color.orange()
        )

        player_str = ""
        for i, player in enumerate(trophy_leaderboards.get("tracking")):
            player_str = (
                player_str
                + f"\n{i + 1}. {player.get('username')} - {Commons.add_commas(player.get('score'))}"
            )

        embed.add_field(name="Trophies", value=f"```{player_str}```", inline=False)

        log.debug("Sending Embed")
        await ctx.respond(embed=embed)


def setup(bot: Bot):
    bot.add_cog(ShowTrophies(bot))
