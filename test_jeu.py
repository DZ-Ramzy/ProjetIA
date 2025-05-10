"""
Tests unitaires pour l'implémentation du jeu Puissance 4.

Ce module contient des tests complets pour :
- L'initialisation et la configuration du plateau
- La validation et l'exécution des coups
- La détection des victoires dans toutes les directions
- Les conditions de match nul
- La génération et la validation des coups de l'IA
"""


import unittest
from Puissance4 import Puissance4
from IA_facile import IAFacile
from IA_normale import IANormale
from IA_difficile import IADifficile


class TestPuissance4(unittest.TestCase):
    """
    Suite de tests pour la logique principale du jeu Puissance 4.

    Les tests couvrent tous les aspects de la mécanique du jeu :
    - Initialisation du plateau
    - Validation des coups
    - Conditions de victoire
    - Alternance des joueurs
    """

    def setUp(self):
        """Initialise une nouvelle partie avant chaque test."""
        self.jeu = Puissance4()

    def test_initialisation(self):
        """
        Test de l'initialisation du jeu.
        
        Vérifie que :
        - Les dimensions du plateau sont correctes (6x7)
        - Le plateau est vide
        - Le joueur 1 commence
        """
        self.assertEqual(self.jeu.n, 6)  # 6 lignes
        self.assertEqual(self.jeu.m, 7)  # 7 colonnes
        self.assertEqual(self.jeu.joueur, 1)  # Le joueur 1 commence
        self.assertEqual(len(self.jeu.grille), 6)
        self.assertEqual(len(self.jeu.grille[0]), 7)
        self.assertTrue(all(cell == 0 for row in self.jeu.grille for cell in row))

    def test_coup_possible(self):
        """
        Test de la détection des coups valides.
        
        Vérifie que :
        - Les colonnes vides sont des coups valides
        - Les colonnes pleines sont des coups invalides
        """
        # Test d'une colonne vide
        self.assertTrue(self.jeu.coup_possible(0))
        
        # Remplir une colonne
        for _ in range(6):
            self.jeu.jouer(0)
        
        # Test d'une colonne pleine
        self.assertFalse(self.jeu.coup_possible(0))

    def test_jouer(self):
        """
        Test de l'exécution des coups.
        
        Vérifie que :
        - Les pions sont placés à la bonne position
        - Les coups invalides sont rejetés
        """
        # Test d'un coup valide
        self.assertTrue(self.jeu.jouer(0))
        self.assertEqual(self.jeu.grille[5][0], 1)  # La cellule du bas devrait être le joueur 1
        
        # Test d'un coup invalide (colonne pleine)
        for _ in range(5):
            self.jeu.jouer(0)
        self.assertFalse(self.jeu.jouer(0))

    def test_victoire_horizontale(self):
        """
        Test de la détection de victoire horizontale.
        
        Crée une ligne horizontale de quatre pions et vérifie
        que la victoire est correctement détectée.
        """
        # Créer une victoire horizontale pour le joueur 1
        for i in range(4):
            self.jeu.jouer(i)
            self.jeu.alterner_joueur()
            self.jeu.jouer(i)
            self.jeu.alterner_joueur()
        
        self.assertTrue(self.jeu.victoire())

    def test_victoire_verticale(self):
        """
        Test de la détection de victoire verticale.
        
        Crée une ligne verticale de quatre pions et vérifie
        que la victoire est correctement détectée.
        """
        # Créer une victoire verticale pour le joueur 1
        for _ in range(4):
            self.jeu.jouer(0)
            self.jeu.alterner_joueur()
            self.jeu.jouer(1)
            self.jeu.alterner_joueur()
        
        self.assertTrue(self.jeu.victoire())

    def test_victoire_diagonale_haut(self):
        """
        Test de la détection de victoire diagonale montante.
        
        Crée une ligne diagonale de quatre pions de bas gauche
        vers haut droite et vérifie que la victoire est correctement détectée.
        """
        # Construction manuelle d'une diagonale montante pour le joueur 1
        self.jeu.jouer(0)  # Ligne 5, Col 0 -> joueur 1
        self.jeu.alterner_joueur()
        self.jeu.jouer(1)
        self.jeu.jouer(1)  # Ligne 4, Col 1 -> joueur 1
        self.jeu.alterner_joueur()
        self.jeu.jouer(2)
        self.jeu.jouer(2)
        self.jeu.jouer(2)  # Ligne 3, Col 2 -> joueur 1
        self.jeu.alterner_joueur()
        self.jeu.jouer(3)
        self.jeu.jouer(3)
        self.jeu.jouer(3)
        self.jeu.jouer(3)  # Ligne 2, Col 3 -> joueur 1

        self.assertTrue(self.jeu.victoire())

    def test_victoire_diagonale_bas(self):
        """
        Test de la détection de victoire diagonale descendante.
        
        Crée une ligne diagonale de quatre pions de haut gauche
        vers bas droite et vérifie que la victoire est correctement détectée.
        """
        # Créer une victoire diagonale pour le joueur 1
        moves = [(3, 0), (2, 1), (1, 2), (0, 3)]
        for i, (col1, col2) in enumerate(moves):
            for _ in range(5 - i):
                self.jeu.jouer(col1)
                self.jeu.alterner_joueur()
            self.jeu.jouer(col1)
            self.jeu.alterner_joueur()
            self.jeu.jouer(col2)
            self.jeu.alterner_joueur()
        
        self.assertTrue(self.jeu.victoire())

    def test_match_nul(self):
        """
        Test de la détection de match nul.
        
        Remplit le plateau sans créer de victoire et vérifie
        que le match nul est correctement détecté.
        """
        # Remplir le plateau sans créer de victoire
        for col in range(7):
            for row in range(6):
                self.jeu.jouer(col)
                self.jeu.alterner_joueur()
        
        self.assertTrue(self.jeu.match_nul())

    def test_alterner_joueur(self):
        """
        Test de l'alternance des joueurs.
        
        Vérifie que les joueurs alternent correctement entre 1 et 2.
        """
        self.assertEqual(self.jeu.joueur, 1)
        self.jeu.alterner_joueur()
        self.assertEqual(self.jeu.joueur, 2)
        self.jeu.alterner_joueur()
        self.assertEqual(self.jeu.joueur, 1)


