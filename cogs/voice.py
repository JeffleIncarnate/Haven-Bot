import discord
from discord.ext import commands
from discord.utils import get


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(descrition="Join the Voice channel")
    async def join(self, ctx: commands.Command):
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.respond(embed=discord.Embed(title="I have joined", color=discord.Colour.from_rgb(66, 135, 245)))
        except:
            await ctx.respond(embed=discord.Embed(
                title="You need to be in a vc for me to join",
                colour=discord.Colour.from_rgb(255, 0, 0))
            )

    @discord.slash_command(descrition="Give it a youtube url, and it will play it")
    async def play(self, ctx: commands.Command):
        pass

    @discord.slash_command(descrition="Pause the current song")
    async def pause(self, ctx: commands.Command):
        pass

    @discord.slash_command(descrition="Continue the current song")
    async def continue_music(self, ctx: commands.Command):
        pass

    @discord.slash_command(descrition="Skip the current song")
    async def skip(self, ctx: commands.Command):
        pass

    @discord.slash_command(descrition="Force the bot to leave")
    async def leave(self, ctx: commands.Command):
        try:
            await ctx.voice_client.disconnect()
            await ctx.respond(embed=discord.Embed(title="I have left.", color=discord.Colour.from_rgb(66, 135, 245)))
        except:
            await ctx.respond(embed=discord.Embed(
                title="I need to be in a vc to leave.",
                colour=discord.Colour.from_rgb(255, 0, 0))
            )


def setup(bot):
    bot.add_cog(Voice(bot))
