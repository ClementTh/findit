from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time
import multiprocessing

# On choisi les options pour notre instance
options = Options()
# Permet de ne pas afficher tous les messages dans la console
options.add_argument("log-level=3")
# On dimensionne la page afin que les éléments soient bien trouvables
options.add_argument("--window-size=1920,1080")
options.headless = True  # vire l'affichage de la page
# On instencie notre webdriver
driver = webdriver.Chrome(options=options)


# On scrappe une liste de jeux à tester
def scrap_liste():
    driver.get(
        'https://www.showmetech.com.br/fr/meilleurs-jeux-informatiques-metacritic/')
    sleep(1)
    liste_jeux = driver.find_element(
        By.XPATH, '/html/body/div[3]/div/main/div[1]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[1]/ol/li[1]').text
    liste_jeux = liste_jeux.split("\n")
    return liste_jeux[1:26]

# Fonction permettant d'obtenir une liste de base de jeux à scrapper


def get_site(url):
    tables = pd.read_html(url)
    df = tables[0]["Characteristic"]
    df = df.str.replace(
        r"\(.*\)", "", regex=True)
    df = df.str.replace(
        r"\(.*\)", "", regex=True).str.replace("[*^]", "", regex=True)
    df = df.to_frame()
    df = df.rename(columns={'Characteristic': 'Jeux'})
    return df


# Fonction qui va scrapper le prix d'un jeu sur un site prècis

def scraping(driver, path, mot, path2, search_path):

    # On va tester si la search bar est trouvable. Si non on refresh la page au bout de 2s.
    # C'est particulièrement utile pour certains sites qui se bloquent après trop de requêtes
    try:
        wait = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, search_path)))
    except:
        driver.refresh()

    # On va ensuite rechercher le jeu grâce à la barre de recherche
    driver.find_element(By.XPATH, search_path).clear()
    search_field = driver.find_element(By.XPATH, search_path)
    search_field.send_keys(mot)
    search_field.submit()

    # Une fois la recherche effectuée on va vérifier la page pour savoir si le jeu existe ou pas
    # On va tester 2 cases afin de palier le fait que des fois le premier jeu affiché n'a pas de prix
    # Si rien n'est trouvé on retourne "Pas trouvé"
    try:

        wait = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, path)))
        # driver.find_element(By.XPATH, path)
    except:
        try:
            wait = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, path)))
            # driver.find_element(By.XPATH, path2)
        except:
            return "Pas trouvé"
        return driver.find_element(By.XPATH, path2).text
    prix = driver.find_element(By.XPATH, path).text
    return prix

# Cette fonction permet de boucler sur tous les jeux sur un même site


def boucle(site, path, path2, search_path, liste_jeux):

    start_time = time.time()
    # On crée une data frame pour stocker les données
    df = pd.DataFrame(liste_jeux, columns=['Jeux'])
    df['prix'] = ""
    df['lien'] = ""

    # On ouvre le site dans notre driver
    driver.get(site)

    # Boucle
    for i in range(len(df)):
        df['prix'][i] = scraping(
            driver, path, df['Jeux'][i], path2, search_path)
        df['lien'][i] = driver.current_url
        print("Numéro {0} sur {1}".format(i+1, len(df)))
    return (df, time.time() - start_time)


# Ci-après, chaque fonction est dédiée à un site, elle contient les constantes de ces sites ainsi que l'appel de la fonction boucle

def scrap_instant_gaming(liste_jeux):

    # Constantes spécifiques à chaque site (Archéologie de site web)
    site = "https://www.instant-gaming.com/fr/"
    path = '/html/body/div[4]/div/div/div[1]/div/div[2]'
    path2 = '/html/body/div[4]/div/div/div[2]/div/div[2]'
    search_path = '/html/body/header/div[1]/div[2]/form/div/input'

    return (boucle(site, path, path2, search_path, liste_jeux))


