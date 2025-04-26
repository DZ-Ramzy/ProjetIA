# 🎮 Puissance 4 avec IA - Projet d'Intelligence Artificielle

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Licence](https://img.shields.io/badge/Licence-MIT-green)](LICENSE)

Un jeu de Puissance 4 implémentant des intelligences artificielles de difficulté progressive, développé dans le cadre d'un projet universitaire.

## 📋 Table des matières
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Algorithmes](#-algorithmes-implémentés)
- [Auteurs](#-auteurs)
- [Licence](#-licence)

## 🚀 Fonctionnalités

- **3 niveaux d'IA** :
  - 🟢 **Facile** : Algorithme Minimax (profondeur 4)
  - 🟠 **Normal** : Minimax + élagage alpha-beta (profondeur 6)
  - 🔴 **Difficile** : Table de transposition + heuristiques avancées (profondeur 8)
- Mode **Joueur vs Joueur**
- Interface console interactive
- Détection automatique des victoires/nuls

## 📦 Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-utilisateur/puissance4-ia.git
cd puissance4-ia
```

## ▶️ Utilisation
Lancer le jeu :
```bash
python main.py
```

## 🧩 Structure du projet

├── main.py                 # Programme principal<br>
├── Puissance4.py           # Logique du jeu<br>
├── IA_facile.py            # IA basique<br>
├── IA_normale.py           # IA intermédiaire<br>
├── IA_difficile.py         # IA experte<br>
└── README.md               # Documentation<br>

## 🧠 Algorithmes implémentés
+ Minimax avec élagage alpha-beta
+ Évaluation heuristique multi-critères :
  + Alignements (horizontal/vertical/diagonal)
  + Menaces immédiates
  + Positionnement stratégique
+ Optimisations :
  + Tri des coups par potentiel
  + Mémoization avec tables de transposition

## 👥 Auteurs
[Ramzy CHIBANI](https://github.com/DZ-Ramzy)
[Mathieu MOUSTACHE](https://github.com/whoismathieu)
