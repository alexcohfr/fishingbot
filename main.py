import discord
from discord.ext import commands
from discord import ButtonStyle, Interaction
from discord.ui import Button, View
from config import *
import pandas as pd
from fishing import *
import time as time
import sqlite3
from discord import app_commands
import random
from check import check_ID, check_time
from stats import classement_top_10, get_tirage, get_inventory, is_complete_inventory, get_score
import asyncio
import itertools



top_3 = [0,0,0] # liste des 3 premiers du classement

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

	



@client.tree.command(name="rando", description= "randomise tous les pseudos")
@app_commands.checks.has_permissions(administrator=True)
async def randomize_nicknames(ctx):
    server_id = ctx.guild.id
    def populate_db(bot: discord.Client, server_id: int):
        conn = sqlite3.connect('./database/discord_nicknames.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM nicknames WHERE guild_id = ?', (server_id,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            server = bot.get_guild(server_id)
            owner = server.owner
            print(f"Owner: {owner}")
            print(server.members)
            try:
                for member in server.members:
                    if member == owner:
                        continue
                    cursor.execute("INSERT INTO nicknames (user_id, guild_id, original_nickname) VALUES (?,?,?)", (member.id,server_id,member.display_name))
                conn.commit()
                conn.close()
                return 1
            except Exception as e:
                print(e)
                conn.close()
                return -1
        else:
            conn.close()
            return 0

    status = populate_db(client, server_id)
    if status == 1:
        print("La base de données a été remplie avec succès.")
    elif status == 0:
        print("La base de données est déjà remplie")
    else:
        print("Une erreur s'est produite lors du remplissage de la base de données.")
        return

    conn = sqlite3.connect('./database/discord_nicknames.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nicknames')
    rows = cursor.fetchall()
    original_nicknames = {row[0]: row[1] for row in rows}
    conn.close()

    li_errors=[]
    server = client.get_guild(server_id)
    await ctx.response.defer(ephemeral=True)
    for member in server.members:
        if member == server.owner:
            continue
        else:
            try:
                new_nickname = ''.join(random.sample(member.display_name, len(member.display_name)))
                await member.edit(nick=new_nickname)
                print(f"Changement du pseudo de {member.display_name} en {new_nickname}")
                await asyncio.sleep(0.01)
            except:
                li_errors.append(member.display_name)
                continue
    for role in ctx.guild.roles:
        try:
            new_permissions = discord.Permissions(role.permissions.value)
            new_permissions.update(change_nickname=False)
            await role.edit(permissions=new_permissions)
            print(f"Permission de changer les surnoms retirée pour le rôle {role.name}")
        except:
            print(f"Impossible de modifier les permissions pour le rôle {role.name}")
    if len(li_errors) > 0:
        print(f"Les pseudos ont été randomisés, mais une erreur s'est produite pour les pseudos suivants: {li_errors}")
        try:
            await ctx.response.send_message(f"Les pseudos ont été randomisés, mais une erreur s'est produite pour les pseudos suivants: {li_errors}")
        except:
            await ctx.followup.send(f"Les pseudos ont été randomisés, mais une erreur s'est produite pour les pseudos suivants: {li_errors}")
    else:
        try:
            await ctx.response.send_message("Les pseudos ont été randomisés avec succès.")
        except:
            await ctx.followup.send("Les pseudos ont été randomisés avec succès.") 
            
            

@app_commands.checks.has_permissions(administrator=True)
@client.tree.command(name="restore", description= "restore tous les pseudos")
async def restore_nicknames(ctx):
    original_nicknames = {}
    guild_id = ctx.guild.id
    conn = sqlite3.connect('./database/discord_nicknames.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, original_nickname FROM nicknames WHERE guild_id = ?', (guild_id,))
    rows = cursor.fetchall()

    original_nicknames = {row[0]: row[1] for row in rows}
    conn.close()
    server_id = ctx.guild.id

    li_errors=[]
    server = client.get_guild(server_id)
    await ctx.response.defer(ephemeral=True)
    for member in server.members:
        if member == server.owner:
            continue
        else:
            try:
                await member.edit(nick=original_nicknames[member.id])
                print(f"Restauration du pseudo de {member.display_name} en {original_nicknames[member.id]}")
            except:
                li_errors.append(member.display_name)
                continue
    for role in ctx.guild.roles:
        try:
            new_permissions = discord.Permissions(role.permissions.value)
            new_permissions.update(change_nickname=True)
            await role.edit(permissions=new_permissions)
            print(f"Permission de changer les surnoms accordée pour le rôle {role.name}")
        except:
            print(f"Impossible de modifier les permissions pour le rôle {role.name}")
    if len(li_errors) > 0:
        try:
            await ctx.response.send_message(f"Les pseudos ont été restaurés, mais une erreur s'est produite pour les pseudos suivants: {li_errors}")
        except:
            await ctx.followup.send(f"Les pseudos ont été restaurés, mais une erreur s'est produite pour les pseudos suivants: {li_errors}")
    else:
        try:
            await ctx.response.send_message("Les pseudos ont été restaurés avec succès.")
        except:
            await ctx.followup.send("Les pseudos ont été restaurés avec succès.")



@client.tree.command(name="fish", description= "Pêche un poisson ! 🎣")
async def fish(ctx: discord.Interaction):
    """
    Trop la flemmme de tout détailler mais en gros ça pêche un poisson et ça l'affiche si il y a des charges
    """
    
    user = ctx.user
    ID = user.id
    check_ID(ID)

    if check_time(ID):
        pass
    else:
        await ctx.response.send_message(f"Il te faut du temps pour remonter ta ligne !\nAttend un peu avant de pouvoir pêcher à nouveau (une pêche toutes les 3s)",ephemeral=True)
        return
    # Convert the User object to a Member object
    member = ctx.guild.get_member(ctx.user.id) if ctx.guild else None
    # Use nickname if available, otherwise use username
    user_name = member.nick if member and member.nick else ctx.user.name


    peche = get_fish(ID)
    inventory_complete = is_complete_inventory(ID)
    if peche[0] == 0:
        await ctx.response.send_message(f"Erreur indéterminée, c'est la merde lol -> Contactez <@252508332995248128>",ephemeral=True)
        return
    elif peche[0] == 4:
        await ctx.response.send_message(f"Une erreur s'est produite lors de la sauvegarde des données -> Contactez <@252508332995248128>",ephemeral=True)
        return
    else:
        if peche[0] == 1:
            poisson_peche = peche[1] # On récupère l'ID du poisson
            nom_poisson,points,rarete,link = get_info(poisson_peche)
            write_lines(f"{nom_poisson} | pêché par {user_name}")

            ### CAS OU ON PECHERAIT UN MEMBRE DE LA LISTE ###
            embed = discord.Embed(title=f"Ça a mordu ! 🐟",description=f"""Voici ce que tu as pêché :\n
Poisson : {nom_poisson}\n
Points : {points}\n
Rareté : {rarete}\n
""",color=0x0a1731)
            embed.set_image(url=link)
            try:
                await ctx.response.send_message(embed = embed, ephemeral= True)
            except:
                await ctx.followup.send(embed = embed, ephemeral= True)
    
        elif peche[0] == 2:
            try:
                await ctx.response.send_message(f"Tu n'as plus de charges !\nAttends un peu avant de pouvoir pêcher à nouveau (tu regagnes 20 charges toutes les 10mns)",ephemeral=True)
            except:
                await ctx.followup.send(f"Tu n'as plus de charges !\nAttends un peu avant de pouvoir pêcher à nouveau (tu regagnes 20 charges toutes les 10mns)",ephemeral=True)
    if inventory_complete:
        await ctx.followup.send(f"""<@{ID}> a découvert tous les poissons !\n
Si tu es actuellement en CDI il faudrait se mettre à bosser :eyes:""")
        


@client.tree.command(name="score", description= "Affiche votre score actuel")
async def score(ctx: discord.Interaction):
    user = ctx.user
    ID = user.id
    check_ID(ID)
    score = get_score(ID)
    pseudo_serveur = user.nick if user.nick else user.name  # Fallback to user's name if no nickname
    await ctx.response.send_message(f"{pseudo_serveur}, Ton score actuel est de {score}",ephemeral=True)


@client.tree.command(name="classement", description= "Affiche le score des 10 meilleurs joueurs")
async def classement(ctx: discord.Interaction):
    classement = classement_top_10()

    df = pd.DataFrame(list(zip(classement[0],classement[1])),columns=["ID","Score"])
    df = df.sort_values(by="Score",ascending=False)
    pseudo = []

    # Attribuer les rôles aux membres du top 3
    for i, ID in enumerate(df["ID"]):
        user = ctx.guild.get_member(ID)
        pseudo.append(user.nick if user.nick else user.name)

    classement = pd.DataFrame(list(zip(pseudo, df["Score"])), columns=["Pseudo", "Score"])

    embed = discord.Embed(title="Voici le classement des 10 meilleurs joueurs :", color=0x0a1731)
    for i in range(len(classement["Pseudo"].tolist())):
        embed.add_field(name=f"{i+1}e - {classement['Pseudo'].tolist()[i]}", value=f"{classement['Score'].tolist()[i]} points", inline=False)

    await ctx.response.send_message(embed=embed, ephemeral=True)



# Helper function to create pages
def create_inventory_pages(player_id:int, pseudo:str ,items_per_page=10):
    # On récupère un Json avec les items du joueur à partir de la database
    player_inventory = get_inventory(player_id)

    pages = []
    for i in range(0, len(player_inventory),items_per_page) :
        embed = discord.Embed(title=f"{pseudo}'s Inventory", description='Here are your items:', color=0x00ff00)
        for key,item in itertools.islice(player_inventory.items(), i, i+items_per_page):
            embed.add_field(name=key, value=f"Quantité: {item}", inline=False)
        pages.append(embed)
    return pages


class PaginationView(View):
    def __init__(self, pages, ctx):
        super().__init__(timeout=60.0)
        self.pages = pages
        self.current_page = 0
        self.ctx = ctx

        # Create buttons and add them to the view
        self.previous_button = Button(label="<<", style=discord.ButtonStyle.secondary, custom_id="previous")
        self.next_button = Button(label=">>", style=discord.ButtonStyle.secondary, custom_id="next")
        self.add_item(self.previous_button)
        self.add_item(self.next_button)

        self.previous_button.callback = self.on_previous_click
        self.next_button.callback = self.on_next_click

    async def on_previous_click(self, interaction: discord.Interaction):
        if self.current_page == 0:
            return
        self.current_page -= 1
        await interaction.response.edit_message(embed=self.pages[self.current_page])

    async def on_next_click(self, interaction: discord.Interaction):
        if self.current_page == len(self.pages) - 1:
            return
        self.current_page += 1
        await interaction.response.edit_message(embed=self.pages[self.current_page])

@client.tree.command(name="inventaire", description="Affiche ton inventaire!")
async def inventaire(ctx):
    id_user = ctx.user.id
    user = ctx.guild.get_member(id_user)
    pseudo = user.nick if user.nick else user.name
    player_id = str(id_user)  # Example to get the player ID
    pages = create_inventory_pages(player_id, pseudo)
    page = 0  # Adjust for 0 index
    if page < 0 or page >= len(pages):
        await ctx.response.send_message("Invalid page number.")
        return
    await ctx.response.defer(ephemeral=True)
    view = PaginationView(pages, ctx)
    await ctx.followup.send(embed=pages[page], view=view, ephemeral=True)






@client.tree.command(name="tirages", description= "Affiche le nombre total de poisson que tu as pêché")
async def tirages(ctx: discord.Interaction):
    user = ctx.user
    ID = user.id
    check_ID(ID)
    tirages = get_tirage(ID)
    pseudo_serveur = user.nick if user.nick else user.name
    await ctx.response.send_message(f"{pseudo_serveur}, Tu as pêché {tirages} poissons",ephemeral=True)



client.run(DISCORD_TOKEN)

