import asyncio
import json

import discord

from bot.api import APIClient
from bot.log import get_logger
from bot.utils.commons import Commons
from bot.utils.discord import EZEmbed

log = get_logger(__name__)


class Leaderboards:
    @staticmethod
    def get_campaign_ids(year: str = "2021", season: str = "Fall") -> list[str]:
        """Gets a list of all campaign ids for a given year and season
        Args:
                year (str, optional): The year of the season. Defaults to "2021".
                season (str, optional): The season itself. Defaults to "Fall".
        Returns:
                list[str]: List of ids
        """
        log.debug(f"Opening {year}/{season.lower()} Data File")

        with open(
            f"./bot/resources/json/campaign/{year}/{season.lower()}.json",
            "r",
            encoding="UTF-8",
        ) as file:
            file_data = json.load(file)
            id_list = file_data["ids"]

        log.debug("Not Ignoring First Five Maps")
        return id_list

    @staticmethod
    async def update_campaign_leaderboards(
        id_list: list[str],
        year: str = "2021",
        season: str = "Fall",
        skip_first_five: bool = False,
    ):
        """Updates the leaderboard files for the campaign
        Args:
                id_list (list[str]): Campaign map id list
                year (str, optional): The year of the season. Defaults to "2021"
                season (str, optional): The season itself. Defaults to "Fall".
        """
        log.info("Creating APIClient for Updating Campaign Leaderboards")
        api_client = APIClient()
        log.info("Created APIClient for Updating Campaign Leaderboards")

        for i, id in enumerate(id_list):
            leaderboard_data = []

            log.debug(f"Getting Data from API for Map {i}")
            leaderboard_data = await api_client.get(
                f"http://localhost:3000/tm2020/leaderboard/{id}/5"
            )
            log.debug("Got Data from API")

            with open(
                f"./bot/resources/leaderboard/{year}/{season.lower()}/{i + 1}.json",
                "w",
                encoding="UTF-8",
            ) as file:
                log.debug(f"Dumping Data to File -> {year}>{season}>{i + 1}")
                json.dump(leaderboard_data, file, indent=4)

            log.debug("Sleeping for 10s")
            # time.sleep(10)
            await asyncio.sleep(20)
            log.debug(f"Finished Map #{i + 1}")

        await api_client.close()

    @staticmethod
    def get_player_list(map_no: str, year: str = "2021", season: str = "Fall"):
        log.debug(f"Opening File, Map No -> {map_no}")

        with open(
            f"./bot/resources/leaderboard/{year}/{season.lower()}/{map_no}.json",
            "r",
            encoding="UTF-8",
        ) as file:
            data = json.load(file)

        player_list = []

        log.debug("Appending Players")
        for player in data:
            player_list.append((player["player"]["name"], player["position"]))

        return player_list

    @staticmethod
    def get_player_good_maps(
        player_name: str, year: str = "2021", season: str = "Fall"
    ) -> discord.Embed:
        log.debug(f"Getting Player Details for Player name -> {player_name}")

        player_embed = EZEmbed.create_embed(
            title=f"{player_name} is good at the following maps",
            color=Commons.get_random_color(),
        )

        t100_str, t200_str, t300_str, t400_str, t500_str = "", "", "", "", ""
        for i in range(6, 26, 1):
            player_list = Leaderboards.get_player_list(str(i), year, season.lower())

            for player_tuple in player_list:
                if player_tuple[0].lower() == player_name.lower():
                    if int(player_tuple[1]) <= 100:
                        log.debug(f"{player_name} is a top 100 player for Map {i}")
                        t100_str = (
                            t100_str + str(i) + " - " + str(player_tuple[1]) + "\n"
                        )
                    elif int(player_tuple[1]) <= 200 and int(player_tuple[1]) > 100:
                        log.debug(f"{player_name} is a top 200 player for Map {i}")
                        t200_str = (
                            t200_str + str(i) + " - " + str(player_tuple[1]) + "\n"
                        )
                    elif int(player_tuple[1]) <= 300 and int(player_tuple[1]) > 200:
                        log.debug(f"{player_name} is a top 300 player for Map {i}")
                        t300_str = (
                            t300_str + str(i) + " - " + str(player_tuple[1]) + "\n"
                        )
                    elif int(player_tuple[1]) <= 400 and int(player_tuple[1]) > 300:
                        log.debug(f"{player_name} is a top 400 player for Map {i}")
                        t400_str = (
                            t400_str + str(i) + " - " + str(player_tuple[1]) + "\n"
                        )
                    elif int(player_tuple[1]) <= 500 and int(player_tuple[1]) > 400:
                        log.debug(f"{player_name} is a top 500 player for Map {i}")
                        t500_str = (
                            t500_str + str(i) + " - " + str(player_tuple[1]) + "\n"
                        )

        if t100_str != "":
            log.debug(f"Appending T100 String for {player_name}")
            player_embed.add_field(
                name="**Top 100**", value="```" + t100_str + "```", inline=False
            )
        else:
            log.debug("Player does not have any top 100 ranks")
            player_embed.add_field(
                name="**Top 100**",
                value="Player does not have any top 100 times for maps 06-25",
                inline=False,
            )

        if t200_str != "":
            log.debug(f"Appending Top 100 String for {player_name}")
            player_embed.add_field(
                name="**Top 200**", value="```" + t200_str + "```", inline=False
            )
        else:
            log.debug("Player does not have any top 200 ranks")
            player_embed.add_field(
                name="**Top 200**",
                value="Player does not have any top 200 times for maps 06-25",
                inline=False,
            )

        if t300_str != "":
            log.debug(f"Appending Top 100 String for {player_name}")
            player_embed.add_field(
                name="**Top 300**", value="```" + t300_str + "```", inline=False
            )
        else:
            log.debug("Player does not have any top 300 ranks")
            player_embed.add_field(
                name="**Top 300**",
                value="Player does not have any top 300 times for maps 06-25",
                inline=False,
            )

        if t400_str != "":
            log.debug(f"Appending Top 100 String for {player_name}")
            player_embed.add_field(
                name="**Top 400**", value="```" + t400_str + "```", inline=False
            )
        else:
            log.debug("Player does not have any top 400 ranks")
            player_embed.add_field(
                name="**Top 400**",
                value="Player does not have any top 400 times for maps 06-25",
                inline=False,
            )

        if t500_str != "":
            log.debug(f"Appending Top 100 String for {player_name}")
            player_embed.add_field(
                name="**Top 500**", value="```" + t500_str + "```", inline=False
            )
        else:
            log.debug("Player does not have any top 500 ranks")
            player_embed.add_field(
                name="**Top 500**",
                value="Player does not have any top 500 times for maps 06-25",
                inline=False,
            )

        return player_embed

    @staticmethod
    def get_world_records(year: str = "2021", season: str = "Fall"):
        log.debug(f"Getting World Records for {season} {year}")

        log.debug("Creating Embeds")
        white_maps = EZEmbed.create_embed(
            title="World Records for White Maps", color=0xFFFFFF
        )
        green_maps = EZEmbed.create_embed(
            title="World Records for Green Maps", color=0x00FF00
        )
        blue_maps = EZEmbed.create_embed(
            title="World Records for Blue Maps", color=0x0000FF
        )
        red_maps = EZEmbed.create_embed(
            title="World Records for Red Maps", color=0xFF0000
        )
        black_maps = EZEmbed.create_embed(
            title="World Records for Black Maps", color=0x000000
        )

        maps = (white_maps, green_maps, blue_maps, red_maps, black_maps)
        map_colors = ("white", "green", "blue", "red", "black")

        log.debug("Looping Through Maps")
        for i in range(0, 5):
            log.debug(f"Adding {map_colors[i]} Records")
            for j in range(0, 5):
                with open(
                    f"./bot/resources/leaderboard/{year}/{season.lower()}/{(i * 5) + j + 1}.json",
                    "r",
                    encoding="UTF-8",
                ) as file:
                    leaderboard_data = json.load(file)
                    wr_holder = leaderboard_data[0]

                    username = f'{wr_holder["player"]["name"]}'
                    value = f'Map No: {(i * 5) + j + 1}\nTime: {Commons.format_seconds(wr_holder["time"])}'
                    maps[i].add_field(name=username, value=value, inline=False)

        log.debug("Returning Maps")
        return maps
