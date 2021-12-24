import json
from datetime import datetime
import discord
import util.discord.easy_embed as ezembed
import numpy as np
from util.logging import convert_logging
from util import common_functions


# Creating a logger
log = convert_logging.get_logging()


def save(message: str, author: str, message_link: str, guild_id: str) -> None:
    """Save a Quote to the JSON File

    Args:
        message (str): The Message
        author (str): The Author
    """
    log.debug(f"Saving {message} by {author} at {datetime.now()} from guild {guild_id}")
    log.debug("Opening JSON File")

    quotes = []
    date_created_unformatted = datetime.now()
    date_created = date_created_unformatted.strftime("%c")

    with open(
        f"./data/guild_data/{str(guild_id)}/quotes.json", "r", encoding="UTF-8"
    ) as file:
        log.debug("Loading JSON file")
        quotes = json.load(file)
        log.debug("Opened JSON File")

    new_quote_dict = {
        "Message": message,
        "Author": author,
        "Message Link": message_link,
        "Date Created": date_created,
        "Number": int(get_number_of_quotes(guild_id) + 1),
    }

    quotes["quotes"].append(new_quote_dict)

    log.debug("Dumping to File")
    with open(
        f"./data/guild_data/{str(guild_id)}/quotes.json", "w", encoding="UTF-8"
    ) as file:
        json.dump(quotes, file, indent=4)
    log.debug("Dumped to File")


def quote_dict_to_embed(quote: dict) -> discord.Embed:
    message_link = quote["Message Link"]
    embed = ezembed.create_embed(
        title="***Quote #{}***".format(quote["Number"]),
        description='```"{}" - {}```'.format(quote["Message"], quote["Author"]),
        color=common_functions.get_random_color(),
    )

    embed.add_field(
        name="***Message***", value=f"[Jump!]({message_link})", inline=False
    )
    embed.add_field(name="***Date Created***", value=quote["Date Created"], inline=True)
    embed.add_field(name="***Number***", value=quote["Number"], inline=True)

    return embed


def get_random_quote_dict(guild_id: str) -> dict:
    log.debug(
        f"Generating Random Number Between 0 and {get_number_of_quotes(guild_id)}"
    )
    number = np.random.randint(low=0, high=get_number_of_quotes(guild_id) - 1)

    log.debug("Opening Files")
    with open(
        f"./data/guild_data/{str(guild_id)}/quotes.json", "r", encoding="UTF-8"
    ) as file:
        quotes = json.load(file)["quotes"]
        log.debug(f"Returning quote #{number}")
        return quotes[number]


def get_last_quote(guild_id: str) -> discord.Embed:
    log.debug("Opening JSON File")
    with open(
        f"./data/guild_data/{str(guild_id)}/quotes.json", "r", encoding="UTF-8"
    ) as file:
        log.debug("Loading JSON file")
        quotes = json.load(file)
        log.debug("Read JSON file, returning last quote")

        return quote_dict_to_embed(quotes["quotes"][-1])


def get_number_of_quotes(guild_id: str):
    log.debug("Opening JSON File")
    with open(
        f"./data/guild_data/{str(guild_id)}/quotes.json", "r", encoding="UTF-8"
    ) as file:
        log.debug("Loading JSON file")
        quotes = json.load(file)
        log.debug("Read JSON file, returning length of quotes array")

        return len(quotes["quotes"])
