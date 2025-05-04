from IA_facile import IAFacile
import random

class IANormale(IAFacile):
    def __init__(self):
        super().__init__()
        self.profondeur = 5

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

    def evaluer(self, jeu):
        def score_sequence(seq, joueur):
            score = 0
            if seq.count(joueur) == 4:
                score += 10000
            elif seq.count(joueur) == 3 and seq.count(0) == 1:
                score += 500
            elif seq.count(joueur) == 2 and seq.count(0) == 2:
                score += 50
            if seq.count(3 - joueur) == 3 and seq.count(0) == 1:
                score -= 700
            return score

        score_total = 0
        for r in range(jeu.n):
            for c in range(jeu.m - 3):
                score_total += score_sequence([jeu.grille[r][c + i] for i in range(4)], jeu.joueur)
        for c in range(jeu.m):
            for r in range(jeu.n - 3):
                score_total += score_sequence([jeu.grille[r + i][c] for i in range(4)], jeu.joueur)
        for r in range(jeu.n - 3):
            for c in range(jeu.m - 3):
                score_total += score_sequence([jeu.grille[r + i][c + i] for i in range(4)], jeu.joueur)
        for r in range(3, jeu.n):
            for c in range(jeu.m - 3):
                score_total += score_sequence([jeu.grille[r - i][c + i] for i in range(4)], jeu.joueur)

        for i in range(jeu.n):
            for j in range(jeu.m):
                if jeu.grille[i][j] == jeu.joueur:
                    score_total += self.grille_score[i][j]
                elif jeu.grille[i][j] == 3 - jeu.joueur:
                    score_total -= self.grille_score[i][j]

        return score_total
