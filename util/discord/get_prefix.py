import discord
import json

DEFAULT_PREFIX = "--"


def get_prefix(client, message: discord.Message) -> list[str]:
    """Get's Prefix for the Current Guild

    Args:
        client ([type]): The Bot Client
        message (discord.Message): The Message Where the Message was Sent

    Returns:
        list[str]: Returns all the Prefixes for that Guild
    """

    with open("./data/json_data/prefixes.json", "r") as file:
        prefixes = json.load(file)
        file.close()

    try:
        return prefixes[str(message.guild.id)]
    except:
        return DEFAULT_PREFIX
