import discord
from discord.ext import commands
from discord.utils import get


class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Server Info")
    async def server_info(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.guild.name} server info",
            description=f"Description: {ctx.guild.description}",
            color=discord.Colour.from_rgb(66, 135, 245),
        )
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.add_field(name="Owner", value=f"{ctx.guild.owner}")
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        embed.add_field(name="Member Count", value=f"{ctx.guild.member_count}")
        embed.add_field(name="Voice Channels", value=f"{len(ctx.guild.voice_channels)}")
        embed.add_field(name="Text Channels", value=f"{len(ctx.guild.text_channels)}")
        embed.add_field(name="Verification Level", value=f"{ctx.guild.verification_level}")
        embed.add_field(name="Server Creation", value=f"{ctx.guild.created_at}")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(ServerInfo(bot))
