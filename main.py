import discord
import os
import asyncio
import json
import random 

from discord import reaction, user
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from dotenv import load_dotenv
from itertools import cycle


load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN') #pulls token from the .env file
client=commands.Bot(command_prefix='!', intents=discord.Intents.all())
client.remove_command('help')



#cycles through status at set intervals
bot_status=cycle(['Uno', 'Blackjack', 'Poker', 'Go Fish'])

@tasks.loop(seconds=500)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))






#lets us know if bot was turn on properly, and starboard functionality
@client.event
async def on_ready():
    print(f"You have successfully logged into {client.user.name}")
    print('----------------------')
    change_status.start()
   

    
async def load():
    for filename in os.listdir('./features'):
        if filename.endswith('.py'):
            await client.load_extension(f'features.{filename[:-3]}')






#banned words and message detection
banned_words=[]

@client.event
async def on_message(message):
    await client.process_commands(message)
    for word in banned_words:
        if word in message.content.lower() or word in message.content.upper():
            await message.delete()
            await message.channel.send(f'{message.author.mention} You cannot say that word!')
    if 'hello' in message.content:
        await message.channel.send('Hey buddy!')
    if 'bye' in message.content:
        await message.channel.send('Cya buddy!')

    




#mute role server based
@client.event
async def on_guild_join(guild):
    with open('cogs/jsonfiles/mutes.json', 'r') as f:
        
        mute_role = json.load(f)
        mute_role[str(guild.id)] = None

    with open('cogs/jsonfiles/mutes.json', 'w') as f:
        json.dump(mute_role, f, indent=5)

@client.event
async def on_guild_remove(guild):
    with open('cogs/jsonfiles/mutes.json', 'r') as f:
        
        mute_role = json.load(f)
        mute_role.pop(str(guild.id))

    with open('cogs/jsonfiles/mutes.json', 'w') as f:
        json.dump(mute_role, f, indent=5)







response = ['You got lucky this time!', 'Luck was on your side today!', 'You live, try your luck again?', 'Try again, if you dare.']

def check(message):
    try:
        int(message.content)
        return True
    except ValueError:
        return False

#russian roulette command, bans the user if they guess the random number, check above and random responses.
@client.command()
async def roulette(ctx, member:discord.Member=None):

    if member is None:
        member = ctx.author
    elif member is not None:
        member = member

    await ctx.send('Choose a number between 1 and 6.')

    chamber = random.randint(1,6)
    msg = await client.wait_for("message", check=check)
    choice = int(msg.content)

    if choice == chamber:
        await asyncio.sleep(1)
        await ctx.send(f"Guess you can't be so lucky always!")
        await asyncio.sleep(1)
        for number in range(5,0,-1):
            await asyncio.sleep(1)
            await ctx.send(number)
        await member.ban(member)
    
    else:
        await asyncio.sleep(1)
        await ctx.send(random.choice(response))







#server setup command, you can change this to how you like, with the same format!
@client.command()
@has_permissions(manage_messages=True)
async def create(ctx):
    guild = ctx.guild
    await ctx.send('Setup in progress!')
    await guild.create_text_channel(name='welcome')
    await guild.create_text_channel(name='gen')
    await guild.create_text_channel(name='music')
    await guild.create_voice_channel(name='gen')
    await guild.create_voice_channel(name='music')
    
    






#multipage help command

#page1
page1 = discord.Embed(
    title='Admin Commands', 
    description='Commands only mods can use!',
      color=discord.Color.dark_gold()
)
page1.add_field(name='clear', value='Deletes a specified amount of messages', inline=False)
page1.add_field(name='kick', value='Kicks a specified user', inline=False)
page1.add_field(name='ban', value='Bans a specified user', inline=False)
page1.add_field(name='unban', value='Unbans a specified user', inline=False)
page1.add_field(name='mute', value='Adds a mute role to a speicifed user', inline=False)
page1.add_field(name='unmute', value='Takes away the mute role from a specified user', inline=False)
page1.add_field(name='setup', value='Automatically sets up very basic discord channels and vcs', inline=False)



