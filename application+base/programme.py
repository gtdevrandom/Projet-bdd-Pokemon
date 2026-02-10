from tkinter import *
from tkinter.ttk import Style, Combobox, Treeview, Frame as TTKFrame
from tkinter.ttk import Label as TTKLabel, Button as TTKButton
import sqlite3
import os

"""Fonction de connexion permettant de se connecter à la base pokedex
"""
def connexion():
    try:
        #connexion à la bdd
        sqliteConnection = sqlite3.connect('pokedex.db')
        return sqliteConnection
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

"""<summary>Fonction de connexion à la bdd</summary>
"""
def deconnexion(sqliteConnection):
   if (sqliteConnection):
       #fermeture de la co
            sqliteConnection.close()
            print("The SQLite connection is closed")


"""<summary>La fonction va chercher la liste des pokemon dans la bdd</summary>
<return>Retourne un tableau contenant la liste des noms de pokemon</return>
"""
def RemplirListeDeroulantePokemon():
    sqliteConnection = connexion()
    cursor = sqliteConnection.cursor()
    #ecriture de la requéte
    sqlite_select_Query = "select nom from pokemon;"
    #execution de la requéte
    cursor.execute(sqlite_select_Query)
    #on place tout les enregistrements dans une variable record
    record = cursor.fetchall()
    #declaration du tableau qui va contenir les données a afficher dans la liste déroulante
    tabPoke = []
    #parcours notre tableau de retour de base de données et ajoute les éléments dans le tableau data
    for row in record:
        tabPoke.append(row[0])

    #on ferme le curseur
    cursor.close()
    deconnexion(sqliteConnection)

    #retourne le tableau
    return tabPoke   

"""<summary>Recupére et affiche les informations récupérer par la requéte</summary>
"""
def AffichezPokemon():
    
    sqliteConnection = connexion()
    cursor = sqliteConnection.cursor()
    
    # Sécurité si la liste est vide
    selection = listeDeroulantePokemon.get()
    if not selection:
        return

    #ecriture de la requéte, on récupére le contenu de la listeDeroulante avec la fonction .get()
    # Ajout de taille, poids, region et route dans la requête
    sqlite_select_Query = "select nom,HP,attaque,defense,attaque_spe,defense_spe,vitesse,taille,poids,region,route,url_image,libelle_type from pokemon INNER JOIN type ON type.idType = pokemon.idType WHERE nom ='" + selection + "';"
    #execution de la requéte
    cursor.execute(sqlite_select_Query)
    #on place tout les enregistrements dans une variable record
    record = cursor.fetchall()

    if record:
        #la variable record est un tableau à plusieurs dimension, chaque case contient une information

        #on modifie la valeur de la StringVar "value_label_nom" avec une valeur du tableau
        value_label_nom.set(record[0][0].upper()) # Mettre en majuscule pour le style

        #on modifie la valeur de la StringVar "value_label_hp" avec une valeur du tableau
        value_label_hp.set("HP: "+ str(record[0][1]))
        #on modifie la valeur de la StringVar "value_label_attaque" avec une valeur du tableau + du texte
        value_label_attaque.set("Attaque: " + str(record[0][2]))
        #on modifie la valeur de la StringVar "value_label_defense" avec une valeur du tableau + du texte
        value_label_defense.set("Defense: " + str(record[0][3]))
        #on modifie la valeur de la StringVar "value_label_attaque_spe" avec une valeur du tableau + du texte
        value_label_attaque_spe.set("Attaque Spé: " + str(record[0][4]))
        #on modifie la valeur de la StringVar "value_label_defense_spe" avec une valeur du tableau + du texte
        value_label_defense_spe.set("Défense Spé: " + str(record[0][5]))
        #on modifie la valeur de la StringVar "value_label_vitesse" avec une valeur du tableau + du texte
        value_label_vitesse.set("Vitesse: " + str(record[0][6]))
        #on modifie la valeur de la StringVar "value_label_type" avec une valeur du tableau + du texte
        # Nouveaux champs: taille, poids, région, route
        value_label_taille.set("Taille: " + str(record[0][7]) + " m")
        value_label_poids.set("Poids: " + str(record[0][8]) + " kg")
        value_label_region.set("Région: " + str(record[0][9]))
        value_label_route.set("Route: " + str(record[0][10]))
        value_label_type.set("Type: " + str(record[0][12]))

        #construction du lien de l'image (url_image est désormais à l'index 11)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        lien_image = os.path.join(script_dir, "images", str(record[0][11]))

        #affichage de l'image avec gestion d'erreur simple
        try:
            img2 = PhotoImage(file=lien_image)
            image_pokemon.configure(image=img2)
            image_pokemon.image = img2
        except:
            image_pokemon.configure(image="") # Pas d'image si erreur

        print("SQLite Database Version is: ", record)
    
    #on ferme le curseur
    cursor.close()
    deconnexion(sqliteConnection)
    
