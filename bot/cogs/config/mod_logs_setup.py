import json

import discord.ext.commands as commands
from discord import ApplicationContext, SlashCommandOptionType
from discord.commands import Option

from bot.bot import Bot
from bot.log import get_logger, log_command

log = get_logger(__name__)


class SetupModLogs(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # TODO: Set permissions. ManageServer
    @commands.slash_command(
        name="set-mod-logs",
        description="Set a mod logs channel",
    )
    @commands.has_permissions(manage_guild=True)
    async def _set_mod_logs(
        self,
        ctx: ApplicationContext,
        channel: Option(
            SlashCommandOptionType.channel,
            "The channel to send moderator logs",
            required=True,
        ),
    ):
        log_command(ctx, "set_mod_logs")

        await ctx.defer()

        log.info(
            "Saving mod-logs channel %s for guild %s", channel.name, ctx.guild.name
        )
        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/config.json",
            "r",
            encoding="UTF-8",
        ) as file:
            config_data = json.load(file)

        config_data["mod_logs_channel"] = channel.id

        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/config.json",
            "w",
            encoding="UTF-8",
        ) as file:
            json.dump(config_data, file, indent=4)

        log.info("Stored ModLogs channel for %s", ctx.guild.name)
        await ctx.respond(
            f"Stored ModLogs channel for {ctx.guild.name} as {channel.name}",
            delete_after=10,
        )

    @commands.slash_command(
        name="remove-mod-logs",
        description="Remove the mod logs channel set for this guild",
    )
    @commands.has_permissions(manage_guild=True)
    async def _remove_mod_logs(self, ctx: ApplicationContext):
        log_command(ctx, "remove_mod_logs")

        await ctx.defer()

        log.info("Removed mod-logs channel for guild %s", ctx.guild.name)
        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/config.json",
            "r",
            encoding="UTF-8",
        ) as file:
            config_data = json.load(file)

        config_data["mod_logs_channel"] = 0

        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/config.json",
            "w",
            encoding="UTF-8",
        ) as file:
            json.dump(config_data, file, indent=4)

        log.info("Removed ModLogs channel for %s", ctx.guild.name)
        await ctx.respond(
            f"Removed ModLogs channel for {ctx.guild.name}", delete_after=10
        )


def setup(bot: Bot):
    bot.add_cog(SetupModLogs(bot))
