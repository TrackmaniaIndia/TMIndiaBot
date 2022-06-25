import os

import discord.ext.commands as commands
from discord import Guild

import bot.utils.checks as checks
from bot.bot import Bot
from bot.log import get_logger

log = get_logger(__name__)


class GuildJoinStuff(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        log.critical("Bot joined %s with ID %s", guild.name, guild.id)

        log.info("Creating Folders and required files for %s", guild.name)
        if os.path.exists(f"./bot/resources/guild_data/{guild.id}/"):
            log.info("The guild already has a folder")
        else:
            log.info("Creating folder for %s", guild.name)
            os.mkdir(f"./bot/resources/guild_data/{guild.id}/")

        checks.create_config(guild.id)
        checks.create_quotes(guild.id)
        checks.create_trophy_tracking(guild.id)
        checks.create_birthdays(guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        log.critical(
            "Bot has left/been kicked out of %s with id %s", guild.name, guild.id
        )
        return


def setup(bot: Bot):
    bot.add_cog(GuildJoinStuff(bot))
