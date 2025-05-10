from IA_facile import IAFacile
import random

class IANormale(IAFacile):
    """
    Implémentation d'une IA de niveau normal pour le jeu de Puissance 4.
    Hérite de IAFacile et améliore la stratégie avec une meilleure évaluation.
    """
    def __init__(self):
        super().__init__()
        # Augmentation de la profondeur de recherche pour une meilleure stratégie
        self.profondeur = 5

    def choisir_coup(self, jeu):
        """
        Choisit le prochain coup à jouer avec une stratégie améliorée.
        Vérifie d'abord les coups gagnants et défensifs.
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

        # Évaluation de tous les coups possibles
        for col in range(jeu.m):
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

        # Choix aléatoire parmi les meilleurs coups
        return random.choice(meilleurs_coups)

    def evaluer(self, jeu):
        """
        Évalue la position actuelle avec une fonction d'évaluation améliorée.
        Prend en compte les alignements et les menaces.
        """
        def score_sequence(seq, joueur):
            """
            Évalue une séquence de 4 positions.
            Attribue des scores différents selon le nombre de pions alignés.
            """
            score = 0
            # Score pour une victoire
            if seq.count(joueur) == 4:
                score += 10000
            # Score pour trois pions alignés avec un espace
            elif seq.count(joueur) == 3 and seq.count(0) == 1:
                score += 500
            # Score pour deux pions alignés avec deux espaces
            elif seq.count(joueur) == 2 and seq.count(0) == 2:
                score += 50
            # Pénalité pour une menace adverse
            if seq.count(3 - joueur) == 3 and seq.count(0) == 1:
                score -= 700
            return score

        # Calcul du score total en évaluant toutes les séquences possibles
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
