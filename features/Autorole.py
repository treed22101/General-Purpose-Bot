import discord

from discord.ext import commands


class AutoRole(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("AutoRole.py is online.")
        


#auto role, local only/ SET THE ROLE AUTOMATICALLY GIVEN
    @commands.Cog.listener()
    async def on_member_join(self, member):             #SET THE ROLE HERE
        join_role = discord.utils.get(member.guild.roles, name='')
        await member.add_roles(join_role)




async def setup(client):
    await client.add_cog(AutoRole(client))
