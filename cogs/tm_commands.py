import discord
from discord.ext import commands
import logging
import datetime
from dotenv import load_dotenv
import asyncio
from disputils.pagination import BotEmbedPaginator

import functions.cog_helpers.tm_commands_functions
import functions.logging.convert_logging as convert_logging
import functions.common_functions.common_functions as common_functions
from functions.logging.usage import record_usage, finish_usage

load_dotenv()
# log_level = os.getenv("LOG_LEVEL")
# version = os.getenv("VERSION")
# discord_log_level = os.getenv("DISCORD_LOG_LEVEL")


log = logging.getLogger(__name__)
log = convert_logging.get_logging()

guild_ids = [876042400005505066, 805313762663333919]


class TMCommands(commands.Cog, description="Commands for Trackmania"):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="viewmap",
        aliases=["map", "track"],
        help="Views Track/Map Details By ID Given",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def view_map(
        self, ctx: commands.Context, game_flag: str, tmx_id: str = None
    ) -> None:
        valid_flags = ["tmnf", "tm2020"]

        if game_flag.lower() not in valid_flags:
            log.error(f"Not a Valid Flag, Returning")
            embed = discord.Embed(
                title="Not A Valid Flag",
                description="Valid Flags are: TMNF, TM2020\nUsage ```viewmap <game_flag>```",
                color=discord.Colour.red(),
            ).timestamp = datetime.now()
            await ctx.send(embed=embed)
            return None

        if game_flag.lower() == "tm2020":
            log.debug(f"TM2020 Flag Given")
            tmioIdMessage = ""

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            log.debug(f"Requesting TMIO ID from User")

            if tmx_id == None:
                try:
                    embed = (
                        discord.Embed(
                            title="Please Enter a TMIO UID",
                            color=0x00FF00,
                            description="TMIO UID can be found in the map's TMIO page.\nExample ([Fall 2021 01](https://trackmania.io/#/campaigns/leaderboard/45569279-a101-446d-b5d6-649471deadcf/Nhg8q0K47asKBYRVBCNC8OguB8)):",
                        )
                        .set_image(
                            url="https://cdn.discordapp.com/attachments/746693237112176703/894243672193916978/unknown.png"
                        )
                        .timestamp
                    ) = datetime.now()
                    await ctx.send(embed=embed)
                    tmioIdMessage = await self.client.wait_for(
                        "message", check=check, timeout=30.0
                    )
                    tmx_id = tmioIdMessage.content
                    log.debug(f"Received tmio ID from User")
                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="Bot Timed Out", color=discord.Colour.red()
                    ).timestamp = datetime.now()
                    await ctx.send(embed=embed)
                    return

            embed = functions.cog_helpers.tm_commands_functions.getTm2020Map(
                tmx_id
            ).timestamp = datetime.now()
            await ctx.send(embed=embed)

        elif game_flag.lower() == "tmnf":
            log.debug(f"TMNF Flag Given")
            tmx_id_message = ""

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            log.debug(f"Requesting TMX ID from User")

            if tmx_id == None:
                try:
                    embed = discord.Embed(
                        title="Please Enter a TMX ID",
                        color=0x00FF00,
                        description="TMX ID can be found at the end of map url.\nExample: tmnforever.tm-exchange.com/trackshow/**2233**",
                    ).timestamp = datetime.now()
                    await ctx.send(embed=embed)
                    tmx_id_message = await self.client.wait_for(
                        "message", check=check, timeout=30.0
                    )
                    tmx_id = tmx_id_message.content
                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="Bot Timed Out", color=discord.Colour.red()
                    ).timestamp = datetime.now()
                    await ctx.send(embed=embed)
                    return

            log.debug(f"Received TMX ID from User")

            log.debug(f"Sending Final Embed")
            embed = functions.cog_helpers.tm_commands_functions.get_tmnf_map(
                tmx_id=str(tmx_id)
            )
            embed.set_footer(
                text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)
            log.debug(f"Sent final embed")

    @commands.command(
        name="leaderboards",
        aliases=["lb", "ld"],
        help="Leaderboards for a Specific Map",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def get_leaderboards(
        self, ctx: commands.Context, game_flag: str, tmx_id: int = None
    ) -> None:
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
            embed.timestamp = datetime.now()

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
                        color=common_functions.get_random_color(),
                        description="MAP ID can be found at the end of map url.\nExample: tmnforever.tm-exchange.com/trackshow/**2233**",
                    )

                    embed.set_footer(
                        text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url
                    )
                    embed.timestamp = datetime.now()

                    await ctx.send(embed=embed)

                    tmx_id_message = await self.client.wait_for(
                        "message", check=check, timeout=30
                    )
                    tmx_id = tmx_id_message.content
                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="Bot Timed Out", color=discord.Colour.red()
                    ).timestamp = datetime.now()
                    await ctx.send(embed=embed)
                    return None

            log.debug(f"Received TMX ID from User")

            log.debug(f"Asking for Embeds")
            embeds = functions.cog_helpers.tm_commands_functions.get_leaderboards(
                str(tmx_id), ctx.author.avatar_url
            )

            # Epic Bodge
            try:
                new_embed = embeds[0]
            except:
                log.error("Invalid TMNF ID Given")
                await ctx.send(embed=embeds)
                return None

            log.debug(f"Received Embeds")

            log.debug(f"Creating Paginator")
            paginator = BotEmbedPaginator(ctx, embeds)
            log.debug(f"Created Paginator")

            log.debug(f"Running Paginator")
            await paginator.run()
            log.debug(f"Finished Paginator, Sending Finished Embed")

            embed = discord.Embed(
                title=f"{ctx.command} successfully run",
                colour=discord.Colour.green(),
            ).timestamp = datetime.now()

            await ctx.send(embed=embed)

            log.debug(f"Sent Finished Embed")

        if game_flag.lower() == "tm2020":
            embed = discord.Embed(
                title="Under Construction", color=discord.Colour.red()
            ).timestamp = datetime.now()
            await ctx.send(embed=embed)

    # @view_map.error
    # async def error(self, ctx: commands.Context, error: commands.CommandError):
    #     log.error(error)
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
    #         return None

    @get_leaderboards.error
    async def error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            log.error("Missing required argument")

            log.debug(f"Sending Error Embed")
            embed = discord.Embed(
                title=":warning: Missing required argument: Game Flag",
                description="**Game Flag is a required argument that is missing**,\n\nUsage: leaderboards {TMNF/TM2020}",
                color=discord.Colour.red(),
            ).timestamp = datetime.now()
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(TMCommands(client))
