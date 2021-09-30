import os
import json
import logging
import functions.logging.convert_logging as convert_logging
from datetime import datetime
import random
import discord
from functions.other_functions.b64_wrapper import b64encode_string
from uuid import uuid4

log = logging.getLogger(__name__)
log = convert_logging.get_logging()


def save(message: str, author: str, authorId: str) -> None:
    log.debug(f"Saving {message} by {author} at {datetime.now()}")
    log.debug(f"Opening JSON File")

    quotes = []
    date_created_unformatted = datetime.now()
    # date_created = date_created_unformatted.strftime('%d %B, %Y - %I:%M:%S %p')
    date_created = date_created_unformatted.strftime("%c")

    with open("./json_data/quotes.json", "r") as file:
        log.debug(f"Loading JSON file")
        quotes = json.load(file)
        log.debug(f"Opened JSON File")

    new_quote_dict = {
        "Message": message,
        "Author": author,
        "Date Created": date_created,
        "Number": int(get_number_of_quotes() + 1),
        "authorId": b64encode_string(str(authorId)),
        "quoteId": str(uuid4()),
    }

    quotes["quotes"].append(new_quote_dict)

    log.debug(f"Dumping to File")
    with open("./json_data/quotes.json", "w") as file:
        json.dump(quotes, file, indent=4)
    log.debug(f"Dumped to File")
    log.debug(f"Returning")
    return None


def get_random_quote_dict_to_embed(quote: dict) -> discord.Embed:
    embed = discord.Embed(
        title="***Quote #{}***".format(quote["Number"]), color=discord.Colour.random()
    )
    embed.add_field(name=f"***Message***", value=quote["Message"], inline=False)
    embed.add_field(name=f"***Author***", value=quote["Author"], inline=True)
    embed.add_field(
        name=f"***Date Created***", value=quote["Date Created"], inline=True
    )
    embed.add_field(name=f"***Number***", value=quote["Number"], inline=True)

    return embed


def get_random_quote_dict() -> dict:
    log.debug(f"Generating Random Number Between 0 and {get_number_of_quotes()}")
    number = random.randint(0, get_number_of_quotes() - 1)

    log.debug(f"Opening Files")
    with open("./json_data/quotes.json", "r") as file:
        quotes = json.load(file)["quotes"]
        log.debug(f"Returning quote #{number}")
        return quotes[number]


def get_number_of_quotes():
    log.debug(f"Opening JSON File")
    with open("./json_data/quotes.json", "r") as file:
        log.debug(f"Loading JSON file")
        quotes = json.load(file)
        log.debug(f"Read JSON file, returning length of quotes array")

        return len(quotes["quotes"])


def get_quotes_by_id(id: str):
    b64id = b64encode_string(id)

    with open("./json_data/quotes.json", "r") as file:
        quotes = json.load(file)["quotes"]

        userQuotes = []
        for quote in quotes:
            try:
                if quote["authorId"] == b64id:
                    userQuotes.append(quote)
            except KeyError:
                continue

        return userQuotes
