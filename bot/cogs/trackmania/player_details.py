import country_converter as coco
import discord
import discord.ext.commands as commands
import flag
import matplotlib.pyplot as plt
from discord import ApplicationContext, Embed, SlashCommandOptionType
from discord.commands import Option
from discord.ext.pages import PageGroup, Paginator
from trackmania import (
    BestCOTDStats,
    InvalidIDError,
    Player,
    PlayerCOTD,
    PlayerCOTDResults,
    PlayerMetaInfo,
    PlayerZone,
    TMIOException,
)

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
        description="Gets the player and COTD details of a specific username",
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
        if username.lower() == "iridium_":
            # Temporary jank solution.
            player_id = "20acef53-a982-4bc3-989f-399e03c70f4d"
        else:
            player_id = await Player.get_id(username)
        page = 0
        pop_flag = True
        cotd_success = True

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

        log.debug("Creating Player Details Pages")
        pages = PlayerDetails.__create_pages(player_data)

        if isinstance(pages, str):
            await ctx.respond(pages)
            return

        try:
            log.debug("Getting COTD Data")
            cotd_stats = await PlayerCOTD.get_page(player_id, page)
        except TMIOException as e:
            log.error(f"Failed to get COTD Data: %s", e)
            cotd_success = False
            msg = f"TMIOException: {e}"
        except InvalidIDError as e:
            log.error(f"Failed to get COTD Data: %s", e)
            cotd_success = False
            msg = f"This player has never played Trackmania COTD."

        if cotd_success:
            log.debug("Creating COTD Details Pages")
            cotd_pages = PlayerDetails.__parse_pages(
                cotd_stats, username, PlayerDetails.__get_flag(player_data.zone)
            )

            log.debug("Popping COTDs")
            popped, original = PlayerDetails.__pop_reruns(cotd_stats.recent_results)

            while (len(popped) <= 25 and page < 5) or pop_flag:
                page += 1
                cotd_stats_new = await PlayerCOTD.get_page(player_id, page)

                _new_popped, _new_original = PlayerDetails.__pop_reruns(
                    cotd_stats_new.recent_results
                )
                popped.extend(_new_popped)
                original.extend(_new_original)

                pop_flag = False

            if len(popped) > 25:
                popped = popped[:25]
            if len(original) > 25:
                original = original[:25]

            log.debug("Creating COTD Graphs")
            PlayerDetails.__create_graphs(popped, original)

            log.debug("Sending Images to Channel")
            channel = self.bot.get_channel(962961137924726834)

            try:
                image_message = await channel.send(
                    files=[
                        discord.File("./bot/resources/temp/overall.png"),
                        discord.File("./bot/resources/temp/primary.png"),
                    ]
                )
            except Exception as e:
                log.error("An Unexpected error has occured: %s", e)
                await ctx.respond(
                    "An unexpected error has occured. Contact NottCurious#4351"
                )
                return

            log.debug("Getting Image URLs")
            url_one = image_message.attachments[0].url
            url_two = image_message.attachments[1].url

            cotd_pages[0].set_image(url=url_one)
            cotd_pages[1].set_image(url=url_two)
        else:
            cotd_pages = [
                Embed(
                    title="An Error Occured with the API",
                    description=f"An Unexpected Error Occured.\n{msg}.\nPlease Try Again Later. (And ping NottCurious#4351 if you think this is wrong).",
                )
            ]

        log.debug("Creating Page Group List")
        page_groups = [
            PageGroup(
                pages=pages,
                label="Player Details",
                description=f"Player Details of {username}",
            ),
            PageGroup(
                pages=cotd_pages,
                label="COTD Details",
                description=f"COTD Details of {username}",
            ),
        ]

        # Show Menu parameter creates the drop down menu needed to switch between the groups.
        log.debug("Running Paginator")
        paginator = Paginator(pages=page_groups, show_menu=True)
        await paginator.respond(ctx.interaction)
        log.debug("Paginator Finished")

    @staticmethod
    def __create_pages(player_data: Player) -> list[discord.Embed]:
        log.info(f"Creating PlayerDetail pages for {player_data.name}")
        display_name = player_data.name
        player_flag = PlayerDetails.__get_flag(player_data.zone)

        try:
            log.debug("Creating Strings to Use in the Pages.")
            zone_str = PlayerZone.to_string(player_data.zone)
        except TypeError:
            zone_str = ""

        log.debug("Getting Trophies String")
        trophy_str = str(player_data.trophies)

        matchmaking_str = str(player_data.m3v3_data)
        royal_str = str(player_data.royal_data)

        log.debug("Creating Embed Pages")

        if player_flag is not None:
            page_one = create_embed(
                f"Player Data for {player_flag} {display_name} - Page 1"
            )
            page_two = create_embed(
                f"Player Data for {player_flag} {display_name} - Page 2"
            )
            page_three = create_embed(
                f"Player Data for {player_flag} {display_name} - Page 3"
            )
        else:
            page_one = create_embed(f"Player Data for {display_name} - Page 1")
            page_two = create_embed(f"Player Data for {display_name} - Page 2")
            page_three = create_embed(f"Player Data for {display_name} - Page 3")

        log.debug("Adding Fields to Embed Pages")
        if zone_str != "":
            page_one.add_field(
                name="Zone Data", value=f"```{zone_str}```", inline=False
            )
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

        return [page_one, page_two, page_three]

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
    def __parse_pages(
        cotd_stats: PlayerCOTD, username: str, player_flag: str | None = None
    ) -> list[Embed]:
        log.info(f"Parsing Pages for {cotd_stats.player_id}")

        log.debug("Creating 2 Embeds")
        if player_flag is not None:
            page_one = create_embed(title=f"Overall Data for {player_flag} {username}")
            page_two = create_embed(title=f"Primary Data for {player_flag} {username}")
        else:
            page_one = create_embed(title=f"Overall Data for {username}")
            page_two = create_embed(title=f"Primary Data for {username}")

        log.debug("Adding Total COTDs Played")
        page_one.add_field(name="Total Played", value=cotd_stats.total, inline=False)
        page_two.add_field(name="Total Played", value=cotd_stats.total, inline=False)

        log.debug("Adding Average Data")
        average_data = PlayerDetails.__create_avg_data_str(cotd_stats)
        page_one.add_field(name="Average Stats", value=average_data, inline=False)
        page_two.add_field(name="Average Stats", value=average_data, inline=False)

        log.debug("Adding Best Stats")
        page_one = PlayerDetails.__parse_best_stats(
            page_one, cotd_stats.stats.best_overall
        )
        page_two = PlayerDetails.__parse_best_stats(
            page_two, cotd_stats.stats.best_primary
        )

        log.debug("Returning Embed Pages")
        return [page_one, page_two]

    @staticmethod
    def __parse_best_stats(page: discord.Embed, stats: BestCOTDStats):
        log.debug("Parsing Best Stats")
        temp_str = f"Best Division - {stats.best_div}\nBest Division Time Achieved -> {stats.best_div_time}\n\nBest Rank -> {stats.best_rank}\nRank Achieved in Division of Best Rank -> {stats.best_rank_div_rank}\nBest Rank - Time Achieved -> {stats.best_rank_time}\n\nBest Rank in Division -> {stats.best_rank_in_div}\nBest Rank in Division - Division Achived -> {stats.best_rank_in_div_div}\nBest Rank in Division - Time Achieved -> {stats.best_rank_in_div_time}"

        page.add_field(name="Best Stats", value=f"```\n{temp_str}\n```")

        return page

    @staticmethod
    def __pop_reruns(cotds: list[PlayerCOTDResults]) -> tuple[list[PlayerCOTDResults]]:
        popped = cotds
        temp = []

        for cotd in popped:
            if cotd.name.endswith("#1"):
                log.debug("Popping %s", cotd.name)
                temp.append(popped[popped.index(cotd)])

        return (temp, cotds)

    @staticmethod
    def __create_graphs(
        popped: list[PlayerCOTDResults], original: list[PlayerCOTDResults]
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

    @staticmethod
    def __get_flag(zones: list[PlayerZone] | None) -> str | None:
        try:
            if zones is None or zones is False:
                return None

            log.debug("Getting Flag")
            flags = [z.flag for z in zones]
            converted_flags = coco.convert(names=flags, to="ISO2")

            for the_flag in converted_flags:
                if the_flag.lower() != "not found":
                    return flag.flag(the_flag)

            return None
        except:
            # Catch unexpected errors
            log.error("Unexpected error finding the flag.")
            return None


def setup(bot: Bot):
    """Adds the PlayerDetails cog"""
    bot.add_cog(PlayerDetails(bot))
