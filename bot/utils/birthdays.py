import json
import typing
from datetime import datetime
from typing import List

import discord
from bot import constants
from bot.log import get_logger
from bot.utils.commons import Commons
from bot.utils.discord import EZEmbed

log = get_logger(__name__)


class Birthday:
    def __init__(
        self,
        username: str,
        discriminator: int,
        id: int,
        year: int,
        month: str,
        day: int,
    ):
        self.username = username
        self.discriminator = discriminator
        self.id = id

        self.year = year
        self.month = month
        self.day = day

        self.MONTHS = constants.Consts.months

    def save(self):
        log.debug("Opening Birthday List")
        birthdays: dict[list] = {}

        with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
            birthdays = json.load(file)

        # Checks if person already has a saved birthday
        for person in birthdays["birthdays"]:
            if person["ID"] == self.id:
                log.critical("Player already has a saved birthday, popping")
                birthdays["birthdays"].pop(birthdays["birthdays"].index(person))

        birthdays["birthdays"].append(
            {
                "Name": self.username,
                "Discriminator": self.discriminator,
                "ID": self.id,
                "Year": self.year,
                "Month": self.month,
                "Day": self.day,
            }
        )

        log.debug("Dumping birthdays data to file")
        with open("./bot/resources/json/birthdays.json", "w", encoding="UTF-8") as file:
            json.dump(birthdays, file, indent=4)

    @staticmethod
    def list_birthdays() -> list[discord.Embed]:
        MONTHS = constants.Consts.months

        log.debug("Opening the birthdays.json file")
        with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
            birthdays = Birthday._sort_birthdays(json.load(file)["birthdays"])

        if len(birthdays) > 10:
            birthdays = Commons.split_list_of_lists(birthdays)
            embed_list = []
            for birthday_lst in birthdays:
                embed_list.append(
                    EZEmbed.create_embed(
                        description=Birthday.__format_lst(birthday_lst)
                    )
                )

            return embed_list
        else:
            return [EZEmbed.create_embed(description=Birthday.__format_lst(birthdays))]

    @staticmethod
    def next_birthday() -> discord.Embed:
        MONTHS = constants.Consts.months

        log.debug("Opening the birthdays.json file")
        with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
            birthdays = Birthday._sort_birthdays(json.load(file)["birthdays"])

        log.debug("Looping through birthday list to find next birthday")
        year = int(datetime.now().date().strftime("%Y"))
        smallest_diff = birthdays[0]
        timestamp_diff = 100000000
        for person in birthdays:
            if (
                int(
                    Commons.timestamp_date(
                        year=year,
                        month=MONTHS.index(person["Month"]) + 1,
                        day=person["Day"],
                    )
                    - Commons.timestamp()
                )
                < timestamp_diff
                and int(
                    Commons.timestamp_date(
                        year=year,
                        month=MONTHS.index(person["Month"]) + 1,
                        day=person["Day"],
                    )
                    - Commons.timestamp()
                )
                > 0
            ):
                timestamp_diff = int(
                    Commons.timestamp_date(
                        year=year,
                        month=MONTHS.index(person["Month"]) + 1,
                        day=person["Day"],
                    )
                    - Commons.timestamp()
                )
                smallest_diff = person

        return EZEmbed.create_embed(description=Birthday.__format_lst([smallest_diff]))

    @staticmethod
    def month_birthdays(month: int) -> list[discord.Embed]:
        MONTHS = constants.Consts.months

        log.debug("Opening the birthdays.json file")
        with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
            birthdays = Birthday.__split_birthdays(json.load(file)["birthdays"])[month]

        if len(birthdays) == 0:
            return None
        elif len(birthdays) > 10:
            birthdays = Commons.split_list_of_lists(Birthday._sort_birthdays(birthdays))
            embed_list = []
            for birthday_lst in birthdays:
                embed_list.append(
                    EZEmbed.create_embed(
                        description=Birthday.__format_string(birthday_lst)
                    )
                )

            return embed_list
        else:
            return [EZEmbed.create_embed(description=Birthday.__format_lst(birthdays))]

    @staticmethod
    def today_birthday() -> typing.Union[None, List[discord.Embed]]:
        MONTHS = constants.Consts.months

        log.debug("Opening the birthdays.json file")
        with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
            birthdays = Birthday._sort_birthdays(json.load(file)["birthdays"])

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
                birthday_list.append(
                    EZEmbed.create_embed(
                        description=Birthday.__format_lst_today([person])
                    )
                )

        if len(birthday_list) > 0:
            return birthday_list
        else:
            log.debug("No one's birthday today")
            return None

    @staticmethod
    def _sort_birthdays(birthdays: list) -> list:
        return Birthday.__append_birthdays(Birthday.__split_birthdays(birthdays))

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

            t1 = Commons.timestamp()
            t2 = Commons.timestamp_date(
                year=year, month=MONTHS.index(person["Month"]) + 1, day=person["Day"]
            )

            age = year - int(person["Year"])

            if t2 - t1 <= 0:
                log.debug("Birthday has passed, adding one year to t2 timestamp")
                t2 += 31536000
                age += 1

            # Removing the +530 IST Offset
            t2 -= 19800

            birthdays_str += f"**Name:** {person['Name']}#{person['Discriminator']}\n**Birthday:** {Commons.get_ordinal_number(person['Day'])} {person['Month']}\nTurning `{age}` in <t:{t2}:R>\n\n"

        return birthdays_str

    @staticmethod
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

            t1 = Commons.timestamp()
            t2 = Commons.timestamp_date(
                year=year, month=MONTHS.index(person["Month"]) + 1, day=person["Day"]
            )

            age = year - int(person["Year"])

            if t2 - t1 <= 0:
                log.debug("Birthday has passed, adding one year to t2 timestamp")
                t2 += 31536000
                age += 1

            # Removing the +530 IST Offset
            t2 -= 19800

            birthdays_str += f"**Name:** {person['Name']}#{person['Discriminator']}\n**Birthday:** {Commons.get_ordinal_number(person['Day'])} {person['Month']}\nTurning `{age}` **TODAY!!**\n\n"

        return birthdays_str
