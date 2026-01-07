# API Reference

## Fonctions principales

### `add(a, b, **kwargs)`

Fonction principale d'addition sécurisée.

**Paramètres :**
- `a` : Premier opérande (nombre, séquence, ou type spécial)
- `b` : Second opérande (nombre, séquence, ou type spécial)
- `mode` : Mode de calcul (`"strict"`, `"fast"`, `"paranoid"`)
- `precision` : Mode de précision (`"auto"`, `"float64"`, `"decimal"`, `"fraction"`, `"interval"`)
- `overflow` : Politique d'overflow (`"raise"`, `"inf"`, `"saturate"`, `"wrap"`)
- `nan` : Politique NaN (`"raise"`, `"propagate"`, `"replace"`)
- `vectorize` : Activer la vectorisation (défaut: `True`)
- `units` : Supporter les unités Pint (défaut: `True`)
- `trace` : Activer le tracing (défaut: `True`)
- `kahan` : Utiliser Kahan pour les sommes (défaut: `True`)

**Retourne :**
- Résultat de l'addition (type dépend des opérandes)

**Exemples :**
```python
add(2, 3)  # 5
add(0.1, 0.2, precision="decimal")  # Decimal('0.3')
add([1, 2, 3], [4, 5, 6])  # [5, 7, 9]
```

**Raises :**
- `TypeError` : Si les types ne sont pas numériques
- `OverflowError` : Si overflow et `overflow="raise"`
- `ArithmeticError` : Si NaN et `nan="raise"`

---

### `sum_safe(values, precision="kahan", **kwargs)`

Somme sécurisée de plusieurs valeurs avec compensation d'erreur.

**Paramètres :**
- `values` : Séquence de valeurs à sommer
- `precision` : Algorithme (`"kahan"`, `"pairwise"`, `"neumaier"`, `"auto"`)

**Retourne :**
- Somme avec précision maximale

**Exemples :**
```python
values = [0.1] * 100
sum_safe(values, precision="kahan")  # 10.0 (précis)
```

---

### `gradient(f, x)`

Calcule le gradient d'une fonction par différentiation automatique.

**Paramètres :**
- `f` : Fonction à différencier (callable)
- `x` : Point où calculer le gradient

**Retourne :**
- Valeur du gradient `f'(x)`

**Exemples :**
```python
def f(x):
    return x * x * x

gradient(f, 2.0)  # 12.0 (= 3×2²)
```

---

### `add_with_error(a, b)`

Addition retournant aussi les bornes d'erreur.

**Paramètres :**
- `a` : Premier opérande (float)
- `b` : Second opérande (float)

**Retourne :**
- Tuple `(résultat, intervalle)` contenant la vraie valeur

**Exemples :**
```python
result, bounds = add_with_error(0.1, 0.2)
# result = 0.30000000000000004
# bounds = Interval garantissant que 0.3 est dedans
```

---

## Classes principales

### `NuclearConfig`

Configuration complète du moteur d'addition.

**Méthodes de classe :**
- `strict()` : Mode strict IEEE 754
- `fast()` : Mode rapide, moins de vérifications
- `paranoid()` : Mode paranoïaque, toutes vérifications
- `scientific(precision=100)` : Mode scientifique haute précision

**Attributs principaux :**
- `math_mode` : Mode de calcul (`MathMode`)
- `precision_mode` : Mode de précision (`PrecisionMode`)
- `overflow_policy` : Politique d'overflow (`OverflowPolicy`)
- `nan_policy` : Politique NaN (`NaNPolicy`)
- `decimal_precision` : Précision décimale (int)
- `enable_tracing` : Activer le tracing (bool)
- `vectorize` : Activer la vectorisation (bool)

**Exemples :**
```python
config = NuclearConfig.strict()
config = NuclearConfig.paranoid()
config = NuclearConfig.scientific(precision=200)
```

---

### `NuclearEngine`

Moteur d'exécution pour le calcul numérique.

**Méthodes :**
- `add(a, b)` : Addition principale
- `add_many(values, use_kahan=None)` : Somme de plusieurs valeurs
- `add_interval(a, b, ulp_error=1)` : Addition avec intervalles
- `add_autodiff(a, b, grad_a=True)` : Addition avec autodiff
- `add_symbolic(a, b)` : Addition symbolique (SymPy)

