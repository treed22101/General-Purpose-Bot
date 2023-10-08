import discord
from discord.ext import commands
import json

class Starboard(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Starboard.py is online.")
        
        





async def setup(client):
    await client.add_cog(Starboard(client))