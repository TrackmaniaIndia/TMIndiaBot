import discord
from discord import player
import requests
import util.common_functions as common_functions
import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed
from util.trackmania.tm2020.cotd import _get_avg_global_rank, _get_avg_div, _get_num_completed_cotds, _get_num_all_cotds
import os
import threading
import json

log = convert_logging.get_logging()
BASE_API_URL = "http://localhost:3000"


def get_player_id(username: str) -> str:
    """Grabs player id for given username from api

    Args:
        username (str): The username of the player

    Returns:
        str: the player id
    """
    log.debug(f"Getting Player ID for {username}")
    player_data = requests.get(f"{BASE_API_URL}/tm2020/player/{username}").json()
    log.debug(f"Received Player Data, Parsing")
    player_id = player_data[0]["player"]["id"]
    log.debug(f"Player ID is {player_id}")
    return player_id


def get_player_data(username: str) -> discord.Embed:
    """Get's the TM2020 Player Data for a given username

    Args:
        username (str): The player username

    Returns:
        discord.Embed: Embed containing all the player information
    """
    log.debug(f"Pinging API for Data of {username}")
    data = requests.get(BASE_API_URL + f"/tm2020/player/{username}").json()[0]

    if data == []:
        log.error("Username given is not valid")
        return None

    log.debug(f"Parsing Data")
    name = data["player"]["name"]
    zone = data["player"]["zone"]["name"]
    parent_zone = data["player"]["zone"]["parent"]["name"]

    log.debug(f"Trying for Twitch Data")
    try:
        twitch_username = data["player"]["meta"]["twitch"]
        log.debug(f"Twitch Data Exists -> {twitch_username}")
    except:
        twitch_username = ""
        log.debug(f"{username} does not have a twitch listed")

    log.debug(f"Checking if TMGL Player")
    try:
        tmgl_flag = data["player"]["meta"]["tmgl"]
        log.debug(f"TMGL Player")
    except:
        tmgl_flag = False
        log.debug(f"{username} is not a TMGL Player")

    log.debug(f"Checking for Youtube")
    try:
        youtube_link = data["player"]["meta"]["youtube"]
        log.debug(f"Youtube Link Exists -> {youtube_link}")
    except:
        youtube_link = ""
        log.debug(f"{username} does not have a youtube listed")

    log.debug(f"Checking for Twitter")
    try:
        twitter_username = data["player"]["meta"]["twitter"]
        log.debug(f"Twitter Exists -> {twitter_username}")
    except:
        twitter_username = ""
        log.debug(f"{username} does not have a twitter listed")

    player_details = ezembed.create_embed(
        title=f"Player Details for {name}", color=discord.Colour.random()
    )

    log.debug(f"Adding Location for {username}")
    player_details.add_field(
        name="Location", value=f"```Area: {zone}, {parent_zone}```", inline=False
    )
    log.debug(f"Added Zone: {zone} and Parent Zone: {parent_zone}")

    log.debug(f"Parsing Matchmaking Data for {username}")
    match_making_rank = common_functions.add_commas(data["matchmaking"][0]["rank"])
    match_making_score = data["matchmaking"][0]["score"]
    matchmaking_current_div = data["matchmaking"][0]["division"]["position"] - 1
    matchmaking_percentage_to_next_div = (
        str(
            round(
                (
                    (match_making_score)
                    / (data["matchmaking"][0]["division"]["maxpoints"] + 1)
                )
                * 100,
                2,
            )
        )
        + "%"
    )
    points_to_next = common_functions.add_commas(
        data["matchmaking"][0]["division"]["maxpoints"] - match_making_score + 1
    )
    matchmaking_current_div_string = __div_str(matchmaking_current_div)
    match_making_score = common_functions.add_commas(match_making_score)
    log.debug(f"Parsed Matchmaking Data for {username}, creating string")

    matchmaking_data_str = ""
    matchmaking_data_str = (
        matchmaking_data_str
        + f"```Rank: {match_making_rank}\nScore: {match_making_score}\nCurrent Div: {matchmaking_current_div_string}\nPercentage To Next Div: {matchmaking_percentage_to_next_div}\nPoints Required Until Next Div: {points_to_next}```"
    )
    log.debug(f"Created Matchmaking String, Adding to Embed")
    player_details.add_field(
        name="Matchmaking", value=matchmaking_data_str, inline=False
    )
    log.debug(f"Added Matchmaking Data to {player_details}")

    log.debug(f"Parsing Royal Data for {username}")
    royal_rank = common_functions.add_commas(data["matchmaking"][1]["rank"])
    royal_score = common_functions.add_commas(data["matchmaking"][1]["score"])
    royal_progression = data["matchmaking"][1]["progression"]
    royal_current_div = data["matchmaking"][1]["division"]["position"]
    try:
        royal_percentage_to_next_div = (
            str(
                round(
                    (royal_progression)
                    / (data["matchmaking"][1]["division"]["maxwins"] + 1)
                )
                * 100,
                2,
            )
            + "%"
        )
    except:
        log.error(f"{username} has never won a Royal match, defaulting percentage to 0")
        royal_percentage_to_next_div = "0%"
    royal_progression = common_functions.add_commas(
        data["matchmaking"][1]["progression"]
    )
    try:
        royal_wins_required = common_functions.add_commas(
            data["matchmaking"][1]["division"]["maxwins"] - royal_progression + 1
        )
    except:
        log.error(f"{username} has never won a Royal match, defaulting to 1")
        royal_wins_required = 1
    log.debug(f"Parsed Royal Data for {username}, creating string")

    royal_data_str = ""
    royal_data_str = (
        royal_data_str
        + f"```Rank: {royal_rank}\nScore: {royal_score}\nCurrent Div: {royal_current_div}\nPercentage to Next Div: {royal_percentage_to_next_div}\nWins required until next div: {royal_wins_required}```"
    )

    log.debug(f"Created Royal String, Adding to Embed")
    player_details.add_field(name="Royal Data", value=royal_data_str, inline=False)
    log.debug(f"Added Royal Data to {player_details}")
    
    log.debug(f'Adding COTD Data to Embed')
    player_details.add_field(name='COTD Data', value=__get_basic_cotd_data(username), inline=False)
    log.debug(f'Added COTD Data to {player_details}')

    player_details = __format_meta_details(
        player_embed=player_details,
        username=name,
        twitch=twitch_username,
        youtube=youtube_link,
        twitter=twitter_username,
        tmgl=tmgl_flag,
    )

    return player_details


def __format_meta_details(
    player_embed: discord.Embed,
    username: str,
    twitter: str = "",
    youtube: str = "",
    twitch: str = "",
    tmgl: bool = False,
) -> str:
    """Formats the Meta Details of a player

    Args:
        player_embed(discord.Embed): The player embed to add the fields
        username (str): The player's username
        twitter (str, optional): The Twitter username. Defaults to ''.
        youtube (str, optional): The YouTube ID. Defaults to ''.
        twitch (str, optional): The Twitch Username. Defaults to ''.
        tmgl (bool, optional): Whether the player is a TMGL player or not. Defaults to False.

    Returns:
        str: [description]
    """
    if twitter != "":
        log.debug(f"Twitter Exists for {username}, Adding Field")
        player_embed.add_field(
            name="Twitter",
            value=f"[{twitter}](https://twitter.com/{twitter})",
            inline=True,
        )
    if youtube != "":
        log.debug(f"YouTube Exists for {username}, Adding Field")
        player_embed.add_field(
            name="YouTube",
            value=f"[Click Here](https://youtube.com/channel/{youtube})",
            inline=True,
        )
    if twitch != "":
        log.debug(f"Twitch Exists for {username}, Adding")
        player_embed.add_field(
            name="Twitch", value=f"[{twitch}](https://twitch.tv/{twitch})", inline=True
        )
    if tmgl == True:
        log.debug(f"This player participates in TMGL")
        player_embed.add_field(
            name="TMGL", value="This player participates in TMGL", inline=True
        )

    log.debug(f"Created Embed, returning {player_embed}")
    return player_embed


def __div_str(current_div: int) -> str:
    log.debug(f"Converting {current_div} to string")
    log.debug(f"Opening JSON file of ranks")
    with open("./data/json/mm_ranks.json", "r") as file:
        log.debug(f"Opened file, parsing data")
        rank_data = json.load(file)["rank_data"]

    log.debug(f"Rank is {rank_data[str(current_div)]}")
    return rank_data[str(current_div)]


def __get_basic_cotd_data(username: str) -> str:
    log.debug(f"Getting COTD Data for {username}")
    log.debug(f"Getting Player ID")
    player_id = get_player_id(username)
    log.debug(f"Got Player ID")

    log.debug(f"Getting COTD Data")
    cotd_data = requests.get(BASE_API_URL + f"/tm2020/player/{player_id}/cotd").json()
    log.debug(f"Got COTD Data")

    log.debug(f'Parsing all COTD Data')
    avg_div = _get_avg_div(cotd_data)
    avg_global_rank = _get_avg_global_rank(cotd_data)
    num_completed = _get_num_completed_cotds(cotd_data)
    num_cotds = _get_num_all_cotds(cotd_data)
    log.debug(f'Parsed all COTD Data')
    
    log.debug(f'Making COTD String')
    cotd_string = f'```Average Div: {avg_div}\nAverage Global Rank: {avg_global_rank}\nNumber of COTDs Completed: {num_completed}\nNumber of COTDs Played: {num_cotds}```'
    log.debug(f'Created COTD String')
    
    log.debug('Returning COTD String')
    return cotd_string