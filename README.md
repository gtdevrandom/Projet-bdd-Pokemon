# 🔴 Projet BDD Pokémon - Pokedex Manager

Ce projet a pour objectif de comprendre le lien entre la **programmation (Python)** et les **bases de données (SQL)** à travers la création d'une interface graphique de gestion de Pokémon.

L'application repose sur le langage **Python**, la bibliothèque **Tkinter** pour l'interface utilisateur, et **SQLite** pour la persistance des données.

---

## 📋 Table des Matières
* [Description](#-description)
* [Fonctionnalités](#-fonctionnalités)
* [Structure de la Base de Données](#-structure-de-la-base-de-données)
* [Installation et Utilisation](#-installation-et-utilisation)
* [Structure du Projet](#-structure-du-projet)

---

## 📝 Description
L'application permet de consulter, rechercher et filtrer des informations contenues dans une base de données de Pokémon (`pokedex.db`). Elle offre une interface visuelle pour interagir avec les tables sans passer par des lignes de commande SQL brutes, facilitant ainsi la compréhension des interactions logicielle/données.

---

## ✨ Fonctionnalités

### 🔹 Fonctionnalités Principales (Socle commun)
* **Recherche de Pokémon** : Sélection d'un Pokémon via une liste déroulante interactive.
* **Affichage Détaillé** : Consultation des statistiques complètes ($HP$, $Attaque$, $Défense$, $Vitesse$, etc.) et du type du Pokémon sélectionné.
* **Filtrage Avancé** : Recherche textuelle dynamique permettant de filtrer les résultats par **Nom** ou par **Type** dans le tableau d'affichage.
* **Affichage d'images** : Visualisation des sprites disponibles pour illustrer les fiches.

### 🔸 Améliorations Possibles (Bonus)
* Recherche par caractéristiques spécifiques (ex: Pokémon ayant plus de 100 en attaque).
* Ajout de nouveaux Pokémon ou Dresseurs dans la base via un formulaire.
* Simulation de combats entre deux Pokémon basés sur leurs stats.
* Gestion des Pokémon possédés par les dresseurs (système d'inventaire).

---

## 🗄️ Structure de la Base de Données
Le projet utilise une base de données relationnelle composée de 4 tables :



| Table | Champs principaux |
| :--- | :--- |
| **POKEMON** | `idPokemon` (PK), `nom`, `hp`, `attaque`, `defense`, `vitesse`, `url_image`, `idType` (FK) |
| **TYPE** | `idType` (PK), `libelle_type` |
| **DRESSEUR** | `idDresseur` (PK), `nom` |
| **POKEMON_POSSEDER** | `idDresseur` (PK/FK), `idPokemon` (PK/FK), `commentaire` |

---

## 🚀 Installation et Utilisation

### Prérequis
* **Python 3.x** installé.
* Bibliothèque **Tkinter** (généralement incluse avec Python).
* Bibliothèque **sqlite3** (incluse avec Python).

### Lancement
1.  Téléchargez ou clonez le dossier du projet.
2.  Assurez-vous que le script, la base de données et le dossier `images/` sont dans le même répertoire.
3.  Exécutez le script principal :
    ```bash
    python programme.py
    ```

> **Astuce :** Pour modifier ou vérifier la base de données manuellement, vous pouvez utiliser le logiciel **DB Browser for SQLite**.

---

## 📂 Structure du Projet
```plaintext
📁 Projet-bdd-Pokemon/
│
├── 🖥️ lanceur.bat           # Script Windows pour lancer l'application
├── 🗄️ pokedex.db            # Base de données SQLite
├── 📄 README.md             # Documentation (ce fichier)
│
└── 📁 application+base/     # Dossier contenant les ressources applicatives
    ├── 📄 programme.py      # Code source principal (Tkinter + SQL)
    └── 📁 images/           # Sprites des Pokémon (ex: Pikachu.gif)

