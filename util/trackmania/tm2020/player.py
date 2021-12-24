import json
import discord
import requests
import flag
from util import common_functions
from util.logging import convert_logging
import util.discord.easy_embed as ezembed
import country_converter as coco


log = convert_logging.get_logging()
base_api_url = "http://localhost:3000"


def get_player_id(username: str) -> str:
    """
    Grabs player id for given username from api

    Args:
        username (str): The username of the player

    Returns:
        str: the player id
    """
    # Checking the File
    log.debug("Checking if Player ID is already stored in the file")
    username_list = _get_username_list()

    if username.lower() in username_list:
        log.debug("Username is stored in the file")
        id_list = _get_username_id_list()

        log.debug(
            f"{username}'s ID is {id_list[username_list.index(username.lower())]}"
        )
        return id_list[username_list.index(username.lower())]

    log.debug(f"Getting Player ID for {username}")
    player_data = requests.get(f"{base_api_url}/tm2020/player/{username}/id").json()
    log.debug("Received Player Data, Parsing")
    try:
        player_id = player_data["id"]
    except:
        player_id = None
    log.debug(f"Player ID is {player_id}")
    return player_id


def get_player_data(player_id: str) -> list[discord.Embed]:
    log.debug(f"Getting Data for {player_id}")
    raw_player_data = requests.get(
        f"http://localhost:3000/tm2020/player/{player_id}/"
    ).json()

    log.debug("Getting Player Flag Unicode")
    player_flag_unicode = get_player_country_flag(raw_player_data)
    log.debug(f"Got Player Unicode Flag -> {player_flag_unicode}")

    display_name = raw_player_data["displayname"]
    log.debug(f"Display Name is {display_name}")

    log.debug("Checking if Player has Played the Game")
    if raw_player_data["trophies"]["points"] == 0:
        return [
            ezembed.create_embed(
                title=f"{player_flag_unicode} {display_name} has never played Trackmania2020",
                color=0xFF0000,
            )
        ]

    log.debug("Creating Two Embeds")
    page_one = ezembed.create_embed(
        title=f"Player Data for {player_flag_unicode} {display_name} - Page 1",
        color=common_functions.get_random_color(),
    )
    page_two = ezembed.create_embed(
        title=f"Player Data for {player_flag_unicode} {display_name} - Page 2",
        color=common_functions.get_random_color(),
    )
    page_three = ezembed.create_embed(
        title=f"Player Data for {player_flag_unicode} {display_name} - Page 3",
        color=common_functions.get_random_color(),
    )

    zones, zone_ranks = get_zones_and_positions(raw_player_data)
    royal_data = get_royal_data(raw_player_data)
    matchmaking_data = get_matchmaking_data(raw_player_data)
    trophy_count = get_trophy_count(raw_player_data)

    log.debug("Adding Zones and Zone Ranks to Page One")
    page_one.add_field(name="Zones", value=zones, inline=False)
    page_one.add_field(name="Zone Ranks", value=zone_ranks, inline=False)

    log.debug("Adding Matchmaking and Royal Data to Page Two")
    page_two.add_field(name="Matchmaking", value=matchmaking_data, inline=False)
    page_two.add_field(name="Royal", value=royal_data, inline=False)

    log.debug("Adding Trophy Count to Page Three")
    page_three.add_field(name="Trophy Count", value=trophy_count, inline=False)

    try:
        log.debug("Adding Meta Data to Page One")
        page_one = add_meta_details(page_one, raw_player_data)
        log.debug("Added Meta Data to Page One")
    except:
        log.debug("Player does not Have Meta Data")
    log.debug(f"Returning {page_one}, {page_two} and {page_three}")
    return [page_one, page_two, page_three]


def get_player_country_flag(raw_data):
    log.debug("Getting Zones")
    try:
        zone_one = raw_data["trophies"]["zone"]["name"]
        zone_two = raw_data["trophies"]["zone"]["parent"]["name"]

        log.debug(f"Zones are -> {zone_one} and {zone_two}")
        continents = (
            "Asia",
            "Middle East",
            "Europe",
            "North America",
            "South America",
            "Africa",
        )

        if zone_two in continents:
            log.debug("Only First Zone is Required")
            iso_letters = coco.convert(names=[zone_one], to="ISO2")
            unicode_letters = flag.flag(iso_letters)
        else:
            log.debug("Need to Use Zone Two")
            iso_letters = coco.convert(names=[zone_two], to="ISO2")
            unicode_letters = flag.flag(iso_letters)

        log.debug(f"Unicode Letters are {unicode_letters}")
        return unicode_letters
    except:
        log.error("Player has never played Trackmania 2020")
        return ":flag_white:"


