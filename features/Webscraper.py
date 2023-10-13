import discord
from discord.ext import commands, tasks
import aiohttp
from bs4 import BeautifulSoup





#NEED TO FIX THIS, WILL SPEND SOME TIME ON IT
PRODUCT_URL = 'https://www.bestbuy.com/site/searchpage.jsp?st=rtx+4090+ti'

class Webscraper(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.check_restock.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Webscraper.py is online')

    def cog_unload(self):
        self.check_restock.cancel()

    async def fetch_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()


    #this loops through our restock check function every 5 minutes
    @tasks.loop(minutes=5)
    async def check_restock(self, guild):
        try:
            async with aiohttp.ClientSession() as session:
                html = await self.fetch_page(session, PRODUCT_URL)
                soup = BeautifulSoup(html, 'html.parser')
                out_of_stock_elements = soup.select('.add-to-cart-button[disabled]')


            #set channel you want to provide the 4090 updates to here
                channel_id = 1162376636675666023
                channel = guild.get_channel(channel_id)
            
                if not out_of_stock_elements:
                    await channel.send(f'Might be back in stock now! Go ahead and check: {PRODUCT_URL}')
                else:
                    await channel.send('Still out of stock.')
        except Exception as e:
            print(f"Error: {e}")


    @check_restock.before_loop
    async def before_check_restock(self):
        await self.client.wait_until_ready()


async def setup(client):
    await client.add_cog(Webscraper(client))
