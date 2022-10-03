import discord
from discord.ext import commands
import youtube_dl
from req import get_youtube


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(descrition="Join the Voice channel")
    async def join(self, ctx: commands.Command):
        if ctx.author.voice is None:
            await ctx.respond(
                embed=discord.Embed(
                    title="You need to be in a voice channel for me to join",
                    colour=discord.Colour.from_rgb(255, 0, 0),
                )
            )
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await ctx.respond(
                embed=discord.Embed(
                    title="I have joined!", color=discord.Colour.from_rgb(66, 135, 245)
                )
            )
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            await ctx.respond(
                embed=discord.Embed(
                    title="Moving voice channels!",
                    color=discord.Colour.from_rgb(66, 135, 245),
                )
            )

    @discord.slash_command(descrition="Give it a youtube url, and it will play it")
    async def play(self, ctx: commands.Command, url: str):
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.respond(
                embed=discord.Embed(
                    title="I have joined!", color=discord.Colour.from_rgb(66, 135, 245)
                )
            )

        ctx.voice_client.stop()
        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }
        ytdl_options = {"format": "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(ytdl_options) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info["formats"][0]["url"]
            source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
            items = url.split("/")
            video_id = items[3][8:]
            data = get_youtube(video_id)

            embed = discord.Embed(
                title=f"Now playing: {data['title']}",
                description=f"Author: {data['author_name']}",
                color=discord.Colour.from_rgb(66, 135, 245),
                url=url,
            )
            embed.set_image(url=data["thumbnail"])

            await ctx.respond(embed=embed)
            vc.play(source)

    @discord.slash_command(descrition="Pause the current song")
    async def pause(self, ctx: commands.Command):
        embed = discord.Embed(
            title="Paused ⏸",
            description="/resume to continue",
            color=discord.Colour.from_rgb(66, 135, 245),
        )
        await ctx.respond(embed=embed)
        await ctx.voice_client.pause()

    @discord.slash_command(descrition="Continue the current song")
    async def resume(self, ctx: commands.Command):
        embed = discord.Embed(
            title="Resumed ▶",
            description="/pause to pause",
            color=discord.Colour.from_rgb(66, 135, 245),
        )
        await ctx.respond(embed=embed)
        await ctx.voice_client.resume()

    @discord.slash_command(descrition="Skip the current song")
    async def skip(self, ctx: commands.Command):
        pass

    @discord.slash_command(descrition="Force the bot to leave")
    async def leave(self, ctx: commands.Command):
        try:
            await ctx.voice_client.disconnect()
            await ctx.respond(
                embed=discord.Embed(
                    title="I have left", color=discord.Colour.from_rgb(66, 135, 245)
                )
            )
        except:
            await ctx.respond(
                embed=discord.Embed(
                    title="I need to be in a vc to leave.",
                    colour=discord.Colour.from_rgb(255, 0, 0),
                )
            )


def setup(bot):
    bot.add_cog(Music(bot))
