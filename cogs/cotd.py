import discord
from discord.ext import commands
import json
import logging
import datetime
from dotenv import load_dotenv
import asyncio
import os
import requests

from functions.custom_errors.custom_errors import NotAValidTrackmaniaUsername
import functions.logging.convert_logging as convert_logging
from functions.logging.usage import record_usage, finish_usage
import functions.tm_username_functions.username_functions as username_functions
from functions.cog_helpers.cotd_functions import (
    get_average_data,
    make_global_rank_plot_graph,
)
from functions.other_functions.timestamp import curr_time


load_dotenv()
BASE_API_URL = os.getenv("BASE_API_URL")

log = logging.getLogger(__name__)
log = convert_logging.get_logging()

guild_ids = [876042400005505066, 805313762663333919]


class COTD(commands.Cog, description="Commands related to COTD Standings"):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="COTD",
        aliases=["cotd", "totd", "stats", "cotdstats"],
        help="COTD Stats for a given player, if none is given it will use your stored username",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def cotd(self, ctx: commands.Command, username: str = None) -> None:
        """Get COTD Data for a Given Player

        Args:
            ctx (commands.Command): [description]
            username (str, optional): [description]. Defaults to None.
        """
        if username is None:
            log.debug(f"No Username is Given, Getting Username from File")
            username = username_functions.get_trackmania_username(str(ctx.author.id))

        log.debug(f"Getting ID for {username}")
        user_id = username_functions.get_id(username)

        if user_id is None:
            log.error("A Valid Username was Not Given")
            embed = discord.Embed(
                title="Not a Valid Trackmania Username/Your Username is not stored in the file",
                description="If your username is not in the file, please use `--storeusername *username*`",
                color=discord.Colour.red(),
            )
            embed.timestamp = curr_time()
            await ctx.send(embed=embed)
            return
            # raise NotAValidTrackmaniaUsername("A Valid Username was not Given")

        log.debug(f"Getting COTD Data")
        PLAYER_URL = BASE_API_URL + "/tm2020/player/" + user_id + "/cotd"
        cotd_data = requests.get(PLAYER_URL).json()
        log.debug(f"Got COTD Data")

        log.debug(f"Checking if COTD Data actually exists")
        try:
            if cotd_data["error"] == "INVALID_PLAYER_ID":
                log.error(f"{username} has not played any cotds")
                embed = discord.Embed(
                    title=f"{username} has not played any cotds",
                    color=discord.Colour.red(),
                )
                embed.timestamp = curr_time()
                await ctx.send(embed=embed)
                return
        except:
            pass

        log.debug(f"Parsing through the data and getting average values")
        avg_global_rank, avg_server_rank, avg_div, total_cotds = get_average_data(
            cotd_data
        )

        if total_cotds == 0:
            log.error(f"{username} has not played any cotds")
            embed = discord.Embed(
                title=f"{username} has not played any cotds", color=discord.Colour.red()
            )
            embed.timestamp = curr_time()
            await ctx.send(embed=embed)
            return

        PILString = make_global_rank_plot_graph(cotd_data)
        if PILString != "DONE":
            log.error(
                "AN ERROR HAS OCCURED, IDK WHAT WILL CAUSE THIS, BUT IT'S HERE JUST IN CASE"
            )
            await ctx.send("AN ERROR HAS OCCURED")
            return

        embed = discord.Embed(
            title=f"COTD Data for {username}",
            description="COTD Data does not consider cotds where you did not complete/left the match early\nPlease Note: Your graph only shows the previous 30 COTDs\n~~----~~",
        )
        embed.add_field(name="Total COTDs Completed", value=total_cotds, inline=False)
        embed.add_field(name="Average Global Rank", value=avg_global_rank, inline=True)
        embed.add_field(name="Average Division", value=avg_div, inline=True)
        embed.add_field(name="Average Server Rank", value=avg_server_rank, inline=True)
        embed.timestamp = curr_time()

        log.debug(f"Sending Embed")

        file = discord.File("./data/cotddata.png", filename="cotd.png")
        embed.set_image(url="attachment://cotd.png")
        await ctx.send(file=file, embed=embed)

    @cotd.error
    async def cotd_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"Command is Still on Cooldown for {round(error.retry_after, 2)}s"
            )


def setup(client):
    client.add_cog(COTD(client))
