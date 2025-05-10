"""
Connect Four (Puissance 4) game implementation.

This module implements the core game logic for Connect Four, including:
- Board representation and state management
- Move validation and execution
- Victory detection (horizontal, vertical, diagonal)
- Game state tracking (current player, draw conditions)
"""


class Puissance4:
    """
    A class representing a Connect Four game board and its rules.

    The game is played on a 6x7 grid where players take turns dropping pieces
    into columns. The first player to connect four pieces horizontally,
    vertically, or diagonally wins.

    Attributes:
        n (int): Number of rows in the game board (6)
        m (int): Number of columns in the game board (7)
        grille (list): 2D list representing the game board
        joueur (int): Current player (1 or 2)
    """

    def __init__(self):
        """Initialize a new Connect Four game with an empty board."""
        self.n = 6  # Number of rows
        self.m = 7  # Number of columns
        self.grille = [[0 for _ in range(self.m)] for _ in range(self.n)]  # 0 = empty, 1 = player 1, 2 = player 2
        self.joueur = 1  # Player 1 starts

    def est_termine(self) -> bool:
        """
        Check if the game is over.

        Returns:
            bool: True if there is a winner or the board is full, False otherwise
        """
        return self.victoire() or self.match_nul()

    def afficher_grille(self) -> None:
        """
        Display the current state of the game board in the console.
        
        Uses ASCII characters to represent the board:
        - '.' for empty cells
        - 'X' for player 1's pieces
        - 'O' for player 2's pieces
        """
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

    def coup_possible(self, colonne: int) -> bool:
        """
        Check if a move is valid in the specified column.

        Args:
            colonne (int): The column to check (0-based index)

        Returns:
            bool: True if the column is not full, False otherwise
        """
        return self.grille[0][colonne] == 0

    def jouer(self, col: int) -> bool:
        """
        Place a piece in the specified column.

        Args:
            col (int): The column to place the piece in (0-based index)

        Returns:
            bool: True if the move was successful, False if the column is full
        """
        for i in range(self.n - 1, -1, -1):  # Start from bottom of column
            if self.grille[i][col] == 0:
                self.grille[i][col] = self.joueur
                return True
        return False

    def victoire(self) -> bool:
        """
        Check if the current player has won the game.

        Checks for four connected pieces in any direction:
        - Horizontal
        - Vertical
        - Diagonal (both directions)

        Returns:
            bool: True if the current player has won, False otherwise
        """
        for lig in range(self.n):
            for col in range(self.m):
                if self.horiz(lig, col) or self.vert(lig, col) or self.diag_haut(lig, col) or self.diag_bas(lig, col):
                    return True
        return False

    def horiz(self, lig: int, col: int) -> bool:
        """
        Check for a horizontal victory starting at the given position.

        Args:
            lig (int): Starting row
            col (int): Starting column

        Returns:
            bool: True if there are four connected pieces horizontally
        """
        return col <= self.m - 4 and all(self.grille[lig][col + i] == self.joueur for i in range(4))

    def vert(self, lig: int, col: int) -> bool:
        """
        Check for a vertical victory starting at the given position.

        Args:
            lig (int): Starting row
            col (int): Starting column

        Returns:
            bool: True if there are four connected pieces vertically
        """
        return lig <= self.n - 4 and all(self.grille[lig + i][col] == self.joueur for i in range(4))

    def diag_haut(self, lig: int, col: int) -> bool:
        """
        Check for a diagonal victory (top-left to bottom-right) starting at the given position.

        Args:
            lig (int): Starting row
            col (int): Starting column

        Returns:
            bool: True if there are four connected pieces diagonally
        """
        return lig <= self.n - 4 and col <= self.m - 4 and all(self.grille[lig + i][col + i] == self.joueur for i in range(4))

    def diag_bas(self, lig: int, col: int) -> bool:
        """
        Check for a diagonal victory (bottom-left to top-right) starting at the given position.

        Args:
            lig (int): Starting row
            col (int): Starting column

        Returns:
            bool: True if there are four connected pieces diagonally
        """
        return lig >= 3 and col <= self.m - 4 and all(self.grille[lig - i][col + i] == self.joueur for i in range(4))

    def match_nul(self) -> bool:
        """
        Check if the game is a draw (board is full).

        Returns:
            bool: True if the board is full, False otherwise
        """
        return all(cell != 0 for row in self.grille for cell in row)

    def alterner_joueur(self) -> None:
        """
        Switch the current player between 1 and 2.
        
        Player 1 becomes 2, and player 2 becomes 1.
        """
        self.joueur = 3 - self.joueur
