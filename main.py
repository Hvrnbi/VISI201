### Modules ###

from PIL import Image
from numpy import asarray, ndarray, array, uint8, delete
from random import choice


### Fonctions ###

def import_image(chemin: str) -> ndarray :
    """Charge l'image donnée, la passe en nuances de gris, et la convertit en tableau (de numpy)"""

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
    """Génère un tableau contenant des pixels noirs avec les dimensions données"""
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
        liste_res = liste_res + [(i, 0, 0)]
    for i in range(10, h, 10):
        liste_res = liste_res + [(l - 1, i, 1)]
    for i in range(l - 11, -1, - 10):
        liste_res = liste_res + [(i, h - 1, 2)]
    for i in range(h - 11, 0, -10):
        liste_res = liste_res + [(0, i, 3)]

    return liste_res

def visible(clou1: tuple, clou2: tuple) -> bool:
    """Renvoie True si les clous se voient, False sinon"""
    return clou1[2] != clou2[2]
    
def clou_choisi_al(liste_clous : list) -> tuple:
    """On choisie un clou aléatoirement"""
    return choice(liste_clous)

def tracer_droite(clou1: tuple, clou2: tuple, image: ndarray) -> ndarray:
    """Trace une droite d'un clou à un autre."""
    if visible(clou1, clou2):
        liste_points = liste_points_traverses(clou1, clou2, image)
        
        for i in range(0, len(liste_points)):
            ligne = liste_points[i][1]
            col = liste_points[i][0]
            image = assombrir_pixel(image, ligne, col)
    else:
        print("il est impossible de tracer un trait sur le même bord")

    return image

def liste_points_traverses(clou1: tuple, clou2: tuple, image: ndarray) -> list:
    """Renvoie les points que le segment [coul1, clou2] traverse"""
    liste_res = []
    liste_motif = liste_points_traverses_par_motif(clou1, clou2, image)

    l = get_longueur_img(image)
    h = get_hauteur_img(image)

    x1 = clou1[0]
    x2 = clou2[0]
    y1 = clou1[1]
    y2 = clou2[1]

    # On inverse l'ordre des clous si besoin, ça pourrait être fait de façon plus propre
    if x1 > x2:
        clou1, clou2, x1, x2, y1, y2 = clou2, clou1, x2, x1, y2, y1
    elif x1 == x2:
        if y1 > y2:
            clou1, clou2, x1, x2, y1, y2 = clou2, clou1, x2, x1, y2, y1

    # On applique le motif depuis le point de départ, et on ajoute les points obtenus dans la liste si ils rentrent dans l'image
    for i in range(0, len(liste_motif)):
            if (liste_motif[i][0] + x1 < l) and (0 <= liste_motif[i][1] + y1) and (liste_motif[i][1] + y1 < h):
                liste_res = liste_res + [(liste_motif[i][0] + x1, liste_motif[i][1] + y1)]
        
    return liste_res


def liste_points_traverses_par_motif(clou1: tuple, clou2: tuple, image: ndarray) -> list:
    """Renvoie la liste des points que le motif de la doite passant par clou1 et clou2 traverse"""
    liste_res = []

    l = get_longueur_img(image)
    h = get_hauteur_img(image)

    x1 = clou1[0]
    x2 = clou2[0]

    # On échange les clous si besoin, pourrait toujours être fait plus proprement
    if x1 > x2:
        clou1, clou2 = clou2, clou1
    # Gestion des droites verticales
    elif x1 == x2:
        liste_res = [(0, i) for i in range(0, h)]

    a, b = calcul_droite(clou1, clou2)

    y1 = clou1[1]
    y2 = clou2[1]

    mu = 0

    # Si la droite "descend"
    if y1 < y2:
        # On teste tous les pixels, ça peut être grandement optimisé
        for x in range(0, l):
            for y in range(0, h):
                # On calcule un "reste" (ax + by) qui lorsqu'il se trouve entre mu et mu + max(a, b) permet de créer un motif. On dessine ici le motif à partir de l'origine
                if (mu <= a * x + b * y) and (a * x + b * y < mu + max(a, b)):
                    liste_res = liste_res + [(x, y)]

    # Si la droite "monte"
    else:
        for x in range(0, l):
            for y in range(0, h):
                # Pareil qu'au dessus, sauf que le reste vaut (ax - by) et qu'on trace le motif à partir du point en bas à gauche
                if (mu <= a * x - b * y) and (a * x - b * y < mu + max(a,  b)):
                    liste_res = liste_res + [(x, - y)]

    return liste_res

def calcul_droite(clou1: tuple, clou2: tuple) -> tuple:
    """Renvoie les coordonnées du vecteur orthogonal au vecteur allant de clou1 à clou2"""
    x1 = clou1[0]
    x2 = clou2[0]
    y1 = clou1[1]
    y2 = clou2[1]

    a = y1 - y2
    b = x2 - x1    

    return (a, b)

