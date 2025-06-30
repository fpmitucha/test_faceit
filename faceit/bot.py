from discord.ext import commands
import discord
from dotenv import load_dotenv
from database import InitDb, closeConnection
import logging
import os
import asyncio

logger = logging.basicConfig(
    level=logging.INFO, 
    format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)

intents = discord.Intents.all()

intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents = intents)

cogs = ['register', 'rules', 'helper_commands', 'monitor_lobby_voices']

async def setup_hook():
    for cog in cogs:
        await bot.load_extension(cog)
    
async def main():
    load_dotenv()

    token = os.getenv('token')

    bot.setup_hook = setup_hook

    try:
        await InitDb()
        await bot.start(token)
    except Exception as e:
        print(e)
    finally:
        await closeConnection()

asyncio.run(main())