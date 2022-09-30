import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="Commands",
            description=""
                        "**1)**\n"
                        "```/bedwars_stats [user]```\n"
                        "**2)**\n"
                        "```/roast_a_dev```\n"
                        "**3)**\n"
                        "```/never_gonna_give_you_up```\n"
                        "**3)**\n"
                        "```/kick [@user]```\n"
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
