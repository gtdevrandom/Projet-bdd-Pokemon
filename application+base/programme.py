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
    #ecriture de la requéte, on récupére le contenu de la listeDeroulante avec la fonction .get()
    # Ajout de taille, poids, region et route dans la requête
    sqlite_select_Query = "select nom,HP,attaque,defense,attaque_spe,defense_spe,vitesse,taille,poids,region,route,url_image,libelle_type from pokemon INNER JOIN type ON type.idType = pokemon.idType WHERE nom ='" + listeDeroulantePokemon.get() + "';"
    #execution de la requéte
    cursor.execute(sqlite_select_Query)
    #on place tout les enregistrements dans une variable record
    record = cursor.fetchall()

    #la variable record est un tableau à plusieurs dimension, chaque case contient une information

    #on modifie la valeur de la StringVar "value_label_nom" avec une valeur du tableau
    value_label_nom.set(record[0][0])

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

    #affichage de l'image
    img2 = PhotoImage(file=lien_image)
    image_pokemon.configure(image=img2)
    image_pokemon.image = img2
    

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
fenetre.title("Pokédex - Version Noir et Blanc")
#permet de modifier la taille de la fenétre
fenetre.geometry("1000x900")
fenetre.configure(bg='#1a1a1a')

#configuration de la police et des couleurs par défaut - Style Pokédex Noir et Blanc
style = Style()
style.theme_use('clam')

# Configuration des couleurs inspirées du Pokédex Version Noir et Blanc
bg_color = '#1a1a1a'  # Noir profond
fg_color = '#ffffff'  # Blanc
header_color = '#2d2d2d'  # Gris foncé pour les sections
accent_color = '#d4a574'  # Doré

# Configurer le style de la fenêtre
fenetre.configure(bg=bg_color)
style.configure('TFrame', background=bg_color)
style.configure('Title.TLabel', font=('Arial', 18, 'bold'), background=bg_color, foreground=accent_color)
style.configure('Normal.TLabel', font=('Arial', 10), background=bg_color, foreground=fg_color)
style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background=header_color, foreground=accent_color)
style.configure('Info.TLabel', font=('Arial', 9), background=bg_color, foreground=fg_color)
style.configure('TButton', font=('Arial', 10, 'bold'), background='#d4a574', foreground='#1a1a1a', relief='raised', borderwidth=2)
style.configure('TCombobox', font=('Arial', 10), fieldbackground='#2d2d2d', background='#2d2d2d', foreground=fg_color)
style.map('TButton', background=[('active', '#e8c68f'), ('pressed', '#b8905c')])
style.map('TCombobox', fieldbackground=[('readonly', '#2d2d2d')], background=[('readonly', '#2d2d2d')])



"""
------Partie liste déroulante + Bouton Recherche-------------
"""

#récupération de la liste des pokemon dans la base de données avec la fonction RemplirListeDeroulantePokemon qui retoune un tableau.
tabPokemon=RemplirListeDeroulantePokemon()

# Frame supérieur pour la recherche
frame_recherche = Frame(fenetre, bg=header_color, height=60)
frame_recherche.place(x=0, y=0, width=1000, height=60)

#création du Label
label_recherche_poke=TTKLabel(frame_recherche, text="Sélectionner Pokémon:", style='Normal.TLabel')
#position du label
label_recherche_poke.place(x=20, y=17, width=150, height=25)

#  Création de la Combobox (liste déroulante) 
listeDeroulantePokemon = Combobox(frame_recherche, values=tabPokemon, state='readonly')
# Choisir l'élément qui s'affiche par défaut
listeDeroulantePokemon.current(0)
#position de la liste
listeDeroulantePokemon.place(x=180, y=17, width=200, height=25)

#bouton recherche qui appele la fonction AffichezPokemon
bouton_search=TTKButton(frame_recherche, text="Voir détails", command=AffichezPokemon)
bouton_search.place(x=400, y=17, width=120, height=25)

"""
------FIN-------------
"""


"""
Partie affichage des informations d'une pokemon
"""

# Frame principal pour les informations
frame_info = Frame(fenetre, bg=bg_color)
frame_info.place(x=10, y=70, width=990, height=310)

# Cadre gauche pour les informations textuelles
frame_left = Frame(frame_info, bg=bg_color)
frame_left.place(x=0, y=0, width=480, height=310)

#création d'une variable StringVar
value_label_nom = StringVar()
#création du label
champ_label=TTKLabel(frame_left, textvariable=value_label_nom, style='Title.TLabel')
champ_label.place(x=10, y=0, width=460, height=40)

champ_label_info=TTKLabel(frame_left, text="CARACTÉRISTIQUES", style='Header.TLabel')
champ_label_info.place(x=10, y=45, width=460, height=22)

#création d'une variable StringVar
value_label_hp = StringVar()
champ_label_hp=TTKLabel(frame_left, textvariable=value_label_hp, style='Info.TLabel')
champ_label_hp.place(x=15, y=72, width=450, height=18)

