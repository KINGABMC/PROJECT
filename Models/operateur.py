import os
import random
from Controller.functions import afficher_erreur, afficher_succes, charger_donnees_txt, sauvegarder_donnees_txt

def generer_numero(index, longueur=7):
    """Génère un numéro unique avec un index donné"""
    suffixe = ''.join([str(random.randint(0, 9)) for _ in range(longueur)])
    return f"{index}{suffixe}"

def verifier_connexion(identifiant, pin):
    """Vérifie si l'identifiant et le code PIN sont valides en les comparant avec le fichier gestionnaire.txt"""
    fichier_gestionnaire = os.path.join("BD", "gestionnaire.txt")
    if not os.path.exists(fichier_gestionnaire):
        afficher_erreur(f"Le fichier {fichier_gestionnaire} est introuvable.")
        return False
    try:
        with open(fichier_gestionnaire, "r") as file:
            for ligne in file:
                idt, pn = ligne.strip().split("|")[:2]
                if identifiant == idt and pin == pn:
                    return True
    except Exception as e:
        afficher_erreur(f"Erreur lors de la lecture du fichier {fichier_gestionnaire}: {str(e)}")
    return False

def creer_operateur(nom, index):
    """Crée un nouvel opérateur et l'ajoute dans operateur.txt"""
    operateurs = charger_donnees_txt('BD/operateurs.txt')
    if any(operateur[0] == nom for operateur in operateurs):
        afficher_erreur(f"Un opérateur avec le nom {nom} existe déjà.")
        return

    try:
        with open('BD/operateurs.txt', 'a') as file:
            file.write(f"{nom}|{index}| | |0,0,0\n")

        with open(f"BD/OPERATEURS/{nom}.txt", 'w') as file:
            for _ in range(100):
                numero = generer_numero(index)
                file.write(f"{numero}\n")
        
        afficher_succes(f"Opérateur {nom} créé avec succès et 100 numéros générés.")
    except Exception as e:
        afficher_erreur(f"Erreur lors de la création de l'opérateur {nom}: {str(e)}")
def recuperer_numeros_operateur(operateur):
        """Récupère les numéros associés à un opérateur"""
        try:
            with open(f"BD/OPERATEURS/{operateur}.txt", "r") as file:
                numeros = file.readlines()
            return [numero.strip() for numero in numeros]
        except FileNotFoundError:
            return []

def recuperer_clients():
        """Récupère les clients existants"""
        try:
            with open("BD/clients.txt", "r") as file:
                clients = file.readlines()
            return [client.split(",")[0].strip() for client in clients]
        except FileNotFoundError:
            return []

def ajouter_client(numero, nom_client):
        """Ajoute un nouveau client au fichier client.txt"""
        with open("BD/client.txt", "a") as file:
            file.write(f"{numero},{nom_client},0,0000\n")

def lister_operateurs():
    """ Liste tous les opérateurs et leurs index """
    operateurs = charger_donnees_txt('BD/operateurs.txt') 
    
    result = []
    for operateur in operateurs:

        if len(operateur) >= 2:
            index = operateur[1].strip()  
            nom = operateur[0].strip()  
            result.append([nom, index])  
    
    return result

def lister_numeros_operateur(nom):
    """Liste les numéros d'un opérateur"""
    try:
        if not os.path.exists(f"{nom}.txt"):
            afficher_erreur(f"Le fichier de l'opérateur {nom} est introuvable.")
            return []
        
        with open(f"{nom}.txt", 'r') as file:
            numeros = file.readlines()
        return [num.strip() for num in numeros]
    except Exception as e:
        afficher_erreur(f"Erreur lors de la lecture des numéros de l'opérateur {nom}: {str(e)}")
        return []

def vendre_numero(operateur, numero):
    """Vente d'un numéro à un client et mise à jour du fichier"""
    try:
        if not os.path.exists(f"{operateur}.txt"):
            afficher_erreur(f"Fichier de l'opérateur {operateur} introuvable.")
            return
        
        with open(f"{operateur}.txt", 'r') as file:
            numeros = file.readlines()
        numeros = [num.strip() for num in numeros]
        
        if numero in numeros:
            numeros.remove(numero)
            with open(f"{operateur}.txt", 'w') as file:
                for num in numeros:
                    file.write(f"{num}\n")
            afficher_succes(f"Numéro {numero} vendu avec succès.")
        else:
            afficher_erreur(f"Le numéro {numero} n'appartient pas à l'opérateur {operateur}.")
    except Exception as e:
        afficher_erreur(f"Erreur lors de la vente du numéro {numero} : {str(e)}")

def ajouter_index(operateur, index):
    """Ajoute un nouvel index pour un opérateur existant"""
    operateurs = charger_donnees_txt('operateur.txt')
    for i, oper in enumerate(operateurs):
        if oper[0] == operateur:
            if index not in oper[1]:
                oper[1] += f",{index}"
                operateurs[i] = oper
                sauvegarder_donnees_txt('operateur.txt', operateurs)
                afficher_succes(f"Index {index} ajouté avec succès pour l'opérateur {operateur}.")
                return
            afficher_erreur(f"L'index {index} existe déjà pour l'opérateur {operateur}.")
            return
    afficher_erreur(f"Opérateur {operateur} non trouvé.")

def etat_caisse(operateur, periode="jour"):
    """Affiche l'état de la caisse d'un opérateur pour la période demandée"""
    operateurs = charger_donnees_txt('operateur.txt')
    for oper in operateurs:
        if oper[0] == operateur:
            if periode == "jour":
                afficher_succes(f"État du jour : {oper[4][2]}")
                return
            elif periode == "mois":
                afficher_succes(f"État du mois : {oper[4][1]}")
                return
            elif periode == "annee":
                afficher_succes(f"État de l'année : {oper[4][0]}")
                return
    afficher_erreur(f"Opérateur {operateur} non trouvé.")
