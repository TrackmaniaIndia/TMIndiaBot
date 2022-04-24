import asyncio
import datetime
import json
import os
from ast import keyword
from curses import killchar
from errno import EMSGSIZE
from itertools import zip_longest

import discord
from discord import ApplicationContext
from discord.ext import commands, tasks
from trackmania import Player

import bot.utils.commons as commons
from bot import constants
from bot.bot import Bot
from bot.log import get_logger
from bot.utils.discord import create_embed

log = get_logger(__name__)


class UpdateTrophies(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        log.info("Starting TrophyLeaderboardUpdates loop")
        self._update_trophy_leaderboards.start()

    @tasks.loop(
        time=datetime.time(hour=19, minute=0, second=0, tzinfo=datetime.timezone.utc)
    )
    async def _update_trophy_leaderboards(self):
        await self.bot.wait_until_ready()
        await self.__update_leaderboards()

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="run-it",
    )
    @discord.is_owner()
    async def _run_it(self, ctx: ApplicationContext):
        await self.__update_leaderboards()

    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="run-it-for-me",
    )
    @discord.is_owner()
    async def _run_it_for_me(self, ctx: ApplicationContext):
        await ctx.defer()
        await self.__update_leaderboards(ctx)

    # TODO: Add permissions
    @commands.slash_command(
        guild_ids=constants.Bot.default_guilds,
        name="update-and-show-leaderboards",
        description="Updates and shows the trophy leaderboards",
    )
    async def _update_and_show_lbs(self, ctx: ApplicationContext):
        await ctx.defer()
        await self.__update_leaderboards(ctx=ctx)

    async def __update_leaderboards(self, ctx: ApplicationContext = None):
        log.info("Updating Trophy Leaderboards")

        if ctx is not None:
            with open(
                f"./bot/resources/guild_data/{ctx.guild.id}/config.json",
                "r",
                encoding="UTF-8",
            ) as file:
                config_data = json.load(file)

                if not config_data.get("trophy_tracking", False):
                    await ctx.respond(
                        "Trophy tracking is not setup. Please use `/setup-tracking` to set this up."
                    )
                    return

            guild_ids = [ctx.guild.id]
            channel_ids = [ctx.channel.id]
        else:
            guild_ids, channel_ids = [], []
            for folder in os.listdir("./bot/resources/guild_data/"):
                with open(
                    f"./bot/resources/guild_data/{folder}/config.json",
                    "r",
                    encoding="UTF-8",
                ) as file:
                    config_data = json.load(file)

                if config_data.get("trophy_tracking", False):
                    log.debug(folder)
                    guild_ids.extend([folder])
                    channel_ids.extend(
                        [config_data.get("trophy_update_channel", 962961137924726834)]
                    )

        sleep_time = 15

        log.info("Got all Guild and Channel IDs")
        for i, guild_id in enumerate(guild_ids):
            player_ids = []

            log.info(f"Updating for {guild_id}")
            log.debug("Getting all player ids")
            with open(
                f"./bot/resources/guild_data/{guild_id}/trophy_tracking.json",
                "r",
                encoding="UTF-8",
            ) as file:
                tracking_data = json.load(file)

            for player in tracking_data.get("tracking"):
                player_ids.append(player.get("player_id"))

            log.info(f"Getting all Trophy Data for {guild_id}")
            new_player_data = []
            no_of_players = len(player_ids)

            if no_of_players == 0 and ctx is None:
                try:
                    log.info(f"No Users stored for {guild_id}")
                    guild = await self.bot.fetch_guild(guild_id)
                    embed = create_embed(
                        title=f"Trophy Leaderboard for {guild.name}",
                        description="No Users are Stored.\nUse the `/add-player-tracking` command to add players to tracking.\nRerun `/setup-tracking` and click `No` if you want to unsubscribe.",
                        color=discord.Colour.red(),
                    )
                    await self.bot.get_channel(channel_ids[i]).send(embed=embed)
                except discord.errors.Forbidden:
                    log.error("%s is forbidden", str(guild_id))
                continue

            for j, player_id in enumerate(player_ids):
                log.debug(
                    f"Getting Data for {player_id} - Remaining: {no_of_players - j - 1}"
                )

                player_data = await Player.get_player(player_id)
                player_name = player_data.name
                player_id = player_data.player_id
                score = player_data.trophies.score()

                new_player_data.extend(
                    [
                        {
                            "username": player_name,
                            "player_id": player_id,
                            "score": score,
                        }
                    ]
                )

                await asyncio.sleep(sleep_time)

            log.debug("Sorting Players based on score")
            new_player_data = sorted(
                new_player_data, key=lambda o: o["score"], reverse=True
            )
            displacements = {}

            log.debug("Looping through new data and finding displacements")
            for j, old_data in enumerate(tracking_data.get("tracking")):
                player_name = old_data.get("username")
                log.debug("Checking %s", player_name)

                for k, new_data in enumerate(new_player_data):
                    if new_data.get("username").lower() == player_name.lower():
                        rank_displacement = j - k
                        trophy_change = new_data.get("score") - old_data.get("score")
                        displacements.update(
                            {
                                player_name: {
                                    "rank": rank_displacement,
                                    "trophy": commons.add_commas(trophy_change),
                                }
                            }
                        )

            log.debug(displacements)

            log.debug("Got Displacements and Ranks")
            split_list = list(zip_longest(*(iter(new_player_data),) * 10))
            pages_needed = len(split_list)
            embed_list = [
                create_embed(
                    f"Trophy Leaderboard - Page {h + 1}",
                    description=f"Updated {datetime.datetime.now()}",
                )
                for h in range(pages_needed)
            ]

            log.debug("Creating string for embed")
            for j, plist in enumerate(split_list):
                log.debug(plist)
                tstr = ""
                for k, person in enumerate(plist):
                    log.debug(person)
                    if person is None:
                        break

                    username = person.get("username")
                    score = commons.add_commas(person.get("score"))
                    rank_displacement = displacements.get(username).get("rank")
                    if rank_displacement > 0:
                        rank_displacement = f"+{rank_displacement} "
                    elif rank_displacement == 0:
                        rank_displacement = " = "
                    else:
                        rank_displacement = f"{rank_displacement} "

                    trophy_change = displacements.get(username).get("trophy")
                    tstr = (
                        tstr
                        + f"({rank_displacement}) {k + 1}. {username} - {score}. Trophy Change -> {trophy_change}\n"
                    )
                embed_list[j].add_field(
                    name="Trophies", value=f"```{tstr}```", inline=False
                )

            # Sending Message
            if ctx is not None:
                try:
                    await ctx.respond(embed=embed_list[0])
                except:
                    continue
            else:
                try:
                    channel = self.bot.get_channel(channel_ids[i])
                    await channel.send(embed=embed_list[0])
                except:
                    continue

            log.debug("Dumping new data to file")
            tracking_data["tracking"] = new_player_data
            with open(
                f"./bot/resources/guild_data/{guild_id}/trophy_tracking.json", "w"
            ) as file:
                json.dump(tracking_data, file, indent=4)

        log.info("Leaderboards Updated.")


def setup(bot: Bot):
    bot.add_cog(UpdateTrophies(bot))
