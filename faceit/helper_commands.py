from discord.ext import commands
import discord
import asyncio

class HelperCommandsCog(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def clear(self, ctx : commands.Context, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.channel.send(f'Deleted {amount} messages', delete_after=5)

    @commands.command()
    async def get_maps(self, ctx : commands.Context):

        main_guild = self.bot.get_guild(1383163443636338830)
        maps = ['zone7', 'sandstone', 'sakura', 'rust', 'province', 'breeze', 'dune']
        emodjis = [e for e in main_guild.emojis if e.name in maps]

        embed = discord.Embed(
            title = 'Выберите карту, 10 cек',
            color = discord.Color.green()
        )

        msg = await ctx.channel.send(embed = embed)
        await asyncio.gather(*(msg.add_reaction(e) for e in emodjis))
    
        await asyncio.sleep(10)

        msg : discord.Message = [m async for m in ctx.channel.history(limit = 1)][0]

        counts = {}

        for reactions in msg.reactions:
            if reactions.emoji.name in maps:
                counts[reactions.emoji] = reactions.count
        
        res : discord.Emoji = max(counts, key=counts.get)

        print(str(res))

        await msg.delete()

        await ctx.channel.send(f'Карта: {str(res.name).capitalize()} {str(res)}')
    
    @commands.command()
    async def get_rounds(self, ctx : commands.Context):

        rounds = ['1️⃣', '2️⃣', '3️⃣']

        embed = discord.Embed(
            title = 'Выберите кол-во раундов. 10 cек',
            color = discord.Color.blue()
        )

        embed.add_field(
            name='1️⃣ - 10 раундов',
            value = 10,
            inline=False
        )

        embed.add_field(
            name='2️⃣ - 13 раундов',
            value = 13,
            inline=False
        )

        embed.add_field(
            name='3️⃣ - 16 раундов',
            value = 16,
            inline=False
        )

        msg = await ctx.channel.send(embed = embed)
        await asyncio.gather(*(msg.add_reaction(e) for e in rounds))
     
        await asyncio.sleep(10)

        msg : discord.Message = [m async for m in ctx.channel.history(limit = 1)][0]

        counts = {}

        for reactions in msg.reactions:
            if reactions.emoji in rounds:
                counts[reactions.emoji] = reactions.count
            
        res = max(counts, key=counts.get)

        await msg.delete()

        await ctx.channel.send(res)

async def setup(bot : commands.Bot):
    await bot.add_cog(HelperCommandsCog(bot))
