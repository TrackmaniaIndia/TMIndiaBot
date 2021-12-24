from typing import List, Union

import discord
from discord import abc
from discord.commands import ApplicationContext
from discord.ext.commands import Context
from discord.interactions import Interaction
from discord.utils import MISSING

import util.discord.easy_embed as ezembed
from util.logging import convert_logging

log = convert_logging.get_logging()


class Paginator(discord.ui.View):
    """A paginator is a useful tool for discord bots that allows you to put multiple messages/embeds in a single message."""

    def __init__(
        self,
        pages: Union[List[str], List[discord.Embed]],
        author_check=True,
        sending=False,
    ):
        super().__init__()
        self.pages = pages
        self.current_page = 1
        self.page_count = len(self.pages)
        self.go_first = self.children[0]
        self.previous_button = self.children[1]
        self.forward_button = self.children[2]
        self.go_last = self.children[3]
        self.end = self.children[4]
        self.user_check = author_check
        self.user = None
        self.send = sending

        log.debug(
            f"Created Paginator with {self.pages} pages and author_check={self.user_check}"
        )

    async def interaction_check(self, interaction: Interaction) -> bool:
        """Checks if the interaction was used by the creater of the original command

        Args:
            interaction (Interaction): The interaction

        Returns:
            bool: a True or False value depending on whether it was the owner who used the command
        """
        if self.user_check:
            return self.user == interaction.user
        return True

    @discord.ui.button(label="⭅", style=discord.ButtonStyle.primary, disabled=True)
    async def go_to_start(
        self, button: discord.ui.Button, interaction: discord.Interaction, disabled=True
    ):
        """This button takes the userto the first page of the paginator

        Args:
            button (discord.ui.Button)
            interaction (discord.Interaction)
            disabled (bool, optional): Whether the button is disabled or not. Defaults to True.
        """
        log.debug(
            f'"Go First" button clicked for {interaction} by {interaction.user.display_name} in channel {interaction.channel.name} in guild {interaction.guild.name}'
        )
        # The page the bot is currently on
        self.current_page = 1

        # Because the bot is on the first page, we can disable the go first and back buttons as they are not useful
        log.debug("Disabling Previous Button")
        self.previous_button.disabled = True
        log.debug("Disabling Go To Start Button")
        button.disabled = True

        self.children[2].disabled = False
        self.children[3].disabled = False

        # Editing the message to display the first page
        page = self.pages[self.current_page - 1]
        await interaction.response.edit_message(
            content=page if isinstance(page, str) else None,
            embed=page if isinstance(page, discord.Embed) else MISSING,
            view=self,
        )

    @discord.ui.button(label="⟸", style=discord.ButtonStyle.primary, disabled=True)
    async def previous(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        """Takes the user back one page in the Paginator

        Args:
            button (discord.ui.Button)
            interaction (discord.Interaction)
        """
        log.debug(
            f'"Go Previous" button clicked for {interaction} by {interaction.user.display_name} in channel {interaction.channel.name} in guild {interaction.guild.name}'
        )

        # Since the bot goes back one page, we subtract one page from the current page
        self.current_page -= 1

        # Checks if the current page is the first page, if it is we have to disable the go first and back buttons
        if self.current_page == 1:
            log.debug("Current Page is 1 disabling previous button and gofirst button")
            self.go_first.disabled = True
            button.disabled = True

        self.children[2].disabled = False
        self.children[3].disabled = False

        # Editing the message to display the previous page
        page = self.pages[self.current_page - 1]
        await interaction.response.edit_message(
            content=page if isinstance(page, str) else None,
            embed=page if isinstance(page, discord.Embed) else MISSING,
            view=self,
        )

    @discord.ui.button(label="⟹", style=discord.ButtonStyle.primary)
    async def forward(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        """Takes the user forward one page in the Paginator

        Args:
            button (discord.ui.Button)
            interaction (discord.Interaction)
        """
        log.debug(
            f'"Go Forward" button clicked for {interaction} by {interaction.user.display_name} in channel {interaction.channel.name} in guild {interaction.guild.name}'
        )

        # Since the bot is moving forwards, we have to add one to the current page.
        self.current_page += 1

        # Checks if the bot is on the last page, if it is we have to disable the Forward and Go Last buttons
        if self.current_page == self.page_count:
            log.debug("Current Page is Last Page, Disabling Button and GoLast Button")
            self.go_last.disabled = True
            button.disabled = True

        self.children[1].disabled = False
        self.children[0].disabled = False

        # Editing the message to display the next page
        page = self.pages[self.current_page - 1]
        await interaction.response.edit_message(
            content=page if isinstance(page, str) else None,
            embed=page if isinstance(page, discord.Embed) else MISSING,
            view=self,
        )

    @discord.ui.button(label="⭆", style=discord.ButtonStyle.primary)
    async def go_to_end(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        """Takes the user to the last page of the Paginator

        Args:
            button (discord.ui.Button)
            interaction (discord.Interaction)
        """
        log.debug(
            f'"Go Last" button clicked for {interaction} by {interaction.user.display_name} in channel {interaction.channel.name} in guild {interaction.guild.name}'
        )

        # Since the bot is on the last page, we have to disable the forward and last buttons
        self.current_page = len(self.pages)

        log.debug("Disabling Forward Button")
        self.forward_button.disabled = True
        log.debug("Disabling Go Last Button")
        button.disabled = True

        self.children[1].disabled = False
        self.children[0].disabled = False

        # Editing the message to display the last page
        page = self.pages[self.current_page - 1]
        await interaction.response.edit_message(
            content=page if isinstance(page, str) else None,
            embed=page if isinstance(page, discord.Embed) else MISSING,
            view=self,
        )

    @discord.ui.button(label="⤫", style=discord.ButtonStyle.red)
    async def kill_switch(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        """Removes all the buttons from the Paginator, essentially killing it.

        Args:
            button (discord.ui.Button)
            interaction (discord.Interaction)
        """
        log.debug(
            f"Kill Switch Received for {interaction} by {interaction.user.display_name} in channel {interaction.channel.name} in guild {interaction.guild.name}"
        )

        # The kill switch removes all buttons from the paginator to effectively kill it
        # We have to remove all the buttons from the paginator, so we first disable them all and then remove them.

        log.debug("Disabling all Buttons")
        self.go_first.disabled = True
        self.previous_button.disabled = True
        self.forward_button.disabled = True
        self.go_last.disabled = True
        self.end.disabled = True
        log.debug("Disabled all Buttons, Removing")

        self.remove_item(self.go_first)
        self.remove_item(self.previous_button)
        self.remove_item(self.forward_button)
        self.remove_item(self.go_last)
        self.remove_item(self.end)
        log.debug("Removed all buttons")

        page = ezembed.create_embed(
            title="**This Interaction has Ended**", color=0xFF0000
        )
        await interaction.response.edit_message(
            embed=page,
            view=self,
        )

    async def run(self, messageable: abc.Messageable, ephemeral: bool = False):
        """Runs the Paginator"""

        # Runs the paginator
        log.debug("Running Paginator")
        if not isinstance(messageable, abc.Messageable):
            log.error(f"{messageable} is not abc.Messageable")
            raise TypeError("messageable should be a subclass of abc.Messageable")

        # Takes the first page to display it
        page = self.pages[0]

        if isinstance(messageable, (ApplicationContext, Context)):
            self.user = messageable.author

        if isinstance(messageable, ApplicationContext):
            if not self.send:
                message = await messageable.respond(
                    content=page if isinstance(page, str) else None,
                    embed=page if isinstance(page, discord.Embed) else MISSING,
                    view=self,
                )
            else:
                message = await messageable.send(
                    content=page
                    if isinstance(page, str)
                    else messageable.author.mention,
                    embed=page if isinstance(page, discord.Embed) else MISSING,
                    view=self,
                )
        else:
            message = await messageable.send(
                content=page if isinstance(page, str) else None,
                embed=page if isinstance(page, discord.Embed) else MISSING,
                view=self,
            )
        return message

    def next_button(self, label: str, color: str = "primary"):
        """Changes the Label and Color of the Next Button

        Args:
            label (str): The label of the button
            color (str, optional): The colour of the button. Defaults to "primary".
        """
        log.debug(f"Changing Forward Button Label to {label} and color to {color}")
        self.forward_button.label = label
        color = getattr(discord.ButtonStyle, color.lower())
        self.forward_button.style = color

    def back_button(self, label: str, color: str = "primary"):
        """Changes the Label and Color of the Back Button

        Args:
            label (str): The label of the back button
            color (str, optional): The colour of the back button. Defaults to "primary".
        """
        log.debug(f"Changing Back Button Label to {label} and color to {color}")
        self.previous_button.label = label
        color = getattr(discord.ButtonStyle, color.lower())
        self.previous_button.style = color

    def first_button(self, label: str, color: str = "primary"):
        """Changes the Label and Color of the Go First Button

        Args:
            label (str): The label of the Go First button
            color (str, optional): The colour of the Go First button. Defaults to "primary".
        """
        log.debug(f"Changing First Button Label to {label} and color to {color}")
        self.go_first.label = label
        self.go_first.style = getattr(discord.ButtonStyle, color.lower())

    def last_button(self, label: str, color: str = "primary"):
        """Changes the Label and Color of the Go Back Button

        Args:
            label (str): The label of the Go Back button
            color (str, optional): The colour of the Go Back button. Defaults to "primary".
        """
        log.debug(f"Changing Last Button Label to {label} and color to {color}")
        self.go_last.label = label
        self.go_last.style = getattr(discord.ButtonStyle, color.lower())
