import discord
import requests

from discord.ext import commands, tasks

FACT_URL = "https://uselessfacts.jsph.pl/random.json?language=en"

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_fact.start()



    @commands.Cog.listener()
    async def on_ready(self):
        print('RandomFact.py is online.')



    def cog_unload(self):
        self.send_fact.cancel()



    def fetch_random_fact(self):
        try:
            response = requests.get(FACT_URL)
            response.raise_for_status()
            data = response.json()
            return data['text']
        except requests.RequestException:
            return "Error, can't get a fact for you."


    #gets a random fact for us from the url every 12 hours and sends in a specified channel
    @tasks.loop(hours=12)
    async def send_fact(self):
        channel_id = 1162698559502688326
        channel = self.bot.get_channel(channel_id)
        fact = self.fetch_random_fact()
        await channel.send(fact)


    @send_fact.before_loop
    async def before_send_fact(self):
        await self.bot.wait_until_ready()  

async def setup(client):
    await client.add_cog(Random(client))