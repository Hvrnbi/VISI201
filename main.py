from PIL import Image
from numpy import asarray, ndarray, array, uint8, delete
from random import choice

# image = Image.open("images/hibou.jpg")

# image = image.convert("L")

# img_array = asarray(image)

# print(len(img_array[0])//3)


### Fonctions ###

def import_image(chemin: str) -> ndarray :
    """Charge l'image donnée, la passe en nuances de gris, et la convertie en tableau (de numpy)"""

    ## Chargement de l'image ## 

    # On essaie d'ouvrir l'image avec la librairie PIL
    try:
        image = Image.open(chemin)

    # Gestion d'erreur si le fichier n'est pas accessible ou n'existe pas 
    except FileNotFoundError:
        print("Le chemin d'accès est invalide.")
        # TODO Set image sur une image blanche en cas d'erreur
    
    # Gestion d'erreur dans les autres cas
    except:
        print("Une erreur s'est produite")
        # TODO Pareil qu'au dessus


    ## Conversion de l'image en nuances de gris ##

    # On utilise la méthode .convert() de PIL
    image = image.convert("L")


    ## Conversion en tableau ##

    # On utilise la fonction asarrray() de numpy
    image_array = asarray(image)

    return image_array
    
    
def tab_image_blanche(longueur: int, hauteur: int) -> ndarray:
    """Génère un tableau contenant des pixels blancs avec les dimensions données"""
    # On crée autant de lignes que de pixels de hauteur, et autant de pixels que de hauteur
    tab = [ [255] * longueur] * hauteur
    return array(tab)
    
def tab_image_noir(longueur: int, hauteur: int) -> ndarray:
    """Génère un tableau contenant des pixels blancs avec les dimensions données"""
    # On crée autant de lignes que de pixels de hauteur, et autant de pixels que de hauteur
    tab = [ [0] * longueur] * hauteur
    return array(tab)
    
def get_longueur_img(tab_img: ndarray) -> int:
    """Renvoie la longueur du tableau à deux dimensions (représentant une image) donné"""
    return len(tab_img[0])

def get_hauteur_img(tab_img: ndarray) -> int:
    """Renvoie la hauteur du tableau à deux dimensions (représentant une image) donné"""
    return len(tab_img)

def assombrir_pixel(tab_img: ndarray, ligne: int, colonne: int) -> ndarray:
    """Réduit de 51 (parce que c'est 255/5) les valeurs des couleurs du pixel à la position donnée."""
    if tab_img[ligne][colonne] >= 51:
        tab_img[ligne][colonne] = tab_img[ligne][colonne] - 51

    return tab_img

def generer_clous(tab_img: ndarray) -> list:
    """Génère un tableau qui contient des tuples qui représentent des clous : deux coordonnées et un numéro de côté -> 0 pour le haut, 1 pour la droite, 2 pour le bas, 3 pour la gauche"""
    liste_res = []

    h = get_hauteur_img(tab_img)
    l = get_longueur_img(tab_img)

    for i in range(0, l, 10):
        liste_res = liste_res + [(0, i, 0)]
    for i in range(10, h, 10):
        liste_res = liste_res + [(i, l - 1, 1)]
    for i in range(0, l - 10, 10):
        liste_res = liste_res + [(h - 1, i, 2)]
    for i in range(10, h - 10, 10):
        liste_res = liste_res + [(i, 0, 3)]

    return liste_res

def visible(clou1: tuple, clou2: tuple) -> bool:
    """Renvoie True si les clous se voient, False sinon"""
    return clou1[2] != clou2[2]
    
def clou_choisi_al(liste_clous : list) -> tuple:
    """On choisie un clou aléatoirement"""
    return random.choice(liste_clous)

def tracer_droite(clou1: tuple, clou2: tuple, image: list) -> list:
    """Trace une droite d'un clou à un autre."""
    if clou2[3]==clou1[3]:
        print("il est impossible de tracer un trait sur le même bord")
    else:
        
        pass

def lst_zone(image) -> list:
    """Renvoie une liste avec les coordonées de chaques zones"""
    lst = []
    hauteur = get_hauteur_img(image)
    longueur = get_longueur_img(image)
    pas = 10
    for i in range(0,longueur,pas):
        for j in range(0,hauteur, pas):
            lst += [(i,j)] #prends les coordonnées du pixel en haut à gauche de chaque zone
    return lst  

def erreur_moyenne_zone(image1, image2, zone : tuple, longueur : int)  -> float:
    """Renvoie l'erreur moyenne pour une zone"""
    haut = get_hauteur_img(image1)
    long = get_longueur_img(image1)
    coo1 = zone[0]
    coo2 = zone[1]
    pix1 = image1[coo1][coo2]
    pix2 = image2[coo1][coo2]
    diff = abs(pix1 - pix2)
    for i in range(coo1, coo1+longueur):
        for j in range(coo2, coo2+longueur):
            if i != 0 and j != 0:
                if i > long and j > haut:
                    pix1 = image1[i][j]
                    pix2 = image2[i][j]
                    diff += abs(pix1 - pix2)
    return (diff / (longueur * longueur *255)) * 100

def erreur(image1, image2, zones : list) -> float:
    """Renvoie l'erreur moyenne entre les deux images"""
    moy = 0
    for i in range(len(zones)):
        moy += erreur_moyenne_zone(image1, image2,zones[i])
    return moy/len(zones)

image = import_image("images/hibou.jpg")
print(image)

image_blanche = tab_image_blanche(get_longueur_img(image), get_hauteur_img(image))

image_noir = tab_image_noir(get_longueur_img(image), get_hauteur_img(image))

print(image_blanche)

img = Image.fromarray(uint8(image_blanche))

for i in range(0, 50):
    for j in range(0, 50):
            image_blanche = assombrir_pixel(image_blanche, i, j)

img = Image.fromarray(uint8(image_blanche))
#img.show()

print(image_blanche)

clous = generer_clous(image_blanche)
print(clous)

test = tab_image_blanche(111, 111)
c = generer_clous(test)
for i in range(0, len(c)):
    test = assombrir_pixel(test, c[i][0], c[i][1])
im_test = Image.fromarray(uint8(test))
im_test.show()

l_zones = lst_zone(image)
print(erreur_moyenne_zone(image, image_blanche,l_zones[500],10))
### TODO ###

# On peut essayer de regarder des clous aléatoire plutôt que de tout tester

# On regarde l'erreur sur la ligne qu'on vient de tracer, en faisant des moyennes par zones

# Pas forcément la même résolution pour le calcul que pour l'image

# Pas forcément mesurer l'erreur d'une bande de quelques pixels au bord si on met les clous dedans
