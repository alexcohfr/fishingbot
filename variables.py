import pandas as pd
import random as rd


#CSV
CSV_PATH = "assets/bdd.csv"

#Bdd est déclaré
with open(CSV_PATH,"r") as f:
    Bdd = pd.read_csv(f,sep=";",encoding="utf-8",header=0)


#Déclaration des membres de la liste
mbre_liste = {
    "Les boss" : "img.jpg",
    "Requin Boobs": "shark_boobs.jpg",
    "Djoko": "img.jpg",
    "Silvec": "img.jpg",
    "Zippo": "img.jpg",
    "Typh": "img.jpg",
    "Ana": "img.jpg",
    "Booléen": "img.jpg",
    "Saké": "img.jpg",
    "Titane": "img.jpg",
    "Noisette Très Chouette": "img.jpg",
    "Ev": "img.jpg",
    "Wouali": "img.jpg",
    "Mowgli": "img.jpg",
    "Benj": "img.jpg",
    "Teecs": "img.jpg",
    "Karnas": "img.jpg",
    "Belek": "img.jpg",
    "Crayon": "img.jpg",
    "Clutch": "img.jpg",
    "Flash": "img.jpg",
    "Fluffy": "img.jpg",
    "Jane": "img.jpg",
    "Marionnette": "img.jpg",
    "Scooby": "img.jpg",
    "Tom": "img.jpg",
    "Ravel": "img.jpg",
    "Fortiche": "img.jpg",  
    "Cornichon": "img.jpg"
}


# Définir les groupes de rareté
quasi_impossible = ["Les boss"]
legendaire = ["Zippo"]
tres_tres_rare = ["Saké", "Ev", "Titane", "Crayon"]
rare = ["Wouali", "Mowgli", "Belek", "Scooby", "Silvec", "Tom"]
commun = [name for name in mbre_liste.keys() if name not in quasi_impossible + legendaire + tres_tres_rare + rare]

# Créer la liste de 1000 noms
noms = quasi_impossible * 1 + legendaire * 10 + tres_tres_rare * 25 + rare * 50 + commun * 36 + ["Jane"]*13
TAILLE_NOMS = len(noms)

# Créer le DataFrame des poissons
with open("assets\poissons.csv","r") as f:
    poissons = pd.read_csv(f,sep=";",encoding="utf-8",header=0)

        ### On gère la rareté ###
#On crée la liste des poissons communs:
commun_poissons = poissons[poissons['rarete'].str.strip() == 'Commun']['nom_poisson'].tolist()
#On crée la liste des poissons rares:
rare_poissons = poissons[poissons['rarete'].str.strip() == 'Rare']['nom_poisson'].tolist()
#On crée la liste des poissons très rares:
tres_rare_poissons = poissons[poissons['rarete'].str.strip() == 'Très rare']['nom_poisson'].tolist()
#On crée la liste des 1110 poissons en fonction de leur rareté:
poissons_tirage = commun_poissons*300 + rare_poissons*100 + tres_rare_poissons*10
TAILLE_POISSONS = len(poissons_tirage)


rd.shuffle(poissons_tirage)
rd.shuffle(noms)


# On organise les ID des choses pêchables:



pechables = ["Les boss",
    "Requin Boobs",
    "Djoko",
    "Silvec",
    "Zippo",
    "Typh",
    "Ana",
    "Booléen",
    "Saké",
    "Titane",
    "Noisette Très Chouette",
    "Ev",
    "Wouali",
    "Mowgli",
    "Benj",
    "Teecs",
    "Karnas",
    "Belek",
    "Crayon",
    "Clutch",
    "Flash",
    "Fluffy",
    "Jane",
    "Marionnette",
    "Scooby",
    "Tom",
    "Ravel",
    "Fortiche",  
    "Cornichon",
    ]

#TODO: ajouter rareté et lien image pour chaque pêchable
# poissons_avc_images = 

pechables += poissons["nom_poisson","link_img"].tolist()

TAILLE_PECHABLES = len(pechables)