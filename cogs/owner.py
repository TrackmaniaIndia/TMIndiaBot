import discord
import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed
import os

from discord.ext import commands
from discord.commands import permissions
from util.constants import GUILD_IDS

log = convert_logging.get_logging()


class Owner(commands.Cog, description="Owner Commands"):
    def __init__(self, client: discord.Bot):
        self.client = client

        log.debug(f"cogs.owner has finished initializing")

    # @commands.slash_command(
    #     guild_ids=GUILD_IDS, name="reloadall", description="Reloads all cogs"
    # )
    # @permissions.is_owner()
    # async def _reload(self, ctx: commands.Context):
    #     # Reloading Cogs
    #     log.info("Reloading Slash Cogs")
    #     for filename in os.listdir("./cogs"):
    #         if filename == "cogs.owner.py":
    #             continue
    #         if filename.endswith(".py"):
    #             log.info(f"Reloading cogs.{filename[:-3]}")
    #             self.client.reload_extension(f"cogs.{filename[:-3]}")
    #     log.info("Reloaded Slash Cogs")


def setup(client: discord.Bot):
    client.add_cog(Owner(client))
