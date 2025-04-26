from IA_normale import IANormale


class IADifficile(IANormale):
    """IA experte avec profondeur 8 et optimisations avancées"""

    def __init__(self):
        super().__init__()
        self.profondeur = 8
        self.transposition_table = {}

    def minimax(self, jeu, profondeur, maximisant, alpha, beta):
        key = (tuple(tuple(row) for row in jeu.grille), profondeur, maximisant)
        if key in self.transposition_table:
            return self.transposition_table[key]

        if profondeur == 0 or jeu.est_termine():
            return self.evaluer(jeu)

        value = -float("inf") if maximisant else float("inf")
        colonnes = sorted(range(jeu.m), key=lambda x: self.eval_rapide(jeu, x), reverse=maximisant)

        for col in colonnes:
            if not jeu.coup_possible(col):
                continue

            ligne = self.jouer_temp(jeu, col, jeu.joueur if maximisant else 3 - jeu.joueur)
            current_eval = self.minimax(jeu, profondeur - 1, not maximisant, alpha, beta)
            self.annuler_coup(jeu, ligne, col)

            if maximisant:
                value = max(value, current_eval)
                alpha = max(alpha, value)
            else:
                value = min(value, current_eval)
                beta = min(beta, value)

            if alpha >= beta:
                break

        self.transposition_table[key] = value
        return value

    def eval_rapide(self, jeu, col):
        for i in range(jeu.n - 1, -1, -1):
            if jeu.grille[i][col] == 0:
                return self.potentiel_position(jeu, i, col)
        return -1

    def potentiel_position(self, jeu, row, col):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1), (-1, 0), (0, -1)]

        for dx, dy in directions:
            sequence = 0
            for step in range(1, 4):
                x = row + dx * step
                y = col + dy * step
                if 0 <= x < jeu.n and 0 <= y < jeu.m:
                    if jeu.grille[x][y] == jeu.joueur:
                        sequence += 1
                    elif jeu.grille[x][y] == 0:
                        sequence += 0.5
            score += sequence * 10

        return score

    def evaluer(self, jeu):
        score = super().evaluer(jeu)
        if self.detecte_menace(jeu, jeu.joueur):
            score += 10000
        if self.detecte_menace(jeu, 3 - jeu.joueur):
            score -= 15000
        return score

    def detecte_menace(self, jeu, player):
        for col in range(jeu.m):
            if jeu.coup_possible(col):
                ligne = self.jouer_temp(jeu, col, player)
                if jeu.victoire():
                    self.annuler_coup(jeu, ligne, col)
                    return True
                self.annuler_coup(jeu, ligne, col)
        return False
