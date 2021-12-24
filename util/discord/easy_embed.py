from datetime import datetime, timezone, timedelta
from util import common_functions
from util.logging import convert_logging
import discord

log = convert_logging.get_logging()


def create_embed(
    title: str, description: str = "", color: str = None, url: str = None
) -> discord.Embed:
    """Creates an Embed with Basic Data Fields Filled Out

    Args:
        title (str): Title of the Embed
        description (str, optional): Description of the Embed. Defaults to None.
        color (str, optional): Color of the Embed. Defaults to None.
        url (str, url): Url to be added to the embed

    Returns:
        discord.Embed: Final Embed Returned with Data Fields Inside
    """
    if color is None:
        log.debug("Colour is None, Assigning Random Colour")
        color = common_functions.get_random_color()

    # Creates an Embed with the Given Title, Description and Color
    log.debug(
        f"Creating Embed with Title - {title}, description - {description} and colour - {color}"
    )
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        url=discord.Embed.Empty if url is None else url,
    )

    # Adds the timestamp the embed was created on
    embed.timestamp = datetime.now(timezone(timedelta(hours=5, minutes=30)))

    log.debug(f"Returning {embed}")
    return embed
