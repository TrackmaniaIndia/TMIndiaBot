import discord
import matplotlib.pyplot as plt
from discord import ApplicationContext, SlashCommandOptionType
from discord.commands import Option
from discord.ext import commands
from discord.ext.pages import Paginator
from trackmania import Campaign

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import create_embed

log = get_logger(__name__)


class CurrentCampaign(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="Current-Campaign",
        deescription="Displays the detaails of the current Nadeo campaign.",
    )
    async def _current_campaign(self, ctx: ApplicationContext):
        log_command(ctx, "current_campaign")


def setup(bot: Bot):
    bot.add_cog(CurrentCampaign(bot))
