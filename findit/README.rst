#Objectif de notre projet

Notre projet est un comparateur de prix de jeux vidéo. En effet, il y a un certain nombre de sites qui vendent des clés d'activation de jeux, 
et il est parfois difficile de s'y retrouver. Nous avons donc décidé de choisir 5 sites populaires de vente de clés de jeux afin d'en extraire 
le prix pour un jeu donné. Nous allons donc effectuer le scraping de ces 5 sites : Instant Gaming, Eneba, CD Keys, Goclecd et GamersGate à chaque recherche


#Configuration requise

- Docker Desktop 4.14.1.0


#Installation

- Cloner le fichier à partir de git
- Lancer Docker Desktop 
- Ouvrir le dossier findit dans VSCode
- Ouvrir un terminal dans VSCode et verifier que l'on est bien dans le dossier findit
- Exécuter dans le terminal : docker compose up
- Une fois que l'application flask est lancée, se connecter dans un navigateur avec la 1ere adresse indiquée (normalement: http://127.0.0.1:5000/ ou http://localhost:5000/)


#Utilisation


Il y a dans le github un fichier python (scrap_liste.py) et un dossier (findit). Le fichier python a été utilisé pour scrapper une liste de jeux. 
Le dossier correspond à la partie application.

Dans un premier temps, nous partons d'une liste de jeux que nous scrapons sur un site qui référence les meilleures ventes. 
L'idée étant d'avoir une base solide pour notre base de données. Par la suite, l'utilisateur pourra chercher n'importe quel jeu, et il 
sera scrapé en temps réel sur les 5 sites afin d'obtenir un lien et un prix. Ces informations seront stockées dans une base de données MongoDB 
qui agira de la sorte : si le jeu existe déjà, le prix sera mis à jour à condition que l'orthographe soit exacte, sinon le jeu sera ajouté à la base.

Nous utilisons ensuite une application Flask afin de gérer l'affichage de toutes ces informations. 
À partir de cette application, l'utilisateur pourra accéder à la base de données ainsi qu'effectuer une recherche. 
Une fois la recherche effectuée, l'utilisateur pourra voir le prix actuel du jeu qu'il a cherché sur les différents sites, le lien du site, 
et finalement si le prix a baissé, augmenté ou s'il est resté le même. À noter que si l'utilisateur cherche un jeu qui n'est pas dans la base de données,
 la comparaison du prix indiquera que le prix est stable.


#Copyright

Nous déclarons sur l'honneur que le code fourni a été produit par nous-mêmes. Nous avons cependant recouru à la documentation de certaines fonctions

#Conclusion

Notre projet avait pour but de créer une application simple d'usage permettant un comparatif en temps réel de différents sites de vente de jeux en ligne.
Notre application focntionne bien et permet un gain de temps certain. Dans le futur il est possible d'imaginer l'adjonction de nouvelles 
focntionnalités telles que un système d'agrégation de notations (provenant par exemple de la presse spécialisée), et pourquoi pas des propositions
de jeux en fonction des précédentes recherches de l'utilisateur.



