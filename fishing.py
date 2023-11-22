import pandas as pd
import datetime as dt
import random as rd


mbre_liste = {
    "Les boss" : "img.jpg",
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

rd.shuffle(noms)


CSV_PATH = "assets/bdd.csv"

###  - - Fonctions auxiliaires pour clarifier la gestion du pêchage d'un poisson. - - ###



# Vérifie que l'ID en argument (correspondant à l'ID discord du joueur) est présent dans le DataFrame df
def id_in_df(ID:int,df:pd.DataFrame):
    return ID in df["ID_Joueur"].values

# Si la fonction précédente return False, on appelle cette fonction pour l'ajouter.
def add_id_in_df(ID:int,df:pd.DataFrame):
    time = dt.datetime.now()
    df = df.append({"ID_Joueur":ID,"Nbre_charge":2,"Tps_recharge":time,"Score":0},ignore_index=True)
    return df



#Fonction qui vérifie si le joueur a des charges disponibles retourne 1 si c'est le cas (en enlève une au passage) et 0 sinon
def check_charge(ID:int,df:pd.DataFrame):
    charge = df.loc[df["ID_Joueur"]==ID,"Nbre_charge"].values[0]
    tps_actuel = dt.datetime.now()
    tps_last_recharge = df.loc[df["ID_Joueur"]==ID,"Tps_recharge"].values[0]

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
    
    # Si le temps de recharge est supérieur à 0, on met à jour le temps de recharge
    if charge > 0:
        df.loc[df["ID_Joueur"]==ID,"Nbre_charge"] = charge - 1
        return 1
    else:
        return 0
    

def update_df(df:pd.DataFrame):
    with open(CSV_PATH,"w") as f:
        df.to_csv(f,sep = ";",header=True,index=False)
    return


#TODO: Finir cette fonction
def fish():
    # On tire un nombre aléatoire entre 0 et 100
    # Si le nombre est inférieur à 10, on pêche un membre de la liste, sinon on pêche un poisson
    score = 0
    random_number = rd.randint(0,100)
    if random_number<10:
        # On pêche un membre de la liste
        nom_aléatoire = rd.choice(noms)
        if nom_aléatoire in quasi_impossible:
            score = 100
        elif nom_aléatoire in legendaire:
            score = 50
        elif nom_aléatoire in tres_tres_rare:
            score = 25
        elif nom_aléatoire in rare:
            score = 10
        elif nom_aléatoire in commun:
            score = 5
        
        pass

    else:
        # On pêche un poisson

    
    return score