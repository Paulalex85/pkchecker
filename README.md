Cet outil a pour but de passer toutes les pages web d'un site internet dans le but de savoir si il contient le script de Piwik. Cela permet de savoir si il est bien intégré ou non. Pour cela il va simplement regarder dans toutes les pages web du site vérifier si dans les scripts de la page il y a la présence de piwik.php.
Ce script a pour but d'être installé en local. 
Il est réalisé en python et la bibliothèque Scrapy.

Procédure d'installation :
 * Installation python
 * Installation scrapy
    
Pour Python, dans le terminal, lancer la commande suivante :
`sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev`
Elle va installer tout les composants de python.

Maintenant pour installer Scrapy :
`sudo pip install scrapy`
On a maintenant Python et Scrapy d'installé !

Pour executer le programme il faut réaliser la commande suivante lorsque on est dans le répertoire contenant le programme.
`python ./pkchecker.py http://monsite.com`

Il va ainsi s'executer et générer un csv dans le meme répertoire contenant les résultats
