import logging
import discord

import functions.logging.convert_logging as convert_logging

log = logging.getLogger(__name__)
log = convert_logging.get_logging()


def get_random_color() -> discord.Colour:
    return discord.Colour.random()

def checkKey(d: dict, key: str) -> bool:
    found = False
    try:
        if d[key]:
            found = True
        else:
            found = False
    except KeyError or IndexError as e:
        found = False
    
    return found


if __name__ == "__main__":
    for i in range(0, 100):
        print(f"{get_random_color()}")