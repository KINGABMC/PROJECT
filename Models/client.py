import os
from Controller.functions import afficher_erreur
from datetime import datetime



class ClientModel:
    def __init__(self):
        self.client_file = "BD/clients.txt"
        self.historique_dir = "BD/historiques"
        self.repertoire_dir = "BD/repertoires"
        os.makedirs(self.historique_dir, exist_ok=True)
        os.makedirs(self.repertoire_dir, exist_ok=True)

    def chercher_client(self, numero):
        with open(self.client_file, "r") as file:
            for line in file:
                num, nom, credit, pin = line.strip().split(",")
                if num == numero:
                    return [num, nom, int(credit), pin]
        return None

    def ajouter_contact(self, numero_client, nom, numero):
        """
        Ajoute un contact dans le fichier correspondant au client.
        
        Args:
            numero_client (str): Le numéro du client pour identifier le fichier.
            nom (str): Le nom complet du contact (peut inclure des espaces).
            numero (str): Le numéro de téléphone du contact.
        """
        file_path = f"{self.repertoire_dir}/{numero_client}.txt"
    
        
        contact_ligne = f"{nom},{numero}\n"
        
        with open(file_path, "a") as file:
            file.write(contact_ligne)

    def lire_historique(self, numero_client):
        file_path = f"{self.historique_dir}/{numero_client}.txt"
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as file:
            return [line.strip().split(",") for line in file]

    def lire_repertoire(self, numero):
        file_path = f"{self.repertoire_dir}/{numero}.txt"
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as file:
            return [line.strip().split(",") for line in file]

    def enregistrer_appel(self, numero_client, numero_contact):
        file_path = f"{self.historique_dir}/ecrit/{numero_client}.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(file_path, "a") as file:
            file.write(f"{numero_contact},{timestamp}\n")

    def supprimer_contact(self, numero_client, nom_contact):
        """Supprimer un contact du fichier"""
        file_path = f"{self.repertoire_dir}/{numero_client}.txt"
        
        if not os.path.exists(file_path):
            return False  
        
    
        with open(file_path, "r") as file:
            lines = file.readlines()
        
       
        updated_lines = [line for line in lines if not line.startswith(nom_contact)]
        
       
        if len(updated_lines) < len(lines):
            with open(file_path, "w") as file:
                file.writelines(updated_lines)
            return True
        return False


    def modifier_contact(self, numero_client, old_nom, new_nom, new_numero):
        """Modifier un contact dans le fichier"""
        file_path = f"{self.repertoire_dir}/{numero_client}.txt"
        
        if not os.path.exists(file_path):
            return False  
        
     
        with open(file_path, "r") as file:
            lines = file.readlines()
        
 
        updated_lines = []
        for line in lines:
            nom, numero = line.strip().split(",")
            if nom == old_nom:
                updated_lines.append(f"{new_nom},{new_numero}\n")  
                updated_lines.append(line) 
        
        with open(file_path, "w") as file:
            file.writelines(updated_lines)
        return True






def verifier_connexion(numero, pin):
    """Vérifie si le numéro de téléphone et le code PIN sont valides en les comparant avec le fichier client.txt"""
   
    fichier_client = os.path.join("BD", "clients.txt")
    try:
        with open(fichier_client, "r") as file:
            for ligne in file:
                
                num, nom, solde, stored_pin = ligne.strip().split(",")
                print(f"Comparaison : {num} == {numero} et {stored_pin} == {pin}") 
                if num == numero and stored_pin == pin:
                    return True
    except FileNotFoundError:
        afficher_erreur("Le fichier des clients est introuvable.")
    return False
