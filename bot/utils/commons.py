import random

from bot.log import get_logger

bot = get_logger(__name__)


def get_ordinal_number(num: int) -> str:
    return str(num) + {1: "st", 2: "nd", 3: "rd"}.get(
        4 if 10 <= num % 100 < 20 else num % 10, "th"
    )


def add_commas(num: int) -> str:
    return "{:,}".format(num)


def format_seconds(ms: int) -> str:
    sec, ms = divmod(ms, 1000)
    min, sec = divmod(sec, 60)

    return "%01d:%02d.%03d" % (min, sec, ms)


def get_random_color() -> int:
    """Get Random Color for Embed Colors

    Returns:
        int: [description]
    """
    return random.randint(0, 0xFFFFFF)
