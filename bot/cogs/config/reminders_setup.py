# To setup COTD and Super Royal reminders for a guild.
import json

import discord
from click import confirm
from discord import ApplicationContext, Option
from discord.ext import commands

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import Confirmer
from bot.utils.moderation import send_in_mod_logs

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
            "Whether to be reminded for the main COTD at 5pm UTC",
            choices=["Yes", "No"],
            required=True,
        ),
        first_rerun: Option(
            str,
            "Whether to be reminded for the first COTD rerun at 1am UTC",
            choices=["Yes", "No"],
            required=True,
        ),
        second_rerun: Option(
            str,
            "Whether to be reminded for the second COTD rerun at 9am UTC",
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
            await send_in_mod_logs(
                self.bot,
                ctx.guild.id,
                msg=f"{ctx.guild.name} has been unsubscribed from COTD reminders by {ctx.author.mention}.",
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
            await send_in_mod_logs(
                self.bot,
                ctx.guild.id,
                msg=f"{ctx.guild.name} has been subsribed from COTD reminders by {ctx.author.mention} Reminders will be sent in {ctx.channel.mention}.\nMain COTD: {main_cotd}\nFirst Rerun: {first_rerun}\nSecond Rerun: {second_rerun}",
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
            "Whether to be reminded for the main Royal at 6pm UTC",
            choices=["Yes", "No"],
            required=True,
        ),
        first_rerun: Option(
            str,
            "Whether to be reminded for the first Royal rerun at 2am UTC",
            choices=["Yes", "No"],
            required=True,
        ),
        second_rerun: Option(
            str,
            "Whether to be reminded for the second Royal rerun at 10am UTC",
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
            await send_in_mod_logs(
                self.bot,
                ctx.guild.id,
                msg=f"{ctx.guild.name} has been unsubscribed from Royal reminders by {ctx.author.mention}.",
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
            await send_in_mod_logs(
                self.bot,
                ctx.guild.id,
                msg=f"{ctx.guild.name} has been subscribed from Royal reminders by {ctx.author.mention} Reminders will be sent in {ctx.channel.mention}.\nMain Royal: {main_royal}\nFirst Rerun: {first_rerun}\nSecond Rerun: {second_rerun}",
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

    @commands.slash_command(
        name="set-cotd-reminder-roles",
        description="Set a custom role that the bot pings for each COTD reminder.",
    )
    @commands.has_permissions(manage_guild=True)
    async def _set_cotd_reminder_roles(
        self,
        ctx: ApplicationContext,
        main_cotd_role: Option(
            discord.SlashCommandOptionType.role,
            "Role to be pinged for main cotd. Leave empty for no ping.",
            name="main-cotd-role",
            required=False,
        ),
        first_rerun_role: Option(
            discord.SlashCommandOptionType.role,
            "Role to be pinged for first rerun. Leave empty for no ping.",
            name="first-rerun-role",
            required=False,
        ),
        second_rerun_role: Option(
            discord.SlashCommandOptionType.role,
            "Role to be pinged for second rerun. Leave empty for no ping.",
            name="second-rerun-role",
            required=False,
        ),
    ):
        log.info("Saving settings for %s", ctx.guild.name)
        self.__save_role_settings(
            ctx.guild.id, main_cotd_role, first_rerun_role, second_rerun_role, False
        )

        await ctx.respond("Settings Saved Successfully.", delete_after=20)

    @commands.slash_command(
        name="set-royal-reminder-roles",
        description="Set a custom role that the bot pings for each Super Royal reminder.",
    )
    @commands.has_permissions(manage_guild=True)
    async def _set_royal_reminder_roles(
        self,
        ctx: ApplicationContext,
        main_royal_role: Option(
            discord.SlashCommandOptionType.role,
            "Role to be pinged for main royal. Leave empty for no ping.",
            name="main-royal-role",
            required=False,
        ),
        first_rerun_role: Option(
            discord.SlashCommandOptionType.role,
            "Role to be pinged for first rerun. Leave empty for no ping.",
            name="first-rerun-role",
            required=False,
        ),
        second_rerun_role: Option(
            discord.SlashCommandOptionType.role,
            "Role to be pinged for second rerun. Leave empty for no ping.",
            name="second-rerun-role",
            required=False,
        ),
    ):
        log.info("Saving settings for %s", ctx.guild.name)
        self.__save_role_settings(
            ctx.guild.id, main_royal_role, first_rerun_role, second_rerun_role, True
        )

        await ctx.respond("Settings Saved Successfully.", delete_after=20)

    def __save_role_settings(
        self,
        guild_id: int,
        main_role: discord.Role | None,
        first_rerun_role: discord.Role | None,
        second_rerun_role: discord.Role | None,
        royal: bool = False,
    ):
        main_role = main_role.id if main_role is not None else 0
        first_rerun_role = first_rerun_role.id if first_rerun_role is not None else 0
        second_rerun_role = second_rerun_role.id if second_rerun_role is not None else 0

        if not royal:
            main_role_name = "cotd_one_role"
            first_rerun_role_name = "cotd_two_role"
            second_rerun_role_name = "cotd_three_role"
        else:
            main_role_name = "royal_one_role"
            first_rerun_role_name = "royal_two_role"
            second_rerun_role_name = "royal_three_role"

        # Getting data from file.
        with open(
            f"./bot/resources/guild_data/{guild_id}/config.json", "r", encoding="UTF-8"
        ) as file:
            config_data = json.load(file)

        # Changing values
        config_data[main_role_name] = main_role
        config_data[first_rerun_role_name] = first_rerun_role
        config_data[second_rerun_role_name] = second_rerun_role

        # Dumping to File.
        with open(
            f"./bot/resources/guild_data/{guild_id}/config.json", "w", encoding="UTF-8"
        ) as file:
            json.dump(config_data, file, indent=4)

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
