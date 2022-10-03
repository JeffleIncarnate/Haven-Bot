import discord
from discord.ext import commands


class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild_data = await self.bot.conn.fetch(
            "SELECT channel, welcome_text, enabled FROM welcome WHERE guild_id=$1",
            member.guild.id,
        )

        guild_preferences = {
            "channel": guild_data[0][0],
            "welcome_text": guild_data[0][1],
            "enabled": guild_data[0][2],
        }

        if guild_preferences["enabled"] is False:
            return

        guild = self.bot.get_guild(member.guild.id)
        channel = guild.get_channel(guild_preferences["channel"])

        embed = discord.Embed(
            title=f"Welcome {member.name}",
            description=guild_preferences["welcome_text"],
            color=discord.Colour.from_rgb(66, 135, 245),
        )
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MemberJoin(bot))
