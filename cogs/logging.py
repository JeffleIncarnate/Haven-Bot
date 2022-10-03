import discord
from discord.ext import commands
import datetime


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, previous, new):
        y = 1026324004631478284
        channel = await self.bot.fetch_channel(y)

        embed = discord.Embed(
            title="Message Edited",
            description=f"{previous.author.name} edited their message:",
            color=discord.Colour.from_rgb(66, 135, 245),
            timestamp=datetime.datetime.utcnow(),
        )
        embed.add_field(name="Previous Message:", value=f"{previous.content}")
        embed.add_field(name="New Message:", value=f"{new.content}")
        embed.add_field(name="Channel:", value=f"{new.channel}")

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        y = 1026324004631478284
        channel = await self.bot.fetch_channel(y)

        embed = discord.Embed(
            title="Message Deleted",
            description=f"{message.author.name} deleted their message:",
            color=discord.Colour.from_rgb(255, 0, 0),
            timestamp=datetime.datetime.utcnow(),
        )
        embed.add_field(name="Content:", value=f"{message.content}")
        embed.add_field(name="Channel", value=f"{message.channel}")

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        y = 1026324004631478284
        channel = await self.bot.fetch_channel(y)

        embed = discord.Embed(
            title="New Member",
            description=f"{member.name} has joined the server :)",
            color=discord.Colour.from_rgb(66, 135, 245),
            timestamp=datetime.datetime.utcnow(),
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        y = 1026324004631478284
        channel = await self.bot.fetch_channel(y)

        embed = discord.Embed(
            title="Member Left",
            description=f"{member.name} has left the server :(",
            color=discord.Colour.from_rgb(255, 0, 0),
            timestamp=datetime.datetime.utcnow(),
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, previous, new):
        embed = None
        check = False
        y = 1026324004631478284
        channel = await self.bot.fetch_channel(y)
        if previous.nick is not None and new.nick is None:
            embed = discord.Embed(
                color=discord.Color.blue(),
                title="Nick Change",
                description=f"{previous.name} has unicked",
                timestamp=datetime.datetime.utcnow(),
            )
            embed.add_field(name="Before:", value=previous.nick)
            embed.add_field(name="After:", value="No Nick")
            check = True

        if previous.nick is None and new.nick is not None:
            embed = discord.Embed(
                color=discord.Color.blue(),
                title="Nick Change",
                description=f"{previous.name} Has nicked",
                timestamp=datetime.datetime.utcnow(),
            )
            embed.add_field(name="Before:", value="No Nick")
            embed.add_field(name="After:", value=new.nick)
            check = True

        elif previous.nick != new.nick:
            embed = discord.Embed(
                color=discord.Color.blue(),
                title="Nick Change",
                description=f"{previous.name} Has changed their nick",
                timestamp=datetime.datetime.utcnow(),
            )
            embed.add_field(name="Before:", value=previous.nick)
            embed.add_field(name="After:", value=new.nick)
            check = True

        if check:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        y = 1026324004631478284
        channel = await self.bot.fetch_channel(y)
        embed = discord.Embed(
            color=discord.Color.blue(),
            title="Member Banned!",
            description=f"{member.name} Has been banned from the server",
            timestamp=datetime.datetime.utcnow(),
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        y = 1026324004631478284
        channel = await self.bot.fetch_channel(y)
        embed = discord.Embed(
            color=discord.Color.blue(),
            title="Member Unbanned!",
            description=f"{member.name} Has been unbanned from the server",
            timestamp=datetime.datetime.utcnow(),
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel_param):
        y = 1026324004631478284
        channel = await self.bot.fetch_channel(y)
        embed = discord.Embed(
            color=discord.Color.red(),
            title="Channel deleted!",
            description=f"{channel_param.name} Has been deleated from the server",
            timestamp=datetime.datetime.utcnow(),
        )
        embed.add_field(name="Channel:", value=channel_param.name)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel_param):
        y = 1026324004631478284
        channel = await self.bot.fetch_channel(y)
        embed = discord.Embed(
            color=discord.Color.green(),
            title="Channel Created!",
            description=f"{channel_param.name} Has been created on the server",
            timestamp=datetime.datetime.utcnow(),
        )

        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Logger(bot))
