class Puissance4:
    def __init__(self):
        self.n = 6
        self.m = 7
        self.grille = [[0 for _ in range(self.m)] for _ in range(self.n)]
        self.joueur = 1

    def est_termine(self):
        return self.victoire() or self.match_nul()

    def afficher_grille(self):
        print(" ", end="  ")
        for j in range(self.m):
            print(f"{j} ", end="  ")
        print()
        print("   " + "--" * self.m * 2)

        for i in range(self.n):
            print(end=" | ")
            for j in range(self.m):
                if self.grille[i][j] == 0:
                    print(".", end=" | ")
                elif self.grille[i][j] == 1:
                    print("X", end=" | ")
                elif self.grille[i][j] == 2:
                    print("O", end=" | ")
            print()
        print("   " + "--" * self.m * 2)

    def coup_possible(self, colonne):
        return self.grille[0][colonne] == 0

    def jouer(self, col):
        for i in range(self.n - 1, -1, -1):
            if self.grille[i][col] == 0:
                self.grille[i][col] = self.joueur
                return True
        return False

    def victoire(self):
        for lig in range(self.n):
            for col in range(self.m):
                if self.horiz(lig, col) or self.vert(lig, col) or self.diag_haut(lig, col) or self.diag_bas(lig, col):
                    return True
        return False

    def horiz(self, lig, col):
        return col <= self.m - 4 and all(self.grille[lig][col + i] == self.joueur for i in range(4))

    def vert(self, lig, col):
        return lig <= self.n - 4 and all(self.grille[lig + i][col] == self.joueur for i in range(4))

    def diag_haut(self, lig, col):
        return lig <= self.n - 4 and col <= self.m - 4 and all(self.grille[lig + i][col + i] == self.joueur for i in range(4))

    def diag_bas(self, lig, col):
        return lig >= 3 and col <= self.m - 4 and all(self.grille[lig - i][col + i] == self.joueur for i in range(4))

    def match_nul(self):
        return all(cell != 0 for row in self.grille for cell in row)

    def alterner_joueur(self):
        self.joueur = 3 - self.joueur