# Pareil qu'avant
def scrap_eneba(liste_jeux):

    site = 'https://www.eneba.com/fr/store/all?page=1&regions[]=emea&regions[]=europe&regions[]=france&regions[]=global&sortBy=RELEVANCE_DESC&types[]=game'
    path = '/html/body/div[1]/main/div/div/section/div[2]/div[2]/div[1]/div/div[3]/a/div[1]/span[2]/span'
    path2 = '/html/body/div[1]/main/div/div/section/div[2]/div[2]/div[2]/div/div[3]/a/div[1]/span[2]/span'
    search_path = '/html/body/div[1]/main/div/div/aside/form/div[1]/div/input'

    return (boucle(site, path, path2, search_path, liste_jeux))


def scrap_cdkeys(liste_jeux):

    site = 'https://www.cdkeys.com/fr_fr/'
    path = '/html/body/div[2]/div[1]/div/div/div[3]/div/div/div[2]/div/div[3]/div/div/ol/li[1]/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/span[1]'
    path2 = '/html/body/div[2]/div[1]/div/div/div[3]/div/div/div[2]/div/div[3]/div/div/ol/li[3]/div/div/div/div[2]/div/div[1]/div/div[2]/div/div/span[1]'
    search_path = '/html/body/div[2]/header/div[2]/div/div[2]/div/div[2]/form/div/div[1]/input'

    return (boucle(site, path, path2, search_path, liste_jeux))


def scrap_gamersgate(liste_jeux):
    site = 'https://www.gamersgate.com/'
    path = '/html/body/main/section/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div[2]/span'
    path2 = '/html/body/main/section/div/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div[2]/span'
    search_path = '/html/body/main/nav[1]/section/div/form/div/input[1]'

    return (boucle(site, path, path2, search_path, liste_jeux))


def scrap_goclecd(liste_jeux):
    site = 'https://www.goclecd.fr/'
    path = '/html/body/div[3]/div/div[2]/div/ul/li[1]/a/div[4]'
    path2 = '/html/body/div[3]/div/div[2]/div/ul/li[2]/a/div[4]'
    search_path = '/html/body/header/div[2]/form/input'

    return (boucle(site, path, path2, search_path, liste_jeux))


if __name__ == "__main__":

    start_time = time.time()

    url1 = "https://www.statista.com/statistics/1285658/top-ranked-video-games-sales-annual/"
    url2 = "https://www.statista.com/statistics/274072/most-popular-games-in-the-united-kingdom-uk-by-unit-sales/"

    site = [get_site(url1), get_site(url2)]
    jeux = pd.concat(site, ignore_index=True)

    # Afin de grandement réduire le temps d'éxécution on va parraléliser les processus
    with multiprocessing.Pool(processes=5) as pool:
        # démarrer chaque fonction dans un processus séparé
        result1 = pool.apply_async(scrap_instant_gaming, args=(jeux,))
        result2 = pool.apply_async(scrap_eneba, args=(jeux,))
        result3 = pool.apply_async(scrap_cdkeys, args=(jeux,))
        result4 = pool.apply_async(scrap_goclecd, args=(jeux,))
        result5 = pool.apply_async(scrap_gamersgate, args=(jeux,))
        # attendre que chaque processus se termine
        instant = result1.get()
        eneba = result2.get()
        cd_keys = result3.get()
        goclecd = result4.get()
        gamersgate = result5.get()

    # On fusionne ensuite chaque data frame
    df = pd.merge(instant[0].rename(columns={'prix': 'Instant_gaming', 'lien': 'Lien Instant_gaming'}), eneba[0].rename(
        columns={'prix': 'Eneba', 'lien': 'Lien Eneba'}), on='Jeux', how='outer')
    df = pd.merge(df, cd_keys[0].rename(
        columns={'prix': 'Cd_keys', 'lien': 'Lien Cd_keys'}), on='Jeux', how='outer')
    df = pd.merge(df, goclecd[0].rename(
        columns={'prix': 'Goclecd', 'lien': 'Lien Goclecd'}), on='Jeux', how='outer')
    df = pd.merge(df, gamersgate[0].rename(
        columns={'prix': 'Gamersgate', 'lien': 'Lien Gamersgate'}), on='Jeux', how='outer')
    # On crée un fichier csv qui sera utile pour notre base de données
    df.to_csv('Jeux_test.csv', encoding='utf-8', index=False)
    print(df)
    print("Exécuté en {0}s".format(time.time() - start_time))
