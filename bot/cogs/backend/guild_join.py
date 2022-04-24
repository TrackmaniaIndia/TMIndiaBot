import json
import os

import discord
from discord import ApplicationContext, Guild
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger

log = get_logger(__name__)


class GuildJoinStuff(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        log.critical("Bot joined %s with ID %s", guild.name, guild.id)

        log.info("Creating Folders and required files for %s", guild.name)
        if os.path.exists(f"./bot/resources/guild_data/{guild.id}/"):
            log.info("The guild already has a folder")
        else:
            log.info("Creating folder for %s", guild.name)
            os.mkdir(f"./bot/resources/guild_data/{guild.id}/")

        self._create_config(guild.id)
        self._create_quotes(guild.id)
        self._create_trophy_tracking(guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        log.critical(
            "Bot has left/been kicked out of %s with id %s", guild.name, guild.id
        )
        return

    def _create_config(self, guild_id: int):
        config_path = f"./bot/resources/guild_data/{guild_id}/config.json"
        if not os.path.exists(config_path):
            log.debug("Creating Config")

            config_dict = {
                "prefix": ">>",
                "announcement_channel": 0,
                "trophy_update_channel": 0,
                "cotd_one_reminder": False,
                "cotd_two_reminder": False,
                "cotd_three_reminder": False,
                "royal_one_reminder": False,
                "royal_two_reminder": False,
                "royal_three_reminder": False,
                "reminder_channel": 0,
                "totd_data": False,
                "totd_channel": 0,
                "trophy_tracking": False,
                "trophy_announcement_channel": 0,
                "mod_logs_channel": 0,
            }

            with open(config_path, "w", encoding="UTF-8") as file:
                json.dump(config_dict, file, indent=4)
        else:
            log.debug("Config file already exists")

    def _create_quotes(self, guild_id: int):
        quotes_path = f"./bot/resources/guild_data/{guild_id}/quotes.json"

        if not os.path.exists(quotes_path):
            log.debug("Creating quotes")
            quotes_dict = {"quotes": []}
            with open(quotes_path, "w", encoding="UTF-8") as file:
                json.dump(quotes_dict, file, indent=4)
        else:
            log.debug("Quotes file already exists")

    def _create_trophy_tracking(self, guild_id: int):
        tracking_path = f"./bot/resources/guild_data/{guild_id}/trophy_tracking.json"

        if not os.path.exists(tracking_path):
            log.debug("Creating Trophy Tracking")
            tracking_dict = {"tracking": []}
            with open(tracking_path, "w", encoding="UTF-8") as file:
                json.dump(tracking_dict, file, indent=4)
        else:
            log.debug("Trophy Tracking file already exists")


def setup(bot: Bot):
    bot.add_cog(GuildJoinStuff(bot))
