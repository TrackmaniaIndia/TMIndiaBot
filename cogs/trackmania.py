import discord
from discord.ui import view
import util.logging.convert_logging as convert_logging
import util.discord.easy_embed as ezembed
import time

from discord.commands.commands import Option
from discord.commands import permissions
from discord.ext import commands
from util.constants import guild_ids
from util.trackmania.tm2020.player import *
from util.discord.confirmation import Confirmer
from util.trackmania.tm2020.leaderboards.campaign import (
    _get_all_fall_campaign_ids,
    update_leaderboards_campaign,
    get_player_good_maps
)

log = convert_logging.get_logging()


class Trackmania(commands.Cog):
    def __init__(self, client):
        self.client = client
        log.info(f"cogs.trackmania has finished initializing")

    # @commands.slash_command(
    #     guild_ids=guild_ids,
    #     name="player_details",
    #     description="player details for a specific player",
    # )
    # async def _player_details(
    #     self,
    #     ctx: commands.Context,
    #     username: Option(str, "The Trackmania2020 Username", required=True),
    # ):
    #     data = get_player_data(username)

    #     if data == None:
    #         error_embed = ezembed.create_embed(
    #             title="This user does not exist",
    #             description=f"Username given: {username}",
    #             color=discord.Colour.red(),
    #         )
    #         await ctx.respond(embed=error_embed)
    #         log.error(f"{username} is not a valid username")
    #     else:
    #         await ctx.respond(embed=data)

    @commands.slash_command(guild_ids=guild_ids, name="update_campaign_leaderboards")
    @permissions.is_owner()
    async def _update_campaign_leaderboards(self, ctx: commands.Context):
        log.debug(f"Creating Confirmation Prompt")
        confirm_continue = Confirmer()

        log.debug(f"Chaning Button Labels")
        confirm_continue.change_cancel_button(label="No, Stop")
        confirm_continue.change_confirm_button(label="Yes, Continue")
        log.debug(f"Changed Button Labels")

        log.debug(f"Sending Prompt")
        message = await ctx.respond(
            embed=ezembed.create_embed(
                title="Are you sure you want to continue?",
                description="This can take over 10minutes, the bot will be unusable in this period",
                color=discord.Colour.red(),
            ),
            view=confirm_continue,
        )
        log.debug(f"Sent Confirmation Prompt")

        log.debug(f"Awaiting a response")
        await confirm_continue.wait()
        log.debug(f"Response Received")

        log.debug(f"Deleting Original Message")
        await message.delete_original_message()
        log.debug(f"Deleted Message")

        if confirm_continue.value == False:
            log.debug(f"{ctx.author.name} does not want to continue")
            return

        log.debug(f"{ctx.author.name} wants his username added")

        log.debug(f"Getting Fall Campaign IDs, (Excluding First Five)")
        fall_ids = _get_all_fall_campaign_ids(ignore_first_five=False)
        log.debug(f"Got the Fall IDs")

        log.debug(f"Updating Leaderboards")
        update_leaderboards_campaign(fall_ids)
        log.debug(f"Leaderboards Updated, Sleeping for 30s to save API")
        time.sleep(30)

        await ctx.respond("Done")
        
    @commands.slash_command(guild_ids=guild_ids, name='stalkplayerfortscc', description='Checks if the player is in top 500 for the tscc map pool')
    @permissions.has_any_role('TSCC', 'Moderator', 'admin')
    async def _check_player(self, ctx: commands.Context, username: Option(str, description='Username of the player', required=True)):
        log.debug(f'Checking Player Username -> {username}')
        player_id = get_player_id(username)
        log.debug(f'Got Player Id -> {player_id}')
        
        if player_id == None:
            log.error(f'Invalid Username Given, Username -> {username}')
            await ctx.respond('Invalid Username')
        else:
            log.debug(f'Valid Username, Username -> {username}')
            log.debug(f'Executing Function, Pray')
            await ctx.respond(embed=get_player_good_maps(username))


def setup(client):
    client.add_cog(Trackmania(client))
