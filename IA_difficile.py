from IA_normale import IANormale

class IADifficile(IANormale):
    """
    Implémentation d'une IA de niveau difficile pour le jeu de Puissance 4.
    Hérite de IANormale et ajoute des optimisations avancées.
    """
    def __init__(self):
        super().__init__()
        # Profondeur de recherche augmentée pour une meilleure stratégie
        self.profondeur = 8
        # Table de transposition pour mémoriser les positions déjà évaluées
        self.transposition_table = {}

    def choisir_coup(self, jeu):
        """
        Choisit le prochain coup à jouer avec une stratégie optimisée.
        Utilise la table de transposition et des heuristiques avancées.
        """
        # Vérification des coups gagnants et défensifs
        for col in range(jeu.m):
            if jeu.coup_possible(col):
                # Test d'un coup gagnant
                ligne = self.jouer_temp(jeu, col, jeu.joueur)
                if jeu.victoire():
                    self.annuler_coup(jeu, ligne, col)
                    return col
                self.annuler_coup(jeu, ligne, col)

                # Test d'un coup défensif
                ligne = self.jouer_temp(jeu, col, 3 - jeu.joueur)
                if jeu.victoire():
                    self.annuler_coup(jeu, ligne, col)
                    return col
                self.annuler_coup(jeu, ligne, col)

        # Initialisation des variables pour l'algorithme minimax
        meilleur_score = -float("inf")
        meilleurs_coups = []
        alpha = -float("inf")
        beta = float("inf")

        # Tri des colonnes par heuristique pour optimiser l'exploration
        colonnes = list(range(jeu.m))
        colonnes.sort(key=lambda c: -self.heuristique_colonne(jeu, c))

        # Évaluation des coups possibles
        for col in colonnes:
            if jeu.coup_possible(col):
                ligne = self.jouer_temp(jeu, col, jeu.joueur)
                score = self.minimax(jeu, self.profondeur - 1, False, alpha, beta)
                self.annuler_coup(jeu, ligne, col)

                # Mise à jour des meilleurs coups
                if score > meilleur_score:
                    meilleur_score = score
                    meilleurs_coups = [col]
                elif score == meilleur_score:
                    meilleurs_coups.append(col)

                alpha = max(alpha, score)

        # Retourne le meilleur coup sans hasard
        return meilleurs_coups[0]

    def minimax(self, jeu, profondeur, maximisant, alpha, beta):
        """
        Implémentation optimisée de l'algorithme minimax avec table de transposition.
        """
        # Vérification dans la table de transposition
        key = (tuple(map(tuple, jeu.grille)), profondeur, maximisant, jeu.joueur)
        if key in self.transposition_table:
            return self.transposition_table[key]

        # Condition d'arrêt de la récursion
        if profondeur == 0 or jeu.est_termine():
            return self.evaluer(jeu)

        # Initialisation de la valeur selon le joueur
        value = -float("inf") if maximisant else float("inf")

        # Tri des colonnes par heuristique
        colonnes = list(range(jeu.m))
        colonnes.sort(key=lambda c: -self.heuristique_colonne(jeu, c))

        # Exploration des coups possibles
        for col in colonnes:
            if not jeu.coup_possible(col):
                continue

            ligne = self.jouer_temp(jeu, col, jeu.joueur if maximisant else 3 - jeu.joueur)
            current_eval = self.minimax(jeu, profondeur - 1, not maximisant, alpha, beta)
            self.annuler_coup(jeu, ligne, col)

            # Mise à jour des valeurs alpha/beta
            if maximisant:
                value = max(value, current_eval)
                alpha = max(alpha, value)
            else:
                value = min(value, current_eval)
                beta = min(beta, value)

            # Élagage alpha-beta
            if beta <= alpha:
                break

        # Stockage du résultat dans la table de transposition
        self.transposition_table[key] = value
        return value

    def evaluer(self, jeu):
        """
        Évalue la position actuelle avec une fonction sophistiquée.
        Prend en compte les alignements, les menaces et les positions stratégiques.
        """
        def score_sequence(seq, joueur):
            """
            Évalue une séquence de 4 positions avec des scores plus sophistiqués.
            """
            score = 0
            adversaire = 3 - joueur

            # Scores pour les alignements
            if seq.count(joueur) == 4:
                score += 100000
            elif seq.count(joueur) == 3 and seq.count(0) == 1:
                score += 1000
            elif seq.count(joueur) == 2 and seq.count(0) == 2:
                score += 100
            elif seq.count(joueur) == 1 and seq.count(0) == 3:
                score += 10

            # Bonus pour les alignements ouverts
            if seq == [0, joueur, joueur, joueur] or seq == [joueur, joueur, joueur, 0]:
                score += 500

            # Pénalités pour les menaces adverses
            if seq.count(adversaire) == 3 and seq.count(0) == 1:
                score -= 1200
            elif seq.count(adversaire) == 2 and seq.count(0) == 2:
                score -= 200

            return score

        # Calcul du score total
        score_total = 0

        # Évaluation des alignements horizontaux
        for r in range(jeu.n):
            for c in range(jeu.m - 3):
                score_total += score_sequence([jeu.grille[r][c + i] for i in range(4)], jeu.joueur)
        # Évaluation des alignements verticaux
        for c in range(jeu.m):
            for r in range(jeu.n - 3):
                score_total += score_sequence([jeu.grille[r + i][c] for i in range(4)], jeu.joueur)
        # Évaluation des alignements diagonaux (haut-gauche vers bas-droite)
        for r in range(jeu.n - 3):
            for c in range(jeu.m - 3):
                score_total += score_sequence([jeu.grille[r + i][c + i] for i in range(4)], jeu.joueur)
        # Évaluation des alignements diagonaux (bas-gauche vers haut-droite)
        for r in range(3, jeu.n):
            for c in range(jeu.m - 3):
                score_total += score_sequence([jeu.grille[r - i][c + i] for i in range(4)], jeu.joueur)

        # Ajout des scores de position
        for i in range(jeu.n):
            for j in range(jeu.m):
                if jeu.grille[i][j] == jeu.joueur:
                    score_total += self.grille_score[i][j]
                elif jeu.grille[i][j] == 3 - jeu.joueur:
                    score_total -= self.grille_score[i][j]

        return score_total

    def heuristique_colonne(self, jeu, col):
        """
        Évalue une colonne selon sa position et son état.
        Utilisé pour optimiser l'ordre d'exploration des coups.
        """
        for i in range(jeu.n - 1, -1, -1):
            if jeu.grille[i][col] == 0:
                # Bonus pour les colonnes centrales
                score = 3 - abs(col - 3)
                # Bonus pour les colonnes qui peuvent créer des alignements
                if i > 0 and jeu.grille[i - 1][col] == jeu.joueur:
                    score += 2
                return score
        return -1