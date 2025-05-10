from IA_facile import IAFacile
from IA_normale import IANormale
from IA_difficile import IADifficile
from Puissance4 import Puissance4


def tester_match_equitable(IA1_class, IA2_class, nom1, nom2, nb_parties=50):
    """
    Organise un tournoi équitable entre deux IA.
    Alterne qui commence pour assurer l'équité des matchs.
    """
    # Initialisation des statistiques de victoires
    stats = {nom1: 0, nom2: 0, 'nuls': 0}

    # Boucle principale du tournoi
    for partie in range(nb_parties):
        jeu = Puissance4()

        # Alterne qui commence pour plus d'équité
        if partie % 2 == 0:
            ia1, ia2 = IA1_class(), IA2_class()
            nom_j1, nom_j2 = nom1, nom2
        else:
            ia1, ia2 = IA2_class(), IA1_class()
            nom_j1, nom_j2 = nom2, nom1

        jeu.joueur = 1
        while True:
            # Sélectionne l'IA active en fonction du joueur actuel
            ia = ia1 if jeu.joueur == 1 else ia2
            col = ia.choisir_coup(jeu)
            jeu.jouer(col)

            # Vérifie les conditions de fin de partie
            if jeu.victoire():
                gagnant = nom_j1 if jeu.joueur == 1 else nom_j2
                stats[gagnant] += 1
                break
            elif jeu.match_nul():
                stats['nuls'] += 1
                break

            jeu.alterner_joueur()
    return stats


def main():
    """
    Fonction principale du jeu.
    Gère l'interface utilisateur et les différents modes de jeu.
    """
    jeu = Puissance4()
    # Affichage du titre du jeu
    print("#######################################")
    print("#         PUISSANCE 4                 #")
    print("#######################################\n")

    # Menu de sélection du mode de jeu
    mode = input(
        "Choisissez le mode de jeu :\n"
        "1. Joueur vs Joueur\n"
        "2. Joueur vs IA Facile\n"
        "3. Joueur vs IA Normale\n"
        "4. Joueur vs IA Difficile\n"
        "5. IA Facile vs IA Difficile\n"
        "6. IA Facile vs IA Normale\n"
        "7. IA Normale vs IA Difficile\n"
        "Votre choix (1-7) : "
    )
    # Validation de l'entrée utilisateur
    while mode not in [str(i) for i in range(1, 8)]:
        mode = input("Choix invalide. Réessayez (1-7) : ")

    # Configuration des tournois IA vs IA
    if mode in ["5", "6", "7"]:
        # Dictionnaire des combinaisons possibles d'IA
        combinaisons = {
            "5": (IAFacile, IADifficile, "IA Facile", "IA Difficile"),
            "6": (IAFacile, IANormale, "IA Facile", "IA Normale"),
            "7": (IANormale, IADifficile, "IA Normale", "IA Difficile")
        }
        IA1, IA2, nom1, nom2 = combinaisons[mode]
        print(f"\n--- Tournoi {nom1} vs {nom2} ---")
        stats = tester_match_equitable(IA1, IA2, nom1, nom2, nb_parties=50)
        # Affichage des résultats du tournoi
        print(f"\nRésultats après 50 parties :")
        print(f"{nom1} : {stats[nom1]} victoires")
        print(f"{nom2} : {stats[nom2]} victoires")
        print(f"Matchs nuls : {stats['nuls']}")
        return

    # Configuration du mode Joueur vs IA
    ia = None
    if mode == "2":
        ia = IAFacile()
        print("\n--- IA Facile activée ---\n")
    elif mode == "3":
        ia = IANormale()
        print("\n--- IA Normale activée ---\n")
    elif mode == "4":
        ia = IADifficile()
        print("\n--- IA Difficile activée ---\n")

    # Boucle principale du jeu
    while True:
        jeu.afficher_grille()

        # Gestion du tour de l'IA
        if ia and jeu.joueur == 2:
            print(f"Tour de l'IA ({ia.__class__.__name__})...")
            col = ia.choisir_coup(jeu)
            print(f"L'IA joue en colonne {col}\n")
        else:
            # Gestion du tour du joueur humain
            try:
                col = int(input(f"Joueur {jeu.joueur}, choisissez une colonne (0-{jeu.m - 1}) : "))
                if not (0 <= col < jeu.m) or not jeu.coup_possible(col):
                    print("Colonne invalide ou pleine !\n")
                    continue
            except ValueError:
                print("Veuillez entrer un nombre valide.\n")
                continue

        jeu.jouer(col)

        # Vérification des conditions de fin de partie
        if jeu.victoire():
            jeu.afficher_grille()
            if ia and jeu.joueur == 2:
                print("L'IA remporte la partie !")
            else:
                print(f"Le Joueur {jeu.joueur} remporte la partie !")
            break
        elif jeu.match_nul():
            jeu.afficher_grille()
            print("Match nul ! Aucun gagnant.")
            break

        jeu.alterner_joueur()


if __name__ == "__main__":
    main()