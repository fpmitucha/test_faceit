from discord.ext import commands

class HelperCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def clear(self, ctx : commands.Context, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.channel.send(f'Deleted {amount} messages', delete_after=5)
    
async def setup(bot : commands.Bot):
    await bot.add_cog(HelperCommandsCog(bot))