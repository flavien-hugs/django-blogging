# [django-blogging](https://github.com/flavien-hugs/django-blogging)
Site d'information de l'agence Brother's Consulting basé à Bouaké.

![django-blogging](https://github.com/flavien-hugs/django-blogging/blob/master/bcnews.png "screenshot description")

![[django-blogging](https://github.com/flavien-hugs/django-blogging/)](https://img.shields.io/badge/unsta-live--demo-orange.svg?style=flat)
![The MIT License](http://img.shields.io/badge/License-MIT-green.svg?style=flat)

*2019 - Flavien HUGS - CC-BY-NC-SA*
Cette création est mise à disposition sous un contrat Creative Commons.
Voir le fichier licence.txt ci-joint.

Ce blog a été développé et testé avec [python 3.6](http://www.python.org)
et [Django 2.2](http://www.djangoproject.com) version LTS.


### Fonctionalité et prise en main
La plateforme fournit les fonctionnalité comme :

    - un système de commentaire.
    - moteur de recherche interne
    - système de recommendations d'articles
    - la liste des articles récement plubié

Installation et exécution du projet
-----------------------------------

### 1. Installation

    - Commencez par installer le package 'python-3.x' pour votre OS.
    - Créez ensuite un environnement virtuel dans le répertoire de votre choix:
        python3.6 -m venv venv
    - Activez-le :
        source venv/bin/activate ou . venv/bin/activate
    - Enfin on lance le serveur web de développement:
        python manage.py runserver ou ./manage.py runserver
        puis naviguer jusqu'à <http://localhost:8000>


Notes pour le passage en production:
------------------------------------
Il faudra en plus déployer les fichiers statiques
    python manage.py collectstatic

Vous pouvez ensuite utiliser un serveur WSGI HTTP tel que Gunicorn
pour servir votre application Django, ainsi qu'un SGBDR évolué
comme PostgreSQL ou MariaDB.

Credits
------------

Code: [flavien-hugs](https://twitter.com/flavien_hugs)
