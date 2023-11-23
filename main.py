import discord
from discord.ext import commands
from config import *
from variables import *
import random as rd
from discord import app_commands
import pandas as pd
import datetime as dt
from fishing import *
from fishing import get_score



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




@client.tree.command(name="fish", description= "Pêche un poisson ! 🎣")
async def fish(ctx: discord.Interaction):
    user = ctx.message.author
    ID = user.id
    
    await ctx.response.send_message(f"🎣",ephemeral=True)
    await ctx.response.send_message(f"Ca a mordu ! 🐟",ephemeral=True)
    peche = fish(ID)
    if peche[0] == 0:
        await ctx.response.send_message(f"Erreur indéterminée, c'est la merde lol",ephemeral=True)
    else:
        if peche[0] == 1:
            await ctx.response.send_message(f"Tu as pêché un {pechables[peche[1]]} !",ephemeral=True)
        elif peche[0] == 2:
            await ctx.response.send_message(f"Tu n'as plus de charges !\nAttend un peu avant de pouvoir pêcher à nouveau",ephemeral=True)


    return


@client.tree.command(name="score", description= "Affiche votre score actuel")
async def score(ctx: discord.Interaction):
    user = ctx.user
    ID = user.id
    check_ID(ID)
    score = get_score(ID)
    pseudo_serveur = user.nick if user.nick else user.name  # Fallback to user's name if no nickname
    await ctx.response.send_message(f"{pseudo_serveur}, Ton score actuel est de {score}",ephemeral=True)











client.run(DISCORD_TOKEN)