"""<summary>Affiche dans le tree la liste des pokemon retourné par la requéte</summary>
"""
def AffichezListePokemon():
    
    sqliteConnection = connexion()
    cursor = sqliteConnection.cursor()
    #ecriture de la requéte
    sqlite_select_Query = "SELECT idPokemon,nom,HP,libelle_type FROM pokemon INNER JOIN type  ON type.idType = pokemon.idType WHERE nom LIKE '%" + var_texte_recherche.get() + "%' OR libelle_type LIKE '%" + var_texte_recherche.get() + "%';"
    #execution de la requéte
    cursor.execute(sqlite_select_Query)
    #on place tout les enregistrements dans une variable record
    record = cursor.fetchall()
    #vidange du tableau
    tree.delete(*tree.get_children())
    #on parcours le tableau record pour afficher et on insert une nouvelle ligne à chaque row. 
    for row in record:
        tree.insert('', 'end', iid=str(row[0]), text=str(row[1]),
                     values=(str(row[2]),
                             str(row[3])))


    #on ferme le curseur
    cursor.close()
    #deconnexion de la bdd
    deconnexion(sqliteConnection)



#création de la fenetre Tkinter
fenetre=Tk()
fenetre.title("Pokédex - Version Rouge et Bleu")
#permet de modifier la taille de la fenétre (AGRANDIE)
fenetre.geometry("1200x900")
fenetre.resizable(False, False) 

# Configuration des couleurs - Style Pokédex Rouge/Bleu/Blanc
bg_color = '#DC0A2D'  # Rouge Pokédex
screen_bg = '#E3F2FD' # Blanc bleuté pour les écrans
screen_border = '#333333' # Bordure sombre pour les écrans
fg_color = '#ffffff'  # Texte Blanc
text_on_screen = '#000000' # Texte Noir sur les écrans
accent_color = '#FFD700'  # Jaune
btn_color = '#1976D2' # Bleu

fenetre.configure(bg=bg_color)

#configuration de la police et des couleurs par défaut
style = Style()
style.theme_use('clam')

# Configurer le style de la fenêtre
style.configure('TFrame', background=bg_color)

# Styles spécifiques
style.configure('Title.TLabel', font=('Verdana', 20, 'bold'), background=screen_bg, foreground=text_on_screen)
style.configure('Normal.TLabel', font=('Verdana', 11, 'bold'), background=bg_color, foreground=fg_color)
style.configure('Header.TLabel', font=('Verdana', 12, 'bold', 'underline'), background=screen_bg, foreground='#DC0A2D')
style.configure('Info.TLabel', font=('Verdana', 10), background=screen_bg, foreground=text_on_screen)

# Style Boutons (Bleus)
style.configure('TButton', font=('Verdana', 10, 'bold'), background=btn_color, foreground='white', relief='raised', borderwidth=3)
style.map('TButton', background=[('active', '#4A90E2'), ('pressed', '#0D47A1')])

# Style Combobox
style.configure('TCombobox', font=('Verdana', 11), fieldbackground='white', background='white')

