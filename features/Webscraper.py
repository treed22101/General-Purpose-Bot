import discord
from discord.ext import commands, tasks
import aiohttp
from bs4 import BeautifulSoup


PRODUCT_URL = 'https://www.bestbuy.com/site/searchpage.jsp?st=rtx+4090+ti'



class Webscraper(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.check_restock.start()

    def cog_unload(self):
        self.check_restock.cancel()

    async def fetch_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()


    #this loops through our restock check function every 5 minutes
    @tasks.loop(minutes=5)
    async def check_restock(self):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_page(session, PRODUCT_URL)
            soup = BeautifulSoup(html, 'html.parser')
            out_of_stock_elements = soup.select('.add-to-cart-button[disabled]')


            #set channel you want to provide the 4090 updates to here
            channel = self.client.get_channel(1161629542738305107)
            
            if not out_of_stock_elements:
                await channel.send('New update on the RTX 4090 TI! Go check: {}'.format(PRODUCT_URL))
            else:
                await channel.send('No updates. Still out of stock.')




    @check_restock.before_loop
    async def before_check_restock(self):
        await self.client.wait_until_ready()




async def setup(client):
    await client.add_cog(Webscraper(client))
