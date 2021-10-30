import util.logging.convert_logging as convert_logging
import discord

log = convert_logging.get_logging()


def check_key(my_dict: dict, key: str) -> bool:
    """Checks key in my_dict

    Args:
        my_dict (dict): [description]
        key (str): [description]

    Returns:
        bool: [description]
    """
    try:
        if my_dict[key]:
            return True
        else:
            return False
    except KeyError or IndexError as e:
        return False


def get_ordinal_number(num: int) -> str:
    return str(num) + {1: "st", 2: "nd", 3: "rd"}.get(
        4 if 10 <= num % 100 < 20 else num % 10, "th"
    )


def add_commas(num: int) -> str:
    return "{:,}".format(num)
