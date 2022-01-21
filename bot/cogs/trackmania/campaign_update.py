import discord
from discord.commands import Option
from discord.ext import commands

from bot import constants
from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import Confirmer
from bot.utils.discord import EZEmbed
from bot.utils.leaderboard import Leaderboards

log = get_logger(__name__)


class CampaignUpdate(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=[constants.Guild.testing_server],
        name="update_campaign_leaderboards",
        description="Updates the leaderboards for campaigns",
    )
    async def _update_campaign_leaderboards_slash(
        self,
        ctx: commands.Context,
        year: Option(str, "Choose the year", choices=["2020", "2021", "2022"]),
        season: Option(
            str, "Choose the season", choices=["Winter", "Spring", "Summer", "Fall"]
        ),
        firstfive: Option(
            str, "Want to Update the First Five as Well?", choices=["True", "False"]
        ),
    ):
        await ctx.defer()
        log_command(ctx, "update_campaign_leaderboards_slash")

        firstfive = bool(firstfive)
        log.info("Creating Confirmation Prompt")
        confirm_continue = Confirmer()

        # Changing the Button Labels
        log.debug("Changing Button Labels")
        confirm_continue.change_confirm_button(label="Yes, Continue")
        confirm_continue.change_cancel_button(label="No, Stop!")
        log.debug("changed Button Labels")

        # Sending the Confrirmation Prompt
        log.info("Sending Prompt")
        message = await ctx.respond(
            embed=EZEmbed.create_embed(
                title="Are you sure you want to continue?",
                description=f"This can take over 10 minutes, the bot will be unusable in this period\nYear: {year}\nSeason: {season}",
                color=0xFF0000,
            ),
            view=confirm_continue,
        )
        log.info("Sent Confirmation Prompt")

        # Awaiting for the Response to the Confirmation Prompt
        log.info("Awaiting a response")
        await confirm_continue.wait()
        log.info("Response Received")

        # Deleting the Confirmation Prompt
        log.info("Deleting Original Message")
        await message.delete()
        log.info("Deleted Message")

        # Checking if the Confirmation Prompt was Cancelled
        if confirm_continue.value is False:
            log.info(f"{ctx.author.name} does not want to continue")
            return

        log.info(f"{ctx.author.name} wants his username added")

        # Getting the Fall Campaign IDs
        log.info("Getting fall Campaign IDs")
        fall_ids = Leaderboards.get_campaign_ids(year=year, season=season)
        log.info("Got the Fall IDs")

        # Starting Long Update Process using a seperate Thread to allow bot to
        # complete other processes
        await Leaderboards.update_campaign_leaderboards(
            fall_ids, year, season, firstfive
        )

        # Sending a "Finished" message
        await ctx.send(
            embed=EZEmbed.create_embed(
                title=":white_check_mark: Success!",
                description=f"Leaderboard Updates for Year: {year} and Season: {season}",
                color=discord.Colour.green(),
            )
        )


def setup(bot: Bot):
    bot.add_cog(CampaignUpdate(bot))
