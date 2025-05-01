package enumeration;

public enum OptionMenu {
    AJOUTER_ETUDIANT(1),
    AFFICHER_ETUDIANTS(2),
    AJOUTER_NOTE(3),
    AFFICHER_NOTES_ETUDIANT(4),
    AFFICHER_ETUDIANTS_PAR_CLASSE(5),
    AFFICHER_MOYENNE_PAR_CLASSE(6),
    AFFICHER_MEILLEUR_PAR_CLASSE(7),
    QUITTER(8);

    private int valeur;

    OptionMenu(int valeur) {
        this.valeur = valeur;
    }

    public int getValeur() {
        return valeur;
    }
}
