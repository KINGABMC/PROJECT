import tkinter as tk
from tkinter import messagebox
from const import *

def afficher_message(message):
    """Affiche un message d'information dans une boîte de dialogue."""
    messagebox.showinfo("Information", message)

def afficher_erreur(message):
    """Affiche un message d'erreur dans une boîte de dialogue."""
    messagebox.showerror("Erreur", message)

def afficher_succes(message):
    """Affiche un message de succès dans une boîte de dialogue."""
    messagebox.showinfo("Succès", message)


def menu_principal():
    from Controller.client import connexion_client
    from Controller.operateur import connexion_gestionnaire
    import tkinter as tk
   
    root = tk.Tk()
    root.title("Gestion des Opérateurs Téléphoniques")
    root.geometry("400x400")

   
    root.configure(bg=BACKGROUND_COLOR)

    title_font = ("Arial", 16, "bold")
    button_font = ("Arial", 12)

 
    title_label = tk.Label(
        root, 
        text="Gestion des Opérateurs Téléphoniques", 
        font=title_font, 
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR_WHITE
    )
    title_label.pack(pady=(120, 20))

    button_width = 30
    button_height = 2

 
    btn_client = tk.Button(
        root, 
        text="Connexion-Client", 
        font=button_font, 
        width=button_width, 
        height=button_height, 
        command=lambda: connexion_client(root),
        fg=TEXT_COLOR_WHITE,
        bg=BUTTON_COLOR_SECONDARY
    )
    btn_client.pack(pady=15)

    
    btn_gestionnaire = tk.Button(
        root, 
        text="Connexion-Gestionnaire", 
        font=button_font, 
        width=button_width, 
        height=button_height, 
        command=lambda: connexion_gestionnaire(root),
        fg=TEXT_COLOR_WHITE,
        bg=BUTTON_COLOR_SECONDARY
    )
    btn_gestionnaire.pack(pady=15)

    btn_quit = tk.Button(
        root, 
        text="Quitter", 
        bg=BUTTON_COLOR_ALERT,
        font=button_font, 
        width=button_width, 
        height=button_height, 
        command=root.quit,
        fg=TEXT_COLOR_WHITE
    )
    btn_quit.pack(pady=15)

    root.mainloop()
