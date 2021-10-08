from inspect import indentsize
import discord
from discord.ext import commands
import logging
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import asyncio
from disputils.pagination import BotEmbedPaginator
import os
import requests

from functions.cog_helpers.tm_commands_functions import getTm2020Map, get_tmnf_map, get_leaderboards, remove_mania_text_formatting
import functions.logging.convert_logging as convert_logging
import functions.common_functions.common_functions as common_functions
from functions.logging.usage import record_usage, finish_usage
from functions.other_functions.timestamp import curr_time
import functions.tm_username_functions.username_functions as username_functions
from functions.other_functions.timestamp import curr_time
from functions.cog_helpers.cotd_functions import get_cotd_stats

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
            ).timestamp = curr_time()
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
                    ) = curr_time()
                    await ctx.send(embed=embed)
                    tmioIdMessage = await self.client.wait_for(
                        "message", check=check, timeout=30.0
                    )
                    tmx_id = tmioIdMessage.content
                    log.debug(f"Received tmio ID from User")
                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="Bot Timed Out", color=discord.Colour.red()
                    ).timestamp = curr_time()
                    await ctx.send(embed=embed)
                    return

            embed = getTm2020Map(
                tmx_id
            )
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
                    ).timestamp = curr_time()
                    await ctx.send(embed=embed)
                    tmx_id_message = await self.client.wait_for(
                        "message", check=check, timeout=30.0
                    )
                    tmx_id = tmx_id_message.content
                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="Bot Timed Out", color=discord.Colour.red()
                    ).timestamp = curr_time()
                    await ctx.send(embed=embed)
                    return

            log.debug(f"Received TMX ID from User")

            log.debug(f"Sending Final Embed")
            embed = get_tmnf_map(
                tmx_id=str(tmx_id)
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

            embed.timestamp = curr_time()

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

                    embed.timestamp = datetime.now(
                        timezone(timedelta(hours=5, minutes=30))
                    )

                    await ctx.send(embed=embed)

                    tmx_id_message = await self.client.wait_for(
                        "message", check=check, timeout=30
                    )
                    tmx_id = tmx_id_message.content
                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="Bot Timed Out", color=discord.Colour.red()
                    )
                    embed.timestamp = datetime.now(
                        timezone(timedelta(hours=5, minutes=30))
                    )
                    await ctx.send(embed=embed)
                    return None

            log.debug(f"Received TMX ID from User")

            log.debug(f"Asking for Embeds")
            embeds = get_leaderboards(
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
            )
            embed.timestamp = curr_time()

            await ctx.send(embed=embed)

            log.debug(f"Sent Finished Embed")

        if game_flag.lower() == "tm2020":
            embed = discord.Embed(
                title="Under Construction", color=discord.Colour.red()
            )
            embed.timestamp = curr_time()
            await ctx.send(embed=embed)
        
    @commands.command(
        name="player",
        aliases=["pl"],
        help="Stats for a given player, if none is given it will use your stored username",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def player(self, ctx: commands.Command, username: str = None) -> None:
        player_data = None
        
        BASE_API_URL = os.getenv('BASE_API_URL')
        PLAYER_DATA_URL = BASE_API_URL + '/tm2020/player/{}'

        if username == None:
            file_username = username_functions.get_trackmania_username(str(ctx.author.id))
        else:
            file_username = username
        log.debug("Checking if username in file")
        if file_username == None:
            log.debug("Username not found in file, checking API")
            apiResponse = requests.get(PLAYER_DATA_URL.format(username)).json()

            found_username = common_functions.check_key(apiResponse[0], 'player')
            log.debug('Checking if username in API response')
            if found_username:
                log.debug("Username found in API response")
                player_data = apiResponse[0]
            else:
                log.debug("Username not found in API response")
        else:
            log.debug('Getting API response with file username')
            apiResponse = requests.get(PLAYER_DATA_URL.format(file_username)).json()

            found_username = common_functions.check_key(apiResponse[0], 'player')
            log.debug('Checking if username in API response')
            if found_username:
                log.debug("Username found in API response")
                player_data = apiResponse[0]
            else:
                log.debug("Username not found in API response")
        
        if player_data == None:
            log.debug("Player not found")
            embed = discord.Embed(  
                title="Not a Valid Trackmania Username/Your Username is not stored in the file",
                description="If your username is not in the file, please use `--storeusername *username*`",
                color=discord.Colour.red(),
            )
            embed.timestamp = curr_time()
            
            await ctx.send(embed=embed)
            log.debug("Sent embed")
            return

        log.debug("Player found")

        tag = ""

        player, zone, meta, matchmaking, royal = {}, {}, {}, {}, {}
        try:
            player = player_data['player']
            zone = player['zone']
            meta = player['meta']
            matchmaking, royal = player_data['matchmaking']
        except KeyError as e:
            pass

        try:
            flagEmoji = requests.get(BASE_API_URL + '/flag/' + zone['flag']).json()['emoji']
        except KeyError:
            flagEmoji = '🌎'

        hasTwitch = common_functions.check_key(meta, 'twitch')
        hasYoutube = common_functions.check_key(meta, 'youtube')
        hasTwitter = common_functions.check_key(meta, 'twitter')
        hasTag  = common_functions.check_key(player, 'tag')
        hasVanity = common_functions.check_key(meta, 'vanity')
        
        links = ""
        if hasTwitch:
            links += f"[<:twitch:895250576751853598>](https://www.twitch.tv/{meta['twitch']}) "
        
        if hasYoutube:
            links += f"[<:youtube:895250572599513138>](https://www.youtube.com/c/{meta['youtube']}) "
        
        if hasTwitter:
            links += f'[<:twitter:895250587157946388>](https://www.twitter.com/{meta["twitter"]}) '

        playerUrl = f"https://trackmania.io/#/player/{meta['vanity']}" if hasVanity else f"https://trackmania.io/#/player/{player['id']}"
        links += f"[<:tmio:895664664057356378>]({playerUrl})"

        if hasTag:
            tag = f"[{remove_mania_text_formatting(player['tag'])}] "
        

        matchData = f"""
          - Score: {common_functions.add_commas(matchmaking['score'])}
          - Rank:  {common_functions.get_ordinal_number(matchmaking['rank'])}
        """

        royalData = f"""
          - Rank:  {common_functions.get_ordinal_number(royal['rank'])}
          - Score: {common_functions.get_ordinal_number(royal['score'])}
          - Wins:  {common_functions.add_commas(royal['progression'])}
        """

        log.debug("Making embed")
        embed = discord.Embed(
            title=f"{tag}{remove_mania_text_formatting(player['name'])} {flagEmoji}",
            timestamp=curr_time(),
            color = discord.Color.random()
        )

        embed.add_field(name="Links", value=links, inline=False)
        embed.add_field(name="Royal", value=royalData, inline=True)
        embed.add_field(name="Ranked", value=matchData, inline=True)

        embed.set_footer(text="More data will be added as Trackmania.io updates")

        log.debug("Made embed, sending")
        await ctx.send(embed=embed)
        log.debug("Sent embed")

    @view_map.error
    async def error(self, ctx: commands.Context, error: commands.CommandError):
        log.error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            log.error("Missing required arguments")

            log.debug(f"Creating Error Embed")
            await ctx.send(
                embed=discord.Embed(
                    title=":warning: Missing required argument: Game Flag",
                    description="**Game Flag is a required argument that is missing**,\n\nUsage: viewmap {TMNF/TM2020}",
                    color=discord.Colour.red(),
                ).set_footer(
                    text=datetime.datetime.utcnow(), icon_url=ctx.author.avatar_url
                )
            )
            log.debug(f"Sent Error Embed")
            return None

    @get_leaderboards.error
    async def error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            log.error("Missing required argument")

            log.debug(f"Sending Error Embed")
            embed = discord.Embed(
                title=":warning: Missing required argument: Game Flag",
                description="**Game Flag is a required argument that is missing**,\n\nUsage: leaderboards {TMNF/TM2020}",
                color=discord.Colour.red(),
            )
            embed.timestamp = curr_time()
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(TMCommands(client))
