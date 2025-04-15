import json
import os
import random

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

with open("phasmo_maps.json") as f:
    PHASMO_MAPS = json.load(f)

# Define your preset lists here
PRESETS = {
    "all_maps": [x for x in PHASMO_MAPS],
    "size_small": [x for x in PHASMO_MAPS if x["size"] == "small"],
    "size_medium": [x for x in PHASMO_MAPS if x["size"] == "medium"],
    "size_large": [x for x in PHASMO_MAPS if x["size"] == "large"],
}


class SpinBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()


bot = SpinBot()


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")


@bot.tree.command(
    name="phasmo", description="Choose a random Phasmophobia map based on attributes."
)
@app_commands.describe(
    size="Choose a map by its size",
    # options="Enter your own list of options separated by spaces (e.g. red blue green)",
    # preset="Choose from a preset list (e.g. chores, games, food)",
)
async def spin(interaction: discord.Interaction, size: str = None):
    if size:
        size_key = size.lower()
        if size_key in ["small", "medium", "large"]:
            option_list = PRESETS[f"size_{size_key}"]
        else:
            await interaction.response.send_message(
                f"❗ Map size **{size}** not found. Available sizes: {', '.join(["small", "medium", "large"])}",
                ephemeral=True,
            )
            return
    else:
        option_list = PRESETS["all_maps"]

    result = random.choice(option_list)
    await interaction.response.send_message(
        f"You're headed to {result["emoji"]} **{result["full_name"]}**"
    )


bot.run(DISCORD_BOT_TOKEN)
