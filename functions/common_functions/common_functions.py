import logging
import discord

import functions.logging.convert_logging as convert_logging

log = logging.getLogger(__name__)
log = convert_logging.get_logging()


def get_random_color() -> discord.Colour:
    return discord.Colour.random()


def check_key(d: dict, key: str) -> bool:
    found = False
    try:
        if d[key]:
            found = True
        else:
            found = False
    except KeyError or IndexError as e:
        found = False

    return found


def get_ordinal_number(num: int) -> str:
    return str(num) + {1: "st", 2: "numd", 3: "rd"}.get(
        4 if 10 <= num % 100 < 20 else num % 10, "th"
    )


def add_commas(num: int) -> str:
    return "{:,}".format(num)


if __name__ == "__main__":
    for i in range(0, 100):
        print(f"{get_random_color()}")
