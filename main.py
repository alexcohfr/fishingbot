import discord
from discord.ext import commands
from config import *
import datetime
import random as rd
from discord import app_commands
import pandas as pd
import datetime as dt



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

#Fonctions auxiliaires pour clarifier la gestion du pêchage d'un poisson.

def id_in_df(ID:int,df:pd.DataFrame):
    return ID in df["ID_Joueur"].values

def add_id_in_df(ID:int,df:pd.DataFrame):
    time = dt.datetime.now()
    df = df.append({"ID_Joueur":ID,"Nbre_charge":2,"Tps_recharge":time,"Score":0},ignore_index=True)
    return df



@client.tree.command(name="fish")
@app_commands.describe("Fishing")
async def fish(interaction: discord.Interaction):
    await interaction.response.send_message(f"🎣",ephemeral=True)
    ID = interaction.user.id 
    df = pd.read_csv("assets/bdd.csv")
    if ID in df["ID_Joueur"].values:
        df.loc[df["ID_Joueur"]==ID,"fish"] += 1
    else:
        df = df.append({"ID_Joueur":ID,"fish":1},ignore_index=True)









client.run(DISCORD_TOKEN)