from typing import List

import discord
from discord import ApplicationContext, SlashCommandOptionType
from discord.commands import Option
from discord.ext import commands
from discord.ext.pages import Paginator
from trackmania import Player, PlayerMetaInfo, PlayerZone

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import create_embed

log = get_logger(__name__)


class PlayerDetails(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="player-details",
        description="Gets the player details of a sepcific username",
    )
    @discord.ext.commands.cooldown(1, 15, commands.BucketType.guild)
    async def _player_details(
        self,
        ctx: ApplicationContext,
        username: Option(
            SlashCommandOptionType.string, "The username of the player", required=True
        ),
    ):
        log_command(ctx, "player_details")

        await ctx.defer()

        log.debug("Getting Player ID")
        player_id = await Player.get_id(username)

        if player_id is None:
            log.error(f"Invalid Username was given -> {username} by {ctx.author.name}")
            await ctx.respond(
                embed=create_embed(
                    "Invalid Username",
                    f"Username Given: {username}",
                    color=discord.Colour.red(),
                )
            )
            return

        log.debug("Getting PlayerData")
        player_data: Player = await Player.get_player(player_id)

        log.debug("Creating Pages")
        pages = PlayerDetails.__create_pages(player_data)

        if isinstance(pages, str):
            await ctx.respond(pages)
            return

        log.debug("Running Paginator")
        paginator = Paginator(pages)
        await paginator.respond(ctx.interaction)
        log.debug("Paginator Finished")

    @staticmethod
    def __create_pages(player_data: Player) -> List[discord.Embed]:
        log.info(f"Creating PlayerDetail pages for {player_data.name}")
        display_name = player_data.name

        log.debug("Creating Strings to Use in the Pages.")
        zone_str = PlayerZone.to_string(player_data.zone)

        log.debug("Getting Trophies String")
        trophy_str = str(player_data.trophies)

        matchmaking_str = str(player_data.m3v3_data)
        royal_str = str(player_data.royal_data)

        log.debug("Creating Embed Pages")
        page_one = create_embed(f"Player Data for {display_name} - Page 1")
        page_two = create_embed(f"Player Data for {display_name} - Page 2")
        page_three = create_embed(f"Player Data for {display_name} - Page 3")

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


def setup(bot: Bot):
    """Adds the PlayerDetails cog"""
    bot.add_cog(PlayerDetails(bot))
