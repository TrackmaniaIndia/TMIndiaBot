from discord import ApplicationContext, SlashCommandOptionType
from discord.commands import Option
from discord.ext import commands
from discord.ext.pages import Paginator

import bot.utils.birthdays as birthday
from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command

log = get_logger(__name__)


class MonthBirthdays(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="birthdays-of-month",
        description="Lists all the birthdays of a specific month saved with the bot!",
    )
    async def _month_birthdays(
        self,
        ctx: ApplicationContext,
        month: Option(
            SlashCommandOptionType.string,
            "The month",
            choices=constants.Consts.months,
            required=True,
        ),
    ):
        log_command(ctx, "month_birthdays")

        birthdays_embeds = birthday.month_birthdays(
            month=constants.Consts.months.index(month),
            guild_id=ctx.guild.id,
        )

        if birthdays_embeds is None:
            await ctx.respond(
                f"That month does not have any birthdays -> {month}\nIf this message is wrong please use the `addbirthday` command to add your birthday",
                ephemeral=True,
            )
        elif len(birthdays_embeds) == 1:
            await ctx.respond(embed=birthdays_embeds[0], ephemeral=True)
        else:
            log.debug("Creating birthdays paginator")
            birthdays_paginator = Paginator(pages=birthdays_embeds, timeout=60)

            log.debug("Responding with birthdays paginator")
            await birthdays_paginator.respond(ctx.interaction, ephemeral=True)
            log.debug("Birthdays paginator finished")


def setup(bot: Bot):
    bot.add_cog(MonthBirthdays(bot))
