package entites;

public class Classe {
    private static int compteur = 1;
    private int id;
    private String libelle;
    private String filiere; // CDSD ou MAE
    private String niveau;  // L1, L2, L3

    public Classe(String libelle, String filiere, String niveau) {
        this.id = compteur++;
        this.libelle = libelle;
        this.filiere = filiere;
        this.niveau = niveau;
    }

    public int getId() {
        return id;
    }

    public String getLibelle() {
        return libelle;
    }

    public String getFiliere() {
        return filiere;
    }

    public String getNiveau() {
        return niveau;
    }
}
