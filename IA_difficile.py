from IA_normale import IANormale

class IADifficile(IANormale):
    def __init__(self):
        super().__init__()
        self.profondeur = 8  # Profondeur augmentée
        self.transposition_table = {}

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

        colonnes = list(range(jeu.m))
        colonnes.sort(key=lambda c: -self.heuristique_colonne(jeu, c))  # tri vers le centre

        for col in colonnes:
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

        return meilleurs_coups[0]  # Aucun hasard

    def minimax(self, jeu, profondeur, maximisant, alpha, beta):
        key = (tuple(map(tuple, jeu.grille)), profondeur, maximisant, jeu.joueur)
        if key in self.transposition_table:
            return self.transposition_table[key]

        if profondeur == 0 or jeu.est_termine():
            return self.evaluer(jeu)

        value = -float("inf") if maximisant else float("inf")

        colonnes = list(range(jeu.m))
        colonnes.sort(key=lambda c: -self.heuristique_colonne(jeu, c))

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

            if beta <= alpha:
                break

        self.transposition_table[key] = value
        return value

    def evaluer(self, jeu):
        def score_sequence(seq, joueur):
            score = 0
            adversaire = 3 - joueur

            if seq.count(joueur) == 4:
                score += 100000
            elif seq.count(joueur) == 3 and seq.count(0) == 1:
                score += 1000
            elif seq.count(joueur) == 2 and seq.count(0) == 2:
                score += 100
            elif seq.count(joueur) == 1 and seq.count(0) == 3:
                score += 10

            if seq == [0, joueur, joueur, joueur] or seq == [joueur, joueur, joueur, 0]:
                score += 500  # alignement ouvert

            if seq.count(adversaire) == 3 and seq.count(0) == 1:
                score -= 1200
            elif seq.count(adversaire) == 2 and seq.count(0) == 2:
                score -= 150

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

    def heuristique_colonne(self, jeu, col):
        for i in range(jeu.n - 1, -1, -1):
            if jeu.grille[i][col] == 0:
                return self.grille_score[i][col]
        return -100

