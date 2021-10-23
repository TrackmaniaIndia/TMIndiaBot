import json
import util.logging.convert_logging as convert_logging
from datetime import datetime
import discord
import util.discord.easy_embed as ezembed
import numpy as np

log = convert_logging.get_logging()

def save(message: str, author: str) -> None:
    """Save a Quote to the JSON File

    Args:
        message (str): The Message
        author (str): The Author
    """
    log.debug(f"Saving {message} by {author} at {datetime.now()}")
    log.debug(f"Opening JSON File")

    quotes = []
    date_created_unformatted = datetime.now()
    date_created = date_created_unformatted.strftime("%c")

    with open("./data/json/quotes.json", "r") as file:
        log.debug(f"Loading JSON file")
        quotes = json.load(file)
        log.debug(f"Opened JSON File")

    new_quote_dict = {
        "Message": message,
        "Author": author,
        "Date Created": date_created,
        "Number": int(get_number_of_quotes() + 1),
    }

    quotes["quotes"].append(new_quote_dict)

    log.debug(f"Dumping to File")
    with open("./data/json/quotes.json", "w") as file:
        json.dump(quotes, file, indent=4)
    log.debug(f"Dumped to File")
    log.debug(f"Returning")
    return None

def quote_dict_to_embed(quote: dict) -> discord.Embed:
    embed = ezembed.create_embed(title='***Quote #{}***'.format(quote["Number"]), color=discord.Colour.random())
    embed.add_field(name=f"***Message***", value=quote["Message"], inline=False)
    embed.add_field(name=f"***Author***", value=quote["Author"], inline=True)
    embed.add_field(
        name=f"***Date Created***", value=quote["Date Created"], inline=True
    )
    embed.add_field(name=f"***Number***", value=quote["Number"], inline=True)

    return embed


def get_random_quote_dict() -> dict:
    log.debug(f"Generating Random Number Between 0 and {get_number_of_quotes()}")
    number = np.random.randint(low=0, high=get_number_of_quotes() - 1)

    log.debug(f"Opening Files")
    with open("./data/json/quotes.json", "r") as file:
        quotes = json.load(file)["quotes"]
        log.debug(f"Returning quote #{number}")
        return quotes[number]


def get_last_quote() -> discord.Embed:
    log.debug(f'Opening JSON File')
    with open('./data/json/quotes.json', 'r') as file:
        log.debug(f'Loading JSON file')
        quotes = json.load(file)
        log.debug(f'Read JSON file, returning last quote')
        
        return quote_dict_to_embed(quotes['quotes'][-1])

def get_number_of_quotes():
    log.debug(f"Opening JSON File")
    with open("./data/json/quotes.json", "r") as file:
        log.debug(f"Loading JSON file")
        quotes = json.load(file)
        log.debug(f"Read JSON file, returning length of quotes array")

        return len(quotes["quotes"])