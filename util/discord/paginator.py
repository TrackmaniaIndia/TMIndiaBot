import discord
import asyncio
from typing import Union, List

from discord import message
import util.logging.convert_logging as convert_logging

from discord import abc
from discord.interactions import Interaction
from discord.utils import MISSING
from discord.ui.button import button
from discord.commands import ApplicationContext
from discord.ext.commands import Context

log = convert_logging.get_logging()


class Paginate(discord.ui.View):
    def __init__(
        self,
        pages: Union[List[str], List[discord.Embed]],
        author_check=True,
    ):
        super().__init__()
        self.pages = pages
        self.current_page = 1
        self.page_count = len(self.pages)
        self.go_first = self.children[0]
        self.previous_button = self.children[1]
        self.forward_button = self.children[2]
        self.go_last = self.children[3]
        self.usercheck = author_check
        self.user = None

        log.debug(
            f"Created Paginator with {self.pages} pages, show_disabled={self.show_disabled} and author_check={self.usercheck}"
        )

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.usercheck:
            return self.user == interaction.user
        return True

    @discord.ui.button(label="|<<", style=discord.ButtonStyle.green)
    async def go_to_start(
        self, button: discord.ui.Button, interaction: discord.Interaction, disabled=True
    ):
        log.debug(
            f'"Go First" button clicked for {interaction} by {interaction.user.display_name} in channel {interaction.channel.name} in guild {interaction.guild.name}'
        )
        self.current_page = 1

        log.debug(f"Disabling Previous Button")
        self.previous_button.disabled = True
        log.debug(f"Disabling Go To Start Button")
        button.disabled = True

        self.children[2].disabled = False
        self.children[3].disabled = False

        page = self.pages[self.current_page - 1]
        await interaction.response.edit_message(
            content=page if isinstance(page, str) else None,
            embed=page if isinstance(page, discord.Embed) else MISSING,
            view=self,
        )

    @discord.ui.button(label="⬅", style=discord.ButtonStyle.green, disabled=True)
    async def previous(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        log.debug(
            f'"Go Previous" button clicked for {interaction} by {interaction.user.display_name} in channel {interaction.channel.name} in guild {interaction.guild.name}'
        )
        self.current_page -= 1

        if self.current_page == 1:
            log.debug(f"Current Page is 1 disabling previous button and gofirst button")
            self.go_first.disabled = True
            button.disabled = True

        self.children[2].disabled = False
        self.children[3].disabled = False

        page = self.pages[self.current_page - 1]
        await interaction.response.edit_message(
            content=page if isinstance(page, str) else None,
            embed=page if isinstance(page, discord.Embed) else MISSING,
            view=self,
        )

    @discord.ui.button(label="➞", style=discord.ButtonStyle.green)
    async def forward(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        log.debug(
            f'"Go Forward" button clicked for {interaction} by {interaction.user.display_name} in channel {interaction.channel.name} in guild {interaction.guild.name}'
        )
        self.current_page += 1

        if self.current_page == self.page_count:
            log.debug(f"Current Page is Last Page, Disabling Button and GoLast Button")
            self.go_last.disabled = True
            button.disabled = True

        self.children[1].disabled = False
        self.children[0].disabled = False

        page = self.pages[self.current_page - 1]
        await interaction.response.edit_message(
            content=page if isinstance(page, str) else None,
            embed=page if isinstance(page, discord.Embed) else MISSING,
            view=self,
        )

    @discord.ui.button(label=">>|", style=discord.ButtonStyle.green)
    async def go_to_end(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        log.debug(
            f'"Go Last" button clicked for {interaction} by {interaction.user.display_name} in channel {interaction.channel.name} in guild {interaction.guild.name}'
        )
        self.current_page = len(self.pages)

        log.debug(f"Disabling Forward Button")
        self.forward_button.disabled = True
        log.debug(f"Disabling Go Last Button")
        button.disabled = True

        self.children[1].disabled = False
        self.children[0].disabled = False

        page = self.pages[self.current_page - 1]
        await interaction.response.edit_message(
            content=page if isinstance(page, str) else None,
            embed=page if isinstance(page, discord.Embed) else MISSING,
            view=self,
        )

    async def run(self, messageable: abc.Messageable, ephemeral: bool = False):
        log.debug(f"Running Paginator")
        if not isinstance(messageable, abc.Messageable):
            log.error(f"{messageable} is not abc.Messageable")
            raise TypeError("messageable should be a subclass of abc.Messageable")

        page = self.pages[0]

        if isinstance(messageable, (ApplicationContext, Context)):
            self.user = messageable.author

        if isinstance(messageable, ApplicationContext):
            message = await messageable.respond(
                content=page if isinstance(page, str) else None,
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

    def next_button(self, label: str, color: str = "green"):
        log.debug(f"Changing Forward Button Label to {label} and color to {color}")
        self.forward_button.label = label
        color = getattr(discord.ButtonStyle, color.lower())
        self.forward_button.style = color

    def back_button(self, label: str, color: str = "green"):
        log.debug(f"Changing Back Button Label to {label} and color to {color}")
        self.previous_button.label = label
        color = getattr(discord.ButtonStyle, color.lower())
        self.previous_button.style = color

    def first_button(self, label: str, color: str = "green"):
        log.debug(f"Changing First Button Label to {label} and color to {color}")
        self.go_first.label = label
        self.go_first.style = getattr(discord.ButtonStyle, color.lower())

    def last_button(self, label: str, color: str = "green"):
        log.debug(f"Changing Last Button Label to {label} and color to {color}")
        self.go_last.label = label
        self.go_last.style = getattr(discord.ButtonStyle, color.lower())
