import datetime
import random
import time

from bot.log import get_logger

log = get_logger(__name__)


def get_ordinal_number(num: int) -> str:
    """
    1 -> 1st
    2 -> 2nd
    3 -> 3rd
    15 -> 15th
    """
    return str(num) + {1: "st", 2: "nd", 3: "rd"}.get(
        4 if 10 <= num % 100 < 20 else num % 10, "th"
    )


def add_commas(num: int) -> str:
    """Adds commas to an integer in the international number format

    - 1000 -> 1,000
    - 100000 -> 100,000
    - 1000000 -> 1,000,000

    Args:
        num (int): The number

    Returns:
        str: The number with commas
    """
    return "{:,}".format(num)


def format_seconds(ms: int) -> str:
    """Formats milliseconds into min:sec:ms format"""
    sec, ms = divmod(ms, 1000)
    min, sec = divmod(sec, 60)

    return "%01d:%02d.%03d" % (min, sec, ms)


def get_random_color() -> int:
    """Get Random Color for Embed Colors

    Returns:
        int: The colour
    """
    return random.randint(0, 0xFFFFFF)


def split_list_of_lists(long_list: list, length: int = 5) -> list[list]:
    if len(long_list) <= length:
        log.debug("Original list size is smaller than length")
        return [long_list]

    return [long_list[i : i + length] for i in range(0, len(long_list), length)]


def timestamp() -> int:
    return int(time.time())


def timestamp_date(year: int, month: int, day: int) -> int:
    return int(datetime.datetime(year=year, month=month, day=day).timestamp())


def time_since(timestamp: int) -> str:
    minutes, seconds = divmod(timestamp() - timestamp, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365)

    return f"{years} years, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"


def get_times_run() -> int:
    with open("./bot/resources/times_run.txt", "r", encoding="UTF-8") as file:
        return int(file.read())
        
def format_time_split(split: str) -> str:
    split_str = str(split)
    
    ms_split = split_str.split('.')
    
    ms_seconds = ms_split[0]
    ms = ms_split[1]

    ms_format = ""

    if len(ms) == 3:
        ms_format = ms
    elif len(ms) == 2:
        ms_format = f"{ms}0"
    elif len(ms) == 1:
        ms_format = f"{ms}00"
        
    return f"{ms_seconds}.{ms_format}"
