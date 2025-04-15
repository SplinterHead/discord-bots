import json
import os
import random

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
INTRO_LINES = [
    "You're headed to",
    "Pack your equipment, we're rolling out to",
    "Don't panic, it's only",
    "Is it a mansion? Is it a caravan? nah, it's",
    "The spirits are stirring… we're headed to",
    "Pack your EMF reader, we're rolling into",
    "The veil is thin tonight, we go to",
    "Don’t look behind you, just walk toward",
    "They say no one leaves",
    "Hope you brought salt, we're off to",
    "The air’s colder near",
    "Ghosts love this place; we’re heading to",
    "You hear that whisper? It’s calling us to",
    "Something’s waiting in the dark at",
    "Not all who enter return from",
    "Tonight, the hunt leads us to",
    "Grave warnings won’t stop us from going to",
    "Our next investigation takes us to",
    "Lights flicker every time we say",
    "There’s a chill in the wind… must be",
    "The last team never came back from",
    "Whatever’s haunting it, we’re heading to",
    "We don’t go around the haunted place… we go straight to",
    "Say a prayer, we’re off to",
    "Something’s been waiting centuries at",
    "You smell that? Death’s perfume. Welcome to",
    "We’ve traced the anomaly to",
    "The shadows are thickest at",
    "Cross your fingers and follow me to",
    "The dead don’t rest in",
    "Hope you like cold spots—we’re bound for",
    "Heard a scream last night… came from",
    "They say it’s cursed, but we’re going to",
    "Whatever’s lurking in the dark lives in",
]

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
@app_commands.describe(size="Choose a map by its size")
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

    prefix = random.choice(INTRO_LINES)
    result = random.choice(option_list)
    await interaction.response.send_message(
        f"{prefix} **{result["full_name"]}** {result["emoji"]}"
    )


bot.run(DISCORD_BOT_TOKEN)
