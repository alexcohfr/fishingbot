### Fichier qui s'occupent des fonction qui fournissent des stats sur les joueurs ###


import sqlite3
import datetime as dt
from icecream import ic
from check import check_ID



def get_score(ID:int) -> int:
    """Donne le score de qqun 

    Args:
        ID (int): ID discord du joueur

    Returns:
        int : Valeur du score 
    """
    assert check_ID(ID), "Erreur de vérification de l'ID du joueur"
    
    #Connexion à la bdd
    conn = sqlite3.connect('./database/fishingbot.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT Score_Total From Score_joueur WHERE ID_Joueur = {ID}")
    
    #On récupère le score
    score = cursor.fetchone()[0]
    
    conn.close()
    
    return score


def get_tirage(ID:int):
    """Retourne le nombre de tirage d'un joueur (implémenté grâce à Scary)

    Args:
        ID (int): ID discord du joueur

    Returns:
        int : nbre de tirage
    """
    #On ouvre la liste de l'inventaire et on fait la somme de toutes les valeurs pour avoir le nbre de tirage
    assert check_ID(ID), "Erreur de vérification de l'ID du joueur"
    
    #Connexion à la bdd
    conn = sqlite3.connect('./database/fishingbot.db')
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT Nbre_tirage FROM Score_joueur WHERE ID_Joueur = ?
                   """,(ID,))
    
    #On récupère l'inventaire
    nbre_tirage = cursor.fetchone()[0]
    
    conn.close()
    
    return nbre_tirage


def classement_top_10(): # Fonctionne
    """Fonction qui renvoie les 10 meilleurs joueurs

    Returns:
        tuple : (ID discord, score)
    """

    #Connexion à la bdd
    conn = sqlite3.connect('./database/fishingbot.db')
    cursor = conn.cursor()
    
    #On recupère les ID des joueurs
    cursor.execute(f"SELECT ID_Joueur, Score_total as Score FROM Score_joueur ORDER BY Score DESC LIMIT 10")
    df = cursor.fetchall()
    
    #On ferme la connexion
    conn.close()

    #On renvoie les ID et les scores sous forme de liste (on peut trouver un autre moyen + opti de faire ça)
    Id_joueur = [el[0] for el in df]
    Score = [el[1] for el in df]
    
    
    return Id_joueur,Score



def is_complete_inventory(ID:int) -> bool:
    """Fonction qui vérifie si un joueur a pêché tous les poissons du jeu ou pas

    Args:
        ID (int): Id discord du joueur

    Returns:
        bool : True si le joueur a pêché tous les poissons, False sinon
    """
    assert check_ID(ID), "Erreur de vérification de l'ID du joueur"
    
    #Connexion à la bdd
    conn = sqlite3.connect('./database/fishingbot.db')
    cursor = conn.cursor()
    
    #On récupère l'inventaire
    cursor.execute(f"SELECT COUNT(DISTINCT item_id) FROM Inventaire WHERE joueur_id = ?",(ID,))
    inventory = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM Items")
    total_items = cursor.fetchone()[0]

    conn.close()
    if inventory == total_items:
        return True
    else:
        return False



def get_inventory(ID:int)-> dict:
    """Fonction qui renvoie l'inventaire d'un joueur

    Args:
        ID (int): ID discord du joueur

    Returns:
        string list : renvoie une liste des poissons pêchés par le joueur sous cette forme: nom_poisson : nbre_poisson OU ????? : ????? si le joueur n'a pas pêché le poisson
    """
    assert check_ID(ID), "Erreur de vérification de l'ID du joueur"
    
    #Connexion à la bdd
    conn = sqlite3.connect('./database/fishingbot.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT item_id,quantity FROM Inventaire WHERE joueur_id = {ID}")
    
    #On récupère l'inventaire
    inventory = cursor.fetchall()
    inventory = [list(el) for el in inventory]
    res = {}
    for tab in inventory:
        cursor.execute(f"SELECT Name FROM Items WHERE ID_item = ?",(tab[0],))
        name = cursor.fetchone()[0]
        res[name] = tab[1]
    return res
    


### FONCTION PAS UTILISEE ###


def create_inventory_embed(page,ID):
    """Fonction pas utilisée

    Args:
        page (_type_): _description_
        ID (_type_): _description_

    Returns:
        _type_: _description_
    """
    nbre_item_page = 11
    nbre_page = 10
    inventaire = get_inventory(ID)
    return_li = []
    for i in range(nbre_page):
        li = []
        for i in range(nbre_item_page):
            li.append(inventaire[i+nbre_item_page*page])
        return_li.append(li)

    return return_li


if __name__ == "__main__":
    ic(classement_top_10())
    ic(get_inventory(252508332995248128))