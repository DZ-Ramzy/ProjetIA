import random

class IAFacile:
    def __init__(self):
        self.profondeur = 2
        self.grille_score = self.generer_grille_score(6, 7)

    def choisir_coup(self, jeu):
        for col in range(jeu.m):
            if jeu.coup_possible(col):
                ligne = self.jouer_temp(jeu, col, jeu.joueur)
                if jeu.victoire():
                    self.annuler_coup(jeu, ligne, col)
                    return col
                self.annuler_coup(jeu, ligne, col)

                ligne = self.jouer_temp(jeu, col, 3 - jeu.joueur)
                if jeu.victoire():
                    self.annuler_coup(jeu, ligne, col)
                    return col
                self.annuler_coup(jeu, ligne, col)

        meilleur_score = -float("inf")
        meilleurs_coups = []
        alpha = -float("inf")
        beta = float("inf")

        for col in range(jeu.m):
            if jeu.coup_possible(col):
                ligne = self.jouer_temp(jeu, col, jeu.joueur)
                score = self.minimax(jeu, self.profondeur - 1, False, alpha, beta)
                self.annuler_coup(jeu, ligne, col)

                if score > meilleur_score:
                    meilleur_score = score
                    meilleurs_coups = [col]
                elif score == meilleur_score:
                    meilleurs_coups.append(col)

                alpha = max(alpha, score)

        return random.choice(meilleurs_coups)

    def minimax(self, jeu, profondeur, maximisant, alpha, beta):
        if profondeur == 0 or jeu.est_termine():
            return self.evaluer(jeu)

        value = -float("inf") if maximisant else float("inf")

        for col in range(jeu.m):
            if jeu.coup_possible(col):
                ligne = self.jouer_temp(jeu, col, jeu.joueur if maximisant else 3 - jeu.joueur)
                score = self.minimax(jeu, profondeur - 1, not maximisant, alpha, beta)
                self.annuler_coup(jeu, ligne, col)

                if maximisant:
                    value = max(value, score)
                    alpha = max(alpha, value)
                else:
                    value = min(value, score)
                    beta = min(beta, value)

                if beta <= alpha:
                    break

        return value

    def evaluer(self, jeu):
        score = 0
        for i in range(jeu.n):
            for j in range(jeu.m):
                if jeu.grille[i][j] == jeu.joueur:
                    score += self.grille_score[i][j]
                elif jeu.grille[i][j] == 3 - jeu.joueur:
                    score -= self.grille_score[i][j]
        return score

    def generer_grille_score(self, n, m):
        grille = [[0 for _ in range(m)] for _ in range(n)]
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

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
        for i in range(jeu.n - 1, -1, -1):
            if jeu.grille[i][col] == 0:
                jeu.grille[i][col] = joueur
                return i
        return -1

    def annuler_coup(self, jeu, ligne, col):
        if ligne != -1:
            jeu.grille[ligne][col] = 0
