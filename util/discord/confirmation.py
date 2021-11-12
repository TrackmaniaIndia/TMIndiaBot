import discord
import util.logging.convert_logging as convert_logging

log = convert_logging.get_logging()

class Confirmer(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.confirm_button = self.children[0]
        self.cancel_button = self.children[1]
        log.debug(f'Created Confirmation Menu')
        
        
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        log.debug(f'Confirm Button Clicked by {interaction.user.name} in {interaction.guild.name} in channel {interaction.channel.name}')
        self.value = True
        self.stop()
        
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        log.debug(f'Cancel Button Clicked by {interaction.user.name} in {interaction.guild.name} in channel {interaction.channel.name}')
        self.value = False
        self.stop()
        
        
    def change_confirm_button(self, label: str, color: str = 'green'):
        log.debug(f'Changing Confirm Button to Label: {label} and Color: {color}')
        self.confirm_button.label = label
        self.confirm_button.style = getattr(discord.ButtonStyle, color.lower())
        
    def change_cancel_button(self, label: str, color: str = 'red'):
        log.debug(f'Changing Cancel Button to Label: {label} and color: {color}')
        self.cancel_button.label = label
        self.cancel_button.style = getattr(discord.ButtonStyle, color.lower())