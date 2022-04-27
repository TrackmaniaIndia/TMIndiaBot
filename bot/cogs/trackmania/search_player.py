from re import L
from typing import List

import discord
from discord import ApplicationContext, Option, SlashCommandOptionType
from discord.ext import commands
from discord.ext.pages import Paginator
from trackmania import Player, PlayerZone
from trackmania.player import PlayerSearchResult

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import create_embed

log = get_logger(__name__)


class SearchPlayer(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="search-player",
        description="Searches for Players With a Certain username",
    )
    async def _search_player(
        self,
        ctx: ApplicationContext,
        username: Option(
            SlashCommandOptionType.string,
            "The username of the player to search",
            required=True,
        ),
    ):
        log_command(ctx, "search_player")

        await ctx.defer()

        log.debug("Searching for Players with Username %s", username)
        player_search_results = await Player.search(username)

        if player_search_results is None:
            log.error("No Players found with username %s", username)
            error_embed = create_embed(
                title=f"Search Results for Username: {username}",
                description="There are no players with this username",
                color=discord.Colour.red(),
            )
            await ctx.respond(embed=error_embed)

        log.debug("Creating Embed List")
        embed_list = [
            create_embed(title=f"Search Results for Username: {username}")
            for _ in range(len(player_search_results))
        ]

        for i, player in enumerate(player_search_results):
            player: PlayerSearchResult
            embed_list[i].add_field(name="Name", value=player.name, inline=True)
            if player.club_tag is not None:
                embed_list[i].add_field(
                    name="Club Tag", value=player.club_tag, inline=True
                )
            if player.zone is not None:
                embed_list[i].add_field(
                    name="Zone",
                    value=PlayerZone.to_string(player.zone, add_pos=False, inline=True),
                    inline=False,
                )
            embed_list[i].add_field(name="ID", value=player.player_id, inline=True)

        paginator = Paginator(
            embed_list, author_check=False, loop_pages=True, timeout=60
        )
        await paginator.respond(ctx.interaction)


def setup(bot: Bot):
    bot.add_cog(SearchPlayer(bot))
