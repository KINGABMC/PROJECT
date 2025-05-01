package vue;

import entites.Classe;
import entites.Etudiant;
import entites.Note;
import enumeration.Message;
import enumeration.OptionMenu;
import services.Etudiantservice;

import java.util.ArrayList;
import java.util.Scanner;

public class Menu {
    private static final Scanner scanner = new Scanner(System.in);

    public static void afficher() {
        int choix;
        do {
            System.out.println("\nQue souhaitez-vous faire ?");
            for (OptionMenu option : OptionMenu.values()) {
                System.out.println(option.getValeur() + ". " + Message.values()[option.ordinal()].getLibelle());
            }
            System.out.print("Votre choix : ");
            choix = Integer.parseInt(scanner.nextLine());

            switch (choix) {
                case 1 -> ajouterEtudiant();
                case 2 -> afficherEtudiants();
                case 3 -> ajouterNote();
                case 4 -> afficherNotesEtudiant();
                case 5 -> afficherEtudiantsParClasse();
                case 6 -> afficherMoyenneParClasse();
                case 7 -> afficherMeilleurParClasse();
                case 8 -> System.out.println("Fin du programme.");
                default -> System.out.println("Choix invalide !");
            }
        } while (choix != 8);
    }

    private static void ajouterEtudiant() {
        System.out.print("Matricule : ");
        String matricule = scanner.nextLine();
        System.out.print("Nom : ");
        String nom = scanner.nextLine();
        System.out.print("Âge : ");
        int age = Integer.parseInt(scanner.nextLine());

        System.out.print("Libellé de la classe : ");
        String libelle = scanner.nextLine();
        System.out.print("Filière (CDSD/MAE) : ");
        String filiere = scanner.nextLine();
        System.out.print("Niveau (L1/L2/L3) : ");
        String niveau = scanner.nextLine();

        Classe classe = new Classe(libelle, filiere, niveau);
        Etudiantservice.classes.add(classe);

        Etudiant etudiant = new Etudiant(matricule, nom, age, classe);
        if (Etudiantservice.ajouterEtudiant(etudiant)) {
            System.out.println("Etudiant ajouté avec succès !");
        } else {
            System.out.println("Matricule déjà existant !");
        }
    }

    private static void afficherEtudiants() {
        for (Etudiant e : Etudiantservice.etudiants) {
            System.out.println(e.getId() + " - " + e.getNom() + " (" + e.getClasse().getLibelle() + ")");
        }
    }

    private static void ajouterNote() {
        System.out.print("Matricule de l'étudiant : ");
        String matricule = scanner.nextLine();
        System.out.print("Valeur de la note : ");
        double valeur = Double.parseDouble(scanner.nextLine());
        Etudiantservice.ajouterNote(matricule, valeur);
    }

    private static void afficherNotesEtudiant() {
        System.out.print("Matricule de l'étudiant : ");
        String matricule = scanner.nextLine();
        Etudiant e = Etudiantservice.chercherParMatricule(matricule);
        if (e != null) {
            for (Note n : e.getNotes()) {
                System.out.println("Note ID " + n.getId() + ": " + n.getValeur());
            }
        } else {
            System.out.println("Etudiant non trouvé.");
        }
    }

    private static void afficherEtudiantsParClasse() {
        System.out.print("Libellé de la classe : ");
        String libelle = scanner.nextLine();
        for (Classe c : Etudiantservice.classes) {
            if (c.getLibelle().equalsIgnoreCase(libelle)) {
                ArrayList<Etudiant> liste = Etudiantservice.chercherParClasse(c);
                for (Etudiant e : liste) {
                    System.out.println(e.getNom());
                }
                return;
            }
        }
        System.out.println("Classe non trouvée.");
    }

    private static void afficherMoyenneParClasse() {
        System.out.print("Libellé de la classe : ");
        String libelle = scanner.nextLine();
        for (Classe c : Etudiantservice.classes) {
            if (c.getLibelle().equalsIgnoreCase(libelle)) {
                System.out.println("Moyenne de la classe : " + Etudiantservice.moyenneClasse(c));
                return;
            }
        }
        System.out.println("Classe non trouvée.");
    }

    private static void afficherMeilleurParClasse() {
        System.out.print("Libellé de la classe : ");
        String libelle = scanner.nextLine();
        for (Classe c : Etudiantservice.classes) {
            if (c.getLibelle().equalsIgnoreCase(libelle)) {
                Etudiant meilleur = Etudiantservice.meilleurEtudiantClasse(c);
                if (meilleur != null) {
                    System.out.println("Meilleur étudiant : " + meilleur.getNom() + " avec moyenne " + meilleur.calculerMoyenne());
                } else {
                    System.out.println("Aucun étudiant.");
                }
                return;
            }
        }
        System.out.println("Classe non trouvée.");
    }
}
