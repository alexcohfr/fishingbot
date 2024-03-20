## Fichier qui regroupe toutes les fonctions de vérification de la base de données et des joueurs
import sqlite3
import datetime as dt
from icecream import ic



# Vérifie que l'ID en argument (correspondant à l'ID discord du joueur) est présent dans le DataFrame df
def check_ID(ID:int): # -> fonction à placer au début de  chaque commande du bot
    """Fonction qui vérifie si le joueur est dans la DB, si non, l'ajoute

    Args:
        ID (int): ID Discord du joueur

    Returns:
        Bool (int ici): 0 ou 1 en fonction du succès ou de l'échec
    """
    conn = sqlite3.connect('./database/fishingbot.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT ID_Joueur FROM players WHERE ID_Joueur = {ID}")
    is_in_db = cursor.fetchone()
    if not is_in_db:
        print(f"Le joueur {ID} n'est pas dans la base de données, on l'ajoute")
        
        time = dt.datetime.now() - dt.timedelta(seconds=3) # On enlève 3s pour que le joueur puisse jouer directement
        
        #On va créer la liste d'inventaire, l'indice correspond au poisson ou membre de la liste
        #Le chiffre à l'intérieur au nbre de gens dedans (cb de poissons attrapé comme ça en gros)
        
        
        # On ajoute le joueur dans la BDD, on garde le try au cas où il y ait une erreur "critique" qui bloque la commande
        try:

            nbre_charge_inital = 100
            #ID_Joueur, Nbre_charge, Tps_recharge
            cursor.execute(f"INSERT INTO Players VALUES (?,?,?)",(ID,nbre_charge_inital,time))
            conn.commit()

        except Exception as err:
            print(f"Une erreur s'est produite : {err}") #Print pour la console
            return 0 #Il y a eu une erreur, on return 0 pour pouvoir gérer ça dans le main
    
    conn.close() #On ferme la connexion

    return 1 #Tout s'est bien passé.


# On vérifie qu'il y a 3s entre chaque tirage
def check_time(ID:int):
    """Anti spam  de 3s

    Args:
        ID (int): ID discord du joueur

    Returns:
        Bool: Dis si ça fait plus de X secondes que le joueur a joué ou non
    """
    check_ID(ID)
    time = dt.datetime.now() #On récupère l'heure actuelle
    
    #Connexion à la BDD avec sqlite3
    conn = sqlite3.connect('./database/fishingbot.db')
    cursor = conn.cursor()
    
    #On récupère le temps de la dernière pêche
    cursor.execute(f"SELECT Tps_recharge FROM Players WHERE ID_Joueur = ?",(ID,))
    tps_last_fish = cursor.fetchone()[0]
    
    #On ferme la connexion
    conn.close()

    #On convertit le temps de la dernière pêche en datetime (fait pour que la comparaison entre time et tps_last_fish fonctionne)
    tps_last_fish = dt.datetime.strptime(tps_last_fish,"%Y-%m-%d %H:%M:%S.%f")
    laps_time = time - tps_last_fish
    if laps_time < dt.timedelta(seconds=3):
        return False #Si le temps entre les deux pêches est inférieur à 3s, on retourne False
    else:
        return True #Sinon on retourne True


#Fonction qui retourne le nombre de charge disponible du joueur
def check_charge(ID:int): 
    """Vérifie que le joueur possède encore des charges

    Args:
        ID (int): Id Discord du joueur

    Returns:
        Bool: Renvoie True si le joueur a encore des charges, False sinon
    """
    #On vérifie que le joueur est dans la BDD
    if not check_ID(ID): 
        return False

    conn = sqlite3.connect('./database/fishingbot.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT Nbre_charge FROM players WHERE ID_Joueur = {ID}")
    charge = cursor.fetchone()[0]
    tps_actuel = dt.datetime.now()
    cursor.execute(f"SELECT Tps_recharge FROM players WHERE ID_Joueur = {ID}")
    tps_last_recharge = cursor.fetchone()[0]
    tps_last_recharge = dt.datetime.strptime(tps_last_recharge,"%Y-%m-%d %H:%M:%S.%f")


    # On vérifie le temps écoulé depuis la dernière recharge
    if tps_actuel - tps_last_recharge > dt.timedelta(minutes=60):
        charge += 100
    elif tps_actuel - tps_last_recharge > dt.timedelta(minutes=40):
        charge += 80
    elif tps_actuel - tps_last_recharge > dt.timedelta(minutes=30):
        charge += 60
    elif tps_actuel - tps_last_recharge > dt.timedelta(minutes=20):
        charge += 40
    elif tps_actuel - tps_last_recharge > dt.timedelta(minutes=10):
        charge += 20

    # if charge > 100:
    #     charge = 100
    if charge <= 0:
        charge = 0
        return False

    cursor.execute(f"UPDATE players SET Nbre_charge = {charge} WHERE ID_Joueur = {ID}")
    conn.commit()
    conn.close()

    return True



if __name__ == "__main__":
    # Testing
    ic(check_ID(1))
    ic(check_time(1))
    ic(check_charge(1))