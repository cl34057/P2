# Projet 2  Web-scrapping

## Mise en place du projet :

### 1. mettre en place un environnement python sur vscode


        - Installer Python sur le site: https://www.python.org/downloads/
        - cocher l'option "Add Python to PATH" pendant l'installation
        - Installer Visual Code sur le site: https://code.visualstudio.com/

        Configuration de l'environnement virtuel
        ----------------------------------------
        Sur terminal- Creer un environnement virtuel. Sur le terminal, On utilise la commande 
                        'python3 -m venv .chemin absolu/nom_env_virtuel'
                    Et l'activer par commande prompt:  
                        nom de l’environnement\Scripts\Activate.bat

                   ou par Power Shell: 
                        nom de l’environnement\Scripts\Activate.ps1   

        Sur Visual Code: - Faire CTRL+SHIFT+P
                         - Faire " Enter interpreter PATH
                         - et choisir l'environnement virtuel  
                   

Les Versions utilisées
----------------------
python --version: Python 3.12.0
pip --version   : pip 23.3.1
git --version   : git version 2.32.0

### 2. Les packages installés

          pip install -r requirements.txt

  

### 3. Execution des scripts
Pour executer les projets suivants

1- Extraction des Caractéristiques d'un seul produit d'une seule pages dans un fichier csv et  enregistrement du fichier image du produit
2- Extraction des Caractéristiques des produits d'une catégorie dans un fichier csv et enregistrement des fichiers images des produits de la catégorie
3- Extraction des Caractéristiques des produits de toutes les catégories du site dans un un fichier csv distinct pour chaque catégorie et enregistrement 
    des fichiers images des produits de chaque catégorie répertoriés

Il y aura donc 3 scripts. 

 tapez  la commande dans un repertoire
        git clone https://github.com/cl34057/P2.git

        qui enregistrera les 3 scripts dans le repertoire choisi.

Avant d'executer la commande, installez les bibliothèques utiles pour le projet, et les importer
tapez:  * pour requests------------>    - pip install requests           
        * pour BeautifulSoup------->    - pip install BeautifulSoup
        * pour pandas-------------->    - pip install pandas

        On peut importer directement 'os' et 're' par 'import os' et   'import re' 
        qui font partie de la bibliothèque standard de Python.

Cette commande permettra aux scripts de s'enregistrer sur votre repertoire.
On peut lancer maintenant les programmes, Ainsi vous pouvez executer chaque script:
        *        soit avec l'environnement python sur Vscode ,
        *        soit tapez sur votre terminal : python 'nom du fichier.py'