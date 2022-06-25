import json

import discord.ext.commands as commands
from discord import ApplicationContext, Option, SlashCommandOptionType

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.moderation import send_in_mod_logs

log = get_logger(__name__)


class SetupBirthday(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="set-birthday-channel",
        description="Set a channel to send birthday messages in for your server",
    )
    @commands.has_permissions(manage_guild=True)
    async def _set_birthday_channel(
        self,
        ctx: ApplicationContext,
        birthday_channel: Option(
            SlashCommandOptionType.channel,
            "The channel for the birthday messages",
            required=True,
        ),
    ):
        log_command(ctx, "set_birthday_channel")
        await ctx.defer()

        log.info(
            "Setting birthdays_channel of %s to %s",
            ctx.guild.name,
            birthday_channel.name,
        )

        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/config.json",
            "r",
            encoding="UTF-8",
        ) as file:
            config = json.load(file)

        config["birthdays_channel"] = birthday_channel.id

        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/config.json",
            "w",
            encoding="UTF-8",
        ) as file:
            json.dump(config, file, indent=4)

        await send_in_mod_logs(
            self.bot,
            ctx.guild.id,
            msg=f"Birthdays channel set to {birthday_channel.mention} by {ctx.author.mention}",
        )
        await ctx.respond(
            f"Birthday channel has been set to {birthday_channel.mention}",
            delete_after=10,
        )


def setup(bot: Bot):
    bot.add_cog(SetupBirthday(bot))
