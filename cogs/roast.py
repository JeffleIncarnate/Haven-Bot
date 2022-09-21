import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
from req import get_text


class Roast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def roast_a_dev(self, ctx):
        roast = dev_roast()
        await ctx.respond(
            embed=discord.Embed(
                title=f"{roast}",
                description="Powered by: https://www.programmerinsults.com/",
                color=discord.Colour.from_rgb(66, 135, 245)
            )
        )


def dev_roast():
    res = requests.get("https://www.programmerinsults.com/")
    soup = BeautifulSoup(res.text, 'html.parser')
    insult_h1 = soup.find_all("h1")
    return insult_h1[0].text


def setup(bot):
    bot.add_cog(Roast(bot))
