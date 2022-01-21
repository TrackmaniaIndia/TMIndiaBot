import json
import os
import shutil
from datetime import datetime, timezone, timedelta

import cv2
import requests
from matplotlib import pyplot as plt
import discord

from bot.api import APIClient
from bot.log import get_logger
from bot.utils.commons import Commons
from bot.utils.discord import EZEmbed

log = get_logger(__name__)


class TOTDUtils:
    @staticmethod
    def _download_thumbail(url: str) -> None:
        """Downloads the Thumbnail from Nadeo's API and stores in `./bot/resources/temp/totd.png`"""
        if os.path.exists("./bot/resources/temp/totd.png"):
            log.debug("Thumbnail already downloaded")
            return

        req = requests.get(url, stream=True)

        if req.status_code == 200:
            log.debug("Image was retrieved succesfully")
            req.raw.decode_content = True

            log.debug("Saving Image to File")
            with open("./bot/resources/temp/totd.png", "wb") as file:
                shutil.copyfileobj(req.raw, file)
        else:
            log.critical("Image could not be retrieved")

    @staticmethod
    def _parse_mx_tags(self, tags: str) -> str:
        """Parses Maniaexchange tags to their strings

        Args:
                tags (str): The tags as a string of `ints`

        Returns:
                str: The tags as a string of `strings`
        """
        log.debug(f"Tags -> {tags}")
        log.debug("Removing Spaces")
        tags.replace(" ", "")
        log.debug(f"Without Spaces -> {tags}")

        tags = tags.split(",")

        tag_string = ""

        with open("./bot/resources/json/mxtags.json", "r") as file:
            mxtags = json.load(file)["mx"]

            for i, tag in enumerate(tags):
                log.debug(f"Converting {tag}")

                for j in range(len(mxtags)):
                    if int(tag) == int(mxtags[j]["ID"]):
                        tag_string = tag_string + mxtags[j]["Name"] + ", "

        log.debug(f"Tag String -> {tag_string}")
        return tag_string[:-2]

    @staticmethod
    async def today():
        """The data of the current day's totd"""
        log.info("Creating an API Client")
        api_client = APIClient()
        log.info("Created an API Client")

        log.debug("Getting TOTD Data from API")
        totd_data = await api_client.get("http://localhost:3000/tm2020/totd/latest")

        log.debug("Parsing TOTD Data")
        map_name = totd_data["name"]
        author_name = totd_data["authorplayer"]["name"]
        thumbnail_url = totd_data["thumbnailUrl"]

        author_time = Commons.format_seconds(int(totd_data["authorScore"]))
        gold_time = Commons.format_seconds(int(totd_data["goldScore"]))
        silver_time = Commons.format_seconds(int(totd_data["silverScore"]))
        bronze_time = Commons.format_seconds(int(totd_data["bronzeScore"]))

        nadeo_uploaded = totd_data["timestamp"]

        wr_holder = totd_data["leaderboard"]["tops"][0]["player"]["name"]
        wr_time = Commons.format_seconds(
            int(totd_data["leaderboard"]["tops"][0]["time"])
        )

        tmio_id = totd_data["mapUid"]
        log.debug("Parsed TOTD Data")

        log.debug("Parsing Download Link")
        download_link = totd_data["fileUrl"]
        log.debug("Parsed Download Link")

        log.debug("Parsing Time Uploaded to Timestamp")
        nadeo_timestamp = (
            datetime.strptime(nadeo_uploaded[:-6], "%Y-%m-%dT%H:%M:%S")
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )
        log.debug("Parsed Time Uploaded to Timestamps")

        log.debug("Creating Strings from Parsed Data")
        medal_times = f"<:author:894268580902883379> {author_time}\n<:gold:894268580970004510> {gold_time}\n<:silver:894268580655411220> {silver_time}\n<:bronze:894268580181458975> {bronze_time}"
        world_record = f"Holder: {wr_holder}\nTime: {wr_time}"

        nadeo_uploaded = f"<t:{int(nadeo_timestamp)}:R>"

        log.debug("Created Strings from Parsed Data")

        log.debug(
            "Getting Map Thumbnail\nChecking if map Thumbnail has Already been Downloaded"
        )

        if not os.path.exists("./bot/resources/temp/totd.png"):
            log.critical("Map Thumbail has not been downloaded")
            TOTDUtils._download_thumbail(thumbnail_url)

        log.debug("Parsing TM Exchange Data")
        try:
            mania_tags = totd_data["exchange"]["Tags"]
            mx_uploaded = totd_data["exchange"]["UploadedAt"]
            tmx_code = totd_data["exchange"]["TrackID"]

            try:
                mx_dt = datetime.strptime(mx_uploaded[:-3], "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                mx_dt = datetime.strptime(mx_uploaded[:-4], "%Y-%m-%dT%H:%M:%S")

            mx_timestamps = mx_dt.replace(tzinfo=timezone.utc).timestamp()
            mx_uploaded = f"<t:{int(mx_timestamps)}:R>"
        except BaseException:
            log.critical("Map has never been uploaded to trackmania.exchange")

        log.debug("Creating Embed")
        current_day = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime(
            "%d"
        )
        current_month = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime(
            "%B"
        )

        # Add Day Suffix
        if int(current_day) % 10 == 1:
            day_suffix = "st"
        elif int(current_day) % 10 == 2:
            day_suffix = "nd"
        elif int(current_day) % 10 == 3:
            day_suffix = "rd"
        else:
            day_suffix = "th"

        embed = EZEmbed.create_embed(
            title=f"Here is the {current_day}{day_suffix} {current_month} TOTD",
            color=Commons.get_random_color(),
        )
        log.debug("Creating Image File")
        image = discord.File("./bot/resources/temp/totd.png", filename="totd.png")
        embed.set_image(url="attachment://totd.png")
        embed.add_field(name="Map Name", value=map_name, inline=False)
        embed.add_field(name="Author", value=author_name, inline=True)

        try:
            embed.add_field(
                name="Tags", value=TOTDUtils._parse_mx_tags(mania_tags), inline=False
            )
        except BaseException:
            pass

        embed.add_field(
            name="Time Uploaded to Nadeo server", value=nadeo_uploaded, inline=False
        )

        try:
            embed.add_field(name="Time Uploaded to TMX", value=mx_uploaded, inline=True)
        except BaseException:
            pass

        embed.add_field(name="Medal Times", value=medal_times, inline=False)
        embed.add_field(name="Word record", value=world_record, inline=False)

        tmio_link = f"https://trackmania.io/#/leaderboard/{tmio_id}"

        try:
            tmx_link = f"https://trackmania.exchange/maps/{tmx_code}/"
        except BaseException:
            tmx_link = None

        log.debug("Created Embed")

        log.info("Closing the API Client")
        await api_client.close()
        log.info("Closed the API Embed")

        return embed, image, download_link, tmio_link, tmx_link


class COTDUtil:
    @staticmethod
    def get_best_rank_primary(cotd_data) -> int:
        log.debug(
            "Getting Best Primary Best Rank -> {}".format(
                cotd_data["stats"]["bestprimary"]["bestrank"]
            )
        )
        return cotd_data["stats"]["bestprimary"]["bestrank"]

    @staticmethod
    def get_best_div_primary(cotd_data) -> int:
        log.debug(
            "Getting Primary Best Div -> {}".format(
                cotd_data["stats"]["bestprimary"]["bestdiv"]
            )
        )
        return cotd_data["stats"]["bestprimary"]["bestdiv"]

    @staticmethod
    def get_best_rank_primary_time(cotd_data) -> int:
        log.debug(
            "Getting the time of Primary Best -> {}".format(
                cotd_data["stats"]["bestprimary"]["bestranktime"]
            )
        )
        return cotd_data["stats"]["bestprimary"]["bestranktime"]

    @staticmethod
    def get_best_div_primary_time(cotd_data) -> int:
        log.debug(
            "Getting the time of Primary Best Div -> {}".format(
                cotd_data["stats"]["bestprimary"]["bestdivtime"]
            )
        )
        return cotd_data["stats"]["bestprimary"]["bestdivtime"]

    @staticmethod
    def get_best_div_rank_primary(cotd_data) -> int:
        log.debug(
            "Getting the Best Rank in Div -> {}".format(
                cotd_data["stats"]["bestprimary"]["bestrankindiv"]
            )
        )
        return cotd_data["stats"]["bestprimary"]["bestrankindiv"]

    @staticmethod
    def get_best_rank_overall(cotd_data) -> int:
        log.debug(
            "Getting the Overall Best Rank -> {}".format(
                cotd_data["stats"]["bestoverall"]["bestrank"]
            )
        )
        return cotd_data["stats"]["bestoverall"]["bestrank"]

    @staticmethod
    def get_best_div_overall(cotd_data) -> int:
        log.debug(
            "Getting the Overall Best Div -> {}".format(
                cotd_data["stats"]["bestoverall"]["bestdiv"]
            )
        )
        return cotd_data["stats"]["bestoverall"]["bestdiv"]

    @staticmethod
    def get_best_rank_overall_time(cotd_data) -> int:
        log.debug(
            f'Getting the time of Overall Best Rank -> {cotd_data["stats"]["bestoverall"]["bestranktime"]}'
        )
        return cotd_data["stats"]["bestoverall"]["bestranktime"]

    @staticmethod
    def get_best_div_overall_time(cotd_data) -> int:
        log.debug(
            "Getting the time of Overall Best Div -> {}".format(
                cotd_data["stats"]["bestoverall"]["bestdivtime"]
            )
        )
        return cotd_data["stats"]["bestoverall"]["bestdivtime"]

    @staticmethod
    def get_best_div_rank_overall(cotd_data) -> int:
        log.debug(
            "Getting the Best Rank in Div Overall -> {}".format(
                cotd_data["stats"]["bestoverall"]["bestrankindiv"]
            )
        )
        return cotd_data["stats"]["bestoverall"]["bestrankindiv"]

    @staticmethod
    def return_cotds(cotd_data):
        log.debug("Returning all COTDs")
        return cotd_data["cotds"]

    @staticmethod
    def return_cotds_without_reruns(cotd_data):
        log.debug("Returning COTDs without reruns")
        cotds_safe = []

        for cotd in cotd_data["cotds"]:
            if "#2" in cotd["name"] or "#3" in cotd["name"]:
                continue
            cotds_safe.append(cotd)

        return cotds_safe

    @staticmethod
    def get_num_cotds_played(cotds):
        log.debug(f"Number of COTDs Played -> {len(cotds)}")
        return len(cotds)

    @staticmethod
    def remove_unfinished_cotds(cotds):
        log.debug("Looping around COTDs")
        cotds_safe = []

        for cotd in cotds:
            if not cotd["score"] == 0:
                cotds_safe.append(cotd)

        log.debug(f"{len(cotds_safe)} COTDs Finished out of Given Set")
        return cotds_safe

    @staticmethod
    def get_average_rank_overall(cotd_data):
        cotds = COTDUtil.return_cotds(cotd_data)

        cotds_played = COTDUtil.get_num_cotds_played(cotds)

        rank_total = 0

        # Looping Through COTDs
        for cotd in cotds:
            rank_total += int(cotd["rank"])

        log.debug(f"Average Rank Overall -> {round(rank_total / cotds_played, 2)}")
        return round(rank_total / cotds_played, 2)

    @staticmethod
    def get_average_rank_primary(cotd_data):
        cotds = COTDUtil.return_cotds_without_reruns(cotd_data)

        cotds_played = COTDUtil.get_num_cotds_played(cotds)

        rank_total = 0

        for cotd in cotds:
            rank_total += int(cotd["rank"])

        try:
            log.debug(f"Average Rank Primary -> {round(rank_total / cotds_played, 2)}")
            return round(rank_total / cotds_played, 2)
        except BaseException:
            log.debug("Average Rank Primary -> 0")
            return 0

    @staticmethod
    def get_average_div_overall(cotd_data):
        cotds = COTDUtil.return_cotds(cotd_data)

        cotds_played = COTDUtil.get_num_cotds_played(cotds)

        div_total = 0

        # Looping Through COTDs
        for cotd in cotds:
            div_total += int(cotd["div"])

        log.debug(f"Average Div Overall -> {round(div_total / cotds_played, 2)}")
        return round(div_total / cotds_played, 2)

    @staticmethod
    def get_average_div_primary(cotd_data):
        cotds = COTDUtil.return_cotds_without_reruns(cotd_data)

        cotds_played = COTDUtil.get_num_cotds_played(cotds)

        div_total = 0

        for cotd in cotds:
            div_total += int(cotd["div"])

        try:
            log.debug(f"Average Div Primary -> {round(div_total / cotds_played, 2)}")
            return round(div_total / cotds_played, 2)
        except BaseException:
            log.debug("Average Div Primary -> 0")
            return 0

    @staticmethod
    def get_average_div_rank_overall(cotd_data):
        cotds = COTDUtil.return_cotds(cotd_data)

        cotds_played = COTDUtil.get_num_cotds_played(cotds)

        div_rank_total = 0

        for cotd in cotds:
            div_rank_total += int(cotd["div"])

        log.debug(
            f"Average Div Rank Overall -> {round(div_rank_total / cotds_played, 2)}"
        )
        return round(div_rank_total / cotds_played, 2)

    @staticmethod
    def get_average_div_rank_primary(cotd_data):
        cotds = COTDUtil.return_cotds_without_reruns(cotd_data)

        cotds_played = COTDUtil.get_num_cotds_played(cotds)

        div_rank_total = 0

        for cotd in cotds:
            div_rank_total += int(cotd["divrank"])

        try:
            log.debug(
                f"Average Div Rank Primary -> {round(div_rank_total / cotds_played, 2)}"
            )
            return round(div_rank_total / cotds_played, 2)
        except BaseException:
            log.debug("Average Div Rank Primary -> 0")
            return 0

    @staticmethod
    def get_list_of_ranks_overall(cotd_data):
        cotds = COTDUtil.return_cotds(cotd_data)
        cotds = COTDUtil.remove_unfinished_cotds(cotds)

        ranks = []

        for cotd in cotds:
            ranks.append(cotd["rank"])

        log.debug(f"Ranks are {ranks[::-1]}")
        return ranks[::-1]

    @staticmethod
    def get_list_of_ranks_primary(cotd_data):
        cotds = COTDUtil.return_cotds_without_reruns(cotd_data)
        cotds = COTDUtil.remove_unfinished_cotds(cotds)

        ranks = []

        for cotd in cotds:
            ranks.append(cotd["rank"])

        log.debug(f"Ranks are {ranks[::-1]}")
        return ranks[::-1]

    @staticmethod
    def get_list_of_dates_overall(cotd_data):
        cotds = COTDUtil.return_cotds(cotd_data)
        cotds = COTDUtil.remove_unfinished_cotds(cotds)

        timestamps = []

        for cotd in cotds:
            timestamps.append(cotd["name"][15:])

        log.debug(f"Timestamps are {timestamps[::-1]}")
        return timestamps[::-1]

    @staticmethod
    def get_list_of_dates_primary(cotd_data):
        cotds = COTDUtil.return_cotds_without_reruns(cotd_data)
        cotds = COTDUtil.remove_unfinished_cotds(cotds)

        timestamps = []

        for cotd in cotds:
            timestamps.append(cotd["name"][15:])

        log.debug(f"Timestamps are {timestamps[::-1]}")
        return timestamps[::-1]

    @staticmethod
    def get_list_of_ids_overall(cotd_data):
        cotds = COTDUtil.return_cotds(cotd_data)
        cotds = COTDUtil.remove_unfinished_cotds(cotds)

        ids = []

        for cotd in cotds:
            ids.append(cotd["id"])

        log.debug(f"IDs are {ids[::-1]}")
        return ids[::-1]

    @staticmethod
    def get_list_of_ids_primary(cotd_data):
        cotds = COTDUtil.return_cotds_without_reruns(cotd_data)
        cotds = COTDUtil.remove_unfinished_cotds(cotds)

        ids = []

        for cotd in cotds:
            ids.append(cotd["id"])

        log.debug(f"IDs are {ids[::-1]}")
        return ids[::-1]

    @staticmethod
    def get_num_wins(cotd_data):
        log.debug(
            "Getting number of wins -> {}".format(cotd_data["stats"]["totalwins"])
        )
        return cotd_data["stats"]["totalwins"]

    @staticmethod
    def _create_rank_plot(
        ranks: list, dates: list, ids: list, plot_name: str, image_name: str
    ):
        log.debug("Clearing Plot")
        plt.clf()

        if len(dates) >= 40:
            log.debug(
                f"{plot_name} -> Player has played more than 40 COTDs, using ids instead of dates"
            )
            plt.plot(ids, ranks, label=plot_name)
            plt.xlabel("COTD IDs")
        else:
            log.debug(
                f"{plot_name} -> Player has less than 40 COTDs, using dates instead of ids"
            )
            plt.plot(dates, ranks, label=plot_name)
            plt.xlabel("COTD Dates")

        log.debug(f"{plot_name} -> Setting Plot Rotation to 90Deg")
        plt.xticks(rotation=90)

        log.debug(f"{plot_name} -> Setting YLabel to Ranks")
        plt.ylabel("Ranks")

        log.debug(f"{plot_name} -> Setting title to {plot_name}")
        plt.title(f"Rank Graph for {plot_name}")

        log.debug(f"{plot_name} -> Setting Tight Layout")
        plt.tight_layout()

        log.debug(f"{plot_name} -> Saving the Plot to Computer")
        plt.savefig("./bot/resources/temp/" + image_name)

    @staticmethod
    def _concat_graphs():
        log.info("Concatenating Graphs")
        log.debug("Opening First Graph")
        first_graph = cv2.imread("./bot/resources/temp/overallranks.png")
        log.debug("First Graph Opened")
        log.debug("Opening Second Graph")
        second_graph = cv2.imread("./bot/resources/temp/primaryranks.png")
        log.debug("Second Graph Opened")

        log.debug("Concatenating Graphs")
        concatenated_graphs = cv2.hconcat([first_graph, second_graph])
        log.debug("Concatenated Graphs")

        log.info("Saving Graphs")
        cv2.imwrite("./bot/resources/temp/concatenated_graphs.png", concatenated_graphs)
