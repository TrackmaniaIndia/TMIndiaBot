import json
import os

from bot.log import get_logger

log = get_logger(__name__)


def create_config(guild_id: int):
    config_path = f"./bot/resources/guild_data/{guild_id}/config.json"
    if not os.path.exists(config_path):
        log.debug("Creating Config")

        config_dict = {
            "prefix": ">>",
            "announcement_channel": 0,
            "cotd_one_reminder": False,
            "cotd_two_reminder": False,
            "cotd_three_reminder": False,
            "royal_one_reminder": False,
            "royal_two_reminder": False,
            "royal_three_reminder": False,
            "cotd_reminder_channel": 0,
            "royal_reminder_channel": 0,
            "totd_data": False,
            "totd_channel": 0,
            "birthdays_channel": 0,
            "trophy_tracking": False,
            "trophy_update_channel": 0,
            "mod_logs_channel": 0,
            "main_cotd_role": 0,
            "first_rerun_cotd_role": 0,
            "second_rerun_cotd_role": 0,
            "main_royal_role": 0,
            "first_rerun_royal_role": 0,
            "second_rerun_royal_role": 0,
        }

        with open(config_path, "w", encoding="UTF-8") as file:
            json.dump(config_dict, file, indent=4)
    else:
        log.debug("Config file already exists")


def create_quotes(guild_id: int):
    quotes_path = f"./bot/resources/guild_data/{guild_id}/quotes.json"

    if not os.path.exists(quotes_path):
        log.debug("Creating quotes")
        quotes_dict = {"quotes": []}
        with open(quotes_path, "w", encoding="UTF-8") as file:
            json.dump(quotes_dict, file, indent=4)
    else:
        log.debug("Quotes file already exists")


def create_trophy_tracking(guild_id: int):
    tracking_path = f"./bot/resources/guild_data/{guild_id}/trophy_tracking.json"

    if not os.path.exists(tracking_path):
        log.debug("Creating Trophy Tracking")
        tracking_dict = {"tracking": []}
        with open(tracking_path, "w", encoding="UTF-8") as file:
            json.dump(tracking_dict, file, indent=4)
    else:
        log.debug("Trophy Tracking file already exists")


def create_birthdays(guild_id: int):
    birthdays_path = f"./bot/resources/guild_data/{guild_id}/birthdays.json"

    if not os.path.exists(birthdays_path):
        log.debug("Creating Birthdays")
        birthday_dict = {"birthdays": []}
        with open(birthdays_path, "w", encoding="UTF-8") as file:
            json.dump(birthday_dict, file, indent=4)
    else:
        log.debug("Birthdays file already exists")
