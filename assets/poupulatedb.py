# On va utiliser les .csv pour peupler la base de données


import csv
import sqlite3
import pandas as pd

# On se connecte à la base de données
conn = sqlite3.connect('../database/fishingbot.db')
c = conn.cursor()

# Les tables sont déjà crées selon le schéma Players, Items, Inventaire

#On va peupler la table Items avec les données des fichiers liste_membres.csv etc...
def populate_items(fichier_csv):

    # On ouvre le fichier liste_membres.csv et on le rentre dans la table Items
    with open(fichier_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        extension = fichier_csv.split('.csv')[0]

        for row in reader:
            # On passe la première ligne
            if row[0] == "nom_poisson":
                continue
            else:
                nom = row[0]
                rarete = row[1]
                lien = row[2]
                type_poisson = row[3]

                if rarete == "Commun":
                    score = 10
                elif rarete == "Peu Commun":
                    score = 50
                elif rarete == "Rare":
                    score = 150
                elif rarete == "Très Rare":
                    score = 500
                elif rarete == "Inestimable":
                    score = 2000
                elif rarete == "Légendaire":
                    score = 10000
                elif rarete == "Mythique":
                    score = 50000
                elif rarete == "Miraculeux":
                    score = 250000
                elif rarete == "Malus":
                    score = -100
                else:
                    raise ValueError("Erreur dans la rareté",rarete)

            # On vérifie que le poisson n'est pas déjà dans la base de données à l'aide de df
            c.execute("SELECT * FROM Items WHERE Name=?", (nom,))
            data = c.fetchone()
            if data is None:
                c.execute("""
                INSERT INTO Items (Name, Extension, Rarete, Type, Score, Lien)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (nom, extension, rarete, type_poisson, score, lien))
                print(f"{nom} a été ajouté à la base de données")
                conn.commit()
            else:
                print(f"{nom} est déjà dans la base de données")



if __name__ == "__main__":
    populate_items("liste_membres.csv")
    populate_items("animal_crossing.csv")
    populate_items("minecraft.csv")
    populate_items("pokemon.csv")
