import tkinter as tk
from tkinter import ttk, messagebox
import pygame
from Controller.client import deconnexion
from const import *

class ClientApp:
    def __init__(self, root, numero_client):
        from Controller.client import ClientController
        self.root = root
        self.numero_client = numero_client
        self.controller = ClientController()
        self.root.title(f"Client : {numero_client}")
        self.root.geometry("400x400")
        self.create_ui()
        
       
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512) 
        print("Pygame mixer initialisé")
        
        self.duration = 0 
    
    def ajouter_contact(self):
        """Fenêtre pour ajouter un contact"""
        ajout_window = tk.Toplevel(self.root)
        ajout_window.title("Ajouter un contact")
        ajout_window.geometry("300x250") 

        label_nom = tk.Label(ajout_window, text="Nom du contact:", bg=BG_COLOR, fg=TEXT_COLOR)
        label_nom.pack(pady=5)  

        entry_nom = tk.Entry(ajout_window, bg=ENTRY_BG_COLOR, fg=TEXT_COLOR)
        entry_nom.pack(pady=5)

        label_numero = tk.Label(ajout_window, text="Numéro du contact:", bg=BG_COLOR, fg=TEXT_COLOR)
        label_numero.pack(pady=5)

        entry_numero = tk.Entry(ajout_window, bg=ENTRY_BG_COLOR, fg=TEXT_COLOR)
        entry_numero.pack(pady=5)

        label_message = tk.Label(ajout_window, text="", fg="red", bg=BG_COLOR)
        label_message.pack(pady=5)

        def valider_ajout():
            from Controller.functions import valider_numero, valider_nom

            nom = entry_nom.get()
            numero = entry_numero.get()
            label_message.config(text="", fg="red")  

            if not valider_numero(numero):
                label_message.config(text="Numéro de téléphone invalide.")
                return

            if not valider_nom(nom):
                label_message.config(text="Nom invalide. Le nom doit comporter entre 3 et 15 caractères.")
                return

            numero_client = self.numero_client  

            self.controller.ajouter_contact(numero_client, nom, numero)
            tk.messagebox.showinfo("Ajout de contact", f"Contact '{nom}' ajouté avec le numéro {numero}.")
            ajout_window.destroy()  

        btn_valider = tk.Button(ajout_window, text="Ajouter le contact", command=valider_ajout, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        btn_valider.pack(pady=10)  

    def create_ui(self):
        tk.Label(
            self.root,
            text="Bienvenue cher client",
            font=("Arial", 20),
            fg=BACKGROUND_COLOR,
        ).pack(pady=(80,10))

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Consulter Crédit",
            command=self.consulter_credit,
            font=("Arial", 16),
            width=30,
            height=2,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).grid(padx=10, pady=10)

        tk.Button(
            btn_frame,
            text="Afficher Répertoire",
            font=("Arial", 16),
            command=self.afficher_repertoire,
            width=30,
            height=2,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).grid(padx=10, pady=10)

        tk.Button(
            btn_frame,
            text="Effectuer un Appel",
            font=("Arial", 16),
            command=self.effectuer_appel,
            width=30,
            height=2,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).grid(padx=10, pady=10)

        tk.Button(
            btn_frame,
            text="Ajouter un contact",
            font=("Arial", 16),
            command=self.ajouter_contact,  
            width=30,
            height=2,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).grid(padx=10, pady=10)

        tk.Button(
            btn_frame,
            text="Gérer Contacts",
            font=("Arial", 16),
            command=self.gerer_contact, 
            width=30,
            height=2,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).grid(padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="Déconnexion",
            font=("Arial", 16),
            command= lambda: deconnexion(self.root),  
            height=2,
            width=30,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR
        ).grid(padx=10, pady=10)

    def consulter_credit(self):
        solde = self.controller.consulter_credit(self.numero_client)
        messagebox.showinfo("Solde", solde)

    def afficher_repertoire(self):
        contacts = self.controller.lire_repertoire(self.numero_client)

        window = tk.Toplevel(self.root)
        window.title("Répertoire")
        tree = ttk.Treeview(window, columns=("Nom", "Numero"), show="headings", style="Custom.Treeview")
        tree.heading("Nom", text="Nom")
        tree.heading("Numero", text="Numéro")
        tree.pack(fill="both", expand=True)

        for contact in contacts:
            tree.insert("", "end", values=contact)

    def effectuer_appel(self):
        contacts = self.controller.lire_repertoire(self.numero_client)

        if not contacts:
            messagebox.showinfo("Répertoire vide", "Aucun contact disponible.")
            return

        window = tk.Toplevel(self.root)
        window.title("Choisir un contact pour l'appel")

        tree = ttk.Treeview(window, columns=("Nom", "Numero"), show="headings", style="Custom.Treeview")
        tree.heading("Nom", text="Nom")
        tree.heading("Numero", text="Numéro")
        tree.pack(fill="both", expand=True)

        for contact in contacts:
            tree.insert("", "end", values=contact)

        def appeler():
            selected_item = tree.selection()
            if selected_item:
                contact = tree.item(selected_item[0], "values")
                numero_contact = contact[1]
                self.controller.enregistrer_appel(self.numero_client, numero_contact)

                label_compte_a_rebours = tk.Label(window, text="Durée de l'appel: 0s", font=("Arial", 14))
                label_compte_a_rebours.pack(pady=10)

                label_credit = tk.Label(window, text="Crédit restant: 0 FCFA", font=("Arial", 14))
                label_credit.pack(pady=10)

                pygame.mixer.music.load("BD/sound/blue.mp3")
                pygame.mixer.music.play()

                fichier_audio = f"appel_{self.numero_client}_{numero_contact}.wav"
                self.controller.enregistrer_audio(fichier_audio, duration=60)

                duration = 0
                credit_diminuer_par_seconde = 20

                def mise_a_jour_compte_a_rebours():
                    nonlocal duration
                    credit = self.controller.lire_credit(self.numero_client)
                    if credit is None:
                        messagebox.showerror("Erreur", "Le crédit du client est introuvable.")
                        return

                    label_credit.config(text=f"Crédit restant: {credit} FCFA")

                    if credit < credit_diminuer_par_seconde:
                        messagebox.showinfo("Crédit insuffisant", "Crédit insuffisant pour continuer l'appel.")
                        raccrocher()
                        return

                    credit -= credit_diminuer_par_seconde
                    self.controller.diminuer_credit(self.numero_client, credit_diminuer_par_seconde)

                    duration += 1
                    label_compte_a_rebours.config(text=f"Durée de l'appel: {duration}s")

                    if credit >= credit_diminuer_par_seconde:
                        window.after(1000, mise_a_jour_compte_a_rebours)

                def raccrocher():
                    pygame.mixer.music.stop()
                    self.controller.arreter_enregistrement_audio()
                    window.destroy()
                    messagebox.showinfo("Appel", "L'appel a été raccroché.")

                btn_raccrocher = tk.Button(window, text="Raccrocher", command=raccrocher, bg=BUTTON_COLOR, fg=TEXT_COLOR)
                btn_raccrocher.pack(pady=10)

                window.after(1000, mise_a_jour_compte_a_rebours)

            else:
                messagebox.showwarning("Erreur", "Veuillez sélectionner un contact.")

        btn_appeler = tk.Button(window, text="Appeler", command=appeler, bg=BUTTON_COLOR_MAIN, fg=TEXT_COLOR)
        btn_appeler.pack(pady=10)

        window.mainloop()  

    def gerer_contact(self):
        """Sous-programme pour gérer les contacts (ajouter, supprimer, modifier)"""
        
        def repertoire():
            """Afficher les contacts dans une fenêtre avec Treeview"""
            contacts = self.controller.lire_repertoire(self.numero_client)

            window = tk.Toplevel(self.root)
            window.title("Répertoire")
            
            tree = ttk.Treeview(window, columns=("Nom", "Numero"), show="headings", style="Custom.Treeview")
            tree.heading("Nom", text="Nom")
            tree.heading("Numero", text="Numéro")
            tree.pack(fill="both", expand=True)

            for contact in contacts:
                tree.insert("", "end", values=contact)

            return window, tree
        
        def supprimer_contact():
            """Supprimer un contact après confirmation"""
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Sélection invalide", "Veuillez sélectionner un contact.")
                return
            
            contact = tree.item(selected_item, "values")
            nom_contact = contact[0]  # Nom du contact sélectionné
            
            # Demande de confirmation
            result = messagebox.askquestion("Confirmation", f"Voulez-vous vraiment supprimer {nom_contact}?")
            if result == "yes":
                success = self.controller.supprimer_contact(self.numero_client, nom_contact)
                if success:
                    messagebox.showinfo("Succès", f"Le contact {nom_contact} a été supprimé.")
                    tree.delete(selected_item)  # Supprimer de l'affichage
                else:
                    messagebox.showerror("Erreur", "Le contact n'a pas pu être supprimé.")
        
        def modifier_contact():
            """Modifier un contact existant"""
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Sélection invalide", "Veuillez sélectionner un contact.")
                return
            
            contact = tree.item(selected_item, "values")
            numero_contact = contact[1]
            nom_contact = contact[0]  # Nom du contact sélectionné
            
            # Fenêtre pour modifier le contact
            modifier_window = tk.Toplevel(self.root)
            modifier_window.title("Modifier le contact")
            modifier_window.geometry("300x200")
            
            label_nom = tk.Label(modifier_window, text="Nouveau Nom:", fg=TEXT_COLOR, bg=BG_COLOR)
            label_nom.pack(pady=5)
            
            entry_nom = tk.Entry(modifier_window, bg=ENTRY_BG_COLOR, fg=TEXT_COLOR)
            entry_nom.insert(0, nom_contact)  # Remplir avec le nom actuel
            entry_nom.pack(pady=5)
            
            def valider_modification():
                nouveau_nom = entry_nom.get()
                success = self.controller.modifier_contact(self.numero_client, numero_contact, nouveau_nom)
                if success:
                    messagebox.showinfo("Succès", f"Le contact a été modifié avec succès.")
                    modifier_window.destroy()
                else:
                    messagebox.showerror("Erreur", "Erreur lors de la modification du contact.")
                
            btn_valider = tk.Button(modifier_window, text="Valider", command=valider_modification, bg=BUTTON_COLOR_MAIN, fg=TEXT_COLOR)
            btn_valider.pack(pady=10)
            
        window, tree = repertoire()  # Affichage des contacts
        btn_supprimer = tk.Button(window, text="Supprimer Contact", command=supprimer_contact, bg=ROUGE, fg=TEXT_COLOR)
        btn_supprimer.pack(pady=10)

        btn_modifier = tk.Button(window, text="Modifier Contact", command=modifier_contact, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        btn_modifier.pack(pady=10)
