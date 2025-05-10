# Importation des modules nécessaires
import os
class Puissance4:
    """
    Implémentation du jeu de Puissance 4.
    Gère la logique du jeu, l'affichage de la grille et la détection des victoires.
    """
    def __init__(self):
        """
        Initialise une nouvelle partie de Puissance 4.
        Crée une grille vide et définit le joueur qui commence.
        """
        # Dimensions de la grille
        self.n = 6  # nombre de lignes
        self.m = 7  # nombre de colonnes
        # Création de la grille vide (0 = vide, 1 = joueur 1, 2 = joueur 2)
        self.grille = [[0 for _ in range(self.m)] for _ in range(self.n)]
        # Joueur actuel (1 ou 2)
        self.joueur = 1

    def est_termine(self):
        """
        Vérifie si la partie est terminée (victoire ou match nul).
        """
        return self.victoire() or self.match_nul()

    def afficher_grille(self):
        """
        Affiche la grille de jeu dans la console.
        Utilise des caractères spéciaux pour représenter les pions.
        """
        # Efface l'écran pour un affichage plus propre
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Affichage des numéros de colonnes
        print("  " + " ".join(str(i) for i in range(self.m)))
        
        # Affichage de la grille
        for i in range(self.n):
            print("|", end=" ")
            for j in range(self.m):
                if self.grille[i][j] == 0:
                    print("·", end=" ")
                elif self.grille[i][j] == 1:
                    print("●", end=" ")
                else:
                    print("○", end=" ")
            print("|")
        
        # Ligne de séparation
        print("+" + "-" * (2 * self.m + 1) + "+")

    def coup_possible(self, col):
        """
        Vérifie si un coup est possible dans la colonne spécifiée.
        """
        return 0 <= col < self.m and self.grille[0][col] == 0

    def jouer(self, col):
        """
        Joue un coup dans la colonne spécifiée.
        Le pion tombe jusqu'à la première case vide.
        """
        for i in range(self.n - 1, -1, -1):
            if self.grille[i][col] == 0:
                self.grille[i][col] = self.joueur
                break

    def victoire(self):
        """
        Vérifie si le joueur actuel a gagné.
        Vérifie les alignements horizontaux, verticaux et diagonaux.
        """
        return self.horiz() or self.vert() or self.diag_haut() or self.diag_bas()

    def horiz(self):
        """
        Vérifie les alignements horizontaux de 4 pions.
        """
        for i in range(self.n):
            for j in range(self.m - 3):
                if (self.grille[i][j] == self.joueur and
                    self.grille[i][j + 1] == self.joueur and
                    self.grille[i][j + 2] == self.joueur and
                    self.grille[i][j + 3] == self.joueur):
                    return True
        return False

    def vert(self):
        """
        Vérifie les alignements verticaux de 4 pions.
        """
        for i in range(self.n - 3):
            for j in range(self.m):
                if (self.grille[i][j] == self.joueur and
                    self.grille[i + 1][j] == self.joueur and
                    self.grille[i + 2][j] == self.joueur and
                    self.grille[i + 3][j] == self.joueur):
                    return True
        return False

    def diag_haut(self):
        """
        Vérifie les alignements diagonaux de 4 pions (haut-gauche vers bas-droite).
        """
        for i in range(self.n - 3):
            for j in range(self.m - 3):
                if (self.grille[i][j] == self.joueur and
                    self.grille[i + 1][j + 1] == self.joueur and
                    self.grille[i + 2][j + 2] == self.joueur and
                    self.grille[i + 3][j + 3] == self.joueur):
                    return True
        return False

    def diag_bas(self):
        """
        Vérifie les alignements diagonaux de 4 pions (bas-gauche vers haut-droite).
        """
        for i in range(3, self.n):
            for j in range(self.m - 3):
                if (self.grille[i][j] == self.joueur and
                    self.grille[i - 1][j + 1] == self.joueur and
                    self.grille[i - 2][j + 2] == self.joueur and
                    self.grille[i - 3][j + 3] == self.joueur):
                    return True
        return False

    def match_nul(self):
        """
        Vérifie si la partie est un match nul (grille pleine sans vainqueur).
        """
        return all(self.grille[0][j] != 0 for j in range(self.m))

    def alterner_joueur(self):
        """
        Change le joueur actuel (1 -> 2 ou 2 -> 1).
        """
        self.joueur = 3 - self.joueur
