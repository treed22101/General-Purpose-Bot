import discord
from discord.ext import commands, tasks
import os
import asyncio
from dotenv import load_dotenv
from itertools import cycle

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())



bot_status = cycle(['Uno', 'Blackjack', 'Poker', 'Go Fish'])

@tasks.loop(seconds=3600)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))



@client.event
async def on_ready():
    print("You have successfully logged into the Bot")
    print('_________________________________________')
    change_status.start()


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')



banned_words = ['NIGGER', 'NIGGA', 'FAGGOT', 'FAG', 'TRANNY', 'CHINK', 'RETARD']

@client.event
async def on_message(message):
    await client.process_commands(message)
    for word in banned_words:
        if word in message.content.lower() or word in message.content.upper():
            await message.delete()
            await message.channel.send(f'{message.author.mention} You cannot say that word!')




async def main():
    async with client:
        await load()
        await client.start(TOKEN)

asyncio.run(main())