from flask import render_template, request
from . import app
import pandas as pd
from app.scrapping import *
from app.mangodb import *

# On importe la dataframe issue du groupe de jeux que nous avons scrappé
d_f = pd.read_csv('./static/Jeux.csv')

# On crée notre instance mango sur le port 27017
client = pymongo.MongoClient('mongo')
database = client['projet']
collection = database['jeu']
# On insére notre dataframe dans la base de données
documents = d_f.to_dict(orient='records')
collection.insert_many(documents)

# On appelle la fonction mongo afin de créer de nouveaux dictionnaires dans notre base de données
mongo(collection)

# Méthode qui va gérer le traitement de la recherche


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        jeu = request.form.get('jeu')  # On récupère le jeu demandé
        df = scrapper(jeu)  # On scrappe automatiquement le jeu recherché

        df_T = df
        df_T.set_index(['Jeux'], inplace=True)
        df_T = df_T.T

        # On met en forme la dataframe qu'on a obtenu en scrappant
        df = pd.DataFrame(df.iloc[0,]).T
        df = df.reset_index()
        df = df.rename(columns={'index': 'Jeux'})
        df['nouveau_prix_Instant_gaming'] = 0
        df['nouveau_prix_Eneba'] = 0
        df['nouveau_prix_Cd_keys'] = 0
        df['nouveau_prix_Goclecd'] = 0
        df['nouveau_prix_Gamersgate'] = 0
        df = df.applymap(str)

        # On appelle la focntion recuperer qui permet d'actualiser notre base de données si le jeu existe déjà et d'ajouter le jeu si il n'existe pas
        recuperer(df, collection)
        # On récupére ensuite les informations dans notre base de données pour gèrer l'affichage
        query = {'Jeux': jeu}
        result = collection.find_one(query)

        # On transforme le résultat en dataframe qu'on va modifier pour la rendre intelligible
        values = list(result.values())
        val = pd.DataFrame(list(result.values())).tail(5)
        values = values[2:12]
        data_clean = pd.DataFrame()
        data_clean["Site"] = ['Instant_gaming',
                              'Eneba', 'Cd_keys', 'Goclecd', 'Gamersgate']
        data_clean["prix"] = val.reset_index(drop=True)
        data_clean["Liens"] = [i for idx,
                               i in enumerate(values) if idx % 2 != 0]

        # On va tout transformer en float afin de pouvoir comparer les prix, et ceci en faisant attention aux potentielles valeurs manquantes
        data_clean["prix"] = data_clean["prix"].apply(lambda x: str(x).replace(
            ",", ".").replace("€", "").replace(" ", ""))

        data_clean["prix"] = data_clean["prix"].apply(
            lambda x: x.replace("0", "Pas trouvé") if (x == "0") else (x))

        data_clean["prix"] = pd.to_numeric(
            data_clean["prix"], errors='coerce').astype(float)

        nouveau = [i for idx, i in enumerate(values) if idx % 2 == 0]
        diff = pd.DataFrame(nouveau)
        diff['prix'] = data_clean['prix']

        # On va ensuite comparer le prix scraper à celui de notre bdd pour voir si il a évolué
        diff = diff.rename(columns={0: 'new'})
        diff["new"] = diff["new"].apply(lambda x: str(x).replace(
            ",", ".").replace("€", "").replace(" ", ""))

        diff["new"] = diff["new"].apply(
            lambda x: x.replace("0", "Pas trouvé") if (x == "0") else (x))

        diff["new"] = pd.to_numeric(
            diff["new"], errors='coerce').astype(float)

        diff['valeur_min'] = diff.apply(
            lambda row: 'Baisse' if row['new'] < row['prix'] else ('Stable' if row['new'] == row['prix'] else ('Augmentation' if row['new'] > row['prix'] else 'Pas de comparaison')), axis=1)

        data_clean['valeur_min'] = diff['valeur_min']
        data_clean = data_clean.sort_values(by='prix').reset_index(
            drop=True)  # On trie les sites en focntion des prix

        data_clean = data_clean.rename(columns={'valeur_min': 'Comparaison'})

        return render_template("search.html", jeu=jeu, df=data_clean.to_html(classes='Jeux'))

    return render_template("index.html")


# Permet de gèrer l'affichage de la base de données
@app.route("/tab/")
def tab():

    data = list(collection.find())
    df = pd.DataFrame(data)

    df['Jeux'] = df['Jeux'].apply(lambda x: str(x))
    df = df[df['Jeux'] != 'nan'].drop_duplicates(
        subset=['Jeux']).reset_index(drop=True)
    df = df[['Jeux', 'Instant_gaming', 'Eneba',
             'Cd_keys', 'Goclecd', 'Gamersgate']]

    df.set_index(['Jeux'], inplace=True)
    df.index.name = None
    return render_template("tab.html",
                           tables=df.to_html(classes='Jeux'))
