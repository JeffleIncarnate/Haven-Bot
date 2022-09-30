import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from req import get_json

load_dotenv()


class Bedwards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def bedwars_stats(self, ctx, username: str):
        if username == "":
            return await ctx.respond("Provide a username.")

        get_uuid = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        res_json = await get_json(get_uuid)

        try:
            uuid = res_json["id"]
        except KeyError:
            return await ctx.respond(
                embed=discord.Embed(
                    title="User does not exist.",
                    colour=discord.Colour.from_rgb(66, 135, 245)
                )
            )

        hypixel_token = os.environ['HYPIXEL_API_KEY']
        get_stats_url = f"https://api.hypixel.net/player?key={hypixel_token}&uuid={uuid}"
        user_stats = await get_json(get_stats_url)

        user_stats_dict = {
            "wins": user_stats["player"]["stats"]["Bedwars"]["wins_bedwars"],
            "losses": user_stats["player"]["stats"]["Bedwars"]["losses_bedwars"],
            "kills": user_stats["player"]["stats"]["Bedwars"]["kills_bedwars"],
            "final_kills": user_stats["player"]["stats"]["Bedwars"]["final_kills_bedwars"],
            "beds_broken": user_stats["player"]["stats"]["Bedwars"]["beds_broken_bedwars"]
        }
        return await ctx.respond(
            embed=discord.Embed(
                title="User has not logged onto Hypixel Bedwars",
                colour=discord.Colour.from_rgb(66, 135, 245)
            )
        )

        embed = discord.Embed(
            title=f'Bedwars Stats for "{username}"',
            description=f"Total Wins: {user_stats_dict['wins']}\n "
                        f"Total losses: {user_stats_dict['losses']}\n "
                        f"Total Kills: {user_stats_dict['kills']}\n "
                        f"Total Final Kills: {user_stats_dict['final_kills']}\n"
                        f"Total Beds Broken {user_stats_dict['beds_broken']}",
            color=discord.Colour.from_rgb(66, 135, 245)
        )

        try:
            embed.set_thumbnail(url=f"https://mineskin.eu/helm/{username}")
        except:
            return ctx.respond(embed=discord.Embed(
            title=f'Bedwars Stats for "{username}"',
            description=f"Total Wins: {user_stats_dict['wins']}\n "
                        f"Total losses: {user_stats_dict['losses']}\n "
                        f"Total Kills: {user_stats_dict['kills']}\n "
                        f"Total Final Kills: {user_stats_dict['final_kills']}\n"
                        f"Total Beds Broken {user_stats_dict['beds_broken']}",
            color=discord.Colour.from_rgb(66, 135, 245)
        ))

        return await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Bedwards(bot))
