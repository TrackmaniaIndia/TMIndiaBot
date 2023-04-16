import json

import discord.ext.commands as commands
from discord import ApplicationContext, SlashCommandOptionType
from discord.commands import Option
from discord.ext.pages import Paginator
from trackmania import Player

from bot.bot import Bot
from bot.log import get_logger, log_command
from bot.utils.discord import Confirmer, create_embed

log = get_logger(__name__)


class AddPlayerTracking(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(
        name="add-player-tracking",
        description="Adds a player to the trophy tracking list",
    )
    @commands.has_permissions(manage_guild=True)
    async def _add_player_tracking(
        self,
        ctx: ApplicationContext,
        username: Option(
            SlashCommandOptionType.string,
            "The username of the player to add.",
            required=True,
        ),
    ):
        log_command(ctx, "add_player_tracking")

        await ctx.defer(ephemeral=True)

        log.debug(f"Searching for Player with the username -> {username}")
        search_result = await Player.search(username)

        if search_result is None:
            await ctx.respond("This player does not exist.", ephemeral=True)
            return

        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/config.json", "r"
        ) as file:
            config_data = json.load(file)

            if not config_data.get("trophy_tracking", False):
                await ctx.respond(
                    "Trophy Tracking is not set up for this server. Please use the `/setup-tracking` command to start your setup process.",
                    delete_after=45,
                )
                return

            log.debug("Checking if player has already been added.")
            # Checking if the player is already in the list.
            with open(
                f"./bot/resources/guild_data/{ctx.guild.id}/trophy_tracking.json", "r"
            ) as file:
                tracking_data = json.load(file)

                for user in tracking_data.get(
                    "tracking", []
                ):  # looping through all the players in the list.
                    if user.get("username", "").lower() == username.lower():
                        log.info("Player has already been added to the tracking list.")
                        await ctx.respond(
                            "This user has already been added to the tracking list.",
                            ephemeral=True,
                        )
                        # Does not save if player is already in the list.
                        return

            mod_logs_channel_id = config_data.get("mod_logs_channel")

            if mod_logs_channel_id != 0:
                log.debug("Sending Message to Mod Logs")
                mod_logs_channel = self.bot.get_channel(mod_logs_channel_id)
                if mod_logs_channel is not None:

                    try:
                        await mod_logs_channel.send(
                            content=f"Requestor: {ctx.author.mention} is adding {username} to trophy player tracking."
                        )
                    except Exception as e:
                        log.error("Failed to send message to mod logs channel: %s", e)

        confirmation_paginator = None

        try:
            list_len = len(search_result)
            if list_len > 1:
                # Multiple users have been found.
                log.debug("Multiple users have been found.")

                confirmation_prompts: list = []

                for k, indi_search_result in enumerate(
                    search_result
                ):  # Only doing first 9 or 10
                    # Create a confirmation prompt for each player.
                    embed = create_embed(
                        "Multiple Search Results Found: "
                        + str(k + 1)
                        + "/"
                        + str(list_len),
                        "Player Username: "
                        + indi_search_result.name
                        + "\nPlayer ID: "
                        + indi_search_result.player_id,
                    )
                    confirmation_prompts.append([embed])

                log.debug("Created confirmation prompts.")
                log.debug("Creating Paginator.")
                confirmer = Confirmer()
                confirmation_paginator = Paginator(
                    confirmation_prompts, custom_view=confirmer, timeout=30
                )
                paginator_respond = await confirmation_paginator.respond(
                    ctx.interaction, ephemeral=True
                )
                await confirmer.wait()

                if confirmer.value is None:
                    log.debug("Confirmer Timeout.")
                    await confirmation_paginator.cancel(page="Paginator has timed out.")
                    confirmer.disable_all_items()
                    return
                elif not confirmer.value:
                    log.debug("Person declined.")
                    await confirmation_paginator.cancel(
                        page="Adding a player has been cancelled."
                    )
                    confirmer.disable_all_items()
                    return
                else:
                    log.debug("Person confirmed.")
                    player_id = search_result[
                        confirmation_paginator.current_page
                    ].player_id
                    confirmer.disable_all_items()
            else:
                player_id = search_result[0].player_id
        except IndexError:
            log.error("IndexError: Invalid username given. No user was found.")
            errormsg = (
                "Invalid Username was given. No user was found with this username."
            )
            await ctx.respond(errormsg, ephemeral=True)
            return

        log.debug("Getting Trophy Count of Player")
        player_data = await Player.get_player(player_id)

        trophy_count = player_data.trophies.score()

        log.debug(f"Trophy Count of {username} is {trophy_count}")

        log.debug("Opening File")
        with open(
            f"./bot/resources/guild_data/{ctx.guild.id}/trophy_tracking.json", "r"
        ) as file:
            tracking_data = json.load(file)

        log.debug("Adding Player to List")
        tracking_data["tracking"].extend(
            [
                {
                    "username": player_data.name,
                    "player_id": player_data.player_id,
                    "score": trophy_count,
                },
            ],
        )

        log.debug("Sorting tracking data based on trophy count")
        # sort tracking data based on trophy_count
        tracking_data["tracking"] = sorted(
            tracking_data["tracking"], key=lambda k: k["score"], reverse=True
        )

        log.debug("Dumping to File")
        with open(
            f"bot/resources/guild_data/{ctx.guild.id}/trophy_tracking.json", "w"
        ) as file:
            json.dump(tracking_data, file, indent=4)

        if confirmation_paginator is None:
            await ctx.respond(
                f"{username} has been added to the trophy tracking list.",
                ephemeral=True,
            )
        else:
            await confirmation_paginator.cancel(
                page=f"{username} has been added to the trophy tracking list"
            )


def setup(bot: Bot):
    bot.add_cog(AddPlayerTracking(bot))
