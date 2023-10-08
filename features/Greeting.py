import discord
from discord.ext import commands 

class Greeting(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Greeting.py is online.")
        




#when a user joins the server/ SET THE WELCOME CHANNEL ID
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        channel_id = 1068521369941323798
        channel = guild.get_channel(channel_id)

        if channel:
            embed = discord.Embed(
                title='Welcome!',
                description=f'Welcome {member.mention}, thank you for joining!',
                color=discord.Color.dark_purple()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name='Go say hi in gen:', value='You might make some new friends!')
            
            await channel.send(embed=embed) 





#when a user leaves the server/ SET THE WELCOME CHANNEL ID
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        channel_id = 1068521369941323798
        channel = guild.get_channel(channel_id)

        if channel:
            embed = discord.Embed(
                title='Goodbye!',
                description=f'{member.mention}, has left the server!',
                color=discord.Color.dark_purple()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name='Gone but maybe not for good?', value='(Probably gone for good)')
            
            await channel.send(embed=embed) 




async def setup(client):
    await client.add_cog(Greeting(client))