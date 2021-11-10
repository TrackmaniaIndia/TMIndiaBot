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
        show_disabled=True,
        author_check=True,
    ):
        super().__init__()
        self.pages = pages
        self.current_page = 1
        self.page_count = len(self.pages)
        self.show_disabled = show_disabled
        self.forbutton = self.children[1]
        self.prevbutton = self.children[0]
        self.usercheck = author_check
        self.user = None

        log.debug(
            f"Created Paginator with {self.pages} pages, show_disabled={self.show_disabled} and author_check={self.usercheck}"
        )

        if not self.show_disabled:
            self.remove_item(self.children[0])
            if self.page_count == 1:
                self.remove_item(self.children[1])

    async def interaction_check(self, interaction: Interaction) -> bool:
        if self.usercheck:
            return self.user == interaction.user
        return True

    @discord.ui.button(label="<", style=discord.ButtonStyle.green, disabled=True)
    async def previous(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        log.debug(f'"Go Previous" button clicked')
        self.current_page -= 1

        if self.current_page == 1:
            log.debug(f"Current Page is 1 disabling previous button")
            button.disabled = True

        if not self.show_disabled:
            if len(self.children) == 1:
                log.debug(f'Adding Next button')
                self.add_item(self.forbutton)
                self.forbutton.disabled = False
            if button.disabled:
                log.debug(f"Button is disabled, removing the button")
                self.remove_item(button)
        else:
            self.children[1].disabled = False

        page = self.pages[self.current_page - 1]
        await interaction.response.edit_message(
            content=page if isinstance(page, str) else None,
            embed=page if isinstance(page, discord.Embed) else MISSING,
            view=self,
        )

    @discord.ui.button(label=">", style=discord.ButtonStyle.green)
    async def forward(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        log.debug(f'"Go Forward" button clicked')
        self.current_page += 1

        if self.current_page == self.page_count:
            log.debug(f'Current Page is Last Page, Disabling Button')
            button.disabled = True

        if not self.show_disabled:
            if len(self.children) == 1:
                log.debug(f'Adding Previous Button')
                self.add_item(self.prevbutton)
                self.prevbutton.disabled = False
                self.children[0], self.children[1] = self.children[1], self.children[0]
            if button.disabled:
                log.debug(f'Last Page, Removing Next Button')
                self.remove_item(button)
        else:
            self.children[0].disabled = False

        page = self.pages[self.current_page - 1]
        await interaction.response.edit_message(
            content=page if isinstance(page, str) else None,
            embed=page if isinstance(page, discord.Embed) else MISSING,
            view=self,
        )

    async def run(self, messageable: abc.Messageable, ephemeral: bool = False):
        log.debug(f'Running Paginator')
        if not isinstance(messageable, abc.Messageable):
            log.error(f'{messageable} is not abc.Messageable')
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

    def forward_button(self, label: str, color: str = "green"):
        log.debug(f'Changing Forward Button Label to {label} and color to {color}')
        self.forbutton.label = label
        color = getattr(discord.ButtonStyle, color.lower())
        self.forbutton.style = color

    def back_button(self, label: str, color: str = "green"):
        log.debug(f'Changing Back Button Label to {label} and color to {color}')
        self.prevbutton.label = label
        color = getattr(discord.ButtonStyle, color.lower())
        self.prevbutton.style = color
