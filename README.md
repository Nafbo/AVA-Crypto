# Bonnes pratiques de dév 

Pour permettre à d'autres personnes de s'approprier votre code, plusieurs choses sont nécessaires : 

<br/>

## Mise en place d'un environnement 

Installez, créez et activez votre virtualenv sur votre machine (Mac ou GitBash(compatible windows) / a voir pour Powershell Windows):

```bash
# Installation : 
pip install virtualenv

# Création :
virtualenv <ENV-NAME>

# Activation :
source venv/bin/activate

# Pour vérifier quel python est utilisé :
which python
```

Pour que python puisse trouver l'ensemble de vos packages et modules il est nécessaire d'exporter le chemin du projet dans le PYTHONPATH :

```bash
# Ce positionner à la racine du projet :
cd <RACINE-DU-PROJET>

# Export du répertoire courant dans PYTHONPATH :
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

<br/>

## Conteneurisation 

Création d'une image 

Bon tutoriel : https://digicactus.com/conteneuriser-vos-applications-python-part-1/#:~:text=Pour%20cela%2C%20nous%20utilisons%20avec,de%20configurer%20d'autres%20composants.&text=Ensuite%20nous%20cr%C3%A9ons%20un%20r%C3%A9pertoire,des%20autres%20fichiers%20de%20configuration.

Optimisation DockerFile : article de blog Alex (Faire attention à l'image de base utiliser)

<br/>

## CICD (continuous Integration / Continuous Deployment)

Utilisation de GitHub Actions : 
Automatisation des tests, de la construction de l'image, de son enregistrement sur un image registry, puis de son déploiement sur un hébergeur (comme AWS).

Mise en place d'une stratégie de mise à jour de l'application. Les différents types : https://www.techtarget.com/searchitoperations/answer/When-to-use-canary-vs-blue-green-vs-rolling-deployment#:~:text=The%20canary%20deployment%20pattern%20is,version%2C%20rather%20than%20certain%20servers.

<br/>

## Architecture 

```
project/
|-- src/
|   |-- app
|      |-- __init__.py
|      |-- feature1
|          |-- __init__.py
|          |-- module1.py
|          |-- module2.py
|       |-- feature2
|          |-- __init__.py
|          |-- module1.py
|
|   |-- app_test/
|       |-- __init__.py
|       |-- feature1
|           |-- __init__.py
|           |-- module1.py
|           |-- module2.py
|       |-- feature2
|           |-- __init__.py
|           |-- module1.py
|
|-- main.py
|-- .gitignore
|-- requirements.txt
|-- README.md
```

Note : Mettre un fichier "\_\_init\_\_.py" dans chaques dossiers pour le balisage et permettre à python de pouvoir faire les imports des functions des autres dossiers