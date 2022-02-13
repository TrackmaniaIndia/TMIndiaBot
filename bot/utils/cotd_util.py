import json
import os
import shutil
from datetime import datetime, timedelta, timezone

import cv2
import discord
import requests
from matplotlib import pyplot as plt

from bot.api import APIClient
from bot.log import get_logger
from bot.utils.commons import Commons
from bot.utils.discord import EZEmbed

log = get_logger(__name__)


class TOTDUtils:
    @staticmethod
    async def today(task_call: bool = False):
        log.debug("Checking if TOTD Data has already been saved for today")
        todays_day = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime(
            "%d"
        )
        todays_month = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime(
            "%B"
        )

        if os.path.exists("./bot/resources/json/totd.json"):
            log.debug("totd.json exists")
            with open("./bot/resources/json/totd.json", "r", encoding="UTF-8") as file:
                totd_data = json.load(file)

                log.debug("totd.json exists")
                if (
                    totd_data["Day"] == todays_day
                    and totd_data["Month"] == todays_month
                ):
                    log.debug("Taking TOTD Data from File")
                    return TOTDUtils.build_totd_embed_from_file()
        log.debug("Data in TOTD.json file is for wrong day")

        log.debug("Deleting totd.png")
        if os.path.exists("./bot/resources/temp/totd.png"):
            os.remove("./bot/resources/temp/totd.png")

        log.debug("Creating API Client")
        api_client = APIClient()
        log.debug("Created API Client")

        log.debug("Gathering TOTD Data")
        (
            map_name,
            author_name,
            thumbnail_url,
            download_link,
            map_uid,
            author_time,
            gold_time,
            silver_time,
            bronze_time,
            wr_holder,
            wr_time,
            nadeo_uploaded,
        ) = await TOTDUtils._gather_totd_tmio_data(api_client)

        log.debug("Gathering TMX Data")
        mania_tags, mx_uploaded, tmx_code = await TOTDUtils._gather_totd_tmx_data(
            api_client, map_uid
        )

        log.debug("Parsing TOTD Data")

        if task_call:
            todays_day += 1
        totd_data = {
            "Map Name": map_name,
            "Author": author_name,
            "Thumbnail URL": thumbnail_url,
            "Download Link": download_link,
            "UID": map_uid,
            "Author Time": author_time,
            "Gold Time": gold_time,
            "Silver Time": silver_time,
            "Bronze Time": bronze_time,
            "WR Holder": wr_holder,
            "WR Time": wr_time,
            "Nadeo Uploaded": nadeo_uploaded,
            "Mania Tags": mania_tags,
            "TMX Uploaded": mx_uploaded,
            "TMX Code": tmx_code,
            "Day": todays_day,
            "Month": todays_month,
        }

        log.debug("Saving TOTD Data")
        with open("./bot/resources/json/totd.json", "w", encoding="UTF-8") as file:
            json.dump(totd_data, file, indent=4)

        log.debug("Building TOTD Embed from File")
        try:
            await api_client.close()
        except:
            pass
        return TOTDUtils.build_totd_embed_from_file()

    @staticmethod
    def build_totd_embed_from_file():
        log.debug("Getting Data")
        with open("./bot/resources/json/totd.json", "r", encoding="UTF-8") as file:
            totd_data = json.load(file)

        log.debug("Building Embed")
        # Add Day Suffix
        # Add Day Suffix
        if int(totd_data["Day"]) % 10 == 1:
            day_suffix = "st"
        elif int(totd_data["Day"]) % 10 == 2:
            day_suffix = "nd"
        elif int(totd_data["Day"]) % 10 == 3:
            day_suffix = "rd"
        else:
            day_suffix = "th"

        embed = EZEmbed.create_embed(
            title=f"Here is the {totd_data['Day']}{day_suffix} {totd_data['Month']} TOTD",
            color=Commons.get_random_color(),
        )

        log.debug("Creating Image File")
        try:
            image = discord.File("./bot/resources/temp/totd.png", filename="totd.png")
        except FileNotFoundError:
            image = None
        embed.set_image(url="attachment://totd.png")
        embed.add_field(name="Map Name", value=totd_data["Map Name"], inline=False)
        embed.add_field(name="Author", value=totd_data["Author"], inline=True)

        if totd_data["Mania Tags"] is not None:
            embed.add_field(name="Tags", value=totd_data["Mania Tags"], inline=False)

        embed.add_field(
            name="Time Uploaded to Nadeo server",
            value=totd_data["Nadeo Uploaded"],
            inline=False,
        )

        if totd_data["TMX Uploaded"] is not None:
            embed.add_field(
                name="Time Uploaded to TMX server",
                value=totd_data["TMX Uploaded"],
                inline=True,
            )

        embed.add_field(
            name="Medal Times",
            value=f"Author: {totd_data['Author Time']}\nGold: {totd_data['Gold Time']}\nSilver: {totd_data['Silver Time']}\nBronze: {totd_data['Bronze Time']}",
            inline=False,
        )
        embed.add_field(
            name="World Record",
            value=f"{totd_data['WR Holder']} - {totd_data['WR Time']}",
            inline=False,
        )

        tmio_link = f"https://trackmania.io/#/leaderboard/{totd_data['UID']}"

        if totd_data["TMX Code"] is not None:
            return (
                embed,
                image,
                totd_data["Download Link"],
                tmio_link,
                f"https://trackmania.exchange/maps/{totd_data['TMX Code']}",
            )
        else:
            return embed, image, totd_data["Download Link"], tmio_link, None

    @staticmethod
    async def _gather_totd_tmio_data(api_client: APIClient) -> tuple:
        log.debug("Pinging API")
        raw_totd_data = await api_client.get("http://localhost:3000/tm2020/totd/latest")

        map_name = raw_totd_data["name"]
        author_name = raw_totd_data["authorplayer"]["name"]
        thumbnail_url = raw_totd_data["thumbnailUrl"]
        map_uid = raw_totd_data["mapUid"]

        author_time = Commons.format_seconds(int(raw_totd_data["authorScore"]))
        gold_time = Commons.format_seconds(int(raw_totd_data["goldScore"]))
        silver_time = Commons.format_seconds(int(raw_totd_data["silverScore"]))
        bronze_time = Commons.format_seconds(int(raw_totd_data["bronzeScore"]))

        wr_holder = raw_totd_data["leaderboard"]["tops"][0]["player"]["name"]
        wr_time = Commons.format_seconds(
            int(raw_totd_data["leaderboard"]["tops"][0]["time"])
        )

        nadeo_uploaded = f"<t:{int(datetime.strptime(raw_totd_data['timestamp'][:-6], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc).timestamp())}:R>"

        download_link = raw_totd_data["thumbnailUrl"]
        TOTDUtils._download_thumbail(download_link)

        log.debug("Returning TMIO Data")
        return (
            map_name,
            author_name,
            thumbnail_url,
            download_link,
            map_uid,
            author_time,
            gold_time,
            silver_time,
            bronze_time,
            wr_holder,
            wr_time,
            nadeo_uploaded,
        )

    @staticmethod
    async def _gather_totd_tmx_data(api_client: APIClient, map_uid: str) -> tuple:
        log.debug("Pinging TMX API")

        try:
            raw_tmx_data = await api_client.get(
                f"https://trackmania.exchange/api/maps/get_map_info/uid/{map_uid}"
            )
        except:
            await api_client.close()
            return None, None, None
        try:
            mania_tags = raw_tmx_data["Tags"]
            mx_uploaded = raw_tmx_data["UploadedAt"]
            tmx_code = raw_tmx_data["TrackID"]

            try:
                mx_dt = datetime.strptime(mx_uploaded[:-3], "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                mx_dt = datetime.strptime(mx_uploaded[:-4], "%Y-%m-%dT%H:%M:%S")

            mx_timestamps = mx_dt.replace(tzinfo=timezone.utc).timestamp()
            mx_uploaded = f"<t:{int(mx_timestamps)}:R>"
        except BaseException:
            log.critical("Map has never been uploaded to trackmania.exchange")
            return None, None, None

        return mania_tags, mx_uploaded, tmx_code

    @staticmethod
    def _download_thumbail(url: str) -> None:
        """Downloads the Thumbnail from Nadeo's API and stores in `./bot/resources/temp/totd.png`"""
        log.debug("Downloading Thumbnail")
        # if os.path.exists("./bot/resources/temp/totd.png"):
        #     log.debug("Thumbnail already downloaded")
        #     return

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
    def _parse_mx_tags(tags: str) -> str:
        """Parses Maniaexchange tags to their strings

        Args:
                tags (str): The tags as a string of `ints`

        Returns:
                str: The tags as a string of `strings`
        """
        log.debug(f"Tags -> {tags}")
        log.debug("Removing Spaces")
        # tags.replace(" ", "")
        log.debug(f"Without Spaces -> {tags}")

        tags = tags.split(",")

        tag_string = ""

        with open("./bot/resources/json/mxtags.json", "r", encoding="UTF-8") as file:
            mxtags = json.load(file)["mx"]

            for i, tag in enumerate(tags):
                log.debug(f"Converting {tag}")

                for j in range(len(mxtags)):
                    if int(tag) == int(mxtags[j]["ID"]):
                        tag_string = tag_string + mxtags[j]["Name"] + ", "

        log.debug(f"Tag String -> {tag_string}")
        return tag_string[:-2]


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
