# To setup COTD and Super Royal reminders for a guild.
import json

from click import confirm
from discord import ApplicationContext, Option
from discord.ext import commands

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import Confirmer

log = get_logger(__name__)


class SetupReminders(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Create config command that allows setting of a custom role to ping upon reminder trigger.

    # Check if the user has the manage-server permission
    @commands.slash_command(
        name="setup-cotd-reminders",
        description="Start the setup process for COTD Reminders",
    )
    @commands.has_permissions(manage_guild=True)
    async def _setup_cotd_reminders(
        self,
        ctx: ApplicationContext,
        main_cotd: Option(
            str,
            "Whether to be reminded for the main COTD at xx:xxUTC",
            choices=["Yes", "No"],
            required=True,
        ),
        first_rerun: Option(
            str,
            "Whether to be reminded for the first COTD rerun at xx:xxUTC",
            choices=["Yes", "No"],
            required=True,
        ),
        second_rerun: Option(
            str,
            "Whether to be reminded for the second COTD rerun at xx:xxUTC",
            choices=["Yes", "No"],
            required=True,
        ),
    ):
        log_command(ctx, "setup_cotd_reminders")

        log.info("Starting setup process for %s", ctx.guild.name)
        await ctx.defer()

        # Confirm where the reminders should be sent.
        log.debug("Creating Confirmation for channel selection.")
        confirmer = Confirmer()
        confirmer.change_confirm_button(label="Yes!")
        confirmer.change_cancel_button(label="No!")

        message = await ctx.respond(
            "Is this the channel where you want your server's COTD reminders to be sent?\nIf this is not the channel you want, please re-run the command in that specific channel.\nIf you click `No` you will be unsubscribed from all reminders.",
            view=confirmer,
        )
        await confirmer.wait()
        await message.delete()
        log.debug("Finished Confirmation for channel selection.")

        if confirmer.value is None:
            log.info("Confirmation Timed Out")
            await ctx.send("Timed Out...", delete_after=10)
        elif not confirmer.value:
            log.info("Setup Declined")
            self.__save_settings(
                False, ctx.guild.id, 0, main_cotd, first_rerun, second_rerun, False
            )
            await ctx.send(
                f"Settings Saved!\nYou have unsubscribed from COTD Reminders.\nGuild Name: {ctx.guild.name} Channel Name: {ctx.channel.name}",
                delete_after=10,
            )
        elif confirmer.value:
            log.info("Setup Accepted")
            self.__save_settings(
                True,
                ctx.guild.id,
                ctx.channel.id,
                main_cotd,
                first_rerun,
                second_rerun,
                False,
            )
            await ctx.send(
                f"Settings Saved!\nYou have subscribed to COTD Reminders.\nGuild Name: {ctx.guild.name} Channel Name: {ctx.channel.name}",
                delete_after=10,
            )
            log.info(
                "Saved Settings. Main: %s, First Rerun: %s, Second Rerun: %s",
                main_cotd,
                first_rerun,
                second_rerun,
            )

    @commands.slash_command(
        name="setup-royal-reminders",
        description="Start the setup process for Royal Reminders",
    )
    @commands.has_permissions(manage_guild=True)
    async def _setup_royal_reminders(
        self,
        ctx: ApplicationContext,
        main_royal: Option(
            str,
            "Whether to be reminded for the main Royal at xx:xxUTC",
            choices=["Yes", "No"],
            required=True,
        ),
        first_rerun: Option(
            str,
            "Whether to be reminded for the first Royal rerun at xx:xxUTC",
            choices=["Yes", "No"],
            required=True,
        ),
        second_rerun: Option(
            str,
            "Whether to be reminded for the second Royal rerun at xx:xxUTC",
            choices=["Yes", "No"],
            required=True,
        ),
    ):
        log_command(ctx, "setup_cotd_reminders")

        log.info("Starting setup process for %s", ctx.guild.name)
        await ctx.defer()

        # Confirm where the reminders should be sent.
        log.debug("Creating Confirmation for channel selection.")
        confirmer = Confirmer()
        confirmer.change_confirm_button(label="Yes!")
        confirmer.change_cancel_button(label="No!")

        message = await ctx.respond(
            "Is this the channel where you want your server's Royal reminders to be sent?\nIf this is not the channel you want, please re-run the command in that specific channel.\nIf you click `No` you will be unsubscribed from all reminders.",
            view=confirmer,
        )
        await confirmer.wait()
        await message.delete()
        log.debug("Finished Confirmation for channel selection.")

        if confirmer.value is None:
            log.info("Confirmation Timed Out")
            await ctx.send("Timed Out...", delete_after=10)
        elif not confirmer.value:
            log.info("Setup Declined")
            self.__save_settings(
                False, ctx.guild.id, 0, main_royal, first_rerun, second_rerun, True
            )
            await ctx.send(
                f"Settings Saved!\nYou have unsubscribed from Royal Reminders.\nGuild Name: {ctx.guild.name} Channel Name: {ctx.channel.name}",
                delete_after=10,
            )
        elif confirmer.value:
            log.info("Setup Accepted")
            self.__save_settings(
                True,
                ctx.guild.id,
                ctx.channel.id,
                main_royal,
                first_rerun,
                second_rerun,
                True,
            )
            await ctx.send(
                f"Settings Saved!\nYou have subscribed to Royal Reminders.\nGuild Name: {ctx.guild.name} Channel Name: {ctx.channel.name}",
                delete_after=10,
            )
            log.info(
                "Saved Settings. Main: %s, First Rerun: %s, Second Rerun: %s",
                main_royal,
                first_rerun,
                second_rerun,
            )

    def __save_settings(
        self,
        subscribe: bool,
        guild_id: int,
        channel_id: int,
        main: str = "No",
        first_rerun: str = "No",
        second_rerun: str = "No",
        royal: bool = False,
    ):
        # Converting string flags to booleans
        if main.lower() == "no":
            main = False
        else:
            main = True

        if first_rerun.lower() == "no":
            first_rerun = False
        else:
            first_rerun = True

        if second_rerun.lower() == "no":
            second_rerun = False
        else:
            second_rerun = True

        # if `subscribe` is false then channel_id should be zero
        if not subscribe:
            channel_id = 0

        # Getting the config file.
        with open(
            f"./bot/resources/guild_data/{guild_id}/config.json", "r", encoding="UTF-8"
        ) as file:
            config_data = json.load(file)

        # Checking if it was called from `/setup-cotd-tracking` or `/setup-royal-tracking`.
        if not royal:
            config_data["cotd_reminder_channel"] = channel_id
            config_data["cotd_one_reminder"] = main
            config_data["cotd_two_reminder"] = first_rerun
            config_data["cotd_three_reminder"] = second_rerun
        else:
            config_data["royal_reminder_channel"] = channel_id
            config_data["royal_one_reminder"] = main
            config_data["royal_two_reminder"] = first_rerun
            config_data["royal_three_reminder"] = second_rerun

        # Dumping Data to File.
        with open(
            f"./bot/resources/guild_data/{guild_id}/config.json", "w", encoding="UTF-8"
        ) as file:
            json.dump(config_data, file, indent=4)


def setup(bot: Bot):
    bot.add_cog(SetupReminders(bot))