def get_royal_data(raw_data) -> str:
    log.debug("Getting Royal Data")
    try:
        royal_data = raw_data["matchmaking"][1]

        rank = royal_data["info"]["rank"]
        wins = royal_data["info"]["progression"]
        current_division = royal_data["info"]["division"]["position"]

        if wins != 0:
            progression_to_next_div = (
                round(
                    (wins - royal_data["info"]["division"]["minwins"])
                    / (
                        royal_data["info"]["division"]["maxwins"]
                        - royal_data["info"]["division"]["minwins"]
                        + 1
                    ),
                    4,
                )
                * 100
            )
        else:
            log.debug("Player Has Not Won a Single Match")
            progression_to_next_div = "0"
        log.debug(
            f"Creating Royal Data String With {rank}, {wins}, {current_division}, {progression_to_next_div}"
        )
        royal_data_string = f"```Rank: {rank}\nWins: {wins}\nCurrent Division: {current_division}\nProgression to Next Division: {progression_to_next_div}%```"

        log.debug(f"Created Royal Data String -> {royal_data_string}")
        return royal_data_string
    except:
        return "An Error Occured While Getting Royal Data, Player has not played Royal"


def get_matchmaking_data(raw_data) -> str:
    log.debug("Getting Matchmaking Data")

    try:
        matchmaking_data = raw_data["matchmaking"][0]

        rank = matchmaking_data["info"]["rank"]
        score = matchmaking_data["info"]["score"]
        current_division_int = matchmaking_data["info"]["division"]["position"]

        with open("./data/json/mm_ranks.json", "r", encoding="UTF-8") as file:
            mm_ranks = json.load(file)
            current_division = mm_ranks["rank_data"][str(current_division_int - 1)]

        progression_to_next_div = (
            round(
                (score - matchmaking_data["info"]["division"]["minpoints"])
                / (
                    matchmaking_data["info"]["division"]["maxpoints"]
                    - matchmaking_data["info"]["division"]["minpoints"]
                    + 1
                ),
                4,
            )
            * 100
        )

        log.debug(
            f"Creating Matchmaking Data String With {rank}, {score}, {current_division}, {progression_to_next_div}"
        )
        matchmaking_data_string = f"```Rank: {rank}\nScore: {score}\nCurrent Division: {current_division}\nProgression to Next Division: {progression_to_next_div}%```"

        log.debug(f"Created Matchmaking Data String -> {matchmaking_data_string}")
        return matchmaking_data_string
    except:
        log.error("Player has never played Matchmaking")
        return "An Error Occured While Getting Matchmaking Data, Player has not played Matchmaking"


def get_trophy_count(raw_data) -> str:
    log.debug("Getting Trophy Counts")
    trophy_count_string = "```\n"

    log.debug("Adding Total Points")
    total_points = common_functions.add_commas(raw_data["trophies"]["points"])
    trophy_count_string += f"Total Points: {total_points}\n\n"
    log.debug(f"Added Total Points -> {total_points}")

    for i, trophy_count in enumerate(raw_data["trophies"]["counts"]):
        trophy_count_string = trophy_count_string + f"Trophy {i + 1}: {trophy_count}\n"
    trophy_count_string += "```"
    log.debug(f"Final Trophy Count -> {trophy_count_string}")
    return trophy_count_string