# Style Treeview
style.configure('Treeview', background='white', foreground='black', fieldbackground='white', font=('Verdana', 10), rowheight=25)
style.configure('Treeview.Heading', background=btn_color, foreground='white', font=('Verdana', 11, 'bold'))
style.map('Treeview', background=[('selected', accent_color)], foreground=[('selected', 'black')])


"""
------Partie liste déroulante + Bouton Recherche-------------
"""

#récupération de la liste des pokemon dans la base de données avec la fonction RemplirListeDeroulantePokemon qui retoune un tableau.
tabPokemon=RemplirListeDeroulantePokemon()

# Frame supérieur pour la recherche (Largeur augmentée à 1200)
frame_recherche = Frame(fenetre, bg=bg_color, height=80, relief='raised', bd=4)
frame_recherche.place(x=0, y=0, width=1200, height=80)

# Ajout de la pokéball dans le coin supérieur gauche
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pokeball_path = os.path.join(script_dir, "images", "pokeball.png")
    pokeball_img = PhotoImage(file=pokeball_path)
    pokeball_label = Label(frame_recherche, image=pokeball_img, bg=bg_color)
    pokeball_label.image = pokeball_img
    pokeball_label.place(x=10, y=10, width=60, height=60)
except Exception as e:
    print(f"le logo n'a pas chargé: {e}")

#création du Label
label_recherche_poke=TTKLabel(frame_recherche, text="Choix du Pokémon:", style='Normal.TLabel')
#position du label
label_recherche_poke.place(x=100, y=25, width=180, height=25)

#  Création de la Combobox (liste déroulante) 
listeDeroulantePokemon = Combobox(frame_recherche, values=tabPokemon, state='readonly')
# Choisir l'élément qui s'affiche par défaut
if len(tabPokemon) > 0:
    listeDeroulantePokemon.current(0)
#position de la liste
listeDeroulantePokemon.place(x=290, y=25, width=250, height=30)

#bouton recherche qui appele la fonction AffichezPokemon
bouton_search=TTKButton(frame_recherche, text="Analyser", command=AffichezPokemon)
bouton_search.place(x=560, y=24, width=150, height=32)

"""
------FIN-------------
"""


"""
Partie affichage des informations d'une pokemon
"""

# Frame global "Écran" (Simulation de l'écran du pokedex avec bordure noire)
frame_ecran_border = Frame(fenetre, bg=screen_border)
frame_ecran_border.place(x=20, y=100, width=1160, height=350)

# Frame principal pour les informations (Fond écran blanc/bleu)
frame_info = Frame(frame_ecran_border, bg=screen_bg)
frame_info.place(x=5, y=5, width=1150, height=340)

# Cadre gauche pour les informations textuelles
frame_left = Frame(frame_info, bg=screen_bg)
frame_left.place(x=10, y=10, width=600, height=320)

#création d'une variable StringVar
value_label_nom = StringVar()
#création du label (Titre)
champ_label=TTKLabel(frame_left, textvariable=value_label_nom, style='Title.TLabel')
champ_label.place(x=0, y=0, width=580, height=40)

champ_label_info=TTKLabel(frame_left, text="STATISTIQUES & INFOS", style='Header.TLabel')
champ_label_info.place(x=0, y=50, width=580, height=25)

#--- Colonne 1 : Stats de combat ---
#création d'une variable StringVar
value_label_hp = StringVar()
champ_label_hp=TTKLabel(frame_left, textvariable=value_label_hp, style='Info.TLabel')
champ_label_hp.place(x=10, y=90, width=250, height=20)

value_label_attaque = StringVar()
champ_label_attaque=TTKLabel(frame_left, textvariable=value_label_attaque, style='Info.TLabel')
champ_label_attaque.place(x=10, y=120, width=250, height=20)

value_label_defense = StringVar()
champ_label_defense=TTKLabel(frame_left, textvariable=value_label_defense, style='Info.TLabel')
champ_label_defense.place(x=10, y=150, width=250, height=20)

value_label_attaque_spe = StringVar()
champ_label_attaque_spe=TTKLabel(frame_left, textvariable=value_label_attaque_spe, style='Info.TLabel')
champ_label_attaque_spe.place(x=10, y=180, width=250, height=20)

