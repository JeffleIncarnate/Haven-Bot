import discord
from discord.ext import commands


class Talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def hello(self, ctx):
        await ctx.respond("Hello small human.")

    @discord.slash_command()
    async def goodbye(self, ctx):
        await ctx.respond("Goodbye small human.")

    @discord.slash_command()
    async def never_gonna_give_you_up(self, ctx):
        embed = discord.Embed(
                title="Click this embed",
                url="https://www.youtube.com/watch?v=xvFZjo5PgG0",
                color=discord.Colour.from_rgb(66, 135, 245)
        )
        embed.set_thumbnail(url="https://variety.com/wp-content/uploads/2021/07/Rick-Astley-Never-Gonna-Give-You-Up.png?w=681&h=383&crop=1")
        await ctx.respond(embed=embed)

    @discord.slash_command()
    async def e(self, ctx):
        embed = discord.Embed(
            title="EEEEEEEEEEEEEEEE",
            color=discord.Colour.from_rgb(66, 135, 245)
        )
        await ctx.respond(embed=embed)

    @discord.slash_command()
    async def eight_ball(self, ctx, question: str):
        pass


def setup(bot):
    bot.add_cog(Talk(bot))
