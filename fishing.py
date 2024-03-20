import datetime as dt
import random as rd
import time as time
import sqlite3
from check import check_ID, check_charge, check_time
import random
from icecream import ic

###  - - Fonctions auxiliaires pour clarifier la gestion du pêchage d'un poisson. - - ###


# à ajouter pour que ça fonctionne sur le perso dans l'adresse du .txt /home/users/assoces/abiisses/
def write_lines(ligne) -> None:
    """Fonction qui écrit le dernier poisson pêché dans un .txt

    Args:
        ligne (string): ligne à écrire dans le .txt

    Cette fonction sert pour l'affichage dynamique sur le site (aucun intérêt autrement)
    """
    print(ligne) #On l'affiche dans le terminal pour pouvoir suivre
    with open("poisson.txt","w",encoding="utf-8") as f:
        f.write(ligne) #Ecriture dans le fichier
    return


def enleve_charge(ID:int) -> int:
    """Fonction qui se charge d'enlever une charge au joueur dans la BDD

    Args:
        ID (int): ID Discord du joueur
    """
    # On regarde si le joueur existe
    assert check_ID(ID), "Erreur de vérification de l'ID du joueur"


    #Connexion à la bdd
    conn = sqlite3.connect('./database/fishingbot.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT Nbre_charge FROM players WHERE ID_Joueur = {ID}")

    #On récupère charge
    charge = cursor.fetchone()[0]
    try:
        #Si il y a une charge disponible, on en enlève une et on change le temps de la dernière utilisation de la charge
        if charge > 0:
            cursor.execute(f"UPDATE players SET Nbre_charge = {charge-1} WHERE ID_Joueur = {ID}")
            cursor.execute(f"UPDATE players SET Tps_recharge = '{dt.datetime.now()}' WHERE ID_Joueur = {ID}")
            conn.commit()

            #On ferme la connexion à la bdd
            conn.close()
            return 1 # On renvoie 1 si tout s'est bien passé et qu'on a enlevé une charge
        else:
            conn.close()
            return 0 # On renvoie 0 si le joueur n'a plus de charge
    except:
        conn.close()
        return -1 # On renvoie -1 si il y a eu une erreur dans la bdd



def get_fish(ID:int) ->tuple[int,str]:
    """Fonction qui renvoie un tuple de longueur 2 sous la forme suivante: (statut exec, id_poisson)
    Le statut exec gère les différentes erreurs qui peuvent arriver et servent à gérer ces erreurs dans le main.
    id_poisson est l'id du poisson dans la bdd

    Args:
        ID (int): ID discord du joueur

    Returns:
        tuple : tuple de longueur 2 sous la forme suivante: (statut exec, id_poisson)
    """

    assert check_ID(ID), "Erreur de vérification de l'ID du joueur"
    nbre_charge = check_charge(ID) #On rappelle que cette fonction renvoie un booléen


    if not nbre_charge: #Cas où il n'y a plus de charges
        return 2,"" #On renvoie 2 pour dire qu'il n'y a plus de charges, -1 pour dire qu'il n'y a pas de poisson, "" pour dire qu'il n'y a pas de rareté et -1 pour dire qu'il n'y a pas de score
    

    elif nbre_charge:
        # On vérifie qu'il y a 3s entre chaque tirage
        # if not check_time(ID):
        #     return 3,"" # On renvoie 3 pour dire qu'il n'y a pas eu 3s entre chaque tirage 
        
        # On enlève une charge
        enleve_charge(ID)

        # On gère les différentes rareté: Commun, Peu Commun, Rare, Très rare, Inestimable, Légendaire, Mythique, Miraculeux, Malus
        # Définition des probabilités cumulées

        probas_cumulees = [
            0.00001,  # Miraculeux
            0.00011,  # Mythique
            0.005,    # Légendaire
            0.1549,   # Inestimable
            4.9549,   # Très Rare
            19.8049,  # Rare
            48.8049,  # Peu Commun
            93.8049,  # Commun
            98.8049,  # Malus
        ]
        # Tirage aléatoire
        tirage = random.uniform(0, 100)
        # Détermination de la catégorie en fonction du tirage
        if tirage < probas_cumulees[0]:
            score = 250000
            rarete = "Miraculeux"
        elif tirage < probas_cumulees[1]:
            score = 50000
            rarete = "Mythique"
        elif tirage < probas_cumulees[2]:
            score = 10000
            rarete = "Légendaire"
        elif tirage < probas_cumulees[3]:
            score = 2000
            rarete = "Inestimable"
        elif tirage < probas_cumulees[4]:
            score = 500
            rarete = "Très Rare"
        elif tirage < probas_cumulees[5]:
            score = 150
            rarete = "Rare"
        elif tirage < probas_cumulees[6]:
            score = 50
            rarete = "Peu Commun"
        elif tirage < probas_cumulees[7]:
            score = 10
            rarete = "Commun"
        else:
            score = -100
            rarete = "Malus"

        # On ajoute le poisson en inventaire
        conn = sqlite3.connect('./database/fishingbot.db')
        cursor = conn.cursor()

        # On tire un poisson aléatoire
        cursor.execute("SELECT ID_item FROM Items WHERE Rarete = ?", (rarete,))
        item_id = cursor.fetchall()
        all_items = [item[0] for item in item_id]
        peche = rd.choice(all_items)


        # Vérifie si l'item existe déjà dans l'inventaire du joueur.
        cursor.execute("SELECT EXISTS(SELECT 1 FROM Inventaire WHERE joueur_id = ? AND item_id = ?)",(ID, peche))
        existe = cursor.fetchone()[0]
        if existe:
            # Si l'item existe, met à jour la quantité.
            cursor.execute("UPDATE Inventaire SET quantity = quantity + ? WHERE joueur_id = ? AND item_id = ?",(1, ID, peche))
        else:
            # Sinon, insère un nouvel item.
            cursor.execute("INSERT INTO Inventaire (joueur_id, item_id, quantity) VALUES (?, ?, ?)", (ID, peche, 1))
        # Sauvegarde les changements.
        conn.commit()
        

        return 1,peche #On renvoie 1 pour dire que tout s'est bien passé, peche pour dire quel poisson a été pêché
    else:
        return 0,"" #Erreur
        


def get_info(poisson_peche: int) -> tuple[str,int,str]:
    """Fonction qui renvoie le nom, le score et la rareté d'un poisson

    Args:
        poisson_peche (int): id du poisson pêché

    Returns:
        tuple : tuple de longueur 3 sous la forme suivante: (nom_poisson, score, rarete)
    """
    #Connexion à la bdd
    conn = sqlite3.connect('./database/fishingbot.db')
    cursor = conn.cursor()

    #On récupère les infos du poisson
    cursor.execute("SELECT Name, Score, Rarete,lien FROM Items WHERE ID_item = ?", (poisson_peche,))
    infos = cursor.fetchone()
    nom_poisson = infos[0]
    score = infos[1]
    rarete = infos[2]
    link = infos[3]

    #On ferme la connexion à la bdd
    conn.close()
    return nom_poisson,score,rarete,link #On renvoie le nom du poisson, son score et sa rareté








if __name__ == "__main__":
    #testing probas
    li_res = []
    for i in range(1000):
        li_res.append(get_fish(2)[1])
    print("fini")
    
    # On veut avoir l'occurence de chaque id de li_res
    occurence = {}
    for i in li_res:
        if i in occurence:
            occurence[i] += 1
        else:
            occurence[i] = 1
    print(occurence)
    




    # ic(enleve_charge(1))
    # ic(get_fish(1))
    # ic(get_score(1))
    # ic(get_fish(2))
    # ic(classement_top_10())
