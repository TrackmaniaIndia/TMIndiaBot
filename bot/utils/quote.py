import datetime
import json

import numpy as np

import discord
from bot.log import get_logger
from bot.utils.commons import get_random_color
from bot.utils.discord.easy_embed import EZEmbed

log = get_logger(__name__)


def save(msg: str, author: str, message_link: str, guild_id: str) -> None:
    """Save a Quote to the JSON File
    Args:
        msg (str): The Message
        author (str): The Author
    """

    log.info(
        f"Saving {msg} by {author} at {datetime.datetime.utcnow()} from guild {guild_id}"
    )

    quotes = []
    date_created = datetime.datetime.now().strftime("%c")
    timestamp = datetime.datetime.timestamp(datetime.datetime.now())

    log.debug("Opening JSON File")
    with open(
        f"./bot/resources/guild_data/{str(guild_id)}/quotes.json", "r", encoding="UTF-8"
    ) as file:
        log.debug("Loading Quotes JSON File")
        quotes = json.load(file)
        log.debug("Opened Quotes JSON File")

    new_quote_dict = {
        "Message": msg,
        "Author": author,
        "Message Link": message_link,
        "Date Created": date_created,
        "Timestamp": timestamp,
        "Number": int(_get_number_of_quotes(guild_id) + 1),
    }

    quotes["quotes"].append(new_quote_dict)

    log.debug("Dumping to Quotes File")
    with open(
        f"./bot/resources/guild_data/{str(guild_id)}/quotes.json", "w", encoding="UTF-8"
    ) as file:
        json.dump(quotes, file, indent=4)
    log.debug("Dumped to Quotes File")


def _quote_dict_to_embed(quote: dict) -> discord.Embed:
    """Changes a given quote dict to an embed format

    Args:
        quote (dict): The quote in `dict` format

    Returns:
        discord.Embed: The embed itself.
    """
    message_link = quote["Message Link"]

    title = f"***Quote #{quote['Number']}***"
    description = f"```\"{quote['Message']}\" - {quote['Author']}```"
    color = get_random_color()

    embed = EZEmbed.create_embed(title=title, description=description, color=color)
    embed.add_field(
        name="***Message***", value=f"[Jump!]({message_link})", inline=False
    )
    embed.add_field(name="***Date Created***", value=quote["Date Created"], inline=True)
    embed.add_field(name="***Number***", value=quote["Number"], inline=True)

    try:
        embed.add_field(
            name="***Uploaded***", value=f"<t:{quote['Timestamp']}:R>", inline=False
        )
    except KeyError:
        log.debug("Timestamp not saved")

    return embed


def _get_random_quote_dict(guild_id: str) -> dict:
    """Gets a random quote from a guild_id in a `dict` format.

    Args:
        guild_id (str): The guild id where the command was invoked.

    Returns:
        dict: The quote in `dict` format.
    """
    log.debug(
        f"Generating Random number Between 0 and {_get_number_of_quotes(guild_id)}"
    )
    number = np.random.randint(low=0, high=_get_number_of_quotes(guild_id) - 1)

    log.debug("Opening File")
    with open(
        f"./bot/resources/guild_data/{str(guild_id)}/quotes.json", "r", encoding="UTF-8"
    ) as file:
        quotes = json.load(file)["quotes"]
        log.debug(f"Returning #{number}")
        return quotes[number]


def get_last_quote(guild_id: str) -> discord.Embed:
    """Get's the last quote saved for a specific guild_id

    Args:
        guild_id (str): The guild_id where the command was invoked.

    Returns:
        discord.Embed: The quote in `discord.Embed` format.
    """
    log.debug("Opening JSON File")
    with open(
        f"./bot/resources/guild_data/{str(guild_id)}/quotes.json", "r", encoding="UTF-8"
    ) as file:
        log.debug("Loading JSON file")
        quotes = json.load(file)
        log.debug("Read JSON file, returning last quote")

        return _quote_dict_to_embed(quotes["quotes"][-1])


def _get_number_of_quotes(guild_id: str):
    """Gets the number of quotes saved for a specific guild_id

    Args:
        guild_id (str): The guild where the command was invoked in.

    Returns:
        int: The number of quotes saved.
    """
    log.debug("Opening JSON File")
    with open(
        f"./bot/resources/guild_data/{str(guild_id)}/quotes.json", "r", encoding="UTF-8"
    ) as file:
        log.debug("Loading JSON file")
        quotes = json.load(file)
        log.debug("Read JSON file, returning length of quotes array")

        return len(quotes["quotes"])
