import re
import discord
import random
from discord.ext import commands
from typing import List
from discord.ui import Select, View

class MonitorLobbyVoicesCog(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member : discord.Member, before : discord.VoiceState, after : discord.VoiceState):
        if after.channel and re.match(r"^Lobby \d+$", after.channel.name):
            category = after.channel.category

            if category:
                members = after.channel.members
                if len(members) == 1:

                    cap1 = random.choice(members)
                    cap2 = random.choice(members)

                    embed = discord.Embed(
                        title='Faceit ranked'
                    )

                    embed.add_field(
                        name='T',
                        value = cap1.mention,
                        inline=False
                    )

                    embed.add_field(
                        name = 'CT',
                        value = cap2.mention,
                        inline = False
                    )

                    view = DropDownView(members)

                    await category.text_channels[0].send(
                        embed=embed,
                        view=view
                    )

        
        if before.channel and re.match(r"^Lobby \d+$", before.channel.name):
            if len(before.channel.members) == 9:
                role = discord.utils.get(self.bot.get_guild(1383163443636338830).roles, name = 'Ненадежный')
                await member.add_roles(role)

class SelectPlayers(Select):
    def __init__(self, members : List[discord.Member]):
        options = []

        for member in members:
            options.append(
                discord.SelectOption(label = f'{member.name}', value=f'{member.name}')
            )
        
        super().__init__(placeholder='Выберите игрока', min_values = 1, max_values = 1, options=options)
    
    async def callback(self, interaction : discord.Interaction):
        await interaction.response.send_message(f"You've choosed {self.values[0]}")

class DropDownView(View):
    def __init__(self, members):
        super().__init__(timeout=None)
        self.add_item(SelectPlayers(members))

async def setup(bot : commands.Bot):
    await bot.add_cog(MonitorLobbyVoicesCog(bot))