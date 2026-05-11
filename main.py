### Modules ###

from PIL import Image, ImageFilter
from numpy import asarray, ndarray, array, uint8, delete
from random import choices, randint, random
from copy import deepcopy
import drawsvg as dw


### Fonction pour importer une image ###

def import_image(chemin: str, resize: tuple = (0, 0), lap: bool = False) -> ndarray :
    """Charge l'image donnée, la passe en nuances de gris, et la convertit en tableau (de numpy)"""

    ## Chargement de l'image ## 

    # gestion des chemins d'accès Windows avec les supers \
    if chemin[:2] in ("c:\\", "C:\\"):
        chemin.encode('unicode_escape')

    # On essaie d'ouvrir l'image avec la librairie PIL
    try:
        image = Image.open(chemin)

    # Gestion d'erreur si le fichier n'est pas accessible ou n'existe pas 
    except FileNotFoundError:
        print("Le chemin d'accès est invalide.")
        return asarray([[]])
    
    # Gestion d'erreur dans les autres cas
    except:
        print("Une erreur s'est produite")
        return asarray([[]])

    ## Conversion de l'image en nuances de gris ##

    # On utilise la méthode .convert() de PIL
    image = image.convert("L")

    if resize != (0, 0):
        image = image.resize(resize)

    if lap:
        image = image.filter(ImageFilter.FIND_EDGES)


    ## Conversion en tableau ##

    # On utilise la fonction asarrray() de numpy
    image_array = asarray(image)

    return image_array


### Fonctions pour générer des matrice-images vierges ###
    
def tab_image_blanche(longueur: int, hauteur: int) -> ndarray:
    """Génère un tableau contenant des pixels blancs avec les dimensions données"""
    # On crée autant de lignes que de pixels de hauteur, et autant de pixels que de hauteur
    tab = [ [255] * longueur] * hauteur
    return array(tab)


def tab_image_noire(longueur: int, hauteur: int) -> ndarray:
    """Génère un tableau contenant des pixels noirs avec les dimensions données"""
    # On crée autant de lignes que de pixels de hauteur, et autant de pixels que de hauteur
    tab = [ [0] * longueur] * hauteur
    return array(tab)

# On l'utilise pas finalement mais on la laisse pour la postérité
def tab_image_grise(longueur: int, hauteur: int) -> ndarray:
    """Génère un tableau contenant des pixels gris avec les dimensions données"""
    # On crée autant de lignes que de pixels de hauteur, et autant de pixels que de hauteur
    tab = [ [127] * longueur] * hauteur
    return array(tab)


### Fonctions pour récupérer les dimensions d'une matrice-image ###
    
def get_longueur_img(tab_img: ndarray) -> int:
    """Renvoie la longueur du tableau à deux dimensions (représentant une image) donné"""
    return len(tab_img[0])


def get_hauteur_img(tab_img: ndarray) -> int:
    """Renvoie la hauteur du tableau à deux dimensions (représentant une image) donné"""
    return len(tab_img)


### Fonctions pour modifier la valeur des pixels ###

def assombrir_pixel(tab_img: ndarray, ligne: int, colonne: int) -> ndarray:
    """Réduit de 51 (parce que c'est 255/5) les valeurs des couleurs du pixel à la position donnée."""
    if tab_img[ligne][colonne] >= 51:
        tab_img[ligne][colonne] = tab_img[ligne][colonne] - 51

    return tab_img


def eclaircir_pixel(tab_img: ndarray, ligne: int, colonne: int) -> ndarray:
    """Augmente de 51 (parce que c'est 255/5) les valeurs des couleurs du pixel à la position donnée."""
    if tab_img[ligne][colonne] <= 214:
        tab_img[ligne][colonne] += 51

    return tab_img


### Fonctions pour générer des clous ###

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


def generer_clous_plus_clous_aleatoires(tab_img: ndarray, nombre_clous: int):
    """Génère un tableau de clous classiques (cf generer_clous) + des clous aleatoires au milieu de l'image"""
    h = get_hauteur_img(tab_img)
    l = get_longueur_img(tab_img)

    liste_res = generer_clous(tab_img)

    for i in range(nombre_clous):
        liste_res.append((randint(20, l - 20), randint(20, h - 20), i + 4))
    
    return liste_res


