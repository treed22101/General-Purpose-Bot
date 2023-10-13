import discord
from discord.ext import commands 

class Greeting(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Greeting.py is online.")
        




#when a user joins the server it will send a greeting and dm them info about the server/ SET THE WELCOME CHANNEL ID
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        channel_id =
        channel = guild.get_channel(channel_id)

        if channel:
            welcome_embed = discord.Embed(
                title='Welcome!',
                description=f'Welcome {member.mention}, thank you for joining!',
                color=discord.Color.dark_purple()
            )
            welcome_embed.set_thumbnail(url=member.avatar.url)
            welcome_embed.add_field(name='Go say hi in gen:', value='You might make some new friends!')

            await channel.send(embed=welcome_embed)

            dm_embed = discord.Embed(
                title=f'Welcome to {guild.name}!',
                description=f"The command prefix for the bot is '!' \n\n Use '!help' if you want to know all of the commands in the server! \n\n BE RESPECTFUL AND HAVE FUN!!",
                color=discord.Color.brand_red()
            )
        try:
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            print(f"Was unable to dm {member.name}.")
        except Exception as e:
            print(f"Error while trying to dm {member.name}: {e}")

            

        

#when a user leaves the server/ SET THE WELCOME CHANNEL ID
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        channel_id =
        channel = guild.get_channel(channel_id)

        if channel:
            leave_embed = discord.Embed(
                title='Goodbye!',
                description=f'{member.mention}, has left the server!',
                color=discord.Color.dark_purple()
            )
            leave_embed.set_thumbnail(url=member.avatar.url)
            leave_embed.add_field(name='Gone but maybe not for good?', value='(Probably gone for good)')
            
            await channel.send(embed=leave_embed) 


async def setup(client):
    await client.add_cog(Greeting(client))
