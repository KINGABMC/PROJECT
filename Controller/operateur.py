import tkinter as tk
from Models.operateur import *

def deconnexion(root):
 from Views.functions import menu_principal

 if root:
        root.quit() 
        root.destroy()  


 menu_principal()

class OperateurController:
    def __init__(self, root):
        from Views.operateur import OperateurView
        self.view = OperateurView(root, self)
    
    def creer_operateur(self, nom, index):
        """Appelle la méthode de création d'un opérateur du modèle"""
        creer_operateur(nom, index)

    def renommer_operateur(self, ancien_nom, nouveau_nom):
        """Renomme un opérateur"""
        operateurs = charger_donnees_txt('BD/operateurs.txt')
        for operateur in operateurs:
            if operateur[0] == ancien_nom:
                operateur[0] = nouveau_nom
                sauvegarder_donnees_txt('BD/operateurs.txt', operateurs)
                afficher_succes("Opérateur renommé avec succès.")
                return
        afficher_erreur("Opérateur non trouvé.")
    def lister_operateurs(self):
        from Models.operateur import lister_operateurs
        return lister_operateurs()

    def get_numeros_operateur(self, operateur):
        from Models.operateur import recuperer_numeros_operateur
        """Appelle le modèle pour récupérer les numéros de l'opérateur"""
        return recuperer_numeros_operateur(operateur)

    def get_clients(self):
        from Models.operateur import recuperer_clients
        """Appelle le modèle pour récupérer les clients"""
        return recuperer_clients()

    def ajouter_client(self, numero, nom_client):
        from Models.operateur import ajouter_client
        ajouter_client(numero, nom_client)

    def etat_caisse(self, operateur, periode):
        """Affiche l'état de la caisse pour un opérateur et une période"""
        etat_caisse(operateur, periode)

    def ajouter_index(self, operateur, index):
        """Ajoute un nouvel index pour un opérateur"""
        ajouter_index(operateur, index)
    
    def verifier_connexion(self, identifiant, pin):
        """Vérifie la connexion avec les identifiants du gestionnaire"""
        if verifier_connexion(identifiant, pin):
            afficher_succes("Bienvenue🤗")
        else:
            afficher_erreur("Identifiant ou PIN incorrect.")


def connexion_gestionnaire(root):
    from Views.operateur import OperateurView
    from Controller.functions import valider_nom, valider_code_pin
    def valider_connexion():
        identifiant = entry_identifiant.get()
        pin = entry_pin.get()

    
        label_message.config(text="", fg="red")

        if not valider_code_pin(pin):
            label_message.config(text="L'identifiant doit être entre 8 et 16 caractères alphanumériques ")
            return
        if not valider_nom(identifiant):
            label_message.config(text="le PIN doit comporter 4 chiffres.")
            return

       
        if verifier_connexion(identifiant, pin):
            root.withdraw()  
            controller=OperateurController(root)
            gestionnaire_window = tk.Toplevel(root)
            app = OperateurView(gestionnaire_window,controller) 
            connexion_window.destroy() 
        else:
            label_message.config(text="Identifiant ou code PIN incorrect.")


    connexion_window = tk.Toplevel(root)
    connexion_window.title("Connexion Gestionnaire")
    connexion_window.geometry("300x250")
    connexion_window.resizable(False, False)

    label_identifiant = tk.Label(connexion_window, text="Identifiant:")
    label_identifiant.pack(pady=5)

    entry_identifiant = tk.Entry(connexion_window)
    entry_identifiant.pack(pady=5)

    label_pin = tk.Label(connexion_window, text="Code PIN:")
    label_pin.pack(pady=5)

    entry_pin = tk.Entry(connexion_window, show="*")  
    entry_pin.pack(pady=5)

    label_message = tk.Label(connexion_window, text="", fg="red")
    label_message.pack(pady=5)


    btn_valider = tk.Button(connexion_window, text="Se connecter", command=valider_connexion)
    btn_valider.pack(pady=15)

    
    def annuler_connexion():
        connexion_window.destroy()
        root.deiconify() 

    btn_annuler = tk.Button(connexion_window, text="Annuler", command=annuler_connexion)
    btn_annuler.pack(pady=5)

 
    connexion_window.mainloop()
