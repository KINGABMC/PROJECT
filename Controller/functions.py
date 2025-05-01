from Views.functions import afficher_erreur, afficher_succes
import random




def charger_donnees_txt(fichier):
    """Charge les données depuis un fichier texte (.txt)."""
    try:
        with open(fichier, 'r') as file:
            lignes = file.readlines()
            donnees = [ligne.strip().split('|') for ligne in lignes]
            return donnees
    except FileNotFoundError:
        afficher_erreur(f"Fichier {fichier} introuvable.")
        return []
    except Exception as e:
        afficher_erreur(f"Erreur : {str(e)}")
        return []

def sauvegarder_donnees_txt(fichier, donnees):
    """Sauvegarde les données dans un fichier texte (.txt)."""
    try:
        with open(fichier, 'w') as file:
            for ligne in donnees:
                file.write('|'.join(ligne) + '\n')
        afficher_succes("Données sauvegardées avec succès.")
    except Exception as e:
        afficher_erreur(f"Erreur lors de la sauvegarde : {str(e)}")

def valider_nom(nom):
    """
    Vérifie si un nom est valide :
    - Doit être une chaîne de caractères
    - Doit comporter entre 3 et 15 caractères

    Args:
        nom (str): Le nom à valider.

    Returns:
        bool: True si le nom est valide, False sinon.
    """
   
    if not isinstance(nom, str):
        afficher_erreur("Le nom doit être une chaîne de caractères.")
        return False

    if 3 <= len(nom) <= 15:
        return True

    afficher_erreur("Le nom doit comporter entre 3 et 15 caractères.")
    return False


def valider_index(index):
    """Vérifie si un index est valide (2 chiffres)."""
    if len(index) == 2 and index.isdigit():
        return True
    afficher_erreur("L'index doit comporter 2 chiffres.")
    return False

def valider_numero(numero):
        """Validation du numéro (doit commencer par 76, 77 ou 70 et faire 9 chiffres)."""
        if len(numero) == 9 and numero.isdigit() and numero[:2] in ['76', '77', '70']:
            return numero
def valider_code_pin(pin):
        return pin.isdigit() and len(pin) == 4

def generer_numero(index, longueur=7):
    """Génère un numéro unique avec un index donné."""
    suffixe = ''.join([str(random.randint(0, 9)) for _ in range(longueur)])
    return f"{index}{suffixe}"

def verifier_unicite(liste, valeur):
    """Vérifie si une valeur est unique dans une liste."""
    return valeur not in liste
