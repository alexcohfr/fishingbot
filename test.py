## Header (import des librairies)
import pandas as pd
import datetime as dt
from variables import *


# Vérifie que l'ID en argument (correspondant à l'ID discord du joueur) est présent dans le DataFrame df
def check_ID(ID:int): # -> fonction à placer au début de chaque commande du bot
    df = pd.read_csv(CSV_PATH,sep=";")
    bool = ID in df["ID_Joueur"].values
    if not bool:
        time = dt.datetime.now()
        #On va créer la liste d'inventaire
        #L'indice -1 correspond au poisson ou membre de la liste
        #Le chiffre à l'intérieur au nbre de gens dedans (cb de poissons attrapé comme ça en gros)
        inventory_init = [0 for k in range(TAILLE_PECHABLES)] # Taille pechable correspond à la taille de tout ce qui est pêchable
        try:
            with open("assets/bdd.csv","a") as f:
                f.write(f"{ID};3;{time};0;{inventory_init}\n")
        except Exception as err:
            print(f"Une erreur s'est produite : {err}")
            return 0

    return 1 #Tout s'est bien passé.

def check_charge(ID:int): 
    assert check_ID(ID), "Erreur de vérification de l'ID du joueur"
    # Lecture du fichier csv puis stockage dans un DataFrame
    df = pd.read_csv(CSV_PATH,sep=";")

    # On récupère le nombre de charges du joueur
    charge = df.loc[df["ID_Joueur"]==ID,"Nbre_charge"].values[0]
    tps_actuel = dt.datetime.now()
    tps_last_recharge = dt.datetime.strptime(df.loc[df["ID_Joueur"]==ID,"Tps_recharge"].values[0],"%Y-%m-%d %H:%M:%S.%f")

    # On vérifie le temps écoulé depuis la dernière recharge
    if tps_actuel - tps_last_recharge > dt.timedelta(minutes=20):
        charge += 1
    elif tps_actuel - tps_last_recharge > dt.timedelta(minutes=40):
        charge += 2
    elif tps_actuel - tps_last_recharge > dt.timedelta(minutes=60):
        charge += 3

    # On vérifie que le nombre de charges n'est pas supérieur à 3
    if charge>3:
        charge = 3

    return charge
## Fonctions

def fish(ID:int):
    # On tire un nombre aléatoire entre 0 et 100
    # Si le nombre est inférieur à 10, on pêche un membre de la liste, sinon on pêche un poisson
    nbre_charge = check_charge(ID)
    if nbre_charge == 0:
        return 2 # Pas assez de charges
    elif nbre_charge > 0:
        # On enlève une charge
        df = pd.read_csv(CSV_PATH,sep=";")
        df.loc[df["ID_Joueur"]==ID,"Nbre_charge"] = nbre_charge - 1
        df.loc[df["ID_Joueur"]==ID,"Tps_recharge"] = dt.datetime.now()
        df.to_csv(CSV_PATH,sep=";",index=False)
    else:
        return 0 # Erreur indéterminée donc c'est la merde lol
    
    random_number = rd.randint(0,100)
    print(random_number)
    if random_number<=10:
        # On pêche un membre de la liste
        peche = rd.choice(noms)
        if peche in quasi_impossible:
            score = 1000
        elif peche in legendaire:
            score = 500
        elif peche in tres_tres_rare:
            score = 200
        elif peche in rare:
            score = 150
        elif peche in commun:
            score = 50
    else:
        # On pêche un poisson
        peche = rd.choice(poissons_tirage)
        if peche in commun_poissons:
            score = 10
        elif peche in rare_poissons:
            score = 20
        elif peche in tres_rare_poissons:
            score = 40
    # On ajoute le score et le poisson en inventaire
    df = pd.read_csv(CSV_PATH,sep=";")
    df.loc[df["ID_Joueur"]==ID,"Score"] += score
    
    # Gestion de l'inventaire (bordel avec des strings mais ça marche on espère)
    index_peche = pechables.index(f"{peche}")
    inventory = eval(df.loc[df["ID_Joueur"]==ID,"inventaire"][0])
    inventory[index_peche] += 1
    df.loc[df["ID_Joueur"]==ID,"inventaire"] = str(inventory)
    df.to_csv(CSV_PATH,sep=";",index=False)
    
    return 1 # Tout s'est bien passé


def get_inventory(ID:int):
    assert check_ID(ID), "Erreur de vérification de l'ID du joueur"
    df = pd.read_csv(CSV_PATH,sep=";")
    inventory = eval(df.loc[df["ID_Joueur"]==ID,"inventaire"][0])
    li_peche = [(pechables[k],inventory[k]) for k in range(TAILLE_PECHABLES) if inventory[k]>0]
    msg_prep = [f"{el[0]} : {el[1]}" for el in li_peche]
    li_photos = [f"assets/{peche}.png" for peche in li_peche]
    return msg_prep,li_photos

fish(12)
print(get_inventory(12))