**Propriétés :**
- `backend` : Backend actuel (lazy-loaded)
- `tracer` : Traceur actuel
- `config` : Configuration

**Exemples :**
```python
engine = NuclearEngine(NuclearConfig.paranoid())
result = engine.add(2, 3)
```

---

## Types avancés

### `Interval`

Arithmétique d'intervalles pour propagation d'incertitude.

**Méthodes de classe :**
- `from_value(value, ulp_error=1)` : Créer depuis une valeur
- `exact(value)` : Créer un intervalle exact

**Propriétés :**
- `low`, `high` : Bornes de l'intervalle
- `midpoint` : Point central
- `width` : Largeur totale
- `radius` : Rayon (demi-largeur)
- `relative_error` : Erreur relative

**Méthodes :**
- `overlaps(other)` : Vérifie le chevauchement
- `contains_interval(other)` : Vérifie l'inclusion
- `sqrt()` : Racine carrée

**Exemples :**
```python
a = Interval.from_value(0.1)
b = Interval.from_value(0.2)
c = a + b
print(0.3 in c)  # True
```

---

### `DualNumber`

Nombre dual pour différentiation automatique.

**Méthodes de classe :**
- `variable(value)` : Créer une variable (dual=1)
- `constant(value)` : Créer une constante (dual=0)

**Propriétés :**
- `real` : Valeur réelle
- `dual` : Dérivée

**Méthodes :**
- `exp()`, `log()`, `sin()`, `cos()`, `sqrt()` : Fonctions mathématiques

**Exemples :**
```python
x = DualNumber.variable(3.0)
y = x * x  # f(x) = x²
print(y.real)  # 9.0
print(y.dual)  # 6.0 (= 2x)
```

---

### `LazyExpr`

Expression paresseuse pour graphes de calcul.

**Méthodes de classe :**
- `var(name, value)` : Créer une variable
- `const(value)` : Créer une constante

**Méthodes :**
- `eval()` : Évaluer l'expression
- `grad(var_name)` : Calculer le gradient symbolique
- `to_graph()` : Générer le graphe DOT

**Exemples :**
```python
x = LazyExpr.var("x", 3.0)
y = LazyExpr.var("y", 4.0)
z = (x * x + y * y).sqrt()
print(z.eval())  # 5.0
print(z.grad("x").eval())  # 0.6
```

---

### `TracedValue`

Valeur avec historique complet des opérations.

**Méthodes :**
- `get_full_trace()` : Obtenir le trace complet formaté

**Exemples :**
```python
a = TracedValue(10.0)
b = TracedValue(5.0)
c = a + b
print(c.get_full_trace())
```

---

## Backends

### `get_backend(name="auto", **kwargs)`

Obtient un backend par nom.

**Paramètres :**
- `name` : Nom du backend (`"python"`, `"numpy"`, `"cupy"`, `"numba"`, `"decimal"`, `"auto"`)
- `**kwargs` : Arguments pour le constructeur (ex: `precision=100` pour Decimal)

**Retourne :**
- Instance du backend

**Exemples :**
```python
backend = get_backend("python")
backend = get_backend("decimal", precision=100)
backend = get_backend("auto")  # Sélection automatique
```

---

### `list_available_backends()`

Liste les backends disponibles sur le système.

**Retourne :**
- Liste des noms de backends disponibles

**Exemples :**
```python
backends = list_available_backends()
# ['python', 'numpy'] si NumPy est installé
```

---

## Tracing

### `NumericTracer`

Traceur d'erreurs numériques.

**Méthodes :**
- `log(event)` : Enregistrer un événement
- `log_error(...)` : Raccourci pour créer et logger
- `clear()` : Effacer tous les événements
- `get_by_type(error_type)` : Filtrer par type
- `get_by_severity(min_severity)` : Filtrer par sévérité
- `get_summary()` : Obtenir un résumé
- `to_json()` : Exporter en JSON

**Propriétés :**
- `events` : Liste des événements enregistrés

**Exemples :**
```python
tracer = NumericTracer()
# ... opérations ...
summary = tracer.get_summary()
print(summary["total_events"])
```

---

### `get_global_tracer()` / `set_global_tracer(tracer)`

Gérer le traceur global.

**Exemples :**
```python
tracer = get_global_tracer()
tracer.log_error(...)
```

