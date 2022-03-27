# Bonnes pratiques de dév 

Pour permettre à d'autres personnes de s'approprier votre code, plusieurs choses sont nécessaires : 

<br/>

## Mise en place d'un environnement 

Installez, créez et activez votre virtualenv sur votre machine (Mac ou GitBash(compatible windows) / a voir pour Powershell Windows):

```python
# Installation : 
pip install virtualenv

# Création :
virtualenv <ENV-NAME>

# Activation :
source venv/bin/activate

# Pour vérifier quelle python est utilisé :
which python
```

<br/>

## Conteneurisation 

Création d'une image 

Bon tutoriel : https://digicactus.com/conteneuriser-vos-applications-python-part-1/#:~:text=Pour%20cela%2C%20nous%20utilisons%20avec,de%20configurer%20d'autres%20composants.&text=Ensuite%20nous%20cr%C3%A9ons%20un%20r%C3%A9pertoire,des%20autres%20fichiers%20de%20configuration.

Optimisation DockerFile : article de blog Alex (Faire attention à l'image de base utiliser)

<br/>

## CICD (continuous Integration / Continuous Deployment)

Utilisation de GitHub Actions : 
Automatisation des test, de la construction de l'image, de son enregistrement sur un image registry, puis de son déploiment sur un hébergeur (comme AWS).

Mise en place d'une stratégie de mise à jour de l'application. Les différents type : https://www.techtarget.com/searchitoperations/answer/When-to-use-canary-vs-blue-green-vs-rolling-deployment#:~:text=The%20canary%20deployment%20pattern%20is,version%2C%20rather%20than%20certain%20servers.

<br/>

## Architecture 

```
project/
|-- bin/
|   |-- feature1
|       |-- __init__.py
|       |-- module1
|       |-- module2
|   |-- feature2
|       |-- __init__.py
|       |-- module1
|
|-- bin_test/
|   |-- feature1
|       |-- __init__.py
|       |-- module1
|       |-- module2
|   |-- feature2
|       |-- __init__.py
|       |-- module1
|
|-- project/
|   |-- __init__.py
|   |-- main.py
|
|-- project_test/
|   |-- __init__.py
|   |-- test_main.py
|
|-- setup.py
|-- requirements.txt
|-- README
```

Note : Mettre un fichier init dans chaque dossier pour le balisage et permettre à python de pouvoir faire les import des functions des autres dossiers