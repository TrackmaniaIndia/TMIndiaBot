import discord
from discord.ext import commands

import util.logging.convert_logging as convert_logging
from util.cog_helpers.generic_helper import get_version
from util.logging.usage import record_usage, finish_usage
from util.constants import guild_ids, role_ids
import util.discord.easy_embed as ezembed
from discord.commands.commands import slash_command

log = convert_logging.get_logging()

# role_ids = [905321194071416872, 905321269451427840, 905321297146441729]

class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role):
        super().__init__(label=role.name, style=discord.enums.ButtonStyle.primary, custom_id=str(role.id))
        
    async def callback(self, interaction: discord.Interaction):
        # Which user clicked the button
        log.debug(f'Getting User who Clicked this')
        user = interaction.user
        log.info(f'The user who clicked a button was {user.name}')
        # get the role this button is for
        log.debug(f'Getting the button clicked')
        role = interaction.guild.get_role(int(self.custom_id))
        log.info(f'The role that was asked for is {role}')
        
        if role is None:
            log.error('This role does not exist, returning without doing anything')
            return
        
        if role not in user.roles:
            log.debug(f'User does not have role, adding')
            await user.add_roles(role)
            await interaction.response.send_message(f"You have been given the role {role.mention}", ephemeral=True)
            log.debug(f'Add {role} for {user.name}')
        else:
            log.debug(f'User has role, removing')
            await user.remove_roles(role)
            await interaction.response.send_message(f'The {role.mention} role has been taken from you', ephemeral=True)
            log.debug(f'Removed {role} for {user.name}')
class ReactionRole(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @slash_command(guild_ids=guild_ids, name='post_cotd_roles', description="Post the button role message")
    async def _post_cotd_roles(self, ctx: commands.Context):
        log.debug(f'Making View')
        view = discord.ui.View(timeout=None)
        log.debug(f'Created View')
        
        for role_id in role_ids[str(ctx.guild.id)]:
            log.debug(f'Adding {role_id}')
            role = ctx.guild.get_role(role_id)
            view.add_item(RoleButton(role))
            
        await ctx.respond('Click a button to assign yourself a role', view=view)
        
    @commands.Cog.listener()
    async def on_ready(self):
        """This function is called every time the bot restarts.
        If a view was already created before (with the same custom IDs for buttons)
        it will be loaded and the bot will start watching for button clicks again.
        """

        # we recreate the view as we did in the /post command
        log.debug(f'Recreating View')
        view = discord.ui.View(timeout=None)
        # make sure to set the guild ID here to whatever server you want the buttons in
        log.debug(f'Looping through Guild Ids')
        for guild_id in role_ids:
            log.debug(f'Doing {guild_id}')
            guild = self.client.get_guild(int(guild_id))
            log.debug(f'Guild Name: {guild.name}')
            for role_id in role_ids[guild_id]:
                role = guild.get_role(role_id)
                log.debug(f'Adding {role.name} with {role_id}')
                view.add_item(RoleButton(role))

        # add the view to the bot so it will watch for button interactions
        self.client.add_view(view)
    
def setup(client):
    client.add_cog(ReactionRole(client))