import threading
import time
import json

import discord
from discord.commands import permissions
from discord.commands.commands import Option
from discord.ext import commands

import util.discord.easy_embed as ezembed
import util.trackmania.tm2020.leaderboards.campaign as tm2020_campaign
import util.trackmania.tm2020.player as tm2020_player
from util import common_functions
from util.constants import GUILD_IDS
from util.discord.confirmation import Confirmer
from util.discord.paginator import Paginator
from util.discord.view_adder import ViewAdder
from util.logging import convert_logging
from util.logging.command_log import log_command
from util.trackmania.tm2020.cotd.cotd import get_cotd_data
from util.trackmania.tm2020.totd import _get_current_totd

log = convert_logging.get_logging()


class Trackmania(commands.Cog):
    def __init__(self, client):
        self.client = client
        log.info("cogs.trackmania has finished initializing")

    @commands.slash_command(
        name="playerdetails",
        description="player details for a specific player",
    )
    async def _player_details(
        self,
        ctx: commands.Context,
        username: Option(str, "The Trackmania2020 Username", required=True),
    ):
        log_command(ctx, ctx.command.name)
        # Gets the Player Details of a given username
        player_id = tm2020_player.get_player_id(username)

        if player_id is None:
            # An Invalid Username was given, sending a message to the user
            log.critical("Invalid Player Username Received, Sending Error Message")
            await ctx.respond(
                embed=ezembed.create_embed(
                    title="Invalid Username Given",
                    description=f"Username Given: {username}",
                    color=common_functions.get_random_color(),
                ),
                delete_after=5,
                ephemeral=False,
            )
            return

            # Deferring the Response to Allow the Bot some time to do its stuff
        log.info("Deferring Command")
        await ctx.defer()
        log.info("Command Deferred, Thinking")
        log.info("Valid Username Given")

        # A Valid Username was given, so were getting the Player Details
        log.info("Getting Player Data")
        data_pages = tm2020_player.get_player_data(player_id)

        if len(data_pages) == 1:
            log.info("Only 1 Page was Returned")
            await ctx.respond(embed=data_pages[0])
            return

        # Creating a Paginator with Player Data
        log.info("Received Data Pages")
        log.info("Creating Paginator")
        player_detail_paginator = Paginator(pages=data_pages, sending=False)

        # Running the Paginator
        await player_detail_paginator.run(ctx)

    @commands.slash_command(
        guild_ids=[876042400005505066], name="updatecampaignleaderboards"
    )
    @permissions.is_owner()
    async def _update_campaign_leaderboards(
        self,
        ctx: commands.Context,
        year: Option(str, "Choose the year", choices=["2020", "2021"]),
        season: Option(
            str, "Choose the season", choices=["Winter", "Spring", "Summer", "Fall"]
        ),
        firstfive: Option(
            str, "Want to Update the First Five as Well?", choices=["True", "False"]
        ),
    ):
        log_command(ctx, ctx.command.name)
        # Updates the Campaign Leaderboards by sending pings to the API and saving the Top 500 players, this takes quite a while to finish
        # Try to only update the leaderboards using your testing bot so the main bot does not get slowed down by the constant
        # saving to files.
        firstfive = bool(firstfive)
        log.info("Creating Confirmation Prompt")
        confirm_continue = Confirmer()

        # Changing the button labels
        log.info("Changing Button Labels")
        confirm_continue.change_confirm_button(label="Yes, Continue")
        confirm_continue.change_cancel_button(label="No, Stop")
        log.info("Changed Button Labels")

        # Sending the Confirmation Prompt
        log.info("Sending Prompt")
        message = await ctx.respond(
            embed=ezembed.create_embed(
                title="Are you sure you want to continue?",
                description=f"This can take over 10minutes, the bot will be unusable in this period\nYear: {year}\nSeason: {season}",
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
        await message.delete_original_message()
        log.info("Deleted Message")

        # Checking if the Confirmation Prompt was Cancelled
        if confirm_continue.value is False:
            log.info(f"{ctx.author.name} does not want to continue")
            return

        log.info(f"{ctx.author.name} wants his username added")

        # Getting the Fall Campaign IDs
        log.info("Getting Fall Campaign IDs")
        fall_ids = tm2020_campaign.get_all_campaign_ids(year=year, season=season)
        log.info("Got the Fall IDs")

        # Starting Long Update Process using a seperate Thread to allow bot to complete other processes
        log.info("Updating Leaderboards")
        log.info("Creating Thread to Update Leaderboards")
        leaderboard_update = threading.Thread(
            target=tm2020_campaign.update_leaderboards_campaign,
            args=(fall_ids, year, season, firstfive),
        )
        # update_leaderboards_campaign(fall_ids)
        log.info("Thread Created to Update Leaderboards")
        log.info("Starting Thread")
        leaderboard_update.run()
        log.info("Thread Finished")
        log.info("Leaderboards Updated, Sleeping for 30s to save API")

        # Sleeping 30s to allow our API requests to restore
        time.sleep(30)

        # Sending a "Finished" Message
        await ctx.send(
            embed=ezembed.create_embed(
                title=":white_check_mark: Success!",
                description=f"Leaderboard Updated for Year: {year} and Season: {season}",
                color=discord.Colour.green(),
            )
        )

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="stalkplayerfortscc",
        description="Checks if the player is in top 500 for the tscc map pool",
        default_permission=False,
    )
    @permissions.has_any_role("TSCC", "Moderator", "admin")
    async def _check_player(
        self,
        ctx: commands.Context,
        username: Option(str, description="Username of the player", required=True),
    ):
        log_command(ctx, ctx.command.name)
        # Check if Username is in the Top 500 for any maps in the TSCC Map Pool
        log.info("Deferring Response")
        await ctx.defer()
        log.info("Deferred Response")
        log.info(f"Checking Player Username -> {username}")
        player_id = tm2020_player.get_player_id(username)
        log.info(f"Got Player Id -> {player_id}")

        if player_id is None:
            log.error(f"Invalid Username Given, Username -> {username}")
            await ctx.respond("Invalid Username")
        else:
            log.info(f"Valid Username, Username -> {username}")
            log.info("Executing Function, Pray")
            await ctx.respond(embed=tm2020_campaign.get_player_good_maps(username))
            log.info("Player stalking was a success")

    @commands.slash_command(
        name="totd",
        description="Latest TOTD",
    )
    async def _totd(
        self,
        ctx: commands.Context,
    ):
        log.info("Deferring Response")
        await ctx.defer()
        log.info("Deferred Response, Awaiting Information")

        log.info("Getting Information")
        totd_embed, image, download_link, tmio_link, tmx_link = _get_current_totd()
        log.info("Got Information, Sending Response")

        log.info("Creating Buttons to Add")
        download_map = discord.ui.Button(
            label="Download Map!", style=discord.ButtonStyle.primary, url=download_link
        )
        tmio_button = discord.ui.Button(
            label="TMIO", style=discord.ButtonStyle.url, url=tmio_link
        )

        if tmx_link is not None:
            tmx_button = discord.ui.Button(
                label="TMX", style=discord.ButtonStyle.url, url=tmx_link
            )

            await ctx.respond(
                file=image,
                embed=totd_embed,
                view=ViewAdder([download_map, tmio_button, tmx_button]),
            )
        else:
            await ctx.respond(
                file=image,
                embed=totd_embed,
                view=ViewAdder([download_map, tmio_button]),
            )

    @commands.slash_command(
        name="cotddetails",
        description="COTD Data of a Given Username",
    )
    async def _cotd(
        self,
        ctx: commands.Context,
        username: Option(str, "The TM2020 Username of the Player", required=True),
    ):
        log.info("Deferring Response")
        await ctx.defer()
        log.info("Deferred Response")

        log.info("Checking Player")
        player_id = tm2020_player.get_player_id(username)

        if player_id is None:
            log.critical("Username given is invalid")
            await ctx.respond(
                embed=ezembed.create_embed(
                    title="Invalid Username",
                    description=f"Username: {username}",
                    color=0xFF0000,
                )
            )
            return

        # Temp Code Starts
        cotd_data, image = get_cotd_data(player_id, username)

        if image is not None:
            await ctx.respond(file=image, embed=cotd_data)
        else:
            await ctx.respond(embed=cotd_data)

    @commands.slash_command(
        guild_ids=GUILD_IDS,
        name="totdreminderswitch",
        descriptions="Switches on or off the TOTD Reminder",
    )
    @permissions.is_owner()
    async def _totd_reminder_switch(self, ctx: commands.Context):
        await ctx.defer()
        log.debug(f"Opening Config Data")
        with open("./data/config.json", "r", encoding="UTF-8") as file:
            config_data = json.load(file)
            log.debug(f"Got Config Data")

        config_data["totdReminders"] = not config_data["totdReminders"]

        log.critical(f'TOTD Reminders set to {config_data["totdReminders"]}')

        log.debug(f"Dumping Config Data to File")
        with open("./data/config.json", "w", encoding="UTF-8") as file:
            json.dump(config_data, file, indent=4)

        await ctx.respond(
            f"TOTD Reminders set to: {config_data['totdReminders']}", ephemeral=True
        )


def setup(client: discord.Bot):
    client.add_cog(Trackmania(client))
