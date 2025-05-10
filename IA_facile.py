import random

class IAFacile:
    """
    Implémentation d'une IA de niveau facile pour le jeu de Puissance 4.
    Utilise des règles heuristiques simples et une profondeur de recherche limitée.
    """
    def __init__(self):
        # Profondeur de recherche limitée pour une IA facile
        self.profondeur = 2
        # Grille de scores pour évaluer les positions
        self.grille_score = self.generer_grille_score(6, 7)

    def choisir_coup(self, jeu):
        """
        Choisit le prochain coup à jouer en utilisant une stratégie simple.
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

    def minimax(self, jeu, profondeur, maximisant, alpha, beta):
        """
        Implémentation de l'algorithme minimax avec élagage alpha-beta.
        Évalue les positions jusqu'à une profondeur donnée.
        """
        # Conditions d'arrêt
        if profondeur == 0 or jeu.est_termine():
            return self.evaluer(jeu)

        # Initialisation de la valeur selon le joueur
        value = -float("inf") if maximisant else float("inf")

        # Exploration des coups possibles
        for col in range(jeu.m):
            if jeu.coup_possible(col):
                ligne = self.jouer_temp(jeu, col, jeu.joueur if maximisant else 3 - jeu.joueur)
                score = self.minimax(jeu, profondeur - 1, not maximisant, alpha, beta)
                self.annuler_coup(jeu, ligne, col)

                # Mise à jour des valeurs alpha/beta
                if maximisant:
                    value = max(value, score)
                    alpha = max(alpha, value)
                else:
                    value = min(value, score)
                    beta = min(beta, value)

                # Élagage alpha-beta
                if beta <= alpha:
                    break

        return value

    def evaluer(self, jeu):
        """
        Évalue la position actuelle en utilisant la grille de scores.
        Compare les positions des pions de l'IA et de l'adversaire.
        """
        score = 0
        for i in range(jeu.n):
            for j in range(jeu.m):
                if jeu.grille[i][j] == jeu.joueur:
                    score += self.grille_score[i][j]
                elif jeu.grille[i][j] == 3 - jeu.joueur:
                    score -= self.grille_score[i][j]
        return score

    def generer_grille_score(self, n, m):
        """
        Génère une grille de scores basée sur les alignements possibles.
        Les positions centrales ont un score plus élevé.
        """
        grille = [[0 for _ in range(m)] for _ in range(n)]
        # Directions possibles pour les alignements
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

        # Calcul des scores pour chaque position
        for i in range(n):
            for j in range(m):
                for dx, dy in directions:
                    for k in range(-3, 1):
                        positions = []
                        for l in range(4):
                            x = i + (k + l) * dx
                            y = j + (k + l) * dy
                            if 0 <= x < n and 0 <= y < m:
                                positions.append((x, y))
                            else:
                                break
                        if len(positions) == 4:
                            grille[i][j] += 1
        return grille

    def jouer_temp(self, jeu, col, joueur):
        """
        Joue temporairement un coup pour l'évaluation.
        Retourne la ligne où le coup a été joué.
        """
        for i in range(jeu.n - 1, -1, -1):
            if jeu.grille[i][col] == 0:
                jeu.grille[i][col] = joueur
                return i
        return -1

    def annuler_coup(self, jeu, ligne, col):
        """
        Annule un coup temporaire en remettant la case à 0.
        """
        if ligne != -1:
            jeu.grille[ligne][col] = 0
