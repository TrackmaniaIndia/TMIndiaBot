from re import L

from discord.ext.commands.core import after_invoke, before_invoke
import functions.tm_username_functions.username_functions as username_functions
import discord
from discord.ext import commands
import logging
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

import functions.logging.convert_logging as convert_logging
from functions.logging.usage import record_usage, finish_usage
from functions.other_functions.get_data import get_version

load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")


log = logging.getLogger(__name__)
log = convert_logging.get_logging()

version = get_version()

guild_ids = [876042400005505066, 805313762663333919]


class UsernameCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="storeusername",
        aliases=["setusername", "setname", "setuser"],
        help="Set your trackmania username to reduce amount of typing needed while using TM2020 commands",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def store_username(self, ctx: commands.Context, username: str):
        log.debug(f"Checking Username")
        if not username_functions.check_valid_trackmania_username(username):
            log.debug(f"Username not found")
            embed = discord.Embed(
                title="Username not found or does not exist",
                colour=discord.Colour.red(),
            )
            embed.timestamp = datetime.now(timezone(timedelta(hours=5, minutes=30)))
            await ctx.send(embed=embed)
            return None
        log.debug(f"User Exists, Continuing")

        log.debug(f"Storing {username} for {ctx.author.name}. ID: {ctx.author.id}")
        username_functions.store_trackmania_username(ctx.author.id, username)
        log.debug(f"Stored Username for {ctx.author.name}")

        log.debug(f"Sending Success Message")
        embed = discord.Embed(title="SUCCESS!", color=discord.Colour.green())
        embed.timestamp = datetime.now(timezone(timedelta(hours=5, minutes=30)))
        await ctx.send(embed=embed)
        log.debug(f"Sent Success Message")

    @commands.command(
        name="checkusername",
        aliases=["usernamecheck", "namecheck", "checkname", "checkuser", "usercheck"],
        help="Checks if you have a username stored with the bot",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def check_username(self, ctx: commands.Context):
        if username_functions.check_discord_id_in_file(str(ctx.author.id)):
            log.debug(f"Username in json file")
            embed = discord.Embed(
                title="Your Username Exists", colour=discord.Colour.green()
            )
            embed.timestamp = datetime.now(timezone(timedelta(hours=5, minutes=30)))

            await ctx.send()
        else:
            log.debug(f"Username not in json file")
            embed = discord.Embed(
                title="Your Username does not Exist", colour=discord.Colour.red()
            )
            embed.timestamp = datetime.now(timezone(timedelta(hours=5, minutes=30)))

            await ctx.send(embed=embed)

    @commands.command(
        name="removeusername",
        aliases=["usernameremove", "userremove", "nameremove"],
        help="Removes your username from the bot",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def remove_username(self, ctx: commands.Context):
        if not username_functions.check_discord_id_in_file(str(ctx.author.id)):
            log.debug(f"User does not exist in file")
            embed = discord.Embed(
                title="User does not exist", colour=discord.Colour.red()
            )
            embed.timestamp = datetime.now(timezone(timedelta(hours=5, minutes=30)))
            await ctx.send(embed=embed)
            return

        log.debug(f"Removing Trackmania Username")
        username_functions.remove_trackmania_username(ctx.author.id)
        log.debug(f"Removed Trackmania Username")
        embed = discord.Embed(title="SUCCESS!!", colour=discord.Colour.green())
        embed.timestamp = datetime.now(timezone(timedelta(hours=5, minutes=30)))
        await ctx.send(embed=embed)

    @store_username.error
    async def store_username_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            log.error("Username Not Given")

            embed = discord.Embed(
                title=":warning: Trackmania Username not given",
                description="Usage: storeusername <trackmania-username>\nExample: --storeusername ",
                color=discord.Colour.red(),
            )
            embed.timestamp = datetime.now(timezone(timedelta(hours=5, minutes=30)))
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(UsernameCommands(client))