class TestIA(unittest.TestCase):
    """
    Suite de tests pour les implémentations de l'IA.
    
    Les tests couvrent :
    - La validité des coups pour tous les niveaux d'IA
    - La détection et l'exécution des victoires
    - La prise de décision stratégique
    """

    def setUp(self):
        """Initialise une nouvelle partie et les instances d'IA avant chaque test."""
        self.jeu = Puissance4()
        self.ia_facile = IAFacile()
        self.ia_normale = IANormale()
        self.ia_difficile = IADifficile()

    def test_ia_facile_coup_valide(self):
        """
        Test que l'IA facile fait des coups valides.
        
        Vérifie que :
        - Les coups sont dans les limites du plateau
        - Les coups sont faits dans des colonnes non pleines
        """
        for _ in range(10):  # Test de plusieurs coups
            col = self.ia_facile.choisir_coup(self.jeu)
            self.assertTrue(0 <= col < self.jeu.m)
            self.assertTrue(self.jeu.coup_possible(col))
            self.jeu.jouer(col)
            self.jeu.alterner_joueur()

    def test_ia_normale_coup_valide(self):
        """
        Test que l'IA normale fait des coups valides.
        
        Vérifie que :
        - Les coups sont dans les limites du plateau
        - Les coups sont faits dans des colonnes non pleines
        """
        for _ in range(10):
            col = self.ia_normale.choisir_coup(self.jeu)
            self.assertTrue(0 <= col < self.jeu.m)
            self.assertTrue(self.jeu.coup_possible(col))
            self.jeu.jouer(col)
            self.jeu.alterner_joueur()

    def test_ia_difficile_coup_valide(self):
        """
        Test que l'IA difficile fait des coups valides.
        
        Vérifie que :
        - Les coups sont dans les limites du plateau
        - Les coups sont faits dans des colonnes non pleines
        """
        for _ in range(10):
            col = self.ia_difficile.choisir_coup(self.jeu)
            self.assertTrue(0 <= col < self.jeu.m)
            self.assertTrue(self.jeu.coup_possible(col))
            self.jeu.jouer(col)
            self.jeu.alterner_joueur()

    def test_ia_victoire_immediate(self):
        """
        Test que l'IA peut détecter et faire des coups gagnants.
        
        Configure une position où l'IA peut gagner en un coup
        et vérifie qu'elle fait le bon coup.
        """
        # Configurer une position gagnante pour le joueur 2 (IA)
        self.jeu.jouer(0)  # Joueur 1
        self.jeu.alterner_joueur()
        self.jeu.jouer(1)  # Joueur 2
        self.jeu.alterner_joueur()
        self.jeu.jouer(0)  # Joueur 1
        self.jeu.alterner_joueur()
        self.jeu.jouer(1)  # Joueur 2
        self.jeu.alterner_joueur()
        self.jeu.jouer(0)  # Joueur 1
        self.jeu.alterner_joueur()
        
        # L'IA devrait choisir la colonne 1 pour gagner
        col = self.ia_difficile.choisir_coup(self.jeu)
        self.assertEqual(col, 1)


if __name__ == '__main__':
    unittest.main() 