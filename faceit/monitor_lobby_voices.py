from discord.ext import commands
import re
import discord
import random

class MonitorLobbyVoicesCog(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member : discord.Member, before : discord.VoiceState, after : discord.VoiceState):
        if after.channel and re.match(r"^Lobby \d+$", after.channel.name):
            category = after.channel.category

            if category:
                if len(after.channel.members) == 10:

                    cap1 = random.choice(after.channel.members)
                    cap2 = random.choice(after.channel.members)

                    await category.text_channels[0].send('''
                        TEST
                    ''')
        
        if before.channel and re.match(r"^Lobby \d+$", before.channel.name):
            if len(before.channel.members) == 9:
                role = discord.utils.get(self.bot.get_guild(1383163443636338830).roles, name = 'Ненадежный')
                await member.add_roles(role)

async def setup(bot : commands.Bot):
    await bot.add_cog(MonitorLobbyVoicesCog(bot))