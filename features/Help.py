import discord
from discord.ext import commands
import asyncio




class Help(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
            print("Help.py is online.")



    #multi page help command
    @commands.command()
    async def help(self, ctx):
        embed_pages = [
            self.create_embed(title="Owner", description='serverwipe: wipes all messages from all channels. \n\ndm: dms a specified user, OWNER only to prevent abuse.', color=discord.Color.red()),
            self.create_embed(title='Admin', description='kick:  kicks a specified user \n\n ban:  bans a specified user \n\n unban:  unbans a specified user \n\n mute:  mutes a specified user \n\n unmute:  unmutes a specified user, \n\n clear:  deletes a set number of messages, \n\n setup:  sets up a generic simple Discord channels layout', color=discord.Color.red()),
            self.create_embed(title='Info', description="server:  gives public info about the server \n\n stats:  sends your server stats \n\n help (command you're using right now!) \n\n latency:  sends the ping of the bot", color=discord.Color.red()),
            self.create_embed(title='Fun', description='punch:  punches a specified user \n\n roulette:  you play russian roulette! Guess the number wrong and you get banned! \n\n level:  displays your current level and exp', color=discord.Color.red())
        ]



        current_page = 0
        message = await ctx.send(embed=embed_pages[current_page])

        await message.add_reaction('◀️')
        await message.add_reaction('▶️')



        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['◀️', '▶️'] and reaction.message == message

        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

                
                if str(reaction.emoji) == '▶️' and current_page != len(embed_pages) - 1:
                    current_page += 1
                    await message.edit(embed=embed_pages[current_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == '◀️' and current_page > 0:
                    current_page -= 1
                    await message.edit(embed=embed_pages[current_page])
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                await message.delete()
                break




    #define the embed creation here
    def create_embed(self, title, description, color):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        return embed




async def setup(client):
    await client.add_cog(Help(client))