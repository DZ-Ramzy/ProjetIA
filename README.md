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
  - 🟢 **Facile** : stratégie naïve avec Minimax avec élagage alpha-bêta profondeur faible et pondération simple
  - 🟠 **Normal** : Minimax avec élagage alpha-bêta, meilleure évaluation (alignements, centre)
  - 🔴 **Difficile** : IA optimisée avec profondeur élevée, table de transposition, tri dynamique des coups
- Mode **Joueur vs Joueur**
- Interface console interactive
- Détection automatique des victoires/nuls

## 📦 Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/DZ-Ramzy/ProjetIA
cd puissance4-ia
```

## ▶️ Utilisation
Lancer le jeu :
```bash
python main.py
```

## 🧩 Structure du projet

```
├── main.py                                 # Programme principal
├── Puissance4.py                           # Logique du jeu
├── IA_facile.py                            # IA basique
├── IA_normale.py                           # IA intermédiaire
├── IA_difficile.py                         # IA experte
├── RAMZY_CHIBANI_MATHIEU_MOUSTACHE.pdf     # Documentation
└── README.md                               # Documentation
```


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
