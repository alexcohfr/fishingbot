import sqlite3
import os

# Connexion à la base de données SQLite (elle sera créée si elle n'existe pas)
conn = sqlite3.connect("./fishingbot.db")
c = conn.cursor()

# Création de la table Players
c.execute('''
    CREATE TABLE IF NOT EXISTS Players (
        ID_joueur INTEGER PRIMARY KEY,
        Nbre_charge INTEGER,
        Tps_recharge TEXT
    )
''')

# Création de la table Items
c.execute('''
    CREATE TABLE IF NOT EXISTS Items (
        ID_item INTEGER PRIMARY KEY,
        Name TEXT,
        Extension TEXT,
        Rarete TEXT,
        Type INTEGER,
        Score INTEGER,
        Lien TEXT
    )
''')

# Création de la table Inventaire
c.execute('''
    CREATE TABLE IF NOT EXISTS Inventaire (
        joueur_id INTEGER,
        item_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (joueur_id) REFERENCES Players (ID_joueur),
        FOREIGN KEY (item_id) REFERENCES Items (ID_item)
    )
''')

# Création de la vue vue_score_joueur
c.execute("""
CREATE VIEW Score_joueur AS
SELECT p.ID_Joueur, SUM(i.Score * inv.quantity) AS Score_Total, SUM(inv.quantity) AS Nbre_tirage
FROM Players p
JOIN Inventaire inv ON p.ID_Joueur = inv.joueur_id
JOIN Items i ON inv.item_id = i.ID_item
GROUP BY p.ID_Joueur;
""")


# Sauvegarde des changements et fermeture de la connexion
conn.commit()
conn.close()