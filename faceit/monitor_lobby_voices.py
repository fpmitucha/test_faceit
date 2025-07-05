import re
import discord
from discord.ext import commands
from start_faceit import start_faceit_game

class MonitorLobbyVoicesCog(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.active_lobbies = set()
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member : discord.Member, before : discord.VoiceState, after : discord.VoiceState):
        if after.channel and re.match(r"^Lobby \d+$", after.channel.name):
            category = after.channel.category

            self.bot.get_guild()

            if category:
                members = after.channel.members
                if len(members) == 10 and after.channel.id not in self.active_lobbies:
                    self.active_lobbies.add(after.channel.id)    
                    await start_faceit_game(members, category.text_channels[0])

        if before.channel and re.match(r"^Lobby \d+$", before.channel.name):

            if len(before.channel.members) < 10:
                self.active_lobbies.discard(before.channel.id)

            if len(before.channel.members) == 9:
                role = discord.utils.get(self.bot.get_guild(1383163443636338830).roles, name = 'Ненадежный')
                await member.add_roles(role)

async def setup(bot : commands.Bot):
    await bot.add_cog(MonitorLobbyVoicesCog(bot))