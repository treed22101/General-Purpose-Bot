import discord
import json

from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation.py is online.")
        




#clear messages command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx,count: int):
        await ctx.channel.purge(limit=count)
        await ctx.send(f'{count} message(s) have been deleted.')

    @clear.error
    async def clear_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('How many messages do you want me to clear? Please specify.')





#kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason=None):
        await ctx.guild.kick(member)

        embed=discord.Embed(
            title='Confirmed.',
            color=discord.Color.green()
        )
        
        embed.add_field(name='Kicked:', value=f'{member.mention} has been kicked by {ctx.author.mention}.', inline=False)
        embed.add_field(name='Reason:', value=reason, inline=False)

        await ctx.send(embed=embed)

      
    @kick.error
    async def kick_error(self, ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Who do you want me to kick? Please specify.')





#ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason=None):
        await ctx.guild.ban(member)

        embed=discord.Embed(
            title='Confirmed.', 
            color=discord.Color.dark_gold()
        )

        embed.add_field(name='Banned:', value=f'{member.mention} has been banned by {ctx.author.mention}.', inline=False)
        embed.add_field(name='Reason:', value=reason, inline=False)

        await ctx.send(embed=embed)

  
    @ban.error
    async def ban_error(self, ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Who do you want me to ban? Please specify.')





#unban command
    @commands.command(name='unban')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userId):
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)
        
        embed = discord.Embed(
            title='Confirmed.', 
            color=discord.Color.dark_gold()
        )

        embed.add_field(name='Unbanned:', value=f'{userId} has been unbanned by {ctx.author.mention}.', inline=False)

        await ctx.send(embed=embed)

    
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Who do you want me to unban? Please specify.')





#setmuterole command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setmute(self,ctx, role:discord.Role):
        with open('features/jsonfiles/mutes.json', 'r') as f:
        
            mute_role = json.load(f)
            mute_role[str(ctx.guild.id)] = role.name

        with open('features/jsonfiles/mutes.json', 'w') as f:
            json.dump(mute_role, f, indent=4)

        embed=discord.Embed(
            title='Confirmed.', 
            color=discord.Color.orange()
        )

        embed.add_field(name='Mute role has been set.', value=f'All members who are muted will have this role {role.mention}')

        await ctx.send(embed=embed)

    @setmute.error
    async def setmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('What do you want to be the mute role? Please specify.')
 




#mute command
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member:discord.Member, reason=None):
        with open('features/jsonfiles/mutes.json', 'r') as f:
            role = json.load(f)

        mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])

        await member.add_roles(mute_role)
        await ctx.send(f'{member.mention} has been muted for {reason}.')


    @mute.error
    async def mute_error(self, ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Who do you want me to mute? Please specify.')





#unmute command
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member:discord.Member):
        with open('features/jsonfiles/mutes.json', 'r') as f:
            role = json.load(f)

        mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])

        await member.remove_roles(mute_role)
        await ctx.send(f'{member.mention} has been unmuted.')


    @unmute.error
    async def unmute_error(self, ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Who do you want me to unmute? Please specify.')





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

    @ping.error
    async def ping_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command')




async def setup(client):
    await client.add_cog(Moderation(client))