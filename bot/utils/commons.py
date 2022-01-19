import random

from bot.log import get_logger

bot = get_logger(__name__)


class Commons:
    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def format_seconds(ms: int) -> str:
        """Formats milliseconds into min:sec:ms format"""
        sec, ms = divmod(ms, 1000)
        min, sec = divmod(sec, 60)

        return "%01d:%02d.%03d" % (min, sec, ms)

    @staticmethod
    def get_random_color() -> int:
        """Get Random Color for Embed Colors

        Returns:
            int: The colour
        """
        return random.randint(0, 0xFFFFFF)
