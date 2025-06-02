import requests

# Version patch LoL à jour
version = "13.10.1"
url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/fr_FR/champion.json"

response = requests.get(url)
data = response.json()
champions = data['data']

# Types possibles (à adapter en fonction des données)
types_list = ['Tank', 'Mage', 'Combattant', 'Assassin', 'Tireur', 'Support']
# Rôles possibles
roles_list = ['Toplane', 'Jungle', 'Midlane', 'ADC/Botlane', 'Support']

# On crée des dictionnaires id pour types et rôles
types_dict = {t: i+1 for i, t in enumerate(types_list)}
roles_dict = {r: i+1 for i, r in enumerate(roles_list)}

# Fonction pour échapper les apostrophes dans SQL
def sql_escape(s):
    return s.replace("'", "''")

with open("create_db.sql", "w", encoding="utf-8") as f:

    # Création tables Types, Roles, Champions, Champion_Roles
    f.write("""
CREATE TABLE IF NOT EXISTS Types (
    idType SERIAL PRIMARY KEY,
    nomType VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Roles (
    idRole SERIAL PRIMARY KEY,
    nomRole VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Champions (
    idChampion SERIAL PRIMARY KEY,
    nomChampion VARCHAR(100) NOT NULL UNIQUE,
    title VARCHAR(150),
    attack INT,
    defense INT,
    magic INT,
    difficulty INT,
    idType INT REFERENCES Types(idType)
);

CREATE TABLE IF NOT EXISTS Champion_Roles (
    idChampion INT REFERENCES Champions(idChampion),
    idRole INT REFERENCES Roles(idRole),
    PRIMARY KEY (idChampion, idRole)
);

-- Insertion des Types
""")

    # Insert Types
    for t, idt in types_dict.items():
        f.write(f"INSERT INTO Types (idType, nomType) VALUES ({idt}, '{t}');\n")

    f.write("\n-- Insertion des Roles\n")

    # Insert Roles
    for r, idr in roles_dict.items():
        f.write(f"INSERT INTO Roles (idRole, nomRole) VALUES ({idr}, '{r}');\n")

    f.write("\n-- Insertion des Champions\n")

    # On va stocker idChampions pour insertions roles
    champion_id = 1

    # Certaines infos (type, rôle) ne sont pas directement dans la data Dragon, on déduit par tags (tags = list dans le json)
    # Exemples de tags : Fighter, Mage, Assassin, Tank, Support, Marksman

    for champ_key, champ in champions.items():
        nom = sql_escape(champ['name'])
        title = sql_escape(champ['title'])
        stats = champ['info']
        attack = stats.get('attack', 0)
        defense = stats.get('defense', 0)
        magic = stats.get('magic', 0)
        difficulty = stats.get('difficulty', 0)
        tags = champ['tags']  # ex: ['Fighter', 'Tank']

        # Choix du type : on prend le premier tag qui est dans types_list sinon NULL
        champ_type = None
        for t in tags:
            if t in types_list:
                champ_type = types_dict[t]
                break

        # Insert champion avec idType
        type_sql = str(champ_type) if champ_type else "NULL"
        f.write(f"INSERT INTO Champions (idChampion, nomChampion, title, attack, defense, magic, difficulty, idType) VALUES ({champion_id}, '{nom}', '{title}', {attack}, {defense}, {magic}, {difficulty}, {type_sql});\n")


        # Insertion des rôles : on va utiliser aussi les tags mais attribuer par défaut des rôles logiques
        # Un mapping simple basé sur tags, à affiner selon besoin
        champ_roles = []

        # Correspondance tag => rôles possibles (simplifié)
        tag_to_roles = {
            'Fighter': ['Top', 'Jungle', 'Mid'],
            'Mage': ['Mid', 'Support'],
            'Assassin': ['Mid', 'Jungle', 'Top'],
            'Tank': ['Top', 'Jungle', 'Support'],
            'Marksman': ['ADC', 'Top'],
            'Support': ['Support']
        }

        for t in tags:
            if t in tag_to_roles:
                for role in tag_to_roles[t]:
                    if role in roles_dict and role not in champ_roles:
                        champ_roles.append(role)

        # Pour s'assurer qu'il y a au moins un rôle (sinon Support par défaut)
        if not champ_roles:
            champ_roles.append('Support')

        # Insert dans Champion_Roles
        for role in champ_roles:
            f.write(f"INSERT INTO Champion_Roles (idChampion, idRole) VALUES ({champion_id}, {roles_dict[role]});\n")

        champion_id += 1

print("Fichier 'create_db.sql' généré, prêt à être importé !")
