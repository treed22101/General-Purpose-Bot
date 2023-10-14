import discord
import asyncio

from discord.ext import commands
from collections import defaultdict


#set dicts here to hold the warn count and spam count
class AntiSpam(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.user_message_count = defaultdict(int) 
        self.user_last_message = defaultdict(str)   
        self.warned_users = set()                   



    @commands.Cog.listener()
    async def on_ready(self):
        print('AntiSpam.py is online.')


    #the listener for the spam of 5 messages and the execution of a muted role if spam exceeds 10 after the warning at 5 messages
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        
        if message.content.startswith('!'):
            return

        if message.content == self.user_last_message[message.author.id]:
            self.user_message_count[message.author.id] += 1
        else:
            self.user_message_count[message.author.id] = 1

        self.user_last_message[message.author.id] = message.content

        if self.user_message_count[message.author.id] == 5:
            warning_message = "Don't spam."
            await message.channel.send(f"{message.author.mention} {warning_message}")
            self.warned_users.add(message.author.id)

        elif self.user_message_count[message.author.id] >= 10 and message.author.id in self.warned_users:
            mute_message = "I said don't spam, muted for 2 minutes"
            await message.channel.send(f"{message.author.mention} {mute_message}")

            role = discord.utils.get(message.guild.roles, name="Muted")
            if not role:
                role = await message.guild.create_role(name="Muted")
                for channel in message.guild.channels:
                    await channel.set_permissions(role, send_messages=False, read_messages=True)

            await message.author.add_roles(role)
            await asyncio.sleep(120)  
            await message.author.remove_roles(role)

            self.user_message_count[message.author.id] = 0
            self.warned_users.discard(message.author.id)

        await self.client.process_commands(message)


async def setup(client):
    await client.add_cog(AntiSpam(client))