value_label_defense_spe = StringVar()
champ_label_defense_spe=TTKLabel(frame_left, textvariable=value_label_defense_spe, style='Info.TLabel')
champ_label_defense_spe.place(x=10, y=210, width=250, height=20)

value_label_vitesse = StringVar()
champ_label_vitesse=TTKLabel(frame_left, textvariable=value_label_vitesse, style='Info.TLabel')
champ_label_vitesse.place(x=10, y=240, width=250, height=20)


#--- Colonne 2 : Physique & Type ---
value_label_type = StringVar()
champ_label_type=TTKLabel(frame_left, textvariable=value_label_type, style='Info.TLabel')
champ_label_type.place(x=300, y=90, width=250, height=20)
 
value_label_taille = StringVar()
champ_label_taille=TTKLabel(frame_left, textvariable=value_label_taille, style='Info.TLabel')
champ_label_taille.place(x=300, y=120, width=250, height=20)

value_label_poids = StringVar()
champ_label_poids=TTKLabel(frame_left, textvariable=value_label_poids, style='Info.TLabel')
champ_label_poids.place(x=300, y=150, width=250, height=20)

value_label_region = StringVar()
champ_label_region=TTKLabel(frame_left, textvariable=value_label_region, style='Info.TLabel')
champ_label_region.place(x=300, y=180, width=250, height=20)

value_label_route = StringVar()
champ_label_route=TTKLabel(frame_left, textvariable=value_label_route, style='Info.TLabel')
champ_label_route.place(x=300, y=210, width=250, height=20)


# Cadre droit pour l'image (Ajusté pour la grande fenêtre)
frame_right = Frame(frame_info, bg=screen_bg, relief='flat')
frame_right.place(x=650, y=10, width=480, height=320)

#image affichée à droite
image_pokemon = Label(frame_right, image="", bg=screen_bg)
image_pokemon.place(x=0, y=0, width=480, height=320)

"""
-------------------FIN---------------------------------------
"""


"""
Partie recherche et affichage du tableau
"""

# Frame pour la recherche dans le tableau
frame_search = Frame(fenetre, bg=bg_color, height=60)
frame_search.place(x=0, y=470, width=1200, height=60)

#création d'une variable StringVar
var_texte_recherche = StringVar()
label_recherche_liste=TTKLabel(frame_search, text="Filtrer par nom/type:", style='Normal.TLabel')
label_recherche_liste.place(x=20, y=18, width=200, height=25)

textBoxRecherche = Entry(frame_search, textvariable=var_texte_recherche, width=30, font=('Verdana', 12), bg=screen_bg, fg='black')
textBoxRecherche.place(x=230, y=15, width=300, height=30)

#bouton de recherche
bouton_affichez_pokemon=TTKButton(frame_search, text="Filtrer liste", command=AffichezListePokemon)
bouton_affichez_pokemon.place(x=550, y=14, width=150, height=32)


# Frame container pour le tableau avec bordure noire
frame_tree_container = Frame(fenetre, bg=screen_border, bd=2)
frame_tree_container.place(x=20, y=540, width=1160, height=340)

#création de la grille d'affichage (tableau)
tree = Treeview(frame_tree_container, columns=('HP', 'Type'), height=15)
 
 # Set the heading (Attribute Names)
tree.heading('#0', text='Pokemon')
tree.heading('#1', text='HP')
tree.heading('#2', text='Type')
# Specify attributes of the columns (We want to stretch it!)
tree.column('#0', width=400, stretch=YES)
tree.column('#1', width=150, stretch=YES, anchor='center')
tree.column('#2', width=300, stretch=YES, anchor='center')

# Ajout d'une scrollbar
scrollbar = Scrollbar(frame_tree_container, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
tree.pack(side=LEFT, fill=BOTH, expand=True)

"""-----------------FIN----------------------"""

#On démarre la boucle Tkinter qui s'interrompt quand on ferme la fenêtre
# Afficher les détails du pokémon sélectionné au démarrage (si dispo)
if tabPokemon:
    AffichezPokemon()

fenetre.mainloop()