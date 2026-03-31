### Modules ###

from PIL import Image
from numpy import asarray, ndarray, array, uint8, delete
from random import choices
from copy import deepcopy


### Fonctions ###

def import_image(chemin: str, resize: bool = False) -> ndarray :
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

    if resize:
        image = image.resize((256, 256))


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

def tracer_droite(clou1: tuple, clou2: tuple, image: ndarray) -> ndarray:
    """Trace une droite d'un clou à un autre."""
    if visible(clou1, clou2):
        liste_points = liste_points_traverses(clou1[0], clou1[1], clou2[0], clou2[1])
        
        for i in range(0, len(liste_points)):
            ligne = liste_points[i][1]
            col = liste_points[i][0]
            image = assombrir_pixel(image, ligne, col)

    return image

def liste_points_traverses(x1: int, y1: int, x2: int, y2: int) -> list:
    """Renvoie les points que le segment [(x1, y1), (x2, y2)] traverse"""
    liste_res = []
    a, b = calcul_droite(x1, y1, x2, y2)

    # Si l'angle entre l'axe des abscisses et la droite est compris entre -45° et 45°
    if -1 <= a <= 1:
        if x1 > x2:
            # On cherche y pour chaque x, donc on commence du point dont le x est le plus proche de 0
            x1, y1, x2, y2 = x2, y2, x1, y1

        x = x1 + 1
        y = y1
        liste_res.append((x1, y))

        while x <= x2:
            y = round(a * x + b)
            liste_res.append((x, y))
            x += 1

    else:
        if y1 > y2:
            # On cherche x pour chaque y, donc on commence du point dont le y est le plus proche de 0
            x1, y1, x2, y2 = x2, y2, x1, y1

        if a != 999999999 and b != 999999999:
            x = x1
            y = y1 + 1
            liste_res.append((x, y1))
            while y <= y2:
                x = round((y - b) / a)
                liste_res.append((x, y))
                y += 1

        # Gestion des droites verticales
        else:
            x = x1
            y = y1 + 1
            liste_res.append((x, y1))
            for i in range(y, y2 + 1):
                liste_res.append((x, i))
    
    return liste_res


def calcul_droite(x1: int, y1: int, x2: int, y2: int) -> tuple:
    """Renvoie le coefficient directeur et l'ordonnée à l'origine de la droite passant par (x1, y1) et (x2, y2)"""

    if x1 != x2:
        a = (y2 - y1) / (x2 - x1)
        b = y1 - x1 * a

    # Gestion des droites verticales
    else:
        a = 999999999
        b = 999999999

    return (a, b)


def liste_clous_al(liste_clous : list, taille_l : int) -> list:
    """On créer une liste de clou choisis aléatoirement"""
    lst_res = choices(liste_clous, k=taille_l)
    return lst_res


def reduction_erreur_droite(x1: int, x2: int, y1: int, y2: int, img1:  ndarray, img2: ndarray) -> float:
    """Renvoie la différence entre l'erreur de l'image cible et de l'image actuelle, et l'erreur de l'image cible et de l'image actuelel si on traçait la droite donnée"""
    lst_pts = liste_points_traverses(x1, x2, y1, y2)
    err_act = 0
    nb_pts = len(lst_pts)

    if (x1 == 0 and x2 == 0) or (x1 == get_longueur_img(img2) and x2 == get_longueur_img(img2)) or (y1 == 0 and y2 == 0) or (y1 == get_hauteur_img(img2) and y2 == get_hauteur_img(img2)):
        return 999999999

    for i in range(0, nb_pts):
        err_act += erreur_point(lst_pts[i], img1, img2)

    new_err = 0

    for i in range(0, nb_pts):
        new_err += erreur_point_trace(lst_pts[i], img1, img2)
    
    return (new_err - err_act) / nb_pts


def erreur_point(p: tuple, img1: ndarray, img2: ndarray):
    """Renvoie la différence entre la valeur du pixel sur l'image 1 et la valeur du pixel sur l'image 2"""
    return abs(img1[p[1]][p[0]] - img2[p[1]][p[0]])


def erreur_point_trace(p: tuple, img1: ndarray, img2: ndarray):
    """Renvoie la différence entre la valeur du pixel sur l'image 1 et la valeur du pixel sur l'image 2 lorsqu'on assombrit ce pixel"""
    if img2[p[1]][p[0]] >= 51:
        return abs(img1[p[1]][p[0]] - img2[p[1]][p[0]] + 51)
    else:
        return erreur_point(p, img1, img2)


def trouve_meilleure_droite(img1: ndarray, img2: ndarray, clou_dep: tuple, lst_clous: list) -> tuple:
    """Renvoie le clou dont la droite le traversant lui et le clou de départ réduit le plus l'erreur entre les deux images"""
    liste_c = liste_clous_al(lst_clous, len(lst_clous) // 2)
    liste_red_err = []

    for i in range(0, len(liste_c)):
        liste_red_err.append(reduction_erreur_droite(clou_dep[0], clou_dep[1], liste_c[i][0], liste_c[i][1], img1, img2))
    
    red_err = min(liste_red_err)
    meilleur_clou = liste_c[liste_red_err.index(red_err)]

    return (meilleur_clou, red_err)


def retrace_image(chemin_img_source: str, nom_image_sortie: str, resize: bool = False):
    """Retrace l'image donnée avec des fils et sauvegarde dans le dossier resultat, au chemin donné"""
    image = import_image(chemin_img_source, resize)

    new_img = tab_image_blanche(get_longueur_img(image), get_hauteur_img(image))

    clous = generer_clous(new_img)

    clou_dep = clous[0]
    cpt_augmentation_err = 0
    cpt_droites = 0

    while cpt_augmentation_err < 2:
        meilleur_clou, reduction_err = trouve_meilleure_droite(image, new_img, clou_dep, clous)
        new_img = tracer_droite(clou_dep, meilleur_clou, new_img)
        clou_dep = meilleur_clou
        cpt_droites += 1

        if reduction_err >= 0:
            cpt_augmentation_err += 1

    print(cpt_droites)

    image_res = Image.fromarray(uint8(new_img))
    image_res.save("resultat/" + nom_image_sortie + ".png")



### Tests ###

retrace_image("images/losa.jpg", "losa-egzbogez")


### TODO ###

# Pas forcément mesurer l'erreur d'une bande de quelques pixels au bord si on met les clous dedans
