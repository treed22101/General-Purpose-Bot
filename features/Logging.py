import discord
from discord.ext import commands


class Logging(commands.Cog):
    def __init__(self,client):
        self.client = client




    @commands.Cog.listener()
    async def on_ready(self):
        print("Logging.py is online.")
        




#logging feature/ SET THE NAME OF THE LOGGING CHANNEL 
    @commands.Cog.listener()
    async def on_message(self, message):
        
        if (message.author.bot):
            return
        
                                                        #SET LOGGING CHANNEL NAME HERE 
        log_channel = discord.utils.get(message.guild.channels, name='')

        log_embed = discord.Embed(
            title='Message Logged', 
            description="Message's contents and origin.", 
            color = discord.Color.dark_grey()
            )

        log_embed.add_field(name='Message Author:', value=message.author.mention, inline=False)
        log_embed.add_field(name='Channel Origin:', value=message.channel.mention, inline=False)
        log_embed.add_field(name='Message Content:', value=message.content, inline=False)
        

        await log_channel.send(embed=log_embed)







async def setup(client):
    await client.add_cog(Logging(client))
