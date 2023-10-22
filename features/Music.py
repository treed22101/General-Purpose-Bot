import discord
import yt_dlp

from discord.ext import commands




class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.currently_playing = None


    @commands.Cog.listener()
    async def on_ready(self):
        print('Music.py is online.')                                                                            

        

    #joins the vc you are in, only IF you are in a channel.
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await channel.connect()
            elif ctx.voice_client.channel != channel:
                await ctx.voice_client.move_to(channel)
        else:
            await ctx.send("You need to be in a vc for me to join, silly!")


    #leaves the vc
    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()


    #pauses the current song playing
    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()


    #resumes the paused song
    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()


    #skips to the next song in queue (if there is one)
    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and (ctx.voice_client.is_playing() or ctx.voice_client.is_paused()):
            ctx.voice_client.stop()


    #plays audio from a youtube url
    @commands.command()
    async def play(self, ctx, url: str):
        if not ctx.author.voice:
            await ctx.send("You need to be a vc for me to play music!")
            return

        channel = ctx.author.voice.channel

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'source_address': '0.0.0.0'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']

        if ctx.voice_client is None:
            await channel.connect()
        else:
            if ctx.voice_client.channel != channel:
                await ctx.voice_client.move_to(channel)

        if self.currently_playing is not None:
            self.queue.append(audio_url)
            return
        else:
            self.play_next(ctx, audio_url)



    def play_next(self, ctx, audio_url):
        if audio_url is None and len(self.queue) > 0:
            audio_url = self.queue.pop(0)

        if audio_url is not None:
            self.currently_playing = audio_url
            ctx.voice_client.stop()
            ctx.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=audio_url),
                                  after=lambda e: self.after_playing(ctx, e))



    def after_playing(self, ctx, error):
        if error:
            print(f'Error: {error}')

        self.currently_playing = None
        self.play_next(ctx, None)



    #displays the songs currently in queue
    @commands.command()
    async def queue(self, ctx):
        if not self.queue:
            await ctx.send("There is no songs currently in the queue")
            return

        in_queue = "\n".join(self.queue)
        await ctx.send(f"Current Queue:\n{in_queue}")


async def setup(client):
    await client.add_cog(Music(client))