def lst_zone(image: ndarray) -> list:
    """Renvoie une liste avec les coordonées de chaques zones"""
    lst = []
    hauteur = get_hauteur_img(image)
    longueur = get_longueur_img(image)
    pas = 10
    for i in range(0,longueur,pas):
        for j in range(0,hauteur, pas):
            lst += [(j, i)] #prends les coordonnées du pixel en haut à gauche de chaque zone
    return lst  

def erreur_moyenne_zone(image1: ndarray, image2: ndarray, zone : tuple, longueur : int)  -> float:
    """Renvoie l'erreur moyenne pour une zone"""
    haut = get_hauteur_img(image1)
    long = get_longueur_img(image1)
    coo1 = zone[0]
    coo2 = zone[1]
    pix1 = image1[coo1][coo2]
    pix2 = image2[coo1][coo2]
    diff = abs(pix1 - pix2)
    for i in range(coo1, longueur):
        for j in range(coo2, longueur):
            if i != 0 and j != 0 :
                if i > long and j > haut:
                    pix1 = image1[i][j]
                    pix2 = image2[i][j]
                    diff += abs(pix1 - pix2)
    return (diff / (longueur * longueur *255)) * 100

def erreur(image1: ndarray, image2: ndarray, zones : list, longueur : int) -> float:
    """Renvoie l'erreur moyenne entre les deux images"""
    moy = 0
    for i in range(len(zones)):
        moy += erreur_moyenne_zone(image1, image2, zones[i], longueur)
    return moy/len(zones)

def teste_5_clous_al(img1: ndarray, img2: ndarray, clou_dep, l_clous_img2 :list):
    """Calcul quel clou reduis le plus l'erreur moyenne"""
    lst_c_al = liste_clous_al(l_clous_img2, 50)
    zones = lst_zone(img1)
    erreur_dep = erreur(img1, img2, zones, 10)
    nv_erreur = erreur_dep
    i = 0
    clou = lst_c_al[0]
    while i < len(lst_c_al):
        img_temp = deepcopy(img2)
        clou_arr = lst_c_al[i]
        img_temp = tracer_droite(clou_dep, clou_arr, img_temp)
        erreur_temp = erreur(img1, img_temp, zones, 10)
        if erreur_temp < nv_erreur:
            nv_erreur = erreur_temp
            clou = clou_arr
        i += 1
    return (clou, nv_erreur)

def tracer_image(img1: ndarray, img2: ndarray, clou_dep, l_clous_img2 :list):
    """Fais un filage de la première image sur la deuxième image qui est blanche."""
    compteur = 0
    zones = lst_zone(img1)
    erreur_d = erreur(img1, img2, zones, 10)
    derniere_erreur = erreur_d
    droites_tracees = 0
    while compteur < 8 and droites_tracees < 100: 
        res = teste_5_clous_al(img1, img2, clou_dep, l_clous_img2)
        clou_arr = res[0]
        derniere_erreur = res[1]
        img2 = tracer_droite(clou_dep, clou_arr, img2)
        if derniere_erreur >= erreur_d:
            compteur += 1
        droites_tracees = droites_tracees + 1
        clou_dep = clou_arr
    return img2





### Tests (à nettoyer) ###

image = import_image("images/cercle.jpg")
# print(image)
# print(len(image))
# print(len(image[0]))

image_blanche = tab_image_blanche(get_longueur_img(image), get_hauteur_img(image))

image_noir = tab_image_noir(get_longueur_img(image), get_hauteur_img(image))

img = Image.fromarray(uint8(image_blanche))

for i in range(0, 50):
    for j in range(0, 50):
            image_blanche = assombrir_pixel(image_blanche, i, j)

img = Image.fromarray(uint8(image_blanche))
#img.show()

#print(image_blanche)

clous = generer_clous(image_blanche)
#print(clous)

test = tab_image_blanche(1000, 1000)
c = generer_clous(test)

for i in range(0, len(c)):
    test = assombrir_pixel(test, c[i][0], c[i][1])
test = tracer_droite(c[35], c[321], test)

im_test = Image.fromarray(uint8(test))
im_test.show()

l_zones = lst_zone(image)
# print(erreur_moyenne_zone(image, image_blanche,l_zones[500],10))

img = tracer_image(image, image_blanche, (0,0,0), clous)

imaaaaaage = Image.fromarray(uint8(img))
imaaaaaage.show()



### TODO ###

# On peut essayer de regarder des clous aléatoire plutôt que de tout tester

# On regarde l'erreur sur la ligne qu'on vient de tracer, en faisant des moyennes par zones

# Pas forcément la même résolution pour le calcul que pour l'image

# Pas forcément mesurer l'erreur d'une bande de quelques pixels au bord si on met les clous dedans
