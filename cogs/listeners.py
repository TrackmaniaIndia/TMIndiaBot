import discord
import json
import os

import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed

from discord.ext import commands
from datetime import datetime
from itertools import cycle
from util.cog_helpers.generic_helper import *
from util.cog_helpers.listener_helper import _get_statuses
from util.tasks.keep_alive import keep_alive
from util.tasks.status_change import change_status
from util.tasks.totd_image_delete import totd_deleter
from util.logging.command_log import log_join_guild, log_leave_guild

# Creating logger
log = convert_logging.get_logging()
version = get_version()


class Listeners(commands.Cog, description="Generic Functions"):
    statuses = cycle([])

    def __init__(self, client):
        self.client = client

        # Adding Statuses to the List
        log.debug(f"Adding Statuses")
        self.statuses = cycle(_get_statuses())
        log.debug(f"Received Statuses")
        log.info(f"cogs.listeners has finished initializing")

    @commands.Cog.listener()
    async def on_ready(self):
        # Changes Precense to the default status
        # Default Status is:
        #    Version: VERSION! Online and Ready!
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"Version: {version}! Online and Ready"),
        )
        log.critical("Bot Logged In")

        # Getting number of times bot was run on this computer
        times_run = 0
        log.debug(f"Reading Value from Times Run File")
        with open("./data/times_run.txt", "r") as file:
            times_run = int(file.readline())

        # Adding one to the times run
        times_run += 1

        # Starting the Keep Alive loop that periodically sends a message to a designated channel and pings the API every 30 minutes
        log.debug(f"Starting Keep Alive Loop")
        keep_alive.start(self.client)
        log.debug(f"Started Keep Alive Loop")

        # Starting the Change Status Loop that Changes the Bot's Status Every 10 Minutes
        log.debug(f"Start Change Status Loop")
        change_status.start(self.client, self.statuses)
        log.debug(f"Started Change Status Loop")

        # Deleting the TOTD Image if it exists
        if os.path.exists("./data/temp/totd.png"):
            log.critical("TOTD Image Exists, Deleting")
            os.remove("./data/temp/totd.png")

        # Starting the TOTD Image Deleter Loop
        log.debug(f"Starting TOTD Image Loop")
        totd_deleter.start(self.client)
        log.debug(f"Started TOTD Image")

        # Getting the Announcement Channels for where the bot should send that it is ready
        # Channels taken from ./data/json/announcement_channels.json
        log.debug(f"Getting Announcement Channels")
        with open("./data/json/announcement_channels.json", "r") as file:
            channels = json.load(file)

        # Printing System Info to the Screen
        print_system_info()

        # Looping Through Announcement Channels
        for announcement_channel in channels["announcement_channels"]:
            log.debug(f"Sending Message in {announcement_channel}")

            # Sending Message to the Channel
            channel = self.client.get_channel(int(announcement_channel))
            try:
                # Inside a TryExcept to prevent the bot from crashing if the channel is deleted or permissions to send messages are removed
                await channel.send(
                    f"Bot is Ready, Version: {version} - Times Run: {times_run} - Time of Start: {datetime.now()}"
                )
                log.debug(f"Sent Message to {announcement_channel}")
                if (
                    int(announcement_channel) == 880771916099641364
                    or int(announcement_channel) == 880628511512096778
                ):
                    continue
            except:
                log.debug(f"Can't Send Message to {announcement_channel}")
                continue

        # Printing out the new timesrun value to the file
        log.debug(f"Writing TimesRun to File")
        with open("./data/times_run.txt", "w") as file:
            print(times_run, file=file)

        log.info(f"Bot now Usable")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        log_join_guild(guild)
        # Bot prints a message when it joins a Guild
        log.critical(f"The Bot has Joined {guild.name} with id {guild.id}")

        log.info(f"Creating Guild Data directory for {guild.name}")
        if not os.path.exists(f"./data/guild_data/{guild.id}/"):
            log.debug(f"Creating Guild Directory for {guild.name}")
            os.mkdir(f"./data/guild_data/{guild.id}/")
            log.debug(f"Created Guild Directory for {guild.name}")

        log.debug(f"Creating quotes.json for {guild.name}")
        with open(f"./data/guild_data/{guild.id}/quotes.json", "w") as file:
            log.debug(
                f"Dumping an Empty quotes array into quotes.json for {guild.name}"
            )
            json.dump({"quotes": []}, file, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        # Bot prints a message when it leaves or is removed from a Guild
        log.critical(
            f"The bot has left/been kicked/been banned from {guild.name} with id {guild.id}"
        )

    # @commands.Cog.listener()
    # async def on_application_command_error(
    #     self, ctx, error: discord.ApplicationCommandError
    # ):
    #     # Checking if Error Message Should Be Printed Out
    #     with open("./data/config.json", "r") as file:
    #         config = json.load(file)

    #         if config["print_errors"] == False:
    #             log.error(f"Error Message isn't going to be printed in discord server")
    #             log.error(error)
    #             return

    #         log.debug(f"Error will be printed to discord server")

    #     # Getting the Error Channel
    #     channel = self.client.get_channel(int(config["errorChannel"]))

    #     embed = ezembed.create_embed(
    #         title="An Error Has Occured",
    #         description=error,
    #         color=0xFF0000,
    #     )

    #     embed.add_field(name="Author Username", value=ctx.author.name, inline=False)
    #     embed.add_field(name="Author ID", value=ctx.author.id, inline=False)
    #     embed.add_field(name="Guild Name", value=ctx.guild.name, inline=False)
    #     embed.add_field(name="Guild ID", value=ctx.guild.id, inline=False)
    #     # embed.add_field(name="Message Content", value=ctx.message.content, inline=False)

    #     # Print the Traceback to the Screen
    #     log.error(error.with_traceback(error.__traceback__))
    #     # log.error(error)

    #     await channel.send(embed=embed)


def setup(client: discord.Bot):
    client.add_cog(Listeners(client))
