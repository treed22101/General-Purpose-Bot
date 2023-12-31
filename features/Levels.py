import discord
import json
import asyncio
import math
import random

from discord.ext import commands




class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.loop.create_task(self.save())

        with open('features/jsonfiles/users.json', 'r') as f:
            self.users = json.load(f)
            
        with open('features/jsonfiles/leaderboard.json', 'r') as f:
            self.leaderboard = json.load(f)




    @commands.Cog.listener()
    async def on_ready(self):
        print("Levels.py is online.")



    def level_up(self, author_id):
        current_exp = self.users[author_id]['Exp']
        current_level = self.users[author_id]['Level']

        if current_exp >= math.ceil((6 * (current_level ** 4)) / 2.5):
            self.users[author_id]['Level'] += 1
            return True
        else:
            return False

    async def save(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            with open('features/jsonfiles/users.json', 'w') as f:
                json.dump(self.users, f, indent=4)

            with open('features/jsonfiles/leaderboard.json', 'w') as f:
                json.dump(self.leaderboard, f, indent=4)

            await asyncio.sleep(5)




    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            return
        
        author_id = str(message.author.id)

        if not author_id in self.users:
            self.users[author_id] = {}
            self.users[author_id]['Level'] = 1
            self.users[author_id]['Exp'] = 0

        random_exp = random.randint(5, 15)
        self.users[author_id]['Exp'] += random_exp 

        self.leaderboard[author_id] = self.users[author_id]['Exp']

        if self.level_up(author_id):
            await message.channel.send(f'{message.author.mention} has leveled up to level {self.users[author_id]["Level"]}!')




    #level command (lets us know our level and exp)
    @commands.command(aliases=['rank', 'lvl', 'r'])
    async def level(self, ctx, user:discord.User=None):
        if user is None:
            user = ctx.author
        elif user is not None:
            user = user

        level_card = discord.Embed(title = f"{user.name}'s Level & Exp",color=discord.Color.dark_red())
        level_card.add_field(name='Level:', value=self.users[str(user.id)]['Level'])
        level_card.add_field(name='Exp:', value=self.users[str(user.id)]['Exp'])
        level_card.set_footer(text=f'{ctx.author.name}', icon_url=ctx.author.avatar)

        await ctx.send(embed=level_card)



    #leaderboard command, stores in a json file
    @commands.command(aliases=['lb', 'top'])
    async def leaderboard(self, ctx):
        sorted_leaderboard = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)[:10]
        embed = discord.Embed(title="Leaderboard", color=discord.Color.dark_red())
        rank = 1
        for user_id, exp in sorted_leaderboard:
            user = self.client.get_user(int(user_id))
            embed.add_field(name=f"{rank}. {user.name}", value=f"Exp: {exp}", inline=False)
            rank += 1
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Levels(client))