### Fonctions pour tracer des droites ###

def visible(clou1: tuple, clou2: tuple) -> bool:
    """Renvoie True si les clous se voient, False sinon"""
    return clou1[2] != clou2[2]


def tracer_droite(clou1: tuple, clou2: tuple, image: ndarray) -> ndarray:
    """Trace une droite noire d'un clou à un autre."""
    if visible(clou1, clou2):
        liste_points = liste_points_traverses(clou1[0], clou1[1], clou2[0], clou2[1])
        
        for i in range(0, len(liste_points)):
            ligne = liste_points[i][1]
            col = liste_points[i][0]
            image = assombrir_pixel(image, ligne, col)

    return image


def tracer_droite_blanche(clou1: tuple, clou2: tuple, image: ndarray) -> ndarray:
    """Trace une droite blanche d'un clou à un autre."""
    if visible(clou1, clou2):
        liste_points = liste_points_traverses(clou1[0], clou1[1], clou2[0], clou2[1])
        
        for i in range(0, len(liste_points)):
            ligne = liste_points[i][1]
            col = liste_points[i][0]
            image = eclaircir_pixel(image, ligne, col)

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


### Fonctions pour les calculs de différence d'erreur entre deux images ###

def reduction_erreur_droite(clou_dep: tuple, clou_arr: tuple, img1: ndarray, img2: ndarray) -> float:
    """Renvoie la différence entre l'erreur de l'image cible et de l'image actuelle, et l'erreur de l'image cible et de l'image actuelel si on traçait la droite noire donnée"""
    
    if not visible(clou_dep, clou_arr):
        return 999999999
    

    lst_pts = liste_points_traverses(clou_dep[0], clou_dep[1], clou_arr[0], clou_arr[1])
    err_act = 0
    nb_pts = len(lst_pts)

    for i in range(0, nb_pts):
        err_act += erreur_point(lst_pts[i], img1, img2)

    new_err = 0

    for i in range(0, nb_pts):
        new_err += erreur_point_assombri(lst_pts[i], img1, img2)
    
    return (new_err - err_act) / nb_pts


def reduction_erreur_droite_blanche(clou_dep: tuple, clou_arr: tuple, img1: ndarray, img2: ndarray) -> float:
    """Renvoie la différence entre l'erreur de l'image cible et de l'image actuelle, et l'erreur de l'image cible et de l'image actuelel si on traçait la droite blanche donnée"""
    
    if not visible(clou_dep, clou_arr):
        return 999999999
    

    lst_pts = liste_points_traverses(clou_dep[0], clou_dep[1], clou_arr[0], clou_arr[1])
    err_act = 0
    nb_pts = len(lst_pts)

    for i in range(0, nb_pts):
        err_act += erreur_point(lst_pts[i], img1, img2)

    new_err = 0

    for i in range(0, nb_pts):
        new_err += erreur_point_eclairci(lst_pts[i], img1, img2)
    
    return (new_err - err_act) / nb_pts


def erreur_point(p: tuple, img1: ndarray, img2: ndarray):
    """Renvoie la différence entre la valeur du pixel sur l'image 1 et la valeur du pixel sur l'image 2"""
    return abs(img1[p[1]][p[0]] - img2[p[1]][p[0]])


def erreur_point_assombri(p: tuple, img1: ndarray, img2: ndarray):
    """Renvoie la différence entre la valeur du pixel sur l'image 1 et la valeur du pixel sur l'image 2 lorsqu'on assombrit ce pixel"""
    if img2[p[1]][p[0]] >= 51:
        return abs(img1[p[1]][p[0]] - img2[p[1]][p[0]] + 51)
    else:
        return erreur_point(p, img1, img2)


def erreur_point_eclairci(p: tuple, img1: ndarray, img2: ndarray):
    """Renvoie la différence entre la valeur du pixel sur l'image 1 et la valeur du pixel sur l'image 2 lorsqu'on éclaircit ce pixel"""
    if img2[p[1]][p[0]] <= 51:
        return abs(img1[p[1]][p[0]] - img2[p[1]][p[0]] - 51)
    else:
        return erreur_point(p, img1, img2)