#page 2
page2 = discord.Embed(
    title='Info Commands', 
    description='Commands for info!', 
    color=discord.Color.dark_red()
)
page2.add_field(name='stats', value='Deletes a specified amount of messages', inline=False)
page2.add_field(name='level', value='Deletes a specified amount of messages', inline=False)
page2.add_field(name='help', value='Sends what you are looking at right now!', inline=False)



#page 3
page3 = discord.Embed(
    title='Fun Commands',
    description='Commands for fun!', 
    color=discord.Color.dark_green()
)
page3.add_field(name='roulette', value='Deletes a specified amount of messages', inline=False)
page3.add_field(name='ping', value='Lets you know the latency of the bot', inline=False)
page3.add_field(name='punch', value='Punches a specified user', inline=False)

client.help_pages = [page1, page2, page3]




#(the actual help command)
@client.command()
async def help(ctx):
    buttons = {u'\u23EA', u'\u25C0', u'\u25B6', u'\u23E9'}
    current = 0
    msg = await ctx.send(embed=client.help_pages[current])

    for button in buttons:
        await msg.add_reaction(button)
    
    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60)

        except asyncio.TimeoutError:
            embed = client.help_pages[current]
            embed.set_footer(text='Timed Out.')
            await msg.clear_reactions()

        else:
            previous_page = current

            if reaction.emoji == u'\u23EA':
                current = 0

            elif reaction.emoji == u'\u25C0':
                if current > 0:
                    current -= 1


            elif reaction.emoji == u'\u25B6':
                if current < len(client.help_pages)-1:
                    current +=1
            
            elif reaction.emoji == u'\u23E9':
                current = len(client.help_pages)-1

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if current != previous_page:
                await msg.edit(embed=client.help_pages[current])





#dumb punch command
@client.command()
async def punch(ctx, member:discord.Member):
    punches = [f'{ctx.author.mention} just punched {member.mention}!', 
            f'{ctx.author.mention} just punched {member.mention} with astronomical force!', 
            f'{ctx.author.mention} just punched {member.mention} with the force of a thousand bears!',
            f"{ctx.author.mention} just punched {member.mention} down some stairs and now he can't get back up?", 
            f'{ctx.author.mention} just punched {member.mention} off a cliff!',
            f'{ctx.author.mention} just punched {member.mention} out of this planet!',
            f'{ctx.author.mention} just punched {member.mention} into a volcano!',
            f'{ctx.author.mention} just punched {member.mention} into a wall?'
            f"{ctx.author.mention} just punched {member.mention}'s head into the ground!"
            f'{ctx.author.mention} just punched {member.mention} to death!'
               ]
    await ctx.send(random.choice(punches))









#member info command
@client.command()
async def stats(ctx, member:discord.Member=None):
    if member is None:
        member = ctx.author
    elif member is not None:
        member = member
    
    info_embed = discord.Embed(
        title=f"{member.name}'s User Information",
          description="The member's server info.",
          color=member.color
          )
    
    info_embed.set_thumbnail(url=member.avatar)
    info_embed.add_field(name='Name:', value=member.name, inline=True)
    info_embed.add_field(name='Nickname:', value=member.display_name, inline=True)
    info_embed.add_field(name='ID:', value=member.id, inline=True)
    info_embed.add_field(name='Top Role:', value=member.top_role, inline=True)
    info_embed.add_field(name='Joined at:', value=member.joined_at.__format__('%B / %d / %Y. @ %H:%M:%S'), inline=True)
    
    await ctx.send(embed=info_embed)





#global error handling
@client.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing argument, did you specify who or how many?')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the permissions to use this command.')


async def main():
    async with client:
        await load()
        await client.start(TOKEN)

asyncio.run(main())