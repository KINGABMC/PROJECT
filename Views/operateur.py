import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Controller.operateur import deconnexion
from const import *

class OperateurView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Gestion des Opérateurs")
        self.root.geometry("600x500")
        self.create_buttons()

    def create_buttons(self):
        tk.Label(
            self.root,
            self.root.configure(bg=BACKGROUND_COLOR),
            text="Bienvenue, opérateur",
            font=("Arial", 16),
            fg=TEXT_COLOR,  # Couleur du texte
        ).pack(pady=(80, 10))
        
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, 
                  text="Créer un opérateur",
                  font=("Arial", 16),
                  width=30, height=2,
                  command=self.creer_operateur,
                  bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, 
                  text="Renommer un opérateur",
                  font=("Arial", 16),
                  width=30, height=2,
                  command=self.renommer_operateur,
                  bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, 
                  text="Lister les opérateurs",
                  font=("Arial", 16),
                  width=30, height=2,
                  command=self.lister_operateurs,
                  bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(btn_frame, 
                  text="Vendre un numéro",
                  font=("Arial", 16),
                  width=30, height=2,
                  command=self.vendre_numero,
                  bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(btn_frame, 
                  text="État de la caisse",
                  font=("Arial", 16),
                  width=30, height=2,
                  command=self.etat_caisse,
                  bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(
            btn_frame,
            text="Déconnexion",
            font=("Arial", 16),
            command=lambda: deconnexion(self.root),
            width=30, height=2,
            bg=BUTTON_COLOR, fg=TEXT_COLOR
        ).grid(row=5, column=0, padx=10, pady=10)

    def creer_operateur(self):
        """Fenêtre pour créer un opérateur"""
        ajout_window = tk.Toplevel(self.root)
        ajout_window.title("Créer un opérateur")
        ajout_window.geometry("300x250")
        ajout_window.configure(bg=BG_COLOR)

        label_nom = tk.Label(ajout_window, text="Nom de l'opérateur:", fg=TEXT_COLOR, bg=BG_COLOR)
        label_nom.pack(pady=5)

        entry_nom = tk.Entry(ajout_window, bg=ENTRY_BG_COLOR, fg=TEXT_COLOR)
        entry_nom.pack(pady=5)

        label_index = tk.Label(ajout_window, text="Index de l'opérateur:", fg=TEXT_COLOR, bg=BG_COLOR)
        label_index.pack(pady=5)

        entry_index = tk.Entry(ajout_window, bg=ENTRY_BG_COLOR, fg=TEXT_COLOR)
        entry_index.pack(pady=5)

        label_message = tk.Label(ajout_window, text="", fg="red", bg=BG_COLOR)
        label_message.pack(pady=5)

        def valider_creation():
            nom = entry_nom.get()
            index = entry_index.get()
            label_message.config(text="", fg="red")
            if not nom or not index:
                label_message.config(text="Veuillez entrer un nom et un index valides.")
                return

            self.controller.creer_operateur(nom, index)
            tk.messagebox.showinfo("Création opérateur", f"Opérateur '{nom}' créé avec l'index {index}.")
            ajout_window.destroy()

        btn_valider = tk.Button(ajout_window, text="Créer l'opérateur", command=valider_creation, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        btn_valider.pack(pady=10)

    def renommer_operateur(self):
        """Fenêtre pour renommer un opérateur"""
        ajout_window = tk.Toplevel(self.root)
        ajout_window.title("Renommer un opérateur")
        ajout_window.geometry("300x250")
        ajout_window.configure(bg=BG_COLOR)

        label_ancien_nom = tk.Label(ajout_window, text="Ancien nom:")
        label_ancien_nom.pack(pady=5)

        entry_ancien_nom = tk.Entry(ajout_window)
        entry_ancien_nom.pack(pady=5)

        label_nouveau_nom = tk.Label(ajout_window, text="Nouveau nom:")
        label_nouveau_nom.pack(pady=5)

        entry_nouveau_nom = tk.Entry(ajout_window)
        entry_nouveau_nom.pack(pady=5)

        def valider_renommage():
            ancien_nom = entry_ancien_nom.get()
            nouveau_nom = entry_nouveau_nom.get()

            if not ancien_nom or not nouveau_nom:
                messagebox.showerror("Erreur", "Veuillez entrer les deux noms.")
                return

            self.controller.renommer_operateur(ancien_nom, nouveau_nom)
            tk.messagebox.showinfo("Renommage opérateur", f"Opérateur renommé de {ancien_nom} à {nouveau_nom}.")
            ajout_window.destroy()

        btn_valider = tk.Button(ajout_window, text="Renommer l'opérateur", command=valider_renommage, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        btn_valider.pack(pady=10)

    def lister_operateurs(self):
        """Liste les opérateurs sous forme de tableau"""
        operateurs = self.controller.lister_operateurs() 
        if not operateurs:
            messagebox.showinfo("Opérateurs", "Aucun opérateur trouvé.")
            return

        tableau_window = tk.Toplevel(self.root)
        tableau_window.title("Liste des opérateurs")
        tableau_window.geometry("600x400")
        tableau_window.configure(bg=BG_COLOR)

        tree = ttk.Treeview(tableau_window, columns=("Nom", "Index"), show="headings")
        tree.pack(fill="both", expand=True)

        tree.heading("Nom", text="Nom de l'opérateur")
        tree.heading("Index", text="Index")

        for operateur in operateurs:
            nom = operateur[0]
            index = operateur[1]
            tree.insert("", "end", values=(nom, index))

        scrollbar = ttk.Scrollbar(tableau_window, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

    def vendre_numero(self):
        """Fenêtre pour vendre un numéro"""
        ajout_window = tk.Toplevel(self.root)
        ajout_window.title("Vendre un numéro")
        ajout_window.geometry("500x400")
        ajout_window.configure(bg=BG_COLOR)

        label_operateur = tk.Label(ajout_window, text="Nom de l'opérateur:")
        label_operateur.pack(pady=5)

        entry_operateur = tk.Entry(ajout_window)
        entry_operateur.pack(pady=5)

        label_index = tk.Label(ajout_window, text="Index de l'opérateur:")
        label_index.pack(pady=5)

        entry_index = tk.Entry(ajout_window)
        entry_index.pack(pady=5)

        def recuperer_numeros():
            operateur = entry_operateur.get()
            if not operateur:
                messagebox.showerror("Erreur", "Veuillez entrer le nom de l'opérateur.")
                return

            numeros = self.controller.get_numeros_operateur(operateur)
            clients = self.controller.get_clients()

            if not numeros:
                messagebox.showerror("Erreur", f"Les numéros de l'opérateur {operateur} sont introuvables.")
                return

            tree = ttk.Treeview(ajout_window, columns=("Numéro", "Propriétaire"), show="headings")
            tree.heading("Numéro", text="Numéro")
            tree.heading("Propriétaire", text="Propriétaire")
            tree.pack(fill="both", expand=True)

            for numero in numeros:
                color = "red" if numero in clients else "black"
                tree.insert("", "end", values=(numero, ""), tags=(numero,))
                tree.tag_configure(numero, foreground=color)

            def associer_numero():
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showerror("Erreur", "Veuillez sélectionner un numéro.")
                    return

                numero = tree.item(selected_item, "values")[0]
                nom_client = entry_nom.get()

                if not nom_client:
                    messagebox.showerror("Erreur", "Veuillez entrer un nom de propriétaire.")
                    return

                self.controller.ajouter_client(numero, nom_client)
                tree.item(selected_item, values=(numero, nom_client), tags=(numero,))
                tree.tag_configure(numero, foreground="black")
                messagebox.showinfo("Succès", f"Numéro {numero} attribué à {nom_client}.")
                ajout_window.destroy()

            label_nom = tk.Label(ajout_window, text="Nom du propriétaire:")
            label_nom.pack(pady=5)

            entry_nom = tk.Entry(ajout_window)
            entry_nom.pack(pady=5)

            btn_valider = tk.Button(ajout_window, text="Associer le numéro", command=associer_numero, bg=BUTTON_COLOR, fg=TEXT_COLOR)
            btn_valider.pack(pady=10)

        btn_recuperer = tk.Button(ajout_window, text="Afficher les numéros", command=recuperer_numeros, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        btn_recuperer.pack(pady=10)

    def etat_caisse(self):
        """Fenêtre pour l'état de la caisse"""
        ajout_window = tk.Toplevel(self.root)
        ajout_window.title("État de la caisse")
        ajout_window.geometry("300x250")
        ajout_window.configure(bg=BG_COLOR)

        label_operateur = tk.Label(ajout_window, text="Nom de l'opérateur:")
        label_operateur.pack(pady=5)

        entry_operateur = tk.Entry(ajout_window)
        entry_operateur.pack(pady=5)

        label_periode = tk.Label(ajout_window, text="Période (Jour/Mois/Année):")
        label_periode.pack(pady=5)

        entry_periode = tk.Entry(ajout_window)
        entry_periode.pack(pady=5)

        def valider_etat_caisse():
            operateur = entry_operateur.get()
            periode = entry_periode.get()

            if not operateur or not periode:
                messagebox.showerror("Erreur", "Veuillez entrer l'opérateur et la période.")
                return

            self.controller.etat_caisse(operateur, periode)
            tk.messagebox.showinfo("État de la caisse", f"État de la caisse pour {operateur} en {periode}.")
            ajout_window.destroy()

        btn_valider = tk.Button(ajout_window, text="Vérifier l'état de la caisse", command=valider_etat_caisse, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        btn_valider.pack(pady=10)
