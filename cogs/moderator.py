import discord
from discord.ext import commands


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Clear the chat for `n` messages")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context, amount: int):
        cleared_embed = discord.Embed(title=f"cleared {amount}")

        try:
            await ctx.channel.purge(limit=amount)
            await ctx.respond(embed=cleared_embed)
        except:
            failure_embed = discord.Embed(title="Incorrect role.")
            await ctx.respond(embed=failure_embed)


def setup(bot):
    bot.add_cog(Moderator(bot))
