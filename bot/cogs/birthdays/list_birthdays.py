import json
import os

from discord import ApplicationContext
from discord.ext import commands
from discord.ext.pages import Paginator

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.birthdays import Birthday

log = get_logger(__name__)


class ListBirthdays(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        if not os.path.exists("./bot/resources/json/birthdays.json"):
            log.critical("birthdays.json file does not exist, creating")
            with open(
                "./bot/resources/json/birthdays.json", "w", encoding="UTF-8"
            ) as file:
                json.dump({"birthdays": []}, file, indent=4)

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="listbirthdays",
        description="Lists all the birthdays saved with the bot!",
    )
    async def _list_birthdays(
        self,
        ctx: ApplicationContext,
    ):
        log_command(ctx, "list_birthdays")

        log.debug("Getting Birthdays Embeds")
        birthdays_embeds = Birthday.list_birthdays()

        if len(birthdays_embeds) == 1:
            log.debug("There is only 1 Page")
            await ctx.respond(embed=birthdays_embeds[0], ephemeral=True)
        else:
            log.debug("There are multiple pages, creating Paginator")
            birthdays_paginator = Paginator(pages=birthdays_embeds)

            await birthdays_paginator.respond(ctx.interaction, ephemeral=True)


def setup(bot: Bot):
    bot.add_cog(ListBirthdays(bot))
