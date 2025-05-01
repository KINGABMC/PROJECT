package enumeration;

public enum Message {
    AJOUTER_ETUDIANT("Ajouter un étudiant"),
    AFFICHER_ETUDIANTS("Afficher tous les étudiants"),
    AJOUTER_NOTE("Ajouter une note à un étudiant"),
    AFFICHER_NOTES_ETUDIANT("Afficher les notes d'un étudiant"),
    AFFICHER_ETUDIANTS_PAR_CLASSE("Afficher les étudiants d'une classe"),
    AFFICHER_MOYENNE_PAR_CLASSE("Afficher la moyenne de chaque classe"),
    AFFICHER_MEILLEUR_PAR_CLASSE("Afficher le meilleur étudiant de chaque classe"),
    QUITTER("Quitter");

    private String libelle;

    Message(String libelle) {
        this.libelle = libelle;
    }

    public String getLibelle() {
        return libelle;
    }
}
