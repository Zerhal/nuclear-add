# Architecture de Nuclear Add

## Vue d'ensemble

Nuclear Add est conçu avec une architecture modulaire permettant une extensibilité et une maintenabilité maximales.

```
┌─────────────────────────────────────────────────────────────┐
│                      User API Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   add()  │  │sum_safe()│  │gradient()│  │  types   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Core Engine Layer                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            NuclearEngine                            │   │
│  │  ┌──────────────┐  ┌──────────────┐                │   │
│  │  │ NuclearConfig│  │ TypePromotion│                │   │
│  │  └──────────────┘  └──────────────┘                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Backends   │  │    Types     │  │   Tracing    │
│              │  │              │  │              │
│ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │
│ │ Python   │ │  │ │ Interval │ │  │ │ Tracer   │ │
│ │ NumPy    │ │  │ │ DualNum  │ │  │ │ Analyzer │ │
│ │ CuPy     │ │  │ │ LazyExpr │ │  │ │ Detector │ │
│ │ Numba    │ │  │ │ Traced   │ │  │ └──────────┘ │
│ │ Decimal  │ │  │ │ Stochastic│ │  └──────────────┘
│ └──────────┘ │  │ └──────────┘ │
└──────────────┘  └──────────────┘
```

## Modules principaux

### 1. Core (`core.py`)

**Responsabilités :**
- Configuration du moteur (`NuclearConfig`)
- Exécution des calculs (`NuclearEngine`)
- Fonction principale `add()`
- Gestion des politiques d'erreur
- Promotion des types

**Classes principales :**
- `NuclearConfig` : Configuration complète du moteur
- `NuclearEngine` : Moteur d'exécution
- `TypePromotionRules` : Règles de conversion de types
- `OverflowPolicy`, `NaNPolicy`, `PrecisionMode`, `MathMode` : Enums de configuration

### 2. Backends (`backends.py`)

**Responsabilités :**
- Abstraction des différents backends de calcul
- Sélection automatique du meilleur backend
- Optimisations spécifiques (SIMD, GPU, JIT)

**Backends disponibles :**
- `PythonBackend` : Python pur (portable, référence)
- `NumPyBackend` : NumPy avec optimisations SIMD
- `CuPyBackend` : Calcul GPU CUDA (optionnel)
- `NumbaBackend` : Compilation JIT (optionnel)
- `DecimalBackend` : Précision arbitraire

**Pattern :**
```python
Backend (ABC)
    ├── PythonBackend
    ├── NumPyBackend
    ├── CuPyBackend
    ├── NumbaBackend
    └── DecimalBackend
```

### 3. Types (`types.py`)

**Types avancés disponibles :**

#### Interval
- Arithmétique d'intervalles pour propagation d'incertitude
- Garantit que la vraie valeur est dans l'intervalle

#### DualNumber
- Différentiation automatique (forward mode)
- Calcule valeur + dérivée simultanément

#### LazyExpr
- Évaluation paresseuse
- Graphes de calcul
- Différentiation symbolique

#### TracedValue
- Historique complet des opérations
- Traçabilité pour debugging

#### StochasticValue
- Arrondi stochastique
- Élimine le biais systématique

### 4. Tracing (`tracing.py`)

**Responsabilités :**
- Enregistrement des erreurs numériques
- Analyse de précision
- Détection d'overflow/underflow
- Rapports et statistiques

**Composants :**
- `NumericTracer` : Traceur principal
- `PrecisionAnalyzer` : Analyse de précision
- `OverflowDetector` : Détection d'overflow
- `ErrorEvent`, `ErrorType`, `ErrorSeverity` : Types d'événements

## Flux de données

### Addition simple

```
User calls add(a, b)
    │
    ▼
NuclearEngine.add()
    │
    ├─► _handle_special_types()  (Interval, DualNumber, etc.)
    │
    ├─► _validate_inputs()       (Vérification types)
    │
    ├─► _promote_types()         (Conversion types)
    │
    ├─► _check_pre_operation()   (Détection overflow)
    │
    ├─► _compute_add()           (Calcul via backend)
    │
    └─► _check_post_operation()  (Vérification résultat)
```

### Avec tracing

```
Operation
    │
    ├─► PrecisionAnalyzer.check_addition()
    │   └─► Detect precision loss
    │
    ├─► OverflowDetector.will_overflow_add()
    │   └─► Predict overflow
    │
    └─► NumericTracer.log_error()
        └─► Record event
```

## Sélection de backend

```
Data Input
    │
    ├─► Size < 100? ──► PythonBackend
    │
    ├─► Needs precision? ──► DecimalBackend
    │
    ├─► GPU available? ──► CuPyBackend
    │
    ├─► Numba available? ──► NumbaBackend
    │
    └─► NumPy available? ──► NumPyBackend
```

## Gestion des erreurs

```
Error Detection
    │
    ├─► Overflow ──► Policy: RAISE/INF/SATURATE/WRAP
    │
    ├─► NaN ──► Policy: RAISE/PROPAGATE/REPLACE
    │
    ├─► Precision Loss ──► Log to Tracer
    │
    └─► Type Coercion ──► Warning or Error
```

## Extensibilité

Le système est conçu pour être extensible :

1. **Nouveaux backends** : Implémenter l'interface `Backend`
2. **Nouveaux types** : Ajouter la gestion dans `_handle_special_types()`
3. **Nouvelles politiques** : Ajouter des enums et logique dans `NuclearConfig`
4. **Nouveaux traceurs** : Étendre `NumericTracer` ou créer des analyseurs spécialisés