def get_zones_and_positions(raw_data) -> str:
    """
    Converts raw_player_data into location and their ranks
    """
    ranks_string = ""

    log.debug("Getting Zones")
    zone_one = raw_data["trophies"]["zone"]["name"]
    zone_two = raw_data["trophies"]["zone"]["parent"]["name"]
    zone_three = raw_data["trophies"]["zone"]["parent"]["parent"]["name"]

    try:
        zone_four = raw_data["trophies"]["zone"]["parent"]["parent"]["parent"]["name"]
    except:
        zone_four = ""

    log.debug(f"Got Zones -> {zone_one}, {zone_two}, {zone_three}, {zone_four}")
    log.debug("Getting Position Data")
    raw_zone_positions = raw_data["trophies"]["zonepositions"]
    zone_one_position = raw_zone_positions[0]
    zone_two_position = raw_zone_positions[1]
    zone_three_position = raw_zone_positions[2]

    if zone_four != "":
        zone_four_position = raw_zone_positions[3]
    else:
        zone_four_position = -1

    log.debug("Got Position Data")
    log.debug("Making string for position data")
    ranks_string = "```\n"
    ranks_string += f"{zone_one} - {zone_one_position}\n"
    ranks_string += f"{zone_two} - {zone_two_position}\n"
    ranks_string += f"{zone_three} - {zone_three_position}\n"

    if zone_four != "":
        ranks_string += f"{zone_four} - {zone_four_position}\n"

    ranks_string += "```"

    log.debug(f"Final Ranks String is {ranks_string}")

    log.debug("Creating Zones String")
    zones_string = f"```\n{zone_one}, {zone_two}, {zone_three}"

    if zone_four != "":
        zones_string += f", {zone_four}"

    zones_string += "\n```"

    return zones_string, ranks_string


def add_meta_details(
    player_page: discord.Embed,
    raw_data,
) -> discord.Embed:
    log.debug("Adding Meta Details for Player")

    meta_data = raw_data["meta"]

    try:
        log.debug("Checking if Player has Twitch")
        twitch_name = meta_data["twitch"]
        player_page.add_field(
            name="[<:twitch:895250576751853598>] Twitch",
            value=f"[{twitch_name}](https://twitch.tv/{twitch_name})",
            inline=True,
        )
        log.debug("Twitch Added for Player")
    except:
        log.debug("Player does not have a Twitch Account Linked to TMIO")

    try:
        log.debug("Checking if Player has Twitter")
        twitter_name = meta_data["twitter"]
        player_page.add_field(
            name="[<:twitter:895250587157946388>] Twitter",
            value=f"    [{twitter_name}](https://twitter.com/{twitter_name})",
            inline=True,
        )
        log.debug("Twitter Added for Player")
    except:
        log.debug("Player does not have a Twitter Account Linked to TMIO")

    try:
        log.debug("Checking if Player has YouTube")
        youtube_link = meta_data["youtube"]
        player_page.add_field(
            name="[<:youtube:895250572599513138>] YouTube",
            value=f"[YouTube](https://youtube.com/channel/{youtube_link})",
            inline=True,
        )
        log.debug("YouTube Added for Player")
    except:
        log.debug("Player does not have a YouTube Account Linked to TMIO")

    log.debug("Adding TMIO")
    display_name = raw_data["displayname"]
    player_id = raw_data["accountid"]
    player_page.add_field(
        name="TMIO",
        value=f"[{display_name}](https://trackmania.io/#/player/{player_id})",
    )

    try:
        log.debug("Checking if TMGL Player")
        if meta_data["tmgl"] is True:
            player_page.add_field(
                name="TMGL", value="This Player Participates in TMGL", inline=True
            )
            log.debug("Added TMGL Field")
    except:
        log.debug("Player does not participate in TMGL")

    log.debug("Added TMIO Link")
    log.debug(f"Returning {player_page}")
    return player_page


def _get_username_list() -> list[str]:
    log.debug("Getting Username List")
    username_list = []

    log.debug("Opening Usernames File")
    with open("./data/json/tm2020_usernames.json", "r", encoding="UTF-8") as file:
        username_data = json.load(file)
        for user in username_data["Usernames"]:
            username_list.append(
                str(username_data["Usernames"][user]["TM2020 Username"]).lower()
            )

    log.debug(f"Got Username List -> {username_list}")
    return username_list


def _get_username_id_list() -> list[str]:
    log.debug("Getting Username List")
    username_ids = []

    log.debug("Opening Usernames File")
    with open("./data/json/tm2020_usernames.json", "r", encoding="UTF-8") as file:
        username_data = json.load(file)
        for user in username_data["Usernames"]:
            username_ids.append(
                str(username_data["Usernames"][user]["TM2020 ID"]).lower()
            )

    log.debug(f"Got Username List -> {username_ids}")
    return username_ids
