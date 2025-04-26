from collections import defaultdict

from IA_facile import IAFacile


class IANormale(IAFacile):
    """IA intermédiaire avec profondeur 6 et meilleure évaluation"""

    def __init__(self):
        super().__init__()
        self.profondeur = 6

    def choisir_coup(self, jeu):
        meilleur_score = -float("inf")
        alpha = -float("inf")
        beta = float("inf")
        colonnes = sorted(range(jeu.m), key=lambda x: abs(x - jeu.m // 2))

        for col in colonnes:
            if jeu.coup_possible(col):
                ligne = self.jouer_temp(jeu, col, jeu.joueur)
                score = self.minimax(jeu, self.profondeur - 1, False, alpha, beta)
                self.annuler_coup(jeu, ligne, col)

                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_coup = col
                alpha = max(alpha, score)
        return meilleur_coup

    def evaluer(self, jeu):
        score = 0
        weights = {2: 50, 3: 200, 4: 1000}

        for dir in ['h', 'v', 'd1', 'd2']:
            seq = self.detect_sequences(jeu, jeu.joueur, dir)
            seq_adv = self.detect_sequences(jeu, 3 - jeu.joueur, dir)

            for k, v in seq.items():
                score += weights.get(k, 0) * v
            for k, v in seq_adv.items():
                score -= weights.get(k, 0) * v * 1.5

        return score

    def detect_sequences(self, jeu, player, direction):
        sequences = defaultdict(int)
        n, m = jeu.n, jeu.m

        for i in range(n):
            for j in range(m):
                if jeu.grille[i][j] == player:
                    count = 1
                    ni, nj = i, j
                    while True:
                        if direction == 'h':
                            nj += 1
                        elif direction == 'v':
                            ni += 1
                        elif direction == 'd1':
                            ni += 1; nj += 1
                        else:
                            ni += 1; nj -= 1

                        if 0 <= ni < n and 0 <= nj < m and jeu.grille[ni][nj] == player:
                            count += 1
                        else:
                            break
                    if count >= 2:
                        sequences[count] += 1
        return sequences
