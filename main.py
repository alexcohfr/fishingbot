import discord
from discord.ext import commands
from config import *
import datetime
import random as rd
from discord import app_commands
import pandas as pd
import datetime as dt
from fishing import *



intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix="!")

@client.event
async def on_ready():
    print("Bot logged in as {0.user}".format(client))
    try:
        synced = await client.tree.sync()
        print("synced")
    except:
        print("not synced")

@client.tree.command(name="ping")
@app_commands.describe(thing_to_say = "What should I say ?")
async def ping(interaction: discord.Interaction,thing_to_say:str):
    await interaction.response.send_message(f"pong,{thing_to_say}")




@client.tree.command(name="fish")
@app_commands.describe("Fishing")
async def fish(interaction: discord.Interaction):
    await interaction.response.send_message(f"🎣",ephemeral=True)









client.run(DISCORD_TOKEN)