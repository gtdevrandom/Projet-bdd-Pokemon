from tkinter import *
from tkinter.ttk import Style, Combobox, Treeview, Frame as TTKFrame
from tkinter.ttk import Label as TTKLabel, Button as TTKButton
import sqlite3
import os

# ==========================================
# GESTION DE LA BASE DE DONNÉES
# ==========================================

def connexion():
    """
    Établit une connexion avec la base de données SQLite 'pokedex.db'.
    
    Returns:
        sqlite3.Connection: Objet de connexion à la base de données
    """
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'pokedex.db')
        sqliteConnection = sqlite3.connect(db_path)
        return sqliteConnection
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

def deconnexion(sqliteConnection):
    """
    Ferme la connexion avec la base de données SQLite.
    
    Args:
        sqliteConnection (sqlite3.Connection): Connexion à fermer
    """
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")


def RemplirListeDeroulantePokemon():
    """
    Récupère la liste de tous les noms de Pokémon depuis la base de données.
    
    Returns:
        list: Tableau contenant tous les noms de Pokémon
    """
    sqliteConnection = connexion()
    cursor = sqliteConnection.cursor()
    
    # Requête pour récupérer tous les noms de pokémon
    sqlite_select_Query = "select nom from pokemon;"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    
    # Construction du tableau avec les noms
    tabPoke = []
    for row in record:
        tabPoke.append(row[0])

    cursor.close()
    deconnexion(sqliteConnection)

    return tabPoke


# ==========================================
# AFFICHAGE DES DÉTAILS D'UN POKÉMON
# ==========================================

def AffichezPokemon():
    """
    Récupère et affiche les informations détaillées du Pokémon sélectionné.
    Affiche: stats, taille, poids, région, route, type et image.
    """
    sqliteConnection = connexion()
    cursor = sqliteConnection.cursor()
    
    # Vérification que un pokémon est sélectionné
    selection = listeDeroulantePokemon.get()
    if not selection:
        return

    # Requête pour récupérer toutes les informations du pokémon
    sqlite_select_Query = "select nom,HP,attaque,defense,attaque_spe,defense_spe,vitesse,taille,poids,region,route,url_image,libelle_type from pokemon INNER JOIN type ON type.idType = pokemon.idType WHERE nom ='" + selection + "';"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()

    if record:
        # Mise à jour du nom (en majuscule)
        value_label_nom.set(record[0][0].upper())

        # Mise à jour des stats de combat (HP, Attaque, Défense, etc.)
        value_label_hp.set("HP: "+ str(record[0][1]))
        value_label_attaque.set("Attaque: " + str(record[0][2]))
        value_label_defense.set("Defense: " + str(record[0][3]))
        value_label_attaque_spe.set("Attaque Spé: " + str(record[0][4]))
        value_label_defense_spe.set("Défense Spé: " + str(record[0][5]))
        value_label_vitesse.set("Vitesse: " + str(record[0][6]))

        # Mise à jour des informations physiques et type
        value_label_type.set("Type: " + str(record[0][12]))
        value_label_taille.set("Taille: " + str(record[0][7]) + " m")
        value_label_poids.set("Poids: " + str(record[0][8]) + " kg")
        value_label_region.set("Région: " + str(record[0][9]))
        value_label_route.set("Route: " + str(record[0][10]))

        # Chargement et affichage de l'image du pokémon
        script_dir = os.path.dirname(os.path.abspath(__file__))
        lien_image = os.path.join(script_dir, "images", str(record[0][11]))

        try:
            img2 = PhotoImage(file=lien_image)
            image_pokemon.configure(image=img2)
            image_pokemon.image = img2
        except:
            # Si l'image n'est pas trouvée, affiche un champ vide
            image_pokemon.configure(image="")

        print("SQLite Database Version is: ", record)
    
    cursor.close()
    deconnexion(sqliteConnection)

# ==========================================
# AFFICHAGE DE LA LISTE FILTRÉE DES POKÉMON
# ==========================================

