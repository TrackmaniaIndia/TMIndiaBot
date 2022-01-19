import json
import time
from datetime import date, datetime

import discord
from discord.ext import commands

from bot import constants
from bot.log import get_logger

log = get_logger(__name__)


class Birthday:
    def __init__(self, ctx: commands.Context, year: int, month: str, day: int):
        self.username = ctx.author.name
        self.discriminator = ctx.author.discriminator
        self.id = ctx.author.id

        self.year = year
        self.month = month
        self.day = day

        self.months = constants.Consts.months

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
    def list_birthdays() -> str:
        months = constants.Consts.months

        log.debug(f"Opening the birthdays.json file")
        with open("./bot/resources/json/birthdays.json", "r", encoding="UTF-8") as file:
            birthdays = json.load(file)["birthdays"]

        if len(birthdays) == 0:
            return None
        elif len(birthdays) == 1:
            return "one person"

        birthdays = Birthday._sort_birthdays(birthdays)

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

            t1 = int(time.time())
            t2 = int(
                datetime(
                    year=year,
                    month=months.index(person["Month"]) + 1,
                    day=int(person["Day"]),
                ).timestamp()
            )

            age = year - int(person["Year"])

            if t2 - t1 <= 0:
                log.debug("Birthday has passed, adding one year to t2 timestamp")
                t2 += 31536000
                age += 1

            birthdays_str += f"**Name:** {person['Name']}#{person['Discriminator']}\n**Birthday:** {person['Day']} {person['Month']}\nTurning `{age}` in <t:{t2}:R>\n\n"

        return birthdays_str

    @staticmethod
    def _sort_birthdays(birthdays: list) -> list:
        months: list = constants.Consts.months
        # First by month, then by day

        # First split all birthdays into 12 lists depending on month
        birthdays_month_sep: list[list] = [[] for i in range(12)]

        log.debug("Splitting the original birthday list by month")
        for person in birthdays:
            birthdays_month_sep[months.index(person["Month"])].append(person)
        print(birthdays_month_sep)

        # Sort all the lists individually
        log.debug("Sorting lists individually")
        for i, month_list in enumerate(birthdays_month_sep):
            log.debug(f"Sorting {months[i]}")
            birthdays_month_sep[i] = sorted(
                birthdays_month_sep[i], key=lambda person: person["Day"]
            )

        # Append all lists
        log.debug("Appending all lists")
        birthdays = []
        for i, month_list in enumerate(birthdays_month_sep):
            log.debug(f"Adding {months[i]}")
            for person in month_list:
                birthdays.append(person)

        return birthdays