def trouve_meilleure_droite(img1: ndarray, img2: ndarray, clou_dep: tuple, lst_clous: list) -> tuple:
    """Renvoie le clou dont la droite le traversant lui et le clou de départ réduit le plus l'erreur entre les deux images"""
    liste_c = liste_clous_al(lst_clous, len(lst_clous) // 2)
    liste_red_err = []

    for i in range(0, len(liste_c)):
        liste_red_err.append(reduction_erreur_droite(clou_dep, liste_c[i], img1, img2))
    
    red_err = min(liste_red_err)
    meilleur_clou = liste_c[liste_red_err.index(red_err)]

    return (meilleur_clou, red_err)


def trouve_meilleure_droite_blanche(img1: ndarray, img2: ndarray, clou_dep: tuple, lst_clous: list) -> tuple:
    """Renvoie le clou dont la droite blanche le traversant lui et le clou de départ réduit le plus l'erreur entre les deux images"""
    liste_c = liste_clous_al(lst_clous, len(lst_clous) // 2)
    liste_red_err = []

    for i in range(0, len(liste_c)):
        liste_red_err.append(reduction_erreur_droite_blanche(clou_dep, liste_c[i], img1, img2))
    
    red_err = min(liste_red_err)
    meilleur_clou = liste_c[liste_red_err.index(red_err)]

    return (meilleur_clou, red_err)


### Fonctions pour le laplacien ###

def generer_clous_lap(tab_img: ndarray, nombre_clous: int) -> list:
    """Génère un tableau qui contient des tuples qui représentent des clous : deux coordonnées et un numéro de côté"""
    liste_res = []
    
    # On crée la matrice qui contient pour chaque pixel, la somme de sa valeur et de celle de tous les pixels d'avant
    tab_somme = somme_cumulative_matrice(tab_img)
    # Le dernier élément est la somme de la valeur de tous les pixels
    somme_valeurs_px = tab_somme[-1][-1]

    for i in range(nombre_clous):
        nb_rd = random() * somme_valeurs_px
        pixel = trouve_pixel(tab_somme, nb_rd)
        clou = (pixel[1], pixel[0], i)
        liste_res.append(clou)
        

    return liste_res


def somme_cumulative_matrice(tab: ndarray) -> list:
    """Renvoie la somme cumulative de la matrice"""
    liste_res = []

    for i in range(len(tab)):
        liste_res.append([])
        for j in range(len(tab[i])):
            if j == 0:
                if i == 0:
                    liste_res[i].append(int(tab[i][j]) ** 2)
                else:
                    liste_res[i].append(int(tab[i][j]) ** 2 + liste_res[i - 1][-1])
            else:
                liste_res[i].append(int(tab[i][j]) ** 2 + liste_res[i][j - 1])

    return liste_res
    

def trouve_pixel(tab: list, nb: float) -> tuple:
    """Renvoie les coordonnées du premier nombre dans la matrice qui est plus grand que le nombre donné"""
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            if tab[i][j] >= nb:
                return (i, j)



### Fonction principale ###

def filage_image(chemin_img_source: str, nom_img_sortie: str, format_sortie: str = "svg", resize: tuple = (0, 0), placement_clous: str = "laplacien", nombre_clous: int = 100, couleur_traits: str = "noir", affiche_infos: bool = True):
    """
    Retrace l'image donnée en source comme si elle était filée sur une planche avec des clous.

    Entrées :   chemin_img_source, une chaîne de caractère indiquant le chemin absolu ou relatif vers l'image originale. L'extension est à préciser !
                nom_img_sortie, une chaine de caractère qui correspond au nom sous lequel sera sauvegardée l'image résultat. L'extension peut être précisée grâce au paramètre format_sortie.
                format_sortie, une chaine de caractère qui correspond au format de l'image de sortie. Les valeurs possibles sont 'svg' (par défaut), 'png', 'jpg', 'png+svg' et 'jpg+svg'.
                resize, un tuple qui définit les dimenssions de l'image de sortie. Le tuple (0, 0) (la valeur par défaut) utilise les dimensions de l'image originale.
                placement_clous, une chaine de caractère qui définit le mode de placement des clous sur l'image. Les valeurs possibles sont 'laplacien' (par défaut), 'bords', 'classique', 'aleatoire' et 'random'. 'classique' est un alias de 'bords', et 'random' un alias de 'aleatoire'.
                nombre_clous, un entier qui correspond au nombre de clous si le mode de placement de clous sélectionné est le laplacien, aleatoire ou random. La valeur par défaut est 100.
                couleur_traits: une chaine de caractère qui définit la couleur des traits, et donc celle du fond, qui sera la couleur opposée. Les valeurs possibles sont 'noir' (par défaut) et 'blanc'.
                affiche_infos: un booléen qui active l'affichage de la réduction de l'erreur et des coordonnées des droites tracées lorsqu'il est vrai.

    Sortie :    Cette fonction ne renvoie rien, mais elle sauvegarde des fichiers dans le répertoire './resultats'.
    """

    # Import de l'image source
    image = import_image(chemin_img_source, resize)
    
    # Création de l'image de travail et de l'image résultat
    if couleur_traits == "noir":
        new_img = tab_image_blanche(get_longueur_img(image), get_hauteur_img(image))

        if format_sortie in ("svg", "png+svg", "jpg+svg"):
            svg = dw.Drawing(get_longueur_img(image), get_hauteur_img(image))
            svg.append(dw.Rectangle(x=0, y=0, width='100%', height='100%', fill='white'))

    elif couleur_traits == "blanc":
        new_img = tab_image_noire(get_longueur_img(image), get_hauteur_img(image))

        if format_sortie in ("svg", "png+svg", "jpg+svg"):
            svg = dw.Drawing(get_longueur_img(image), get_hauteur_img(image))
            svg.append(dw.Rectangle(x=0, y=0, width='100%', height='100%', fill='black'))

    else:
        print("Cette couleur est invalide. Les couleurs valides sont 'noir' et 'blanc'.")
        return


    # Génération des clous
    if placement_clous == "laplacien":
        image_lap = import_image(chemin_img_source, resize, lap=True)
        clous = generer_clous_lap(image_lap, nombre_clous)

    elif placement_clous in ("bords", "classique"):
        clous = generer_clous(new_img)
    
    elif placement_clous in ("aleatoire", "random"):
        clous = generer_clous_plus_clous_aleatoires(new_img, nombre_clous)

    else:
        print("Cette façon de placer les clous n'existe pas. Les valeurs valides sont 'laplacien', 'bords', 'classique', 'aleatoire' et 'random'.")
        return

    
    # Initialisation des variables de la boucle
    clou_dep = clous[0]
    cpt_augmentation_err = 0
    cpt_droites = 0


    # Boucle
    while cpt_augmentation_err < 3:
        if couleur_traits == "noir":
            meilleur_clou, reduction_err = trouve_meilleure_droite(image, new_img, clou_dep, clous)
        else:
            meilleur_clou, reduction_err = trouve_meilleure_droite_blanche(image, new_img, clou_dep, clous)

        if affiche_infos:
            print(reduction_err, clou_dep, meilleur_clou)

        if reduction_err >= 0:
            cpt_augmentation_err += 1

        else:
            cpt_augmentation_err = 0

        if couleur_traits == "noir":
            new_img = tracer_droite(clou_dep, meilleur_clou, new_img)

            if format_sortie in ("svg", "png+svg", "jpg+svg"):
                svg.append(dw.Line(clou_dep[0], clou_dep[1], meilleur_clou[0], meilleur_clou[1], stroke='black', stroke_opacity=0.2, stroke_width=1))

        else:
            new_img = tracer_droite_blanche(clou_dep, meilleur_clou, new_img)

            if format_sortie in ("svg", "png+svg", "jpg+svg"):
                svg.append(dw.Line(clou_dep[0], clou_dep[1], meilleur_clou[0], meilleur_clou[1], stroke='white', stroke_opacity=0.2, stroke_width=1))

        clou_dep = meilleur_clou
        cpt_droites += 1

    if affiche_infos:
        print(cpt_droites, " droites tracées")

    if format_sortie in ("png", "jpg", "png+svg", "jpg+svg"):
        image_res = Image.fromarray(uint8(new_img))
        
        if format_sortie in ("png", "png+svg"):
            image_res.save("resultats/" + nom_img_sortie + ".png")
        
        else:
            image_res.save("resultats/" + nom_img_sortie + ".jpg")

    if format_sortie in ("svg", "png+svg", "jpg+svg"):
        svg.save_svg("resultats/" + nom_img_sortie + ".svg")


