import discord
from discord.ext import commands
import os
import config

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Zalogowano jako {bot.user}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.TOKEN)

import asyncio
asyncio.run(main())
