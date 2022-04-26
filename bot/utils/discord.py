import json
import typing
from datetime import datetime, timedelta, timezone
from typing import List

import discord
from discord import ButtonStyle, TextChannel

import bot.utils.commons as commons
from bot.bot import Bot
from bot.log import get_logger

log = get_logger(__name__)


class Confirmer(discord.ui.View):
    """Creates a confirmation prompt that returns a True or False value"""

    def __init__(self):
        super().__init__()
        self.value = None
        self.confirm_button = self.children[0]
        self.cancel_button = self.children[1]
        log.debug("Created Confirmation Menu")

    @discord.ui.button(label="Confirm", style=ButtonStyle.green)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        """If this button is clicked, prompt returns a True value
        Args:
            button (discord.ui.Button): The button that was clicked
            interaction (discord.Interaction): The interaction that was being used
        """
        log.debug(
            f"Confirm Button Clicked by {interaction.user.name} in {interaction.guild.name} in channel {interaction.channel.name}"
        )
        self.value = True
        self.stop()

    @discord.ui.button(label="Cancel", style=ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        """If this button is clicked, prompt returns a False value
        Args:
            button (discord.ui.Button): The button that was clicked
            interaction (discord.Interaction): The interaction that was being used
        """
        log.debug(
            f"Cancel Button Clicked by {interaction.user.name} in {interaction.guild.name} in channel {interaction.channel.name}"
        )
        self.value = False
        self.stop()

    def change_confirm_button(self, label: str, color: str = "green"):
        """Changes the label and color of the confirmation button to help with customizability
        Args:
            label (str): Label of the button
            color (str, optional): Color of the button, only a few possible values. Defaults to "green".
        """
        log.debug(f"Changing Confirm Button to Label: {label} and Color: {color}")
        self.confirm_button.label = label
        self.confirm_button.style = getattr(ButtonStyle, color.lower())

    def change_cancel_button(self, label: str, color: str = "red"):
        """Changes the label and color of the cancel button to help with customizability
        Args:
            label (str): Label of the button
            color (str, optional): Color of the button, only a few possible values. Defaults to "red".
        """
        log.debug(f"Changing Cancel Button to Label: {label} and color: {color}")
        self.cancel_button.label = label
        self.cancel_button.style = getattr(ButtonStyle, color.lower())


def create_embed(
    title: str = None,
    description: str = "",
    color: typing.Union[int, discord.Colour] = None,
    url: str = None,
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
        color = commons.get_random_color()

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


class ViewAdder(discord.ui.View):
    def __init__(self, buttons: List[discord.ui.Button]):
        super().__init__()

        for button in buttons:
            self.add_item(button)


def get_mod_logs_channel(bot: Bot, guild_id: int) -> TextChannel | None:
    """Returns mod-logs channel of the given guild_id

    Args:
        bot (Bot): The bot object.
        guild_id (int): The guild id

    Returns:
        TextChannel | None: TextChannel is returned if the mod-logs channel is set and is not Forbidden. None is sent if mod-logs channel
                            is not set or if `discord.errors.Forbidden` is raised.
    """
    log.debug("Getting mod-logs channel for %s", guild_id)

    with open(
        f"./bot/resources/guild_data/{guild_id}/config.json", "r", encoding="UTF-8"
    ) as file:
        config_data = json.load(file)

    if config_data.get("mod_logs_channel", 0) == 0:
        return None
    else:
        try:
            return bot.get_channel(config_data.get("mod_logs_channel"))
        except discord.errors.Forbidden:
            return None
