import discord
from discord.ext import commands


class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = self.bot.get_guild(1021736744451838004)
        channel = guild.get_channel(1021736745567526965)
        embed = discord.Embed(
            title=f"Welcome {member.name}",
            description="Welcome to this super cool server! :partying_face:",
            color=discord.Colour.from_rgb(66, 135, 245)
        )
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MemberJoin(bot))
