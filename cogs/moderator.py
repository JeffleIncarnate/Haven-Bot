import discord
from discord.ext import commands


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.respond(f"cleared {amount}")


def setup(bot):
    bot.add_cog(Moderator(bot))

