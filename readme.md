# [django-blogging](https://github.com/flavien-hugs/django-blogging)
## un simple moteur de blog fait avec le framework Django
------------------------------------------

*2019 - Flavien HUGS - CC-BY-NC-SA*
Cette création est mise à disposition sous un contrat Creative Commons.
Voir le fichier licence.txt ci-joint.

Ce blog a été développé et testé avec [python 3.6](http://www.python.org)
et [Django 2.2](http://www.djangoproject.com) version LTS.

![django-blogging](https://github.com/flavien-hugs/django-blogging/blob/master/screenshot.png "screenshot description")

![[django-blogging](https://github.com/flavien-hugs/django-blogging/)](https://img.shields.io/badge/unsta-live--demo-orange.svg?style=flat)
![The MIT License](http://img.shields.io/badge/License-MIT-green.svg?style=flat)


### Fonctionalité et prise en main
La plateforme fournit les fonctionnalité comme :

    - un système de commentaire.
    - la liste des articles récement plubié

Installation et exécution du projet
-----------------------------------

### Dépendances
Les bibliothèques Python additionnelles nécessaires à son fonctionnement
sont [Python-Markdown](http://pythonhosted.org/Markdown/) et [Pillow](https://python-pillow.org/).
La liste complète des dépendances se trouve dans le fichier **requirements.txt**.


### 1. Installation

    - Commencez par installer le package 'python-3.x' pour votre OS.
    - Créez ensuite un environnement virtuel dans le répertoire de votre choix:
        -- python3.6 -m venv venv
    - Activez-le :
        -- source venv/bin/activate ou . venv/bin/activate
    - Installer ensuite les dépendances nécessaires :
        -- pip install -r blogging/requirements.txt
    - Enfin on lance le serveur web de développement:
        -- python manage.py runserver ou ./manage.py runserver
        -- puis naviguer jusqu'à <http://localhost:8000>


Comment contribuer
------------------

Faites un Fork et travaillez sur votre propre branche, soumettez des pull requests.

La principale branche de travail est [django-blogging/master](https://github.com/flavien-hugs/django-blogging/tree/master). La branche de production est [django-blogging/master](https://github.com/flavien-hugs/django-blogging/tree/prod).


Credits
------------

Code: [flavien-hugs](https://twitter.com/flavien_hugs)
