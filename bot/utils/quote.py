import datetime
import json

import discord
import numpy as np

import bot.utils.commons as commons
from bot.log import get_logger
from bot.utils.discord import create_embed

log = get_logger(__name__)


def get_quote(guild_id: int, num: int) -> discord.Embed | None:
    """Gets the quote of a specific number of a specific guild. Returns None if the number does not exist.
    If the `num` is -1, it returns the latest quote.

    Args:
        guild_id (int): The guild's id of the quote.
        num (int): The quote number.

    Returns:
        discord.Embed | None: discord.Embed if the quote of that number exists, else return None.
    """
    log.debug("Getting quote %s for guild %s", num, guild_id)
    with open(
        f"./bot/resources/guild_data/{guild_id}/quotes.json", "r", encoding="UTF-8"
    ) as file:
        all_quotes = json.load(file)["quotes"]

    try:
        if num == -1:
            return _quote_dict_to_embed(all_quotes[-1])
        return _quote_dict_to_embed(all_quotes[num - 1])
    except IndexError:
        return None


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
    timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()))

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
    color = commons.get_random_color()

    embed = create_embed(title=title, description=description, color=color)
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


def get_random_quote(guild_id: str) -> discord.Embed:
    """Gets a random quote from a guild_id in a `dict` format.

    Args:
        guild_id (str): The guild id where the command was invoked.

    Returns:
        dict: The quote in `dict` format.
    """
    log.debug("Getting a random quote for %s", guild_id)
    num_quotes = _get_number_of_quotes(guild_id)
    number = np.random.randint(low=0, high=num_quotes) if num_quotes != 1 else 0

    return get_quote(guild_id, number)


def get_last_quote(guild_id: str) -> discord.Embed:
    """Get's the last quote saved for a specific guild_id

    Args:
        guild_id (str): The guild_id where the command was invoked.

    Returns:
        discord.Embed: The quote in `discord.Embed` format.
    """
    log.debug("Getting a random quote for %s", guild_id)
    return get_quote(guild_id, -1)


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
