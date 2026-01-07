# Décisions de conception

## Philosophie de design

### 1. Paranoïa par défaut

**Décision :** Le mode par défaut est `STRICT` avec toutes les vérifications activées.

**Raison :** Mieux vaut détecter les erreurs silencieuses que de les ignorer. Les utilisateurs peuvent choisir `FAST` s'ils veulent des performances.

**Impact :**
- Performance légèrement réduite (acceptable pour la plupart des cas)
- Détection proactive des problèmes numériques
- Comportement prévisible et sûr

### 2. Types spéciaux intégrés

**Décision :** Support natif pour `Interval`, `DualNumber`, `LazyExpr`, etc.

**Raison :** Ces types résolvent des problèmes réels (incertitude, gradients, optimisation).

**Impact :**
- API unifiée pour différents besoins
- Pas besoin de bibliothèques externes pour ces fonctionnalités
- Cohérence dans le comportement

### 3. Backends multiples

**Décision :** Architecture avec plusieurs backends (Python, NumPy, CuPy, Numba).

**Raison :** Différents besoins nécessitent différents outils :
- Python : portable, référence
- NumPy : performance, SIMD
- CuPy : GPU, grandes données
- Numba : JIT, calculs intensifs
- Decimal : précision arbitraire

**Impact :**
- Flexibilité maximale
- Performance optimale selon le contexte
- Dépendances optionnelles (pas de surcharge)

### 4. Tracing optionnel mais activé par défaut

**Décision :** Tracing activé par défaut mais peut être désactivé.

**Raison :** Le tracing aide à comprendre les problèmes mais a un coût en performance.

**Impact :**
- Debugging facilité
- Performance acceptable (tracing léger)
- Peut être désactivé pour la production

### 5. Vectorisation automatique

**Décision :** Vectorisation activée par défaut.

**Raison :** Les opérations sur tableaux sont courantes et bénéficient de la vectorisation.

**Impact :**
- Performance améliorée pour les tableaux
- API simple (même fonction pour scalaires et tableaux)
- Broadcasting intuitif

## Choix techniques

### 1. Structure `src/`

**Décision :** Utilisation de la structure `src/nuclear_add/` au lieu de `nuclear_add/` à la racine.

**Raison :** Meilleure pratique Python moderne :
- Évite les conflits d'imports
- Tests plus clairs (testent le package installé)
- Compatible avec les outils modernes (uv, hatchling)

### 2. Hatchling au lieu de setuptools

**Décision :** Utilisation de `hatchling` comme build backend.

**Raison :**
- Plus moderne et simple
- Meilleure intégration avec uv
- Configuration plus claire

### 3. Type hints partout

**Décision :** Type hints complets dans tout le code.

**Raison :**
- Meilleure documentation
- Vérification statique avec mypy
- Meilleure expérience IDE

### 4. Docstrings en anglais

**Décision :** Toute la documentation en anglais.

**Raison :**
- Standard de l'industrie
- Accessible à un public international
- Compatible avec les outils de documentation automatique

### 5. Tests avec pytest

**Décision :** Utilisation de pytest pour les tests.

**Raison :**
- Standard de l'industrie
- Fonctionnalités avancées (fixtures, paramétrisation)
- Intégration facile avec la couverture

## Trade-offs

### Performance vs Sécurité

**Choix :** Mode `STRICT` par défaut (sécurité) avec option `FAST` (performance).

**Justification :** Pour 99% des cas, la performance est acceptable. Pour le 1% critique, `FAST` est disponible.

### Simplicité vs Fonctionnalités

**Choix :** API simple (`add()`) avec beaucoup de fonctionnalités optionnelles.

**Justification :** L'API de base reste simple, les fonctionnalités avancées sont accessibles via des paramètres ou des types spéciaux.

### Dépendances vs Fonctionnalités

**Choix :** Dépendances optionnelles (NumPy, CuPy, etc.) avec fallback Python pur.

**Justification :** Le module fonctionne sans dépendances externes, mais peut utiliser des optimisations si disponibles.

## Extensibilité

### Points d'extension

1. **Nouveaux backends** : Implémenter l'interface `Backend`
2. **Nouveaux types** : Ajouter la gestion dans `_handle_special_types()`
3. **Nouvelles politiques** : Ajouter des enums dans `core.py`
4. **Nouveaux traceurs** : Étendre `NumericTracer`

### Exemple : Ajouter un nouveau backend

```python
class MyCustomBackend(Backend):
    @property
    def name(self) -> str:
        return "mybackend"
    
    @property
    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(...)
    
    def add(self, a, b):
        # Implémentation
        pass
```

## Considérations de performance

### Optimisations implémentées

1. **Lazy loading** : Backends chargés à la demande
2. **Cache** : Conversions de type mises en cache
3. **Vectorisation** : Utilisation de NumPy quand disponible
4. **JIT** : Support Numba pour compilation

### Points d'attention

1. **Mode PARANOID** : 10-100x plus lent (attendu)
2. **Tracing** : Léger overhead, peut être désactivé
3. **Backends GPU** : Overhead de transfert CPU↔GPU

## Compatibilité

### Versions Python

- Support : Python 3.10+
- Raison : Utilisation de fonctionnalités modernes (type hints, dataclasses)

### Plateformes

- Windows, Linux, macOS
- Backends GPU : Nécessitent CUDA (optionnel)

### Dépendances

- Aucune dépendance requise (fonctionne seul)
- Dépendances optionnelles : NumPy, CuPy, Numba, Pint, SymPy

