import discord
from discord.ext import commands
import random


class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def eight_ball(self, ctx, question: str):
        answer = await return_answer()
        embed = discord.Embed(
            title=answer,
            description="Question: {}".format(question),
            color=discord.Colour.from_rgb(66, 135, 245)
        )

        if answer == "Rick Astly is **GOD**":
            embed.set_thumbnail(url="https://variety.com/wp-content/uploads/2021/07/Rick-Astley-Never-Gonna-Give-You"
                                    "-Up.png?w=681&h=383&crop=1")

        await ctx.respond(embed=embed)


async def return_answer():
    choices = ["Signs point to a yes", "Yes, definitely", "Sounds like a big no.",
               "Sike, you thought :laughing:", "You may rely on it", " ",
               "My reply is no", "Skill issue", "Nah, sounds like a scam", "Rick Astly is **GOD**"]
    return random.choice(choices)


def setup(bot):
    bot.add_cog(EightBall(bot))