#création d'une variable StringVar
value_label_attaque = StringVar()
champ_label_attaque=TTKLabel(frame_left, textvariable=value_label_attaque, style='Info.TLabel')
champ_label_attaque.place(x=15, y=92, width=450, height=18)

#création d'une variable StringVar
value_label_defense = StringVar()
champ_label_defense=TTKLabel(frame_left, textvariable=value_label_defense, style='Info.TLabel')
champ_label_defense.place(x=15, y=112, width=450, height=18)

#création d'une variable StringVar
value_label_attaque_spe = StringVar()
champ_label_attaque_spe=TTKLabel(frame_left, textvariable=value_label_attaque_spe, style='Info.TLabel')
champ_label_attaque_spe.place(x=15, y=132, width=450, height=18)

#création d'une variable StringVar
value_label_defense_spe = StringVar()
champ_label_defense_spe=TTKLabel(frame_left, textvariable=value_label_defense_spe, style='Info.TLabel')
champ_label_defense_spe.place(x=15, y=152, width=450, height=18)

#création d'une variable StringVar
value_label_vitesse = StringVar()
champ_label_vitesse=TTKLabel(frame_left, textvariable=value_label_vitesse, style='Info.TLabel')
champ_label_vitesse.place(x=15, y=172, width=450, height=18)

#création d'une variable StringVar
value_label_type = StringVar()
champ_label_type=TTKLabel(frame_left, textvariable=value_label_type, style='Info.TLabel')
champ_label_type.place(x=15, y=192, width=450, height=18)
 
# Nouveaux champs: taille, poids, région, route
value_label_taille = StringVar()
champ_label_taille=TTKLabel(frame_left, textvariable=value_label_taille, style='Info.TLabel')
champ_label_taille.place(x=15, y=212, width=450, height=18)

value_label_poids = StringVar()
champ_label_poids=TTKLabel(frame_left, textvariable=value_label_poids, style='Info.TLabel')
champ_label_poids.place(x=15, y=232, width=450, height=18)

value_label_region = StringVar()
champ_label_region=TTKLabel(frame_left, textvariable=value_label_region, style='Info.TLabel')
champ_label_region.place(x=15, y=252, width=450, height=18)

value_label_route = StringVar()
champ_label_route=TTKLabel(frame_left, textvariable=value_label_route, style='Info.TLabel')
champ_label_route.place(x=15, y=272, width=450, height=18)

# Cadre droit pour l'image
frame_right = Frame(frame_info, bg=header_color, relief='sunken', borderwidth=2)
frame_right.place(x=490, y=0, width=500, height=310)

#image affichée à droite
image_pokemon = Label(frame_right, image="", bg=header_color)
image_pokemon.place(x=10, y=10, width=480, height=290)

"""
-------------------FIN---------------------------------------
"""


"""
Partie recherche et affichage du tableau
"""

# Frame pour la recherche dans le tableau
frame_search = Frame(fenetre, bg=header_color, height=50)
frame_search.place(x=0, y=385, width=1000, height=50)

#création d'une variable StringVar
var_texte_recherche = StringVar()
label_recherche_liste=TTKLabel(frame_search, text="Filtrer par nom/type:", style='Normal.TLabel')
label_recherche_liste.place(x=20, y=12, width=150, height=25)
textBoxRecherche = Entry(frame_search, textvariable=var_texte_recherche, width=20, font=('Arial', 10), bg='#2d2d2d', fg='#ffffff', insertbackground='#d4a574')
textBoxRecherche.place(x=180, y=12, width=180, height=25)
#bouton de recherche
bouton_affichez_pokemon=TTKButton(frame_search, text="Filtrer liste", command=AffichezListePokemon)
bouton_affichez_pokemon.place(x=370, y=12, width=120, height=25)

# Style pour le Treeview
style.configure('Treeview', background='#2d2d2d', foreground='#ffffff', fieldbackground='#2d2d2d', font=('Arial', 9), rowheight=25)
style.configure('Treeview.Heading', background='#d4a574', foreground='#1a1a1a', font=('Arial', 10, 'bold'))
style.map('Treeview', background=[('selected', '#d4a574')], foreground=[('selected', '#1a1a1a')])

#création de la grille d'affichage (tableau)
tree = Treeview(fenetre, columns=('HP', 'Type'), height=15)
 
 # Set the heading (Attribute Names)
tree.heading('#0', text='Pokemon')
tree.heading('#1', text='HP')
tree.heading('#2', text='Type')
# Specify attributes of the columns (We want to stretch it!)
tree.column('#0', width=200, stretch=YES)
tree.column('#1', width=100, stretch=YES)
tree.column('#2', width=150, stretch=YES)

#placement du tableau
tree.place(x=20, y=440, width=960, height=440)
"""-----------------FIN----------------------"""

#On démarre la boucle Tkinter qui s'interrompt quand on ferme la fenêtre
# Afficher les détails du pokémon sélectionné au démarrage
AffichezPokemon()

fenetre.mainloop()