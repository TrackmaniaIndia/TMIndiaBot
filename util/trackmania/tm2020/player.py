import discord
from discord import player
import requests
import util.common_functions as common_functions
import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed
import os
import threading

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
    log.debug(f'Pinging API for Data of {username}')
    data = requests.get(BASE_API_URL + f'/tm2020/player/{username}').json()[0]
    
    if data == []:
        log.error('Username given is not valid')
        return None
    
    log.debug(f'Parsing Data')
    name = data['player']['name']
    area = data['player']['zone']['name']
    parent_area = data['player']['zone']['parent']['name']
    
    log.debug(f'Trying for Twitch Data')
    try:
        twitch_username = data['player']['meta']['twitch']
        log.debug(f'Twitch Data Exists -> {twitch_username}')
    except:
        twitch_username = ''
        log.debug(f'{username} does not have a twitch listed')
        
    log.debug(f'Checking if TMGL Player')
    try:
        tmgl_flag = data['player']['meta']['tmgl']
        log.debug(f'TMGL Player')
    except:
        tmgl_flag = False
        log.debug(f'{username} is not a TMGL Player')
        
    log.debug(f'Checking for Youtube')
    try:
        youtube_link = data['player']['meta']['youtube']
        log.debug(f'Youtube Link Exists -> {youtube_link}')
    except:
        youtube_link = ''
        log.debug(f'{username} does not have a youtube listed')
    
    log.debug(f'Checking for Twitter')
    try:
        twitter_username = data['player']['meta']['twitter']
        log.debug(f'Twitter Exists -> {twitter_username}')
    except:
        twitter_username = ''
        log.debug(f'{username} does not have a twitter listed')
        
    player_details = ezembed.create_embed(title=f'Player Details for {name}', color=discord.Colour.random())
        
    player_details = __format_meta_details(player_embed=player_details, username=name,twitch=twitch_username, youtube=youtube_link, twitter=twitter_username, tmgl=tmgl_flag)

    return player_details

def __format_meta_details(player_embed: discord.Embed, username: str, twitter: str = '', youtube: str = '', twitch: str = '', tmgl: bool = False) -> str:
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
    final_str = ''
    if twitter != '':
        log.debug(f'Twitter Exists, Adding Field')
        player_embed.add_field(name='Twitter', value=f'[{twitter.capitalize()}](https://twitter.com/{twitter})', inline=True)
    if youtube != '':
        log.debug(f'YouTube Exists, Adding Field')
        player_embed.add_field(name='YouTube', value=f'[Click Here](https://youtube.com/channel/{youtube})', inline=True)
    if twitch != '':
        log.debug(f'Twitch Exists, Adding')
        player_embed.add_field(name='Twitch', value=f'[{twitch.capitalize()}](https://twitch.tv/{twitch})', inline=True)
    if tmgl == True:
        log.debug(f'This is a TMGL Player')
        player_embed.add_field(name='TMGL', value='Yes, This player participates in TMGL', inline=True)
    else:
        log.debug(f'This is not a TMGL Player')
        player_embed.add_field(name='TMGL', value='No, This player does not participate in TMGL', inline=True)
    
    log.debug(f'Created Embed, returning {player_embed}')
    return player_embed