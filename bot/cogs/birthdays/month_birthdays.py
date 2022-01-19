import os
import json

import discord
from discord.ext import commands
from discord.commands import Option

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot import constants
from bot.utils.birthdays import Birthday

log = get_logger(__name__)


class MonthBirthdays(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = Bot

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="birthdaysofmonth",
        description="Lists all the birthdays of a specific month saved with the bot!",
    )
    async def _month_birthdays_slash(
        self,
        ctx: commands.Context,
        month: Option(str, "The month", choices=constants.Consts.months, required=True),
    ):
        log_command(ctx, "month_birthdays_slash")

        birthdays_embeds = Birthday.month_birthdays(
            month=constants.Consts.months.index(month)
        )

        if birthdays_embeds is None:
            await ctx.respond(
                f"That month does not have any birthdays -> {month}\nIf this message is wrong please use the `addbirthday` command to add your birthday"
            )
        elif len(birthdays_embeds) == 1:
            await ctx.respond(embed=birthdays_embeds[0], ephemeral=True)
        else:
            birthdays_paginator = Paginator(pages=birthdays_embeds)

            await birthdays_paginator.respond(ctx.interaction, ephemeral=True)


def setup(bot: Bot):
    bot.add_cog(MonthBirthdays(bot))