import discord
from discord.ext import commands



class Ping(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ping.py is online.")
        print('______________________')





#latency command
    @commands.command()
    async def ping(self, ctx):
        latency = round(self.client.latency * 1000)

        embed = discord.Embed(
            title='Ping!',
            description=f'My current ping is {latency:.2f} ms',
            color=discord.Color.yellow()
        )

        embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)



async def setup(client):
    await client.add_cog(Ping(client))