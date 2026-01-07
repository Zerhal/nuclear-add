# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.0.0] - 2024-01-07

### Ajouté

- Fonction principale `add()` avec support de multiples modes de précision
- Système de configuration flexible (`NuclearConfig`)
- Moteur d'exécution (`NuclearEngine`)
- Support de plusieurs backends (Python, NumPy, CuPy, Numba, Decimal)
- Types avancés :
  - `Interval` : Arithmétique d'intervalles
  - `DualNumber` : Différentiation automatique
  - `LazyExpr` : Évaluation paresseuse et graphes de calcul
  - `TracedValue` : Valeurs avec historique complet
  - `StochasticValue` : Arrondi stochastique
- Système de tracing des erreurs numériques (`NumericTracer`)
- Analyseurs spécialisés (`PrecisionAnalyzer`, `OverflowDetector`)
- Fonctions utilitaires :
  - `sum_safe()` : Somme sécurisée avec Kahan/Neumaier/Pairwise
  - `gradient()` : Calcul de gradient automatique
  - `add_with_error()` : Addition avec bornes d'erreur
- Support de la vectorisation
- Support des unités (Pint)
- Support symbolique (SymPy) en fallback
- Documentation complète dans `docs/`
- Suite de tests complète
- CI/CD avec GitHub Actions

### Configuration

- Modes de calcul : `STRICT`, `FAST`, `PARANOID`
- Modes de précision : `AUTO`, `FLOAT64`, `DECIMAL`, `FRACTION`, `INTERVAL`
- Politiques d'overflow : `RAISE`, `INF`, `SATURATE`, `WRAP`
- Politiques NaN : `RAISE`, `PROPAGATE`, `REPLACE`

### Documentation

- Architecture complète documentée
- Référence API complète
- Guide pratique avec exemples
- Diagrammes et schémas
- Décisions de conception documentées

