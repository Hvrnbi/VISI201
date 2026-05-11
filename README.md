# Filage d'image et tracé de droites pour un rendu artistique

## Présentation

Bienvenue dans le répertoire de cette implémentation en Python d'un algorithme de filage d'image.

Ce projet a été réalisé dans le cadre du cours [VISI201](http://os-vps418.infomaniak.ch:1250/mediawiki/index.php/VISI201_CMI_:_visite_de_laboratoire) dispensé à l'[Université Savoie Mont Blanc](https://www.univ-smb.fr) aux élèves du cursus [CMI Informatique](https://formations.univ-smb.fr/fr/catalogue/licence-XA/cursus-master-en-ingenierie-informatique-KHXGP1NK.html).

Pour des informations complémentaires, vous pouvez consulter [cette page de wiki](http://os-vps418.infomaniak.ch:1250/mediawiki/index.php/Filage_d'image_et_trac%C3%A9_de_droites_pour_un_rendu_artistique)


## Utilisation

### Prérequis

Pour utiliser ce programme, assurez vous que [Python](https://www.python.org/) est installé correctement sur votre machine. La compatibilité avec des versions autres que Python 3.13 n'a pas été testée.
L'installation de [git](https://git-scm.com/) est également recommandée pour télécharger simplement ce répertoire.

Si vous utilisez Linux, vérifiez que votre distribution de Python contient pip ainsi que les environnements virtuels, qui ne sont pas toujours inclus par défaut.
Sous Debian Trixie par exemple, vous aurez besoin des packages python3-venv et python3-pip, disponibles via apt.

### Exécution

- Ouvrez votre terminal et placez vous dans le répertoire de votre choix.
- Clonez ce répertoire à l'aide de la commande ```git clone  https://github.com/Hvrnbi/VISI201```
- Déplacez vous dans le répertoire du projet avec la commande ```cd VISI201```
- Créez un environnement virtuel Python avec la commande ```python3 -m venv .venv``` ou ```python -m venv .venv``` si vous utilisez Windows.
- Installez les dépendances Python avec la commande ```.venv/bin/pip install -r requirements.txt``` ou ```.venv\Scripts\pip install -r requirements.txt``` si vous utilisez Windows
- Créez le dossier qui accueillera les images résultats avec la commande ```mkdir resultats```
- Ouvrez la console python avec la commande ```.venv/bin/python3```  ou ```.venv\Scripts\python```
- Importez la fonction filage_image depuis la console Python ```from main import filage_image```
- Enfin, lancez la fonction avec la commande Python suivante : ```filage_image("CHEMIN_VERS_L_IMAGE_DE_DEPART", "NOM_DE_L_IMAGE_DE_SORTIE", options...)``` La liste des options est disponible ci_dessous.

### Options

Voici la liste des options de la fonction Python filage_image :
- chemin_img_source, une chaîne de caractère indiquant le chemin absolu ou relatif vers l'image originale. L'extension est à préciser ! **OBLIGATOIRE**
- nom_img_sortie, une chaine de caractère qui correspond au nom sous lequel sera sauvegardée l'image résultat. L'extension peut être précisée grâce au paramètre format_sortie. **OBLIGATOIRE**
- format_sortie, une chaine de caractère qui correspond au format de l'image de sortie. Les valeurs possibles sont 'svg' (par défaut), 'png', 'jpg', 'png+svg' et 'jpg+svg'.
- resize, un tuple qui définit les dimenssions de l'image de sortie. Le tuple (0, 0) (la valeur par défaut) utilise les dimensions de l'image originale.
- placement_clous, une chaine de caractère qui définit le mode de placement des clous sur l'image. Les valeurs possibles sont 'laplacien' (par défaut), 'bords', 'classique', 'aleatoire' et 'random'. 'classique' est un alias de 'bords', et 'random' un alias de 'aleatoire'.
- nombre_clous, un entier qui correspond au nombre de clous si le mode de placement de clous sélectionné est le laplacien, aleatoire ou random. La valeur par défaut est 100.
- couleur_traits: une chaine de caractère qui définit la couleur des traits, et donc celle du fond, qui sera la couleur opposée. Les valeurs possibles sont 'noir' (par défaut) et 'blanc'.
- affiche_infos: un booléen qui active l'affichage de la réduction de l'erreur et des coordonnées des droites tracées lorsqu'il est vrai (vrai par défaut).


## Exemples

Des exemples sont disponibles [ici](http://os-vps418.infomaniak.ch:1250/mediawiki/index.php/Filage_d'image_et_trac%C3%A9_de_droites_pour_un_rendu_artistique#R%C3%A9sultats_finaux)

