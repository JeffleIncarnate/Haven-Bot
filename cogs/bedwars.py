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
            return await ctx.respond("Bad human")

        hypixel_token = os.environ['HYPIXEL_API_KEY']
        get_stats_url = f"https://api.hypixel.net/player?key={hypixel_token}&uuid={uuid}"
        user_stats = await get_json(get_stats_url)

        user_stats_dict = {
            "wins": user_stats["player"]["stats"]["Bedwars"]["wins_bedwars"],
            "loses": user_stats["player"]["stats"]["Bedwars"]["losses_bedwars"],
            "final_kills": user_stats["player"]["stats"]["Bedwars"]["final_kills_bedwars"],
            "kills": user_stats["player"]["stats"]["Bedwars"]["kils_bedwars"]
        }

        print(user_stats_dict)
        await ctx.respond(user_stats_dict)


def setup(bot):
    bot.add_cog(Bedwards(bot))
