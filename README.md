# Projet 2  Web-scrapping

## Mise en place du projet :

### 1. mettre en place un environnement python sur vscode


        - Installer Python sur le site: https://www.python.org/downloads/
        - cocher l'option "Add Python to PATH" pendant l'installation
        - Installer Visual Code sur le site: https://code.visualstudio.com/
        - Installer l'extension Python
        - Creer un environnement virtuel. Sur le terminal, On utilise la commande 
                                'python3 -m venv /chemin absolu/nom_env_virtuel'
           L'activer
                   par commande prompt:   nom de l’environnement\Scripts\Activate.bat
                   ou par Power Shell:    nom de l’environnement\Scripts\Activate.ps1     
                   

Les Versions utilisées
----------------------
python --version: Python 3.12.0
pip --version   : pip 23.3.1

### 2. Les packages installés

          pip freeze > requirements.txt

  

### 3. Execution des scripts
Pour executer les projets suivants

1- Extraction des Caractéristiques d'un seul produit d'une seule pages dans un fichier csv et  enregistrement du fichier image du produit
2- Extraction des Caractéristiques des produits d'une catégorie dans un fichier csv et enregistrement des fichiers images des produits de la catégorie
3- Extraction des Caractéristiques des produits de toutes les catégories du site dans un un fichier csv distinct pour chaque catégorie et enregistrement 
    des fichiers images des produits de chaque catégorie répertoriés

Il y aura donc 3 scripts. 

Aller dans le repertoire de votre choix, puis tapez  la commande

        git clone https://github.com/cl34057/P2.git

Cette commande permettra aux scripts de s'enregistrer sur votre repertoire.
Ainsi vous pouvez executer chaque script,
        *        avec l'environnement python sur Vscode ,
        *        ou tapez sur votre terminal : python 'nom du fichier.py'
