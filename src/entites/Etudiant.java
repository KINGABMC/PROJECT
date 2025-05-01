package entites;

import java.util.ArrayList;

public class Etudiant {
    private static int compteur = 1;
    private int id;
    private String matricule;
    private String nom;
    private int age;
    private Classe classe;
    private ArrayList<Note> notes = new ArrayList<>();

    public Etudiant(String matricule, String nom, int age, Classe classe) {
        this.id = compteur++;
        this.matricule = matricule;
        this.nom = nom;
        this.age = age;
        this.classe = classe;
    }

    public int getId() {
        return id;
    }

    public String getMatricule() {
        return matricule;
    }

    public String getNom() {
        return nom;
    }

    public int getAge() {
        return age;
    }

    public Classe getClasse() {
        return classe;
    }

    public ArrayList<Note> getNotes() {
        return notes;
    }

    public void ajouterNote(Note note) {
        notes.add(note);
    }

    public double calculerMoyenne() {
        if (notes.isEmpty()) return 0.0;
        double somme = 0;
        for (Note note : notes) {
            somme += note.getValeur();
        }
        return somme / notes.size();
    }
}
