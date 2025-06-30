from discord.ext import commands
import discord

class RulesCog(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.rules = '''
        RULES
        '''
    
    @commands.Cog.listener()
    async def on_ready(self):
        rule_channels = discord.utils.get(self.bot.get_guild(1383163443636338830).text_channels, name = 'rules')

        embed = discord.Embed(
            title='Правила'
        )

        if rule_channels:
            msg = await rule_channels.send(embed = embed)
            await msg.add_reaction('✅')    
        else:
            raise ValueError("the channel was not found")

async def setup(bot : commands.Bot):
    await bot.add_cog(RulesCog(bot))