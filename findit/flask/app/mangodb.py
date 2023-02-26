import pandas as pd
import pymongo


# Permet de mettre à jour la base de données en ajoutant des dictionnaires

def mongo(collection):

    collection.update_many({}, {'$set': {'nouveau_prix_Instant_gaming': '0'}})
    collection.update_many({}, {'$set': {'nouveau_prix_Eneba': '0'}})
    collection.update_many({}, {'$set': {'nouveau_prix_Cd_keys': '0'}})
    collection.update_many({}, {'$set': {'nouveau_prix_Goclecd': '0'}})
    collection.update_many({}, {'$set': {'nouveau_prix_Gamersgate': '0'}})


# Permet d'actualiser notre base de données si le jeu existe déjà et d'ajouter le jeu si il n'existe pas


def recuperer(df, collection):
    new_prix = ['nouveau_prix_Instant_gaming', 'nouveau_prix_Eneba',
                'nouveau_prix_Cd_keys', 'nouveau_prix_Goclecd', 'nouveau_prix_Gamersgate']
    nom_site = ['Instant_gaming', 'Eneba', 'Cd_keys', 'Goclecd', 'Gamersgate']

    # Si jeu dans la db
    if (collection.count_documents({"Jeux": df['Jeux'][0]}) > 0):
        query = {'Jeux': df['Jeux'][0]}
        collection.find_one(query)

        for i in range(len(new_prix)):
            element_a_mettre_a_jour = {'Jeux': df['Jeux'][0]}
            new_val = {'$set': {new_prix[i]: df[nom_site[i]][0]}}
            collection.update_one(element_a_mettre_a_jour, new_val)

    # Si il n'y est pas
    else:
        collection.insert_one(df.to_dict(orient='records')[
                              0])  # Ajoute le jeu à la db
        # On update la db
        query = {'Jeux': df['Jeux'][0]}
        collection.find_one(query)

        for i in range(len(new_prix)):
            element_a_mettre_a_jour = {'Jeux': df['Jeux'][0]}
            new_val = {'$set': {new_prix[i]: df[nom_site[i]][0]}}
            collection.update_one(element_a_mettre_a_jour, new_val)
