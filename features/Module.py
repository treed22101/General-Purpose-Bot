import discord
from discord.ext import commands
import traceback
import os

class Module(commands.Cog):
    def __init__(self, client):
        self.client = client
    



    @commands.Cog.listener()
    async def on_ready(self):
        print('Module.py is online')




    @commands.command()
    @commands.is_owner()
    async def allcogs(self, ctx):
        try:
            active_cogs = ",\n".join(self.client.extensions)
            await ctx.send(f'Active cogs:\n{active_cogs}' if active_cogs else 'No active cogs')
        except Exception as e:
            await ctx.send(f'An error occurred: {e}')




    @commands.command()
    @commands.is_owner() 
    async def unload(self, ctx, *, cog: str):
        try:
            self.client.unload_extension(f'features.{cog}') 
            await ctx.send(f'Unloaded cog: {cog}')
        except commands.ExtensionNotFound:
            await ctx.send(f'There was no {cog} in the directory')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'{cog} was loaded')
        except Exception as e:
            await ctx.send(f'Error: {cog}: {e}')




    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        cog_path = f'features.{cog}'
        try:
            await self.client.load_extension(cog_path)
        except commands.ExtensionNotFound:
            await ctx.send(f'There was no {cog} found')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'{cog} has been already loaded')
        except Exception as e:
            error_content = traceback.format_exception(type(e), e, e.__traceback__)
            error_content = ''.join(error_content)
            await ctx.send(f'Unable to load {cog}: \n{error_content}')
        else:
            await ctx.send(f'Loaded {cog}')




    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        errors = []
        for filename in os.listdir('./features'):
            if filename.endswith('.py'):
                cog = f"features.{filename[:-3]}" 
                try:
                    await self.client.unload_extension(cog)
                    await self.client.load_extension(cog)
                except Exception as e:
                    errors.append(
                        f"{cog} - {type(e).__name__}: {e}"
                    )

        if errors:
            await ctx.send(f'Failed to reload these:\n{"".join(errors)}\n')
        else:
            await ctx.send('Reloaded all cogs.')


async def setup(client):
    await client.add_cog(Module(client))