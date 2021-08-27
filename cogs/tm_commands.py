import discord
from discord.ext import commands
import json
import logging
import datetime
from dotenv import load_dotenv
import asyncio
from disputils.pagination import BotEmbedPaginator

import functions.tm_commands_functions
import functions.convert_logging as cl
import functions.common_functions as cf
from functions.usage import record_usage, finish_usage

load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log_level, discord_log_level, version = "", "", ""

with open("./json_data/config.json") as file:
    config = json.load(file)

    log_level = config["log_level"]
    discord_log_level = config["discord_log_level"]
    version = config["bot_version"]

log = logging.getLogger(__name__)
log = cl.get_logging(log_level, discord_log_level)

DEFAULT_PREFIX = "*"


class TMCommands(commands.Cog, description="Commands for Trackmania"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="viewmap", aliases=['map', 'track'], help="Views Track/Map Details By ID Given")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def view_map(self, ctx: commands.Context, game_flag: str, tmx_id: int = None) -> None:
        valid_flags = ["tmnf", "tm2020"]

        if game_flag.lower() not in valid_flags:
            log.error(f"Not a Valid Flag, Returning")
            await ctx.send(
                embed=discord.Embed(
                    title="Not A Valid Flag",
                    description="Valid Flags are: TMNF, TM2020\nUsage ```viewmap <game_flag>```",
                    color=discord.Colour.red(),
                )
            ).set_footer(
                text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url
            )
            return None

        if game_flag.lower() == "tmnf":
            log.debug(f"TMNF Flag Given")
            tmx_id_message = ""

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            log.debug(f"Requesting TMX ID from User")

            if tmx_id == None:
                try:
                    await ctx.send(
                        embed=discord.Embed(
                            title="Please Enter a TMX ID",
                            color=0x00FF00,
                            description="TMX ID can be found at the end of map url.\nExample: tmnforever.tm-exchange.com/trackshow/**2233**",
                        )
                    )
                    tmx_id_message = await self.client.wait_for(
                        "message", check=check, timeout=30.0
                    )
                    tmx_id = tmx_id_message.content
                except asyncio.TimeoutError:
                    await ctx.send(
                        embed=discord.Embed(
                            title="Bot Timed Out", color=discord.Colour.red()
                        )
                    )
                    return

            log.debug(f"Received TMX ID from User")

            log.debug(f"Sending Final Embed")
            embed = functions.tm_commands_functions.get_tmnf_map(
                tmx_id=str(tmx_id)
            )
            embed.set_footer(
                text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)
            log.debug(f"Sent final embed")

        if game_flag.lower() == "tm2020":
            await ctx.send(
                embed=discord.Embed(
                    title="Under Construction", color=discord.Colour.red()
                )
            ).set_footer(
                text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url
            )

    @commands.command(
        name="leaderboards",
        aliases=["lb", "ld"],
        help="Leaderboards for a Specific Map",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def get_leaderboards(self, ctx: commands.Context, game_flag: str, tmx_id: int = None) -> None:
        valid_flags = ["tmnf", "tm2020"]

        if game_flag.lower() not in valid_flags:
            log.error(f"Not a Valid Flag, Returning")

            embed = discord.Embed(
                title="Not a Valid Flag",
                description="Valid Flags are: TMNF, TM2020\nUsage: ```leaderboards <game_flag>```",
                color=discord.Colour.red(),
            )
            embed.set_footer(
                text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url
            )

            await ctx.send(embed=embed)
            return None

        if game_flag.lower() == "tmnf":
            log.debug(f"TMNF Flag Given")
            tmx_id_message = ""

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            log.debug(f"Requesting TMX ID from User")

            if tmx_id == None:
                try:
                    embed = discord.Embed(
                        title="Please Enter Map ID",
                        color=cf.get_random_color(),
                        description="MAP ID can be found at the end of map url.\nExample: tmnforever.tm-exchange.com/trackshow/**2233**",
                    )

                    embed.set_footer(
                        text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url
                    )

                    await ctx.send(embed=embed)

                    tmx_id_message = await self.client.wait_for(
                        "message", check=check, timeout=30
                    )
                    tmx_id = tmx_id_message.content
                except asyncio.TimeoutError:
                    await ctx.send(
                        embed=discord.Embed(
                            title="Bot Timed Out", color=discord.Colour.red()
                        )
                    ).set_footer(
                        text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url
                    )
                    return None

            log.debug(f"Received TMX ID from User")

            log.debug(f"Asking for Embeds")
            embeds = functions.tm_commands_functions.get_leaderboards(str(tmx_id), ctx.author.avatar_url)

            # Epic Bodge
            try:
                new_embed = embeds[0]
            except:
                log.error('Invalid TMNF ID Given')
                await ctx.send(embed=embeds)
                return None

            log.debug(f"Received Embeds")

            log.debug(f"Creating Paginator")
            paginator = BotEmbedPaginator(ctx, embeds)
            log.debug(f"Created Paginator")

            log.debug(f"Running Paginator")
            await paginator.run()

        if game_flag.lower() == "tm2020":
            await ctx.send(
                embed=discord.Embed(
                    title="Under Construction", color=discord.Colour.red()
                ).set_footer(
                text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url
            )
            )

    # @view_map.error
    # async def error(self, ctx: commands.Context, error: commands.CommandError):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         log.error("Missing required arguments")

    #         log.debug(f"Creating Error Embed")
    #         await ctx.send(
    #             embed=discord.Embed(
    #                 title=":warning: Missing required argument: Game Flag",
    #                 description="**Game Flag is a required argument that is missing**,\n\nUsage: viewmap {TMNF/TM2020}",
    #                 color=discord.Colour.red(),
    #             ).set_footer(
    #                 text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url
    #             )
    #         )
    #         log.debug(f"Sent Error Embed")

    @get_leaderboards.error
    async def error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            log.error("Missing required argument")

            log.debug(f"Sending Error Embed")
            await ctx.send(
                embed=discord.Embed(
                    title=":warning: Missing required argument: Game Flag",
                    description="**Game Flag is a required argument that is missing**,\n\nUsage: leaderboards {TMNF/TM2020}",
                    color=discord.Colour.red(),
                ).set_footer(
                    text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url
                )
            )


def setup(client):
    client.add_cog(TMCommands(client))
