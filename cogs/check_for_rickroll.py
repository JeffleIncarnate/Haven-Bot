import discord
from discord.ext import commands
from req import get_youtube


class CheckRickroll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Checks if a youtube link is a rickroll, by sending back the video name")
    async def youtube_rickroll_check(self, ctx, url: str):
        items = url.split("/")
        video_id = items[3][8:]
        data = get_youtube(video_id)

        title = data["title"].lower()
        bot_guess = ""

        if "rickroll" in title:
            bot_guess = "100% rickroll"
        elif "rick roll" in title:
            bot_guess = "100% rickroll"
        elif "rick" in title:
            bot_guess = "70% rickroll"
        elif "rick astley" in title:
            bot_guess = "70% rickroll"
        else:
            bot_guess = "Unsure, look for yourself."

        embed = discord.Embed(
            title=title,
            description=bot_guess,
            colour=discord.Colour.from_rgb(66, 135, 245)
        )
        embed.set_thumbnail(url=data["thumbnail"])

        await ctx.respond(embed=embed)



def setup(bot):
    bot.add_cog(CheckRickroll(bot))
