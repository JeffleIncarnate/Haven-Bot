import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from req import get_text


class Roast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Command to get a spicy dev roast")
    async def roast_a_dev(self, ctx):
        roast = await dev_roast()
        await ctx.respond(
            embed=discord.Embed(
                title=f"{roast}",
                description="Powered by: https://www.programmerinsults.com/",
                color=discord.Colour.from_rgb(66, 135, 245),
            )
        )


async def dev_roast():
    res = await get_text("https://www.programmerinsults.com/")
    soup = BeautifulSoup(res, "html.parser")
    insult_h1 = soup.find_all("h1")
    return insult_h1[0].text


def setup(bot):
    bot.add_cog(Roast(bot))
