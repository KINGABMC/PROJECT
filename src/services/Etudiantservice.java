package services;

import entites.Classe;
import entites.Etudiant;
import entites.Note;

import java.util.ArrayList;

public class Etudiantservice {
    public static ArrayList<Etudiant> etudiants = new ArrayList<>();
    public static ArrayList<Classe> classes = new ArrayList<>();

    public static boolean ajouterEtudiant(Etudiant etudiant) {
        for (Etudiant e : etudiants) {
            if (e.getMatricule().equals(etudiant.getMatricule())) {
                return false;
            }
        }
        etudiants.add(etudiant);
        return true;
    }

    public static void ajouterNote(String matricule, double valeur) {
        for (Etudiant e : etudiants) {
            if (e.getMatricule().equals(matricule)) {
                e.ajouterNote(new Note(valeur));
                break;
            }
        }
    }

    public static Etudiant chercherParMatricule(String matricule) {
        for (Etudiant e : etudiants) {
            if (e.getMatricule().equals(matricule)) {
                return e;
            }
        }
        return null;
    }

    public static ArrayList<Etudiant> chercherParClasse(Classe classe) {
        ArrayList<Etudiant> resultat = new ArrayList<>();
        for (Etudiant e : etudiants) {
            if (e.getClasse().equals(classe)) {
                resultat.add(e);
            }
        }
        return resultat;
    }

    public static double moyenneClasse(Classe classe) {
        ArrayList<Etudiant> liste = chercherParClasse(classe);
        if (liste.isEmpty()) return 0.0;
        double total = 0;
        for (Etudiant e : liste) {
            total += e.calculerMoyenne();
        }
        return total / liste.size();
    }

    public static Etudiant meilleurEtudiantClasse(Classe classe) {
        ArrayList<Etudiant> liste = chercherParClasse(classe);
        if (liste.isEmpty()) return null;
        Etudiant meilleur = liste.get(0);
        for (Etudiant e : liste) {
            if (e.calculerMoyenne() > meilleur.calculerMoyenne()) {
                meilleur = e;
            }
        }
        return meilleur;
    }
}
