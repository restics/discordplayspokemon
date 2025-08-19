import atexit
import os

from player import instance
from logger import Logger

import discord
from discord import Button, app_commands
from discord.ext import commands
import dotenv
from ui import GameboyPad, RomsDropdown, play_game_screen

# Load environment variables from .env file
dotenv.load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN environment variable not set.")

intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content

bot = commands.Bot(command_prefix='!', intents=intents)
is_bot_active = False;

romplayer = instance

@bot.event
async def on_ready():
    Logger.info('Logged in as %s!', bot.user)
    try:
        synced = await bot.tree.sync()
        Logger.info("Synced %d commands!", len(synced))
    except Exception as e:
        Logger.error(e)

def get_roms_list():
    return os.listdir("roms")

@bot.tree.command(name="load")
async def load(interaction: discord.Interaction):
    if not is_admin(interaction):
        await interaction.response.send_message("You must be an admin to use this command.", ephemeral=True)
        return
    roms = get_roms_list()
    if is_bot_active:
        await interaction.response.send_message("close the current game first!", ephemeral=True)
        return;
    elif not roms:
        await interaction.response.send_message("No ROMs found.", ephemeral=True)
        return
    view = RomsDropdown(roms)
    await interaction.response.send_message("Select a ROM to load:", view=view, ephemeral=True)


@bot.tree.command(name="play")
async def play(interaction: discord.Interaction):

    view = GameboyPad()
    embed, image = play_game_screen()
    if image:
        await interaction.response.send_message(embed=embed, file=image, view=view, ephemeral=False)
    else:
        await interaction.response.send_message(embed=embed, view=view, ephemeral=False)

@bot.tree.command(name="save")
async def save(interaction: discord.Interaction):
    instance.save()
    await interaction.response.send_message('State saved to saves/save.state', ephemeral=True)

@bot.tree.command(name="setmode")
@app_commands.describe(mode="Set to 'democracy' or 'anarchy'")
async def setmode(interaction: discord.Interaction, mode: str):
    if not is_admin(interaction):
        await interaction.response.send_message("You must be an admin to use this command.", ephemeral=True)
        return 
    if mode.lower() == "democracy":
        instance.is_democracy = True
        await interaction.response.send_message("Mode set to Democracy", ephemeral=True)
    elif mode.lower() == "anarchy":
        instance.is_democracy = False
        await interaction.response.send_message("Mode set to Anarchy", ephemeral=True)
    else:
        await interaction.response.send_message("Invalid mode. Use 'democracy' or 'anarchy'", ephemeral=True)


def is_admin(interaction: discord.Interaction) -> bool:
    member = interaction.user
    # only i can use admin commands >:)
    return member.id == 418986435144581130

def exit_handler():
    Logger.info('application terminating, save game')
    instance.save()

atexit.register(exit_handler)

bot.run(TOKEN)