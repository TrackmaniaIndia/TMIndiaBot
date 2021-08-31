import logging
import json
import discord

import functions.logging.convert_logging as cl

# log_level = os.getenv("LOG_LEVEL")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log_level, discord_log_level = "", ""

with open("./json_data/config.json") as file:
    config = json.load(file)

    log_level = config["log_level"]
    discord_log_level = config["discord_log_level"]

log = logging.getLogger(__name__)
log = cl.get_logging(log_level, discord_log_level)


def get_random_color() -> discord.Colour:
    return discord.Colour.random()


def make_string(my_list: list) -> str:
    list_string = ""

    for list_item in my_list:
        log.debug(f"Adding {list_item} to String")

        list_string += list_item + " "

    return list_string


if __name__ == "__main__":
    for i in range(0, 100):
        print(f"{get_random_color()}")
