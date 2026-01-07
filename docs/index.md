# Documentation Nuclear Add

Bienvenue dans la documentation complète de Nuclear Add, le module d'addition le plus paranoïaque jamais créé.

## 📚 Table des matières

1. [Architecture](architecture.md) - Vue d'ensemble de l'architecture du système
2. [API Reference](api_reference.md) - Documentation complète de l'API
3. [Guide des méthodes](methods_guide.md) - Guide pratique d'utilisation
4. [Décisions de conception](design_decisions.md) - Pourquoi ces choix ont été faits
5. [Diagrammes](diagrams.md) - Schémas et diagrammes visuels (Mermaid)
6. [Guide de contribution](contributing.md) - Comment contribuer au projet

## 🚀 Démarrage rapide

### Installation

```bash
# Installation en mode développement
uv pip install -e .

# Ou depuis un autre projet
uv pip install -e /path/to/nuclear_add
```

### Utilisation basique

```python
from nuclear_add import add

# Addition simple
result = add(2, 3)  # 5

# Avec précision décimale
from decimal import Decimal
result = add(Decimal("0.1"), Decimal("0.2"))  # Decimal('0.3')

# Vectorisation
result = add([1, 2, 3], [4, 5, 6])  # [5, 7, 9]
```

## 🎯 Cas d'usage principaux

### 1. Calcul financier

```python
from nuclear_add import add
from decimal import Decimal

montant1 = Decimal("100.50")
montant2 = Decimal("0.25")
total = add(montant1, montant2)  # Decimal('100.75')
```

### 2. Calcul scientifique

```python
from nuclear_add import sum_safe

# Somme précise de mesures
mesures = [0.1, 0.2, 0.3, ...]  # 1000 valeurs
total = sum_safe(mesures, precision="kahan")
```

### 3. Machine Learning

```python
from nuclear_add import gradient

def loss_function(weight):
    return weight * weight * weight

grad = gradient(loss_function, 2.0)  # Gradient automatique
```

### 4. Simulation physique

```python
from nuclear_add.types import Interval

# Propagation d'incertitude
position = Interval.from_value(1.0, ulp_error=1)
vitesse = Interval.from_value(0.1, ulp_error=1)

for dt in time_steps:
    position = position + vitesse * dt

print(f"Position: {position}, Incertitude: {position.width}")
```

## 📖 Structure de la documentation

- **Architecture** : Comprendre comment le système est construit
- **API Reference** : Documentation complète de toutes les fonctions et classes
- **Guide des méthodes** : Exemples pratiques pour chaque fonctionnalité
- **Décisions de conception** : Comprendre les choix techniques

## 🔗 Liens utiles

- [README principal](../README.md)
- [Guide d'installation](../INSTALL.md)
- [Guide d'utilisation](../USAGE.md)
- [Exemple d'utilisation](../example_usage.py)

## 💡 Concepts clés

### Modes de précision

- `auto` : Détection automatique
- `float64` : Double précision IEEE 754
- `decimal` : Précision arbitraire
- `fraction` : Exact (rationnel)
- `interval` : Arithmétique d'intervalles

### Modes de calcul

- `strict` : Toutes les vérifications (défaut)
- `fast` : Optimisé, moins de vérifications
- `paranoid` : Toutes les vérifications + tracing complet

### Politiques d'erreur

- `raise` : Lever une exception (défaut)
- `inf` / `propagate` : Retourner une valeur spéciale
- `saturate` / `replace` : Remplacer par une valeur sûre

## 🎓 Apprendre par l'exemple

Consultez [methods_guide.md](methods_guide.md) pour des exemples détaillés de chaque fonctionnalité.

## 🤝 Contribution

Pour contribuer au projet, consultez le README principal et les décisions de conception pour comprendre la philosophie du projet.

