import discord
from discord.ext import commands
import json
import logging
import os
import datetime
from dotenv import load_dotenv
import custom_errors

try:
    import cogs.convert_logging as cl
    import cogs.common_functions as cf
except:
    import common_functions as cf
    import convert_logging as cl

load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log_level, discord_log_level, version = "", "", ""

with open("./config.json") as file:
    config = json.load(file)

    log_level = config["log_level"]
    discord_log_level = config["discord_log_level"]
    version = config["bot_version"]

log = logging.getLogger(__name__)
log = cl.get_logging(log_level, discord_log_level)

DEFAULT_PREFIX = "*"


async def record_usage(self, ctx):
    log.info(
        f"{ctx.author} used {ctx.command} at {ctx.message.created_at} in {ctx.guild}"
    )

    log_check = ""

    with open("./config.json") as file:
        data = json.load(file)
        log_check = data["log_function_usage"]
        file.close()

    if not log_check:
        log.debug(f"log_check is False, Returning")
        return
    log.debug(f"log_check is True, Sending Message")

    log.debug(f"Sending Message to Error Channel")
    channel = self.client.get_channel(876442289382248468)

    log.debug(f"Creating Embed")
    embed = discord.Embed(title=":clapper: Command Used", color=0x23FFFF)

    embed.add_field(name="Author Username", value=ctx.author, inline=False)
    embed.add_field(name="Author ID", value=ctx.author.id, inline=False)
    embed.add_field(name="Guild Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Guild ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Message content", value=ctx.message.content, inline=False)
    embed.set_footer(text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url)

    log.debug(f"Created Embed")

    log.debug(f"Sending Embed")
    await channel.send(embed=embed)
    log.debug(f"Embed Sent, Error Handler Quit")


async def finish_usage(self, ctx: commands.Context):
    log.info(f"{ctx.author} finished using {ctx.command} in {ctx.guild}")

    log_check = ""

    with open("./config.json") as file:
        data = json.load(file)
        log_check = data["log_function_usage"]
        file.close()

    if not log_check:
        log.debug(f"log_check is False, Returning")
        return
    log.debug(f"log_check is True, Sending Message")

    log.debug(f"Sending Message to Error Channel")
    channel = self.client.get_channel(876442289382248468)

    log.debug(f"Creating Embed")
    embed = discord.Embed(title=":medal: Command Finished", color=0x00FF00)

    embed.add_field(name="Author Username", value=ctx.author, inline=False)
    embed.add_field(name="Author ID", value=ctx.author.id, inline=False)
    embed.add_field(name="Guild Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Guild ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Message content", value=ctx.message.content, inline=False)

    embed.set_footer(text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url)

    log.debug(f"Created Embed")
    log.debug(f"Sending Embed")
    await channel.send(embed=embed)
    log.debug(f"Embed Sent, Error Handler Quit")


class CommunityContentPromoter(
    commands.Cog, description="Community Content Promoter Functions"
):
    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command(
        name="addchannel",
        aliases=["Addchannel", "addChannel", "AddChannel"],
        help="Add Channel to Community Creators List",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def add_channel(self, ctx):
        channel_link = ""

        log.debug(f"Asking for Channel Link")
        await ctx.send(
            embed=discord.Embed(
                title="Please Type Your Youtube Channel Link",
                description="Example Link: https://www.youtube.com/channel/UCq6VFHwMzcMXbuKyG7SQYIg",
                color=cf.get_random_color(),
            )
        )

        def check(message):
            return str(message.author.id) != '876059862788890685'

        channel_link_message = await self.client.wait_for('message', check=check)
        channel_link = channel_link_message.content
        # log.error(channel_link)

        continue_flag = False
        continue_flag = check_link(channel_link)

        if not continue_flag:
            raise custom_errors.NotAValidYoutubeLink()

    # Error Handling
    @add_channel.error
    async def add_channel_error(self, ctx, error):
        if isinstance(error, custom_errors.NotAValidYoutubeLink):
            log.error('Not a Valid Youtube Link, Sending Embed to User')
            await ctx.send(embed=discord.Embed(title='Not A Valid Youtube Link, Please Try Again', description='Valid Links have ```https://youtube.com/channel/``` in them', color=0xff0000))

            

def setup(client):
    client.add_cog(CommunityContentPromoter(client))
    check_for_community_creators_file()


def check_for_community_creators_file() -> None:
    log.debug(f"Checking for Community Creators File")
    if not os.path.exists("./data"):
        log.critical("Data Directory doesn't Exist, Creating")
        os.mkdir("./data")
    if not os.path.exists("./Data/community_creators.json"):
        log.critical(f"Community Creators File Doesn't Exist, Creating")

        with open("./data/community_creators.json", "w") as file:
            print("{}", file=file)

    return

def check_link(link: str) -> bool:
    if 'https://www.youtube.com/channel/' not in link:
        return False
    return True

# def NotAYoutubeLinkException():
#     raise commands.CommandError(message=f'Not A Valid Youtube Link')