def AffichezListePokemon():
    """
    Affiche la liste des Pokémon dans le tableau, avec filtres appliqués.
    Filtres disponibles: nom/type, HP minimum, et route.
    """
    sqliteConnection = connexion()
    cursor = sqliteConnection.cursor()
    
    # Récupération des critères de filtrage saisis par l'utilisateur
    recherche_texte = var_texte_recherche.get()
    filtrer_hp = var_filtre_hp.get()
    filtrer_route = var_filtre_route.get()
    
    # Construction de la requête avec filtres dynamiques
    sqlite_select_Query = "SELECT idPokemon,nom,HP,route,libelle_type FROM pokemon INNER JOIN type ON type.idType = pokemon.idType WHERE 1=1"
    
    # Filtre par nom ou type
    if recherche_texte:
        sqlite_select_Query += " AND (nom LIKE '%" + recherche_texte + "%' OR libelle_type LIKE '%" + recherche_texte + "%')"
    
    # Filtre par HP minimum
    if filtrer_hp:
        try:
            hp_value = int(filtrer_hp)
            sqlite_select_Query += " AND HP >= " + str(hp_value)
        except ValueError:
            pass
    
    # Filtre par route
    if filtrer_route:
        sqlite_select_Query += " AND route LIKE '%" + filtrer_route + "%'"
    
    sqlite_select_Query += ";"
    
    # Exécution de la requête
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    
    # Vidange du tableau avant insertion des nouvelles données
    tree.delete(*tree.get_children())
    
    # Insertion des pokémon dans le tableau
    for row in record:
        tree.insert('', 'end', iid=str(row[0]), text=str(row[1]),
                     values=(str(row[2]),
                             str(row[3]),
                             str(row[4])))

    cursor.close()
    deconnexion(sqliteConnection)



# ==========================================
# INITIALISATION DE LA FENÊTRE TKINTER
# ==========================================

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("Pokédex - Version Rouge et Bleu")
fenetre.geometry("1200x900")
fenetre.resizable(False, False)

# ==========================================
# CONFIGURATION DES COULEURS (THÈME POKÉDEX)
# ==========================================

bg_color = '#DC0A2D'        # Couleur de fond principale (Rouge Pokédex)
screen_bg = '#E3F2FD'       # Fond des écrans d'affichage (Blanc bleuté)
screen_border = '#333333'   # Bordure des écrans (Gris foncé)
fg_color = '#ffffff'        # Couleur du texte normal (Blanc)
text_on_screen = '#000000'  # Couleur du texte sur les écrans (Noir)
accent_color = '#FFD700'    # Couleur d'accentuation (Jaune)
btn_color = '#1976D2'       # Couleur des boutons (Bleu)

fenetre.configure(bg=bg_color)

# ==========================================
# CONFIGURATION DU STYLE (THÈME TTK)
# ==========================================

style = Style()
style.theme_use('clam')

# Style Frame principal
style.configure('TFrame', background=bg_color)

# Style Labels
style.configure('Title.TLabel', font=('Verdana', 20, 'bold'), background=screen_bg, foreground=text_on_screen)  # Titre pokémon
style.configure('Normal.TLabel', font=('Verdana', 11, 'bold'), background=bg_color, foreground=fg_color)  # Label normal
style.configure('Header.TLabel', font=('Verdana', 12, 'bold', 'underline'), background=screen_bg, foreground='#DC0A2D')  # Entête
style.configure('Info.TLabel', font=('Verdana', 10), background=screen_bg, foreground=text_on_screen)  # Info pokémon

# Style Boutons
style.configure('TButton', font=('Verdana', 10, 'bold'), background=btn_color, foreground='white', relief='raised', borderwidth=3)
style.map('TButton', background=[('active', '#4A90E2'), ('pressed', '#0D47A1')])

# Style Combobox (liste déroulante)
style.configure('TCombobox', font=('Verdana', 11), fieldbackground='white', background='white')

# Style Treeview (tableau)
style.configure('Treeview', background='white', foreground='black', fieldbackground='white', font=('Verdana', 10), rowheight=25)
style.configure('Treeview.Heading', background=btn_color, foreground='white', font=('Verdana', 11, 'bold'))
style.map('Treeview', background=[('selected', accent_color)], foreground=[('selected', 'black')])


# ==========================================
# SECTION 1: BARRE DE RECHERCHE SUPÉRIEURE
# ==========================================
# Contient: Pokéball, sélection pokémon, bouton d'analyse

# Récupération de la liste des pokémon depuis la base de données
tabPokemon = RemplirListeDeroulantePokemon()

# Frame principal pour la barre de recherche
frame_recherche = Frame(fenetre, bg=bg_color, height=80, relief='raised', bd=4)
frame_recherche.place(x=0, y=0, width=1200, height=80)

