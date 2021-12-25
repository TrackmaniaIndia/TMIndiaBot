import os
import json
import discord

from util.logging import convert_logging

# Create Logger
log = convert_logging.get_logging()


def folder_check(client: discord.Bot):
    log.info("Checking Folders")
    log.error(client.guilds)
    for guild in client.guilds:
        log.debug(f"Checking {guild.name} with ID: {guild.id}")

        if not os.path.exists(f"./data/guild_data/{str(guild.id)}"):
            log.critical(f"Folder does not exist for {guild.name} with ID: {guild.id}")

            log.debug(f"Creating folder and empty quote file")
            os.mkdir(f"./data/guild_data/{str(guild.id)}")

            log.debug(f"Creating quotes.json for {guild.name}")
            with open(
                f"./data/guild_data/{guild.id}/quotes.json", "w", encoding="UTF-8"
            ) as file:
                log.info(f"Dumping an Empty Quotes Array into quotes.json")
                json.dump({"quotes": []}, file, indent=4)
