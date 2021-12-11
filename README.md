# Projet HearthStone

~Under construction~


### Origine
Ceci est un projet expérimental, fourre-tout, qui me permet d'expérimenter de nouveaux outils, idées afin de mieux les intégrer. C'est la pagaille, le projet est dispersif et son développeur en apprentissage.


L'objectif initial a été de récréer, en Python, un environnement similaire à celui du jeu HearthStone - Battlegrounds.
Dans l'ensemble, le résultat est satisfaisant, néanmoins, un aspect important n'est pas respecté : les évènements s'exécutent dans leur ordre d'arrivée au lieu de se superposer sous forme de pile, certains évènements influencent les suivants alors qu'ils devraient s'éxécuter 'en parallèle'.

L'idée n'est pas connaître la probabilité de gagner d'une composition face à une autre composition mais de construire différents scénarios et d'en récupérer les résultats. De ces chiffres, il serait possible, au moins partiellement, de fournir une côte pour chaque serviteur, héros, faire des graphiques, analyser tout cela dans tous les sens imaginable, recommencer.
Il peut permettre également d'évaluer leur évolution au fil des mises à jours. De découvrir, d'analyser et de quantifier, l'impact des différentes stratégies, notamment en début de partie. Le chemin est encore long.
Plutôt que de côter un serviteur en analysant 20M de parties en ligne, l'idée est de pouvoir obtenir un résultat en analysant les différentes possibilités. Le résultat sera différent, pas forcément meilleur, mais ce résultat pourra compléter les résultats déjà existants. Un avantage serait également de pouvoir d'obtenir des résultats exploitables très rapidement après une mise à jour. Plutôt qu'attendre 8 semaines pour avoir les 20M de parties.
Plusieurs approches sont possibles, pour le moment une approche par stratégie du joueur est privilégiée.
L'approche par stratégie par carte, est pour le moment mise de côté.


# Création des minions, héros, enchantements & tout le reste
Tout n'est pas encore implanté. Certains pouvoirs sont relativement pernicieux, le fonctionnement de certaines cartes est obscur. Par exemple, le pouvoir d'Eudora, comment est déterminé la carte récupérée ? Depuis le pool, ce qui implique que la probabilité d'obtenir un T1 est deux fois supérieur à celui d'un T6 ? Ou bien toutes les cartes sont équi-probables ? Les 3 cartes nécessaires pour former le triple sont-elles retirées du pool ? Autant de détails qui influencent les résultats et dont la réponse m'est inconnue.


# API externe
Via la commande :
```
    python3 main.py -uDB
```
Il est possible de mettre à jour le fichier db/hearthstone.json avec la dernière version des cartes.
La requête est effectuée sur https://api.hearthstonejson.com/v1/latest/frFR/cards.json.
Toutes les cartes sont sauvegardées.

Via la commande :
```
    python3 main.py -uBG
```
Le fichier `battlegrounds.json` est rempli avec les cartes du set BATTLEGROUNDS.
Ce dernier, couplé avec `battlegrounds_extended.json` produit `HStat.json`.
C'est ce dernier qui est utilisé pour remplir la base de données utilisée par l'API du projet, grâce à 
```
    ./manage.py uDB
```
Une commande regroupant les trois est en cours de réflexion.

Note : Une limite pointe son nez, car cette commande annule tous les changements sur la base de données effectués via l'API.


# Arène
L'arène est un mode gourmand où bon nombre de serviteurs combattent encore et encore.
Les résultats des combats permettent de déterminer la pertinence des différents choix.
Différents résultats sur les serviteurs de taverne 1 sont présents dans le fichier `arene.json`.
Les résultats sont actuellement extrêmement généraux : les héros n'utilisent pas leur pouvoir et aucun type de serviteurs n'est banni. Il est tout à fait possible de mettre en place ces deux contraintes, tout est prêt pour cela, ce qui manque c'est la puissance de calcul ou le manque d'optimisation de la part du concepteur. Ce dernier s'explique en ces termes : "Chaque chose en son temps.".

Le fichier `arene.json` n'étant pas d'une clareté limpide au premier regard, voici un exemple travaillé (après moultes rebondissements), il s'agit d'un résultat de l'analyse "base_T1_to_T3_extended", retro 6, pour la version 20.8.

```
   "2021-11-29 19:50:32.268500": { # date
    "method": "base_T1_to_T3_extended", # nom de la méthode employée : cumul de l'impact des cartes T1 du tour 1 jusqu'au tour 3, la stratégie employée est celle par défaut : levelup au tour2
    "types_ban": [], # types bannis : aucun
    "retro": 6, # nombre d'analyse rétro-active, chacune d'entre elles utilisent les résultats de la rétro précédente pour déterminer les probabilités d'apparition de chaque carte
    "p1": "BaconPHhero", # nom du héros, ici le héros de base, sans pouvoir
    "p2": "BaconPHhero",
    "espérance": -6.1508, # espérance des résultats
    "rating": {
     "976_Chasse-marée murloc": -2.57, # côte, déterminée en fonction des résultats obtenus
     "64038_Élémenplus": -5.34,
     "63614_Acolyte de C’Thun": -5.42,
     "61061_Forban": -6.02,
     "70147_Bronze-couenne": -6.17,
     "72387_Robo-toutou": -6.19,
     "64042_Anomalie actualisante": -6.46,
     "70143_Géomancien de Tranchebauge": -6.66,
     "41245_Chasseur rochecave": -6.77,
     "40426_Chat de gouttière": -6.82,
     "74910_Diablotin dégoûtant": -7.28,
     "74659_Chromaile évolutive": -7.78,
     "59968_Dragonnet rouge": -8.46,
     "61055_Mousse du pont": -9.19,
     "53445_Micromomie": -9.69,
     "59670_Tisse-colère": -9.89,
     "1281_Hyène charognarde": -10.4,
     "72059_Entourloupeur impétueux": -10.94
    }
```
Le résultat n'est pas parfait pour autant. Par exemple, l'avantage de l'Anomalie actualisante peut également être impactante tour 4 ou 5 selon le moment où le roll gratuit est utilisé (cela dit, un patch a été ajouté pour simuler cet impact cela mais cela reste approximatif). Le Tisse-colère est sous-côté car aucun type n'étant banni, les démons sont mécaniquement dilués dans le pool etc


# API
Dernier volet, une API REST (via DjangoRestFramework) a été intégrée au projet afin de pouvoir accéder aux informations relatives à chaque carte.

Elle est accessible via /api/
Actuellement 4 endpoints sont disponibles pour le tout public :

GET `/cards/<dbfId>/` (accès à toutes les cartes)
GET `/races/<RACE>/` (accès aux cartes de la race indiquée)
GET `/rarities/` (accès aux différentes raretés) (expérimental, ne sera pas conservé)
GET `/repops/<dbfId>/` (accès aux cartes possédant un repop) (expérimental mais potentiellement utile)

Une partie admin est également présente :
GET/PUT/PATCH/DELETE `admin/races/<RACE>/` (accès aux cartes de la race indiquée)
GET/PUT/PATCH/DELETE `admin/rarities/` (accès aux différentes raretés)

Les informations des cartes sont d'abord issues de la version officielle puis complétées en fonction des besoins du projet.



# TODO
