from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd


# On choisi les options pour notre instance
options = Options() 
options.add_argument('--no-sandbox')      
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
options.add_argument('--remote-debugging-port=9222')
options.add_argument("--window-size=1920,1080")
# On instencie notre webdriver
driver = webdriver.Remote("http://selenium:4444/wd/hub",options=options)


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


def boucle(site, path, path2, search_path, jeu):

    # On crée une data frame pour stocker les données
    jeu = {jeu}
    df = pd.DataFrame(jeu, columns=['Jeux'])
    df['prix'] = ""
    df['lien'] = ""

    # On ouvre le site dans notre driver
    driver.get(site)

    # Boucle

    df['prix'][0] = scraping(driver, path, df['Jeux'][0], path2, search_path)
    df['lien'][0] = driver.current_url
    print("Numéro {0} sur {1}".format(0+1, len(df)))
    return (df)


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


def scrapper(jeu):

    # attendre que chaque processus se termine
    instant = scrap_instant_gaming(jeu)
    eneba = scrap_eneba(jeu)
    cd_keys = scrap_cdkeys(jeu)
    goclecd = scrap_goclecd(jeu)
    gamersgate = scrap_gamersgate(jeu)

    # On fusionne ensuite chaque data frame
    df = pd.merge(instant.rename(columns={'prix': 'Instant_gaming', 'lien': 'Lien Instant_gaming'}), eneba.rename(
        columns={'prix': 'Eneba', 'lien': 'Lien Eneba'}), on='Jeux', how='outer')
    df = pd.merge(df, cd_keys.rename(
        columns={'prix': 'Cd_keys', 'lien': 'Lien Cd_keys'}), on='Jeux', how='outer')
    df = pd.merge(df, goclecd.rename(
        columns={'prix': 'Goclecd', 'lien': 'Lien Goclecd'}), on='Jeux', how='outer')
    df = pd.merge(df, gamersgate.rename(
        columns={'prix': 'Gamersgate', 'lien': 'Lien Gamersgate'}), on='Jeux', how='outer')

    df.to_csv('TAMERE.csv', encoding='utf-8', index=False)
    return df
