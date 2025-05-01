import tkinter as tk
from Models.client import verifier_connexion
from Models.client import ClientModel


def deconnexion(root):
 from Views.functions import menu_principal

 if root:
        root.quit()  
        root.destroy()  

 menu_principal()

class ClientController:
    def __init__(self):
        self.model = ClientModel()
    
    
    def supprimer_contact(self, numero_client, nom_contact):
        """Supprime un contact du répertoire du client"""
        success = self.model.supprimer_contact(numero_client, nom_contact)
        return success

    def modifier_contact(self, numero_client, old_nom, new_nom, new_numero):
        """Modifie un contact dans le répertoire du client"""
        success = self.model.modifier_contact(numero_client, old_nom, new_nom, new_numero)
        return success

    def verifier_code_pin(self, numero, code_pin):
        client = self.model.chercher_client(numero)
        return client and client[3] == code_pin

    def consulter_credit(self, numero):
        client = self.model.chercher_client(numero)
        return f"Votre solde est de {client[2]} FCFA" if client else "Client introuvable"

    def effectuer_appel(self, numero_client, numero_contact):
        return self.model.enregistrer_appel(numero_client, numero_contact)

    def lire_repertoire(self, numero_client):
        return self.model.lire_repertoire(numero_client)

    def ajouter_contact(self, numero_client, nom, numero):
        self.model.ajouter_contact(numero_client, nom, numero)

    def lire_historique_appels(self, numero_client):
        return self.model.lire_historique(numero_client)

    def enregistrer_appel(self, numero_client, numero_contact):
        self.model.enregistrer_appel(numero_client, numero_contact)


    def enregistrer_audio(self, file_name, duration=10):
        import sounddevice as sd
        import wave
        rate = 44100  # Fréquence d'échantillonnage
        channels = 1  # Mono
        frames = int(rate * duration)  # Nombre d'échantillons à enregistrer

        # Enregistrement audio avec sounddevice
        audio_data = sd.rec(frames, samplerate=rate, channels=channels, dtype='int16')
        sd.wait()  # Attendre la fin de l'enregistrement

        # Sauvegarde dans un fichier WAV
        with wave.open(file_name, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 16 bits par échantillon
            wf.setframerate(rate)
            wf.writeframes(audio_data.tobytes())
        print(f"Enregistrement sauvegardé sous {file_name}")

  

    def diminuer_credit(self, numero_client, montant):
        """Diminue le crédit du client de 'montant' unités"""
        file_path = "BD/clients.txt"
        with open(file_path, "r") as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            client_data = line.strip().split(",")
            numero, nom, credit, pin = client_data[0], client_data[1], int(client_data[2]), client_data[3]
            if numero == numero_client:
                if credit >= montant:
                    new_credit = credit - montant
                    lines[i] = f"{numero},{nom},{new_credit},{pin}\n" 
                    break
                else:
                    return False  
        
        with open(file_path, "w") as file:
            file.writelines(lines)

        return True  

    def lire_credit(self, numero_client):
        from Controller.functions import afficher_erreur
        """Lire le crédit du client à partir du fichier client.txt"""
        try:
            with open("BD/clients.txt", "r") as f:
                for line in f:
                    client_data = line.strip().split(",")
                    if len(client_data) != 4:
                        afficher_erreur("Le format du fichier client.txt est incorrect.")
                        return None

                    numero, nom, credit, pin = client_data[0], client_data[1], client_data[2], client_data[3]

                    try:
                        credit = int(credit)
                    except ValueError:
                        afficher_erreur(f"Crédit invalide pour le client {numero}.")
                        return None

                    if numero == numero_client:
                        return credit  
            return None 
        except FileNotFoundError:
            afficher_erreur("Le fichier des clients est introuvable.")
            return None
        except Exception as e:
            afficher_erreur(f"Une erreur est survenue : {str(e)}")
            return None


def connexion_client(root):
    """Gestion de la connexion client avec la saisie du numéro et du code PIN sur la même fenêtre."""
    from Controller.functions import valider_numero, afficher_succes, valider_code_pin
    from Views.client import ClientApp

    def valider_connexion():
      
        numero = entry_numero.get()
        pin = entry_pin.get()

     
        label_message.config(text="", fg="red")

      
        if not valider_numero(numero):
            label_message.config(text="Numéro de téléphone invalide.")
            return

      
        if not valider_code_pin(pin):
            label_message.config(text="Code PIN invalide.")
            return

       
        client = verifier_connexion(numero, pin)
        
        if client:
            afficher_succes("Bienvenue")
            root.withdraw()  
            client_window = tk.Toplevel(root) 
            app = ClientApp(client_window, numero) 
            connexion_window.destroy()  
        else:
            label_message.config(text="Numéro ou code PIN incorrect.")


    connexion_window = tk.Toplevel(root)
    connexion_window.title("Connexion Client")
    connexion_window.geometry("300x250")
    connexion_window.resizable(False, False)  


    tk.Label(connexion_window, text="Numéro de téléphone:").pack(pady=5)
    entry_numero = tk.Entry(connexion_window)
    entry_numero.pack(pady=5)

    tk.Label(connexion_window, text="Code PIN:").pack(pady=5)
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
