# Projet BDD Pokémon – Pokedex Manager

Ce projet a pour objectif de **comprendre l’interaction entre Python et les bases de données SQL** à travers la création d’une interface graphique de gestion de Pokémon.

L’application utilise :  
- **Python** pour la logique applicative  
- **Tkinter** pour l’interface utilisateur  
- **SQLite** pour la persistance des données  

---

## 📋 Table des matières
- [Description](#-description)  
- [Fonctionnalités](#-fonctionnalités)  
- [Structure de la base de données](#structure-de-la-base-de-donnees)
- [Installation et utilisation](#-installation-et-utilisation)  
- [Structure du projet](#-structure-du-projet)  

---

## 📝 Description
L’application permet de **consulter, rechercher et filtrer des Pokémon** dans une base de données (`pokedex.db`) via une interface graphique. Elle simplifie les interactions avec les données, évitant ainsi les commandes SQL manuelles, et permet de mieux comprendre la relation entre programmation et base de données.

---

## ✨ Fonctionnalités

### 🔹 Fonctionnalités principales
- **Recherche de Pokémon** : Sélection via une liste déroulante interactive.  
- **Affichage détaillé** : Statistiques complètes ($HP$, Attaque, Défense, Vitesse, etc.) et type du Pokémon sélectionné.  
- **Filtrage avancé** : Recherche dynamique par **nom** ou **type** dans le tableau d’affichage.  
- **Affichage d’images** : Visualisation des sprites pour illustrer les fiches.  

---

## Structure de la base de données

La base relationnelle comporte 4 tables principales :  

| Table | Champs principaux |
|-------|------------------|
| **POKEMON** | `idPokemon` (PK), `nom`, `hp`, `attaque`, `defense`, `vitesse`, `url_image`, `idType` (FK) |
| **TYPE** | `idType` (PK), `libelle_type` |
| **DRESSEUR** | `idDresseur` (PK), `nom` |
| **POKEMON_POSSEDER** | `idDresseur` (PK/FK), `idPokemon` (PK/FK), `commentaire` |

---

## 🚀 Installation et utilisation

### Prérequis
- **Python 3.x**  
- Bibliothèque **Tkinter** (inclus avec Python)  
- Bibliothèque **sqlite3** (inclus avec Python)  

### Lancement
1. Téléchargez ou clonez le projet.  
2. Vérifiez que le script, la base de données et le dossier `images/` sont dans le même répertoire.  
3. Exécutez le script principal :  
```bash
python programme.py
```
ou cliquer sur `lanceur.bat`

---

## 📂 Structure du Projet
Voici l'organisation exacte des fichiers du dépôt :

```plaintext
📁 Projet-bdd-Pokemon/
│
├── 🖥️ lanceur.bat           # Script Windows pour lancer l'application
├── 🗄️ pokedex.db            # Base de données SQLite
├── 📄 README.md             # Documentation (ce fichier)
│
└── 📁 application+base/     # Dossier contenant les ressources applicatives
    ├── 📄 programme.py      # Code source principal (Tkinter + SQL)
    └── 📁 images/           # Sprites des Pokémon (ex: Pikachu.gif) + logo
```

## 📜 Licence

Ce projet est sous licence [MIT](LICENSE). Consultez le fichier `LICENSE` pour plus de détails.








