from IA_difficile import IADifficile
from IA_facile import IAFacile
from IA_normale import IANormale
from Puissance4 import Puissance4


def main():
    jeu = Puissance4()
    print("#######################################")
    print("#         PUISSANCE 4                 #")
    print("#######################################\n")

    # Sélection du mode de jeu
    mode = input(
        "Choisissez le mode de jeu :\n"
        "1. Joueur vs Joueur\n"
        "2. Joueur vs IA Facile\n"
        "3. Joueur vs IA Normale\n"
        "4. Joueur vs IA Difficile\n"
        "Votre choix (1-4) : "
    )
    while mode not in ["1", "2", "3", "4"]:
        mode = input("Choix invalide. Réessayez (1-4) : ")

    # Initialisation de l'IA
    ia = None
    if mode == "2":
        ia = IAFacile()
        print("\n--- Mode IA Facile activée (Joueur 2) ---\n")
    elif mode == "3":
        ia = IANormale()
        print("\n--- Mode IA Normale activée (Joueur 2) ---\n")
    elif mode == "4":
        ia = IADifficile()
        print("\n--- Mode IA Difficile activée (Joueur 2) ---\n")

    # Déroulement du jeu
    while True:
        jeu.afficher_grille()

        # Tour de l'IA
        if ia and jeu.joueur == 2:
            print(f"Tour de l'IA ({ia.__class__.__name__})...")
            col = ia.choisir_coup(jeu)
            print(f"L'IA joue en colonne {col}\n")

        # Tour du joueur humain
        else:
            try:
                col = int(input(f"Joueur {jeu.joueur}, choisissez une colonne (0-{jeu.m - 1}) : "))
                if not (0 <= col < jeu.m) or not jeu.coup_possible(col):
                    print("Colonne invalide ou pleine !\n")
                    continue
            except ValueError:
                print("Veuillez entrer un nombre valide.\n")
                continue

        # Exécution du coup
        jeu.jouer(col)

        # Vérification fin de partie
        if jeu.victoire():
            jeu.afficher_grille()
            print(f"Le Joueur {jeu.joueur} remporte la partie !")
            break
        elif jeu.match_nul():
            jeu.afficher_grille()
            print("Match nul ! Aucun gagnant.")
            break

        # Passage au joueur suivant
        jeu.alterner_joueur()

if __name__ == "__main__":
    main()