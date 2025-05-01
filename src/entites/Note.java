package entites;

public class Note {
    private static int compteur = 1;
    private int id;
    private double valeur;

    public Note(double valeur) {
        this.id = compteur++;
        this.valeur = valeur;
    }

    public int getId() {
        return id;
    }

    public double getValeur() {
        return valeur;
    }
}
