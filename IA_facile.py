class IAFacile:
    """IA de base avec Minimax + alpha-beta (profondeur 4)"""

    def __init__(self):
        self.profondeur = 4

    def choisir_coup(self, jeu):
        meilleur_score = -float("inf")
        meilleur_coup = None
        alpha = -float("inf")
        beta = float("inf")

        for col in range(jeu.m):
            if jeu.coup_possible(col):
                ligne = self.jouer_temp(jeu, col, jeu.joueur)
                score = self.minimax(jeu, self.profondeur - 1, False, alpha, beta)
                self.annuler_coup(jeu, ligne, col)

                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_coup = col
                alpha = max(alpha, score)

        return meilleur_coup

    def minimax(self, jeu, profondeur, maximisant, alpha, beta):
        if profondeur == 0 or jeu.est_termine():
            return self.evaluer(jeu)

        if maximisant:
            value = -float("inf")
            for col in range(jeu.m):
                if jeu.coup_possible(col):
                    ligne = self.jouer_temp(jeu, col, jeu.joueur)
                    value = max(value, self.minimax(jeu, profondeur - 1, False, alpha, beta))
                    self.annuler_coup(jeu, ligne, col)
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return value
        else:
            value = float("inf")
            for col in range(jeu.m):
                if jeu.coup_possible(col):
                    ligne = self.jouer_temp(jeu, col, 3 - jeu.joueur)
                    value = min(value, self.minimax(jeu, profondeur - 1, True, alpha, beta))
                    self.annuler_coup(jeu, ligne, col)
                    beta = min(beta, value)
                    if beta <= alpha:
                        break
            return value

    def evaluer(self, jeu):
        score = 0
        for i in range(jeu.n):
            for j in range(jeu.m):
                if jeu.grille[i][j] == jeu.joueur:
                    score += 10
                    if j < jeu.m - 1 and jeu.grille[i][j + 1] == jeu.joueur:
                        score += 50
                    if j < jeu.m - 2 and jeu.grille[i][j + 2] == jeu.joueur:
                        score += 100
                elif jeu.grille[i][j] == 3 - jeu.joueur:
                    score -= 10
        return score

    def jouer_temp(self, jeu, col, joueur):
        for i in range(jeu.n - 1, -1, -1):
            if jeu.grille[i][col] == 0:
                jeu.grille[i][col] = joueur
                return i
        return -1

    def annuler_coup(self, jeu, ligne, col):
        if ligne != -1:
            jeu.grille[ligne][col] = 0
