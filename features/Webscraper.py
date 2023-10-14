import discord
import requests

from bs4 import BeautifulSoup
from discord.ext import commands, tasks


class Webscraper(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channel_id = 
        self.stock_check.start()


    def cog_unload(self):
        self.stock_check.cancel()


    def check_stock(self):
        url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-4090-24gb-gddr6x-graphics-card-titanium-black/6521430.p?skuId=6521430'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        out_of_stock_elements = soup.select('button:-soup-contains("Sold Out")')  

        return len(out_of_stock_elements) == 0



    @tasks.loop(hours=24)
    async def stock_check(self):
        channel = self.client.get_channel(self.channel_id)
        if self.check_stock():
            await channel.send('4090 ti back in stock at Best Buy!')
        else:
            await channel.send('No 4090 ti in stock at Best Buy.')



    @stock_check.before_loop
    async def before_stock_check(self):
        await self.client.wait_until_ready() 



async def setup(client):
    await client.add_cog(Webscraper(client))