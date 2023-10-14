import traceback
import os

from discord.ext import commands

class Module(commands.Cog):
    def __init__(self, client):
        self.client = client
    



    @commands.Cog.listener()
    async def on_ready(self):
        print('Module.py is online')



    #lists all of the functioning cogs of the bot, use this after reloading cogs (owner only)
    @commands.command()
    @commands.is_owner()
    async def allcogs(self, ctx):
        try:
            active_cogs = ",\n".join(self.client.extensions)
            await ctx.send(f'Active cogs:\n{active_cogs}' if active_cogs else 'No active cogs')
        except Exception as e:
            await ctx.send(f'An error occurred: {e}')



    #unloads a cog (if the cog isn't functioning properly) without stopping the bot (owner only)
    @commands.command()
    @commands.is_owner() 
    async def unload(self, ctx, *, cog: str):
        try:
            await self.client.unload_extension(f'features.{cog}') 
            await ctx.send(f'Unloaded cog: {cog}')
        except commands.ExtensionNotFound:
            await ctx.send(f'There was no {cog} in the directory')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'{cog} was loaded')
        except Exception as e:
            await ctx.send(f'Error: {cog}: {e}')



    #loads a new cog so you can keep the bot functional while you add something new instead of stopping the code (owner only)
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



    #reloads all the cogs after you load or unload one to ensure they function properly (owner only)
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