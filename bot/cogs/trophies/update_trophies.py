import asyncio
import datetime
import json
from itertools import zip_longest

import discord
from discord import ApplicationContext, Bot
from discord.ext import commands, tasks
from discord.ext.pages import Paginator
from trackmania import Player

from bot import constants
from bot.bot import Bot
from bot.log import get_logger
from bot.utils.commons import Commons
from bot.utils.discord import EZEmbed

log = get_logger(__name__)


class UpdateTrophies(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        log.info("Starting TrophyLeaderboardUpdates loop")
        self._update_trophy_leaderboards.start()

    @tasks.loop(
        time=datetime.time(hour=18, minute=30, second=0, tzinfo=datetime.timezone.utc)
    )
    async def _update_trophy_leaderboards(self):
        log.info("Updating Trophy Leaderboards")

        player_ids = []
        log.debug("Opening File to Get all PlayerIDs")
        with open("./bot/resources/json/trophy_tracking.json", "r") as file:
            trophy_tracking = json.load(file)

        log.debug("Getting all PlayerIDs")
        for player in trophy_tracking.get("tracking"):
            player_ids.append(player.get("player_id"))

        if len(player_ids) > 10:
            sleep_time = 7.5
        else:
            sleep_time = 0

        log.debug("Getting all Trophy Data")
        new_player_data = []
        for player_id in player_ids:
            log.debug(f"Getting Data for {player_id}")

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
            new_player_data, key=lambda k: k["score"], reverse=True
        )
        displacements = {}

        log.debug("Looping through new data and finding displacements")
        for i, old_data in enumerate(trophy_tracking.get("tracking")):
            player_name = old_data.get("username")

            for j, new_data in enumerate(new_player_data):
                if new_data.get("username").lower() == player_name.lower():
                    rank_displacement = i - j
                    trophy_change = new_data.get("score") - old_data.get("score")
                    displacements.update(
                        {
                            player_name: {
                                "rank": rank_displacement,
                                "trophy": Commons.add_commas(trophy_change),
                            }
                        }
                    )

        log.warn(displacements)

        log.debug("Got Displacements and Ranks")
        split_list = list(zip_longest(*(iter(new_player_data),) * 10))
        pages_needed = len(split_list)
        embed_list = [
            EZEmbed.create_embed(
                f"Trophy Leaderboard - Page {i + 1}",
                description=f"Updated {datetime.datetime.now()}",
            )
            for i in range(pages_needed)
        ]

        log.debug("Creating string for embed")
        for j, plist in enumerate(split_list):
            log.debug(plist)
            tstr = ""
            for i, person in enumerate(plist):
                log.debug(person)
                if person is None:
                    break

                username = person.get("username")
                score = Commons.add_commas(person.get("score"))
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
                    + f"({rank_displacement}) {i + 1}. {username} - {score}. Trophy Change -> {trophy_change}\n"
                )
            embed_list[j].add_field(
                name="Trophies", value=f"```{tstr}```", inline=False
            )

        channel = self.bot.get_channel(constants.Channels.testing_general)

        log.debug("Sending Embed")
        await channel.send(embed=embed_list[0])

        log.debug("Dumping new data to file")
        trophy_tracking["tracking"] = new_player_data
        with open("./bot/resources/json/trophy_tracking.json", "w") as file:
            json.dump(trophy_tracking, file, indent=4)


def setup(bot: Bot):
    bot.add_cog(UpdateTrophies(bot))
