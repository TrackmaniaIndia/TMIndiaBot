import json

import discord
from discord import ApplicationContext, Option, SlashCommandOptionType
from discord.ext import commands

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.moderation import send_in_mod_logs

log = get_logger(__name__)


class UpdatesSetup(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="set-updates-channel",
        description="Set a channel for the bot to send updates to.",
    )
    @commands.has_permissions(manage_guild=True)
    async def _set_updates_channel(
        self,
        ctx: ApplicationContext,
        updates_channel: Option(
            SlashCommandOptionType.channel,
            description="The channel where the bot sends the messages.",
            required=True,
        ),
    ):
        log_command(ctx, "set_updates_channel")

        updates_channel: discord.TextChannel = updates_channel

        await ctx.defer(ephemeral=True)

        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/config.json",
            "r",
            encoding="UTF-8",
        ) as file:
            config_data = json.load(file)

        config_data["announcement_channel"] = updates_channel.id

        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/config.json",
            "w",
            encoding="UTF-8",
        ) as file:
            json.dump(config_data, file, indent=4)

        await send_in_mod_logs(
            self.bot,
            ctx.guild.id,
            msg=f"The announcement channel has been set to {updates_channel.mention} by {ctx.author.mention}.",
        )

        await ctx.respond(
            f"The bot will now send updates to {updates_channel.mention}.",
            ephemeral=True,
        )


def setup(bot: Bot):
    bot.add_cog(UpdatesSetup(bot))
