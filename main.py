import discord
import os
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot(debug_guilds=[1021736744451838004])

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
cog_files = [
    "roast",
    "greetings"
]

for cog in cog_files:
    bot.load_extension(f"cogs.{cog}")

if __name__ == "__main__":
    bot.run(os.environ["TOKEN"])

