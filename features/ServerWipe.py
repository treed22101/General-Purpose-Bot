import discord
import asyncio

from discord.ext import commands


class ServerWipe(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.Cog.listener()
    async def on_ready(self):
        print("ServerWipe.py is online.")



    #here I define the confirm function for the server wipe
    async def confirm(self, ctx, content):
        await ctx.send(content)

        def check(mg):
            return mg.author == ctx.author and mg.channel == ctx.channel and mg.content.lower() in ["yes", "no"]

        try:
            msg = await self.client.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Your time to confirm ran out.")
            return False
        else:
            if msg.content.lower() == "yes":
                await ctx.send('You have decided to server wipe.')
                await asyncio.sleep(1)
                for i in range(5,0,-1):
                    await asyncio.sleep(1)
                    await ctx.send(i)
                await asyncio.sleep(1)
                return True
            elif msg.content.lower() == "no":
                await ctx.send("You have cancelled the server wipe (thank goodness).")
                return False



    #wipes all messages from all server channels, owner only (discord does rate limit though so you would be better off just mass deleting with !clear, up to you.)
    @commands.command()
    @commands.is_owner()
    async def serverwipe(self, ctx):
        if await self.confirm(ctx, "Confirm that you want to DELETE ALL messages from ALL channels.\n\nThis is permanent, be careful with your answer!!\n\n Yes or No?"):
            for channel in ctx.guild.text_channels:
                try:
                    await channel.purge(limit=None)
                except discord.errors.Forbidden:
                    await ctx.send(f"I do not have permissions to delete any messages from {channel.mention} you will have to give me permission?")
                except Exception as ex:
                    await ctx.send(f"Error while trying to delete messages in the channel {channel.mention}: {ex}")




    @serverwipe.error
    async def server_wipe_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You can't use this command (thank goodness).")



async def setup(client):
    await client.add_cog(ServerWipe(client))