# Logo Pokéball en haut à gauche
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pokeball_path = os.path.join(script_dir, "images", "pokeball.png")
    pokeball_img = PhotoImage(file=pokeball_path)
    pokeball_label = Label(frame_recherche, image=pokeball_img, bg=bg_color)
    pokeball_label.image = pokeball_img
    pokeball_label.place(x=10, y=10, width=60, height=60)
except Exception as e:
    print(f"Le logo Pokéball n'a pas chargé: {e}")

# Label "Choix du Pokémon"
label_recherche_poke = TTKLabel(frame_recherche, text="Choix du Pokémon:", style='Normal.TLabel')
label_recherche_poke.place(x=100, y=25, width=180, height=25)

# Liste déroulante pour sélectionner un pokémon
listeDeroulantePokemon = Combobox(frame_recherche, values=tabPokemon, state='readonly')
if len(tabPokemon) > 0:
    listeDeroulantePokemon.current(0)
listeDeroulantePokemon.place(x=290, y=25, width=250, height=30)

# Bouton pour afficher les détails du pokémon sélectionné
bouton_search = TTKButton(frame_recherche, text="Analyser", command=AffichezPokemon)
bouton_search.place(x=560, y=24, width=150, height=32)


# ==========================================
# SECTION 2: ÉCRAN D'AFFICHAGE DES DÉTAILS
# ==========================================
# Affiche les stats et l'image du pokémon sélectionné

# Frame principal avec bordure noire (effet écran pokedex)
frame_ecran_border = Frame(fenetre, bg=screen_border)
frame_ecran_border.place(x=20, y=100, width=1160, height=350)

# Frame intérieur avec fond écran blanc/bleu
frame_info = Frame(frame_ecran_border, bg=screen_bg)
frame_info.place(x=5, y=5, width=1150, height=340)

# ---- PARTIE GAUCHE: INFORMATIONS TEXTUELLES ----
frame_left = Frame(frame_info, bg=screen_bg)
frame_left.place(x=10, y=10, width=600, height=320)

# Titre du pokémon (nom en majuscules)
value_label_nom = StringVar()
champ_label = TTKLabel(frame_left, textvariable=value_label_nom, style='Title.TLabel')
champ_label.place(x=0, y=0, width=580, height=40)

# En-tête "STATISTIQUES & INFOS"
champ_label_info = TTKLabel(frame_left, text="STATISTIQUES & INFOS", style='Header.TLabel')
champ_label_info.place(x=0, y=50, width=580, height=25)

# --- COLONNE 1: STATS DE COMBAT ---
value_label_hp = StringVar()
champ_label_hp = TTKLabel(frame_left, textvariable=value_label_hp, style='Info.TLabel')
champ_label_hp.place(x=10, y=90, width=250, height=20)

value_label_attaque = StringVar()
champ_label_attaque = TTKLabel(frame_left, textvariable=value_label_attaque, style='Info.TLabel')
champ_label_attaque.place(x=10, y=120, width=250, height=20)

value_label_defense = StringVar()
champ_label_defense = TTKLabel(frame_left, textvariable=value_label_defense, style='Info.TLabel')
champ_label_defense.place(x=10, y=150, width=250, height=20)

value_label_attaque_spe = StringVar()
champ_label_attaque_spe = TTKLabel(frame_left, textvariable=value_label_attaque_spe, style='Info.TLabel')
champ_label_attaque_spe.place(x=10, y=180, width=250, height=20)

value_label_defense_spe = StringVar()
champ_label_defense_spe = TTKLabel(frame_left, textvariable=value_label_defense_spe, style='Info.TLabel')
champ_label_defense_spe.place(x=10, y=210, width=250, height=20)

value_label_vitesse = StringVar()
champ_label_vitesse = TTKLabel(frame_left, textvariable=value_label_vitesse, style='Info.TLabel')
champ_label_vitesse.place(x=10, y=240, width=250, height=20)

# --- COLONNE 2: INFOS PHYSIQUES & TYPE ---
value_label_type = StringVar()
champ_label_type = TTKLabel(frame_left, textvariable=value_label_type, style='Info.TLabel')
champ_label_type.place(x=300, y=90, width=250, height=20)

value_label_taille = StringVar()
champ_label_taille = TTKLabel(frame_left, textvariable=value_label_taille, style='Info.TLabel')
champ_label_taille.place(x=300, y=120, width=250, height=20)

