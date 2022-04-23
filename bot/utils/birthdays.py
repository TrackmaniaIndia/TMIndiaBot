import json
import typing
from datetime import datetime
from typing import List

import discord

import bot.utils.commons as commons
from bot import constants
from bot.log import get_logger
from bot.utils.discord import create_embed

log = get_logger(__name__)


def list_birthdays() -> list[discord.Embed]:
    MONTHS = constants.Consts.months

    log.debug("Opening the birthdays.json file")
    with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
        birthdays = _sort_birthdays(json.load(file)["birthdays"])

    if len(birthdays) > 10:
        birthdays = commons.split_list_of_lists(birthdays)
        embed_list = []
        for birthday_lst in birthdays:
            embed_list.append(create_embed(description=__format_lst(birthday_lst)))

        return embed_list
    else:
        return [create_embed(description=__format_lst(birthdays))]


def next_birthday() -> discord.Embed:
    MONTHS = constants.Consts.months

    log.debug("Opening the birthdays.json file")
    with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
        birthdays = _sort_birthdays(json.load(file)["birthdays"])

    log.debug("Looping through birthday list to find next birthday")
    year = int(datetime.now().date().strftime("%Y"))
    smallest_diff = birthdays[0]
    timestamp_diff = 100000000
    for person in birthdays:
        if (
            int(
                commons.timestamp_date(
                    year=year,
                    month=MONTHS.index(person["Month"]) + 1,
                    day=person["Day"],
                )
                - commons.timestamp()
            )
            < timestamp_diff
            and int(
                commons.timestamp_date(
                    year=year,
                    month=MONTHS.index(person["Month"]) + 1,
                    day=person["Day"],
                )
                - commons.timestamp()
            )
            > 0
        ):
            timestamp_diff = int(
                commons.timestamp_date(
                    year=year,
                    month=MONTHS.index(person["Month"]) + 1,
                    day=person["Day"],
                )
                - commons.timestamp()
            )
            smallest_diff = person

    return create_embed(description=__format_lst([smallest_diff]))


def month_birthdays(month: int) -> list[discord.Embed]:
    MONTHS = constants.Consts.months

    log.debug("Opening the birthdays.json file")
    with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
        birthdays = __split_birthdays(json.load(file)["birthdays"])[month]

    if len(birthdays) == 0:
        return None
    elif len(birthdays) > 10:
        birthdays = commons.split_list_of_lists(_sort_birthdays(birthdays))
        embed_list = []
        for birthday_lst in birthdays:
            embed_list.append(create_embed(description=__format_lst(birthday_lst)))

        return embed_list
    else:
        return [create_embed(description=__format_lst(birthdays))]


def today_birthday() -> typing.Union[None, List[discord.Embed]]:
    MONTHS = constants.Consts.months

    log.debug("Opening the birthdays.json file")
    with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
        birthdays = _sort_birthdays(json.load(file)["birthdays"])

    todays_day = int(datetime.now().date().strftime("%d"))
    todays_month = MONTHS[int(datetime.now().date().strftime("%m")) - 1]

    birthday_list = []

    log.debug("Looping through birthdays")
    for person in birthdays:
        if (
            person["Day"] == todays_day
            and person["Month"].lower() == todays_month.lower()
        ):
            log.info(f"It is {person['Name']}'s birthday today")
            birthday_list.append(create_embed(description=__format_lst_today([person])))

    if len(birthday_list) > 0:
        return birthday_list
    else:
        log.debug("No one's birthday today")
        return None


def remove_birthday(id: int) -> bool:
    log.debug("Getting birthday list")
    with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
        birthday_list: list = json.load(file)["birthdays"]

    log.debug("Looping through birthday list")
    for i, birthday in enumerate(birthday_list):
        if int(birthday["ID"]) == id:
            birthday_list.pop(i)
            log.debug("Birthday popped")
            return True

    log.debug("Birthday is not saved")
    return False


def user_birthday(id: int) -> discord.Embed | str:
    log.debug("Getting Birthday list")
    with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
        birthday_list: list = json.load(file)["birthdays"]

        log.debug("Looping through birthday list")
        for _, birthday in enumerate(birthday_list):
            if int(birthday["ID"]) == id:
                log.debug("This user has a birthday saved")
                return create_embed(description=__format_birthday(birthday))

        log.debug("This user does not have a birthday saved")
        return create_embed(
            description="This user does not have a birthday saved!\nAsk him to save the birthday by using the `/addbirthday` command"
        )


def _sort_birthdays(birthdays: list) -> list:
    return __append_birthdays(__split_birthdays(birthdays))


def __split_birthdays(birthdays: list) -> list[list]:
    MONTHS: list = constants.Consts.months
    # First by month, then by day

    # First split all birthdays into 12 lists depending on month
    birthdays_month_sep: list[list] = [[] for i in range(12)]

    log.debug("Splitting the original birthday list by month")
    for person in birthdays:
        birthdays_month_sep[MONTHS.index(person["Month"])].append(person)

    # Sort all the lists individually
    log.debug("Sorting lists individually")
    for i, month_list in enumerate(birthdays_month_sep):
        log.debug(f"Sorting {MONTHS[i]}")
        birthdays_month_sep[i] = sorted(
            birthdays_month_sep[i], key=lambda person: person["Day"]
        )

    return birthdays_month_sep


def __append_birthdays(birthdays_month_sep: list[list]) -> list[dict]:
    MONTHS: list = constants.Consts.months
    # Append all lists
    log.debug("Appending all lists")
    birthdays = []
    for i, month_list in enumerate(birthdays_month_sep):
        log.debug(f"Adding {MONTHS[i]}")
        for person in month_list:
            birthdays.append(person)

    return birthdays


def __format_lst(birthdays: list) -> str:
    MONTHS: list = constants.Consts.months
    # For the string:
    #   loops through list, adding people
    #   Name:
    #   Birthday: day month
    #   Turning age_xx in time_yy(using <t::R> discord)
    #
    # Logic:
    #   get current timestamp -> t1
    #   get timestamp of person at birthday on current year -> t2
    #       if t2 - t1 < 0:
    #            t2 += 31536000
    #            age += 1
    birthdays_str = ""
    for person in birthdays:
        log.debug(f"Adding {person['Name']} to the string")
        year = int(datetime.now().date().strftime("%Y"))

        t1 = commons.timestamp()
        t2 = commons.timestamp_date(
            year=year, month=MONTHS.index(person["Month"]) + 1, day=person["Day"]
        )

        age = year - int(person["Year"])

        if t2 - t1 <= 0:
            log.debug("Birthday has passed, adding one year to t2 timestamp")
            t2 += 31536000
            age += 1

        # Removing the +530 IST Offset
        t2 -= 19800

        birthdays_str += f"**Name:** {person['Name']}#{person['Discriminator']}\n**Birthday:** {commons.get_ordinal_number(person['Day'])} {person['Month']}\nTurning `{age}` in <t:{t2}:R>\n\n"

    return birthdays_str


def __format_lst_today(birthdays: list) -> str:
    MONTHS: list = constants.Consts.months
    # For the string:
    #   loops through list, adding people
    #   Name:
    #   Birthday: day month
    #   Turning age_xx in time_yy(using <t::R> discord)
    #
    # Logic:
    #   get current timestamp -> t1
    #   get timestamp of person at birthday on current year -> t2
    #       if t2 - t1 < 0:
    #            t2 += 31536000
    #            age += 1
    birthdays_str = ""
    for person in birthdays:
        log.debug(f"Adding {person['Name']} to the string")
        year = int(datetime.now().date().strftime("%Y"))

        t1 = commons.timestamp()
        t2 = commons.timestamp_date(
            year=year, month=MONTHS.index(person["Month"]) + 1, day=person["Day"]
        )

        age = year - int(person["Year"])

        if t2 - t1 <= 0:
            log.debug("Birthday has passed, adding one year to t2 timestamp")
            t2 += 31536000
            age += 1

        # Removing the +530 IST Offset
        t2 -= 19800

        birthdays_str += f"**Name:** {person['Name']}#{person['Discriminator']}\n**Birthday:** {commons.get_ordinal_number(person['Day'])} {person['Month']}\nTurning `{age}` **TODAY!!**\n\n"

    return birthdays_str


def __format_birthday(birthday: dict) -> str:
    MONTHS: list = constants.Consts.months

    birthday_str = ""
    log.debug(f"Adding {birthday['Name']} to the string")
    year = int(datetime.now().date().strftime("%Y"))

    t1 = commons.timestamp()
    t2 = commons.timestamp_date(
        year=year, month=MONTHS.index(birthday["Month"]) + 1, day=birthday["Day"]
    )

    age = year - int(birthday["Year"])

    if t2 - t1 <= 0:
        log.debug("Birthday has passed, adding one year to t2 timestamp")
        t2 += 31536000
        age += 1

    # Removing +530 IST Offset
    t2 -= 19800

    birthday_str += f"**Name:** {birthday['Name']}#{birthday['Discriminator']}\n**Birthday:** {commons.get_ordinal_number(birthday['Day'])} {birthday['Month']}\nTurning `{age}` **<t:{t2}:R>**\n\n"
    return birthday_str
