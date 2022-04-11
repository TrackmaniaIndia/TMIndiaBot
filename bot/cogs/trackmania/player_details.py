from typing import List

import discord
from discord import ApplicationContext
from discord.commands import Option
from discord.ext import commands
from discord.ext.pages import Paginator
from trackmania import Player, PlayerMatchmaking, PlayerMetaInfo

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.commons import Commons
from bot.utils.discord import EZEmbed

log = get_logger(__name__)


class PlayerDetails(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="playerdetails",
        description="Gets the player details of a sepcific username",
    )
    @discord.ext.commands.cooldown(1, 15, commands.BucketType.guild)
    async def _player_details(
        self,
        ctx: ApplicationContext,
        username: Option(str, "The username of the player", required=True),
    ):
        log_command(ctx, "player_details")

        await ctx.defer()

        player_id = await Player.get_id(username)

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

        log.debug("Getting PlayerData")
        player_data: Player = await Player.get(player_id)

        log.debug("Creating Pages")
        pages = PlayerDetails.__create_pages(player_data)
        log.debug("Pages Created")

        if isinstance(pages, str):
            await ctx.respond(pages)
            return

        log.debug("Creating Paginator")
        paginator = Paginator(pages)
        await paginator.respond(ctx.interaction)

    @staticmethod
    def __create_pages(player_data: Player) -> List[discord.Embed]:
        log.info(f"Creating PlayerDetail pages for {player_data.name}")
        display_name = player_data.name

        log.debug("Creating Strings to Use in the Pages.")
        zone_str = ""

        try:
            for zone in player_data.zone:
                zone_str = zone_str + zone.zone + " - " + zone.rank + "\n"
        except TypeError:
            return "This player has never played Trackmania 2020 Before."

        trophy_str = ""
        for i, trophyd in enumerate(player_data.trophies.trophies):
            trophy_str = (
                trophy_str + f"T{i + 1} - " + Commons.add_commas(trophyd) + "\n"
            )

        trophy_str = (
            trophy_str + f"\n{Commons.add_commas(player_data.trophies.score())}"
        )

        matchmaking_str = (
            "No 3v3 Data Available"
            if player_data.m3v3_data is None
            else PlayerDetails.__parse_mm(player_data.m3v3_data)
        )
        royal_str = (
            "No Royal Data Available"
            if player_data.royal_data is None
            else PlayerDetails.__parse_mm(player_data.royal_data)
        )

        log.debug("Creating Embed Pages")
        page_one = EZEmbed.create_embed(f"Player Data for {display_name} - Page 1")
        page_two = EZEmbed.create_embed(f"Player Data for {display_name} - Page 2")
        page_three = EZEmbed.create_embed(f"Player Data for {display_name} - Page 3")

        log.debug("Adding Fields to Embed Pages")
        page_one.add_field(name="Zone Data", value=f"```{zone_str}```", inline=False)
        page_one = PlayerDetails.__parse_meta(
            page_one, player_data.meta, player_data.player_id
        )
        page_two.add_field(
            name="3v3 Data", value=f"```{matchmaking_str}```", inline=False
        )
        page_two.add_field(name="Royal Data", value=f"```{royal_str}```", inline=False)
        page_three.add_field(
            name="Trophy Count", value=f"```{trophy_str}```", inline=False
        )

        return (page_one, page_two, page_three)

    @staticmethod
    def __parse_meta(
        page: discord.Embed, player_meta: PlayerMetaInfo, player_id: str | None = None
    ) -> discord.Embed:
        log.debug(f"Parsing Metadata for {player_id}")

        if player_meta.twitch is not None:
            page.add_field(
                name=f"{constants.Emojis.twitch} Twitch",
                value=f"[{player_meta.twitch}](https://twitch.tv/{player_meta.twitch})",
            )
        if player_meta.twitter is not None:
            page.add_field(
                name=f"{constants.Emojis.twitter} Twitter",
                value=f"[{player_meta.twitter}](https://twitter.com/{player_meta.twitter})",
            )
        if player_meta.youtube is not None:
            page.add_field(
                name=f"{constants.Emojis.youtube} Youtube",
                value=f"[YouTube](https://youtube.com/c/{player_meta.youtube})",
            )

        if player_id is not None:
            page.add_field(
                name=f"{constants.Emojis.tmio} TMIO",
                value=f"[TMIO](https://trackmania.io/#/player/{player_id})",
            )

        return page

    @staticmethod
    def __parse_mm(mm_data: PlayerMatchmaking) -> str:
        log.debug("Parsing Matchmaking Data")

        progression = mm_data.progression
        progress = mm_data.progress
        rank = mm_data.rank
        score = mm_data.score
        division = mm_data.division
        division_str = mm_data.division_str
        max_points = mm_data.max_points

        return f"Progression: {progression}\nProgress: {progress}\nRank: {rank}\nScore: {score}\nDivision: {division_str} - {division}\n\nPoints to Next Division: {max_points + 1}"


def setup(bot: Bot):
    """Adds the PlayerDetails cog"""
    bot.add_cog(PlayerDetails(bot))