value_label_poids = StringVar()
champ_label_poids = TTKLabel(frame_left, textvariable=value_label_poids, style='Info.TLabel')
champ_label_poids.place(x=300, y=150, width=250, height=20)

value_label_region = StringVar()
champ_label_region = TTKLabel(frame_left, textvariable=value_label_region, style='Info.TLabel')
champ_label_region.place(x=300, y=180, width=250, height=20)

value_label_route = StringVar()
champ_label_route = TTKLabel(frame_left, textvariable=value_label_route, style='Info.TLabel')
champ_label_route.place(x=300, y=210, width=250, height=20)

# ---- PARTIE DROITE: IMAGE DU POKÉMON ----
frame_right = Frame(frame_info, bg=screen_bg, relief='flat')
frame_right.place(x=650, y=10, width=480, height=320)

# Affichage de l'image du pokémon
image_pokemon = Label(frame_right, image="", bg=screen_bg)
image_pokemon.place(x=0, y=0, width=480, height=320)


# ==========================================
# SECTION 3: BARRE DE FILTRES
# ==========================================
# Contient les champs de recherche/filtrage

frame_search = Frame(fenetre, bg=bg_color, height=60)
frame_search.place(x=0, y=470, width=1200, height=60)

# Variables StringVar pour stocker les valeurs des filtres
var_texte_recherche = StringVar()
var_filtre_hp = StringVar()
var_filtre_route = StringVar()

# Filtre par nom ou type
label_recherche_liste = TTKLabel(frame_search, text="Filtrer par nom/type:", style='Normal.TLabel')
label_recherche_liste.place(x=20, y=18, width=200, height=25)

textBoxRecherche = Entry(frame_search, textvariable=var_texte_recherche, width=30, font=('Verdana', 12), bg=screen_bg, fg='black')
textBoxRecherche.place(x=230, y=15, width=200, height=30)

# Filtre par HP minimum
label_filtre_hp = TTKLabel(frame_search, text="HP min:", style='Normal.TLabel')
label_filtre_hp.place(x=440, y=18, width=60, height=25)

textBoxFiltreHP = Entry(frame_search, textvariable=var_filtre_hp, width=5, font=('Verdana', 12), bg=screen_bg, fg='black')
textBoxFiltreHP.place(x=505, y=15, width=60, height=30)

# Filtre par route
label_filtre_route = TTKLabel(frame_search, text="Route:", style='Normal.TLabel')
label_filtre_route.place(x=580, y=18, width=60, height=25)

textBoxFiltreRoute = Entry(frame_search, textvariable=var_filtre_route, width=10, font=('Verdana', 12), bg=screen_bg, fg='black')
textBoxFiltreRoute.place(x=645, y=15, width=100, height=30)

# Bouton pour appliquer les filtres
bouton_affichez_pokemon = TTKButton(frame_search, text="Filtrer liste", command=AffichezListePokemon)
bouton_affichez_pokemon.place(x=760, y=14, width=150, height=32)


# ==========================================
# SECTION 4: TABLEAU DES POKÉMON
# ==========================================
# Affiche la liste filtrée des pokémon

frame_tree_container = Frame(fenetre, bg=screen_border, bd=2)
frame_tree_container.place(x=20, y=540, width=1160, height=340)

# Création du tableau (Treeview) avec les colonnes
tree = Treeview(frame_tree_container, columns=('HP', 'Route', 'Type'), height=15)

# En-têtes des colonnes
tree.heading('#0', text='Pokemon')
tree.heading('#1', text='HP')
tree.heading('#2', text='Route')
tree.heading('#3', text='Type')

# Configuration des colonnes (Largeur et alignement)
tree.column('#0', width=350, stretch=YES)  # Colonne Pokémon
tree.column('#1', width=100, stretch=YES, anchor='center')  # Colonne HP
tree.column('#2', width=150, stretch=YES, anchor='center')  # Colonne Route
tree.column('#3', width=250, stretch=YES, anchor='center')  # Colonne Type

# Barre de défilement verticale
scrollbar = Scrollbar(frame_tree_container, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
tree.pack(side=LEFT, fill=BOTH, expand=True)


# ==========================================
# DÉMARRAGE DE L'APPLICATION
# ==========================================

# Affichage du détail du premier pokémon au lancement
if tabPokemon:
    AffichezPokemon()

fenetre.mainloop()