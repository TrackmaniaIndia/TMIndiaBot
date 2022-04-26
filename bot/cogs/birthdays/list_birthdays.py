import json
import os

import discord
from discord import ApplicationContext
from discord.ext import commands
from discord.ext.pages import Paginator

import bot.utils.birthdays as birthday
from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import create_embed

log = get_logger(__name__)


class ListBirthdays(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="list-birthdays",
        description="Lists all the birthdays saved with the bot!",
    )
    async def _list_birthdays(
        self,
        ctx: ApplicationContext,
    ):
        log_command(ctx, "list_birthdays")

        log.debug("Getting Birthdays Embeds")
        birthdays_embeds = birthday.list_birthdays(ctx.guild.id)

        if len(birthdays_embeds) == 1:
            try:
                log.debug("There is only 1 Page")
                await ctx.respond(embed=birthdays_embeds[0], ephemeral=True)
            except discord.HTTPException:
                await ctx.respond(
                    embed=create_embed(
                        title="No users are stored with the bot",
                        color=discord.Colour.red(),
                    )
                )
        else:
            log.debug("There are multiple pages, creating Paginator")
            birthdays_paginator = Paginator(pages=birthdays_embeds)

            await birthdays_paginator.respond(ctx.interaction, ephemeral=True)


def setup(bot: Bot):
    bot.add_cog(ListBirthdays(bot))
