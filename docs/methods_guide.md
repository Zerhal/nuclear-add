# Guide des méthodes

## Méthodes d'addition

### 1. Addition basique

```python
from nuclear_add import add

# Entiers
add(2, 3)  # 5

# Flottants
add(1.5, 2.5)  # 4.0

# Complexes
add(1+2j, 3+4j)  # (4+6j)
```

### 2. Addition avec précision contrôlée

```python
from decimal import Decimal
from fractions import Fraction

# Précision décimale arbitraire
add(Decimal("0.1"), Decimal("0.2"))  # Decimal('0.3')

# Fractions exactes
add(Fraction(1, 3), Fraction(1, 6))  # Fraction(1, 2)

# Forcer un mode de précision
add(0.1, 0.2, precision="decimal")  # Decimal('0.3')
add(0.1, 0.2, precision="fraction")  # Fraction(3, 10)
```

### 3. Addition avec gestion d'erreur

```python
# Overflow - lever une exception (défaut)
try:
    add(1e308, 1e308)
except OverflowError:
    print("Overflow détecté!")

# Overflow - retourner inf
add(1e308, 1e308, overflow="inf")  # inf

# Overflow - saturer
add(1e308, 1e308, overflow="saturate")  # ~1.79e308

# NaN - lever une exception (défaut)
try:
    add(float('nan'), 1)
except ArithmeticError:
    print("NaN détecté!")

# NaN - propager
add(float('nan'), 1, nan="propagate")  # nan

# NaN - remplacer
add(float('nan'), 1, nan="replace")  # 0.0
```

### 4. Addition vectorisée

```python
# Vecteur + Vecteur
add([1, 2, 3], [4, 5, 6])  # [5, 7, 9]

# Broadcasting (scalaire + vecteur)
add([1, 2, 3], 10)  # [11, 12, 13]

# Tuples
add((1.5, 2.5), (3.5, 4.5))  # (5.0, 7.0)
```

## Méthodes de sommation

### 1. Somme sécurisée (Kahan)

```python
from nuclear_add import sum_safe

values = [0.1] * 100
result = sum_safe(values, precision="kahan")  # 10.0 (précis)
```

### 2. Somme par paires

```python
result = sum_safe(values, precision="pairwise")  # Bon compromis vitesse/précision
```

### 3. Somme Neumaier

```python
result = sum_safe(values, precision="neumaier")  # Amélioration de Kahan
```

## Méthodes de différentiation

### 1. Gradient automatique

```python
from nuclear_add import gradient

def f(x):
    return x * x * x  # f(x) = x³

grad = gradient(f, 2.0)  # 12.0 (= 3×2²)
```

### 2. Dual Numbers

```python
from nuclear_add.types import DualNumber

x = DualNumber.variable(3.0)  # x = 3, dx/dx = 1
y = x * x + 2 * x  # f(x) = x² + 2x
print(y.real)  # 15.0 (= f(3))
print(y.dual)  # 8.0 (= f'(3) = 2x + 2)
```

### 3. Gradient symbolique (LazyExpr)

```python
from nuclear_add.types import LazyExpr

x = LazyExpr.var("x", 2.0)
y = x * x  # f(x) = x²
grad = y.grad("x")
print(grad.eval())  # 4.0 (= 2x)
```

## Méthodes d'intervalles

### 1. Création d'intervalles

```python
from nuclear_add.types import Interval

# Depuis une valeur avec erreur ULP
a = Interval.from_value(0.1, ulp_error=1)

# Intervalle exact
b = Interval.exact(0.2)

# Intervalle manuel
c = Interval(0.99, 1.01)  # 1.0 ± 0.01
```

### 2. Opérations sur intervalles

```python
a = Interval.from_value(0.1)
b = Interval.from_value(0.2)
c = a + b

# Vérifier l'appartenance
print(0.3 in c)  # True

# Propriétés
print(c.midpoint)  # 0.3
print(c.width)  # Largeur de l'intervalle
print(c.relative_error)  # Erreur relative
```

### 3. Propagation d'incertitude

```python
# Simuler une chaîne de calculs
pos = Interval.from_value(1.0, ulp_error=1)
for i in range(10):
    pos = pos + Interval.from_value(0.1, ulp_error=1)

print(f"Position finale: {pos}")
print(f"Incertitude: {pos.width}")
```

## Méthodes de configuration

### 1. Presets de configuration

```python
from nuclear_add.core import NuclearConfig, NuclearEngine

# Mode strict (défaut)
config = NuclearConfig.strict()
engine = NuclearEngine(config)

# Mode rapide
config = NuclearConfig.fast()

# Mode paranoïaque
config = NuclearConfig.paranoid()

# Mode scientifique
config = NuclearConfig.scientific(precision=100)
```

### 2. Configuration personnalisée

```python
from nuclear_add.core import NuclearConfig, MathMode, PrecisionMode

config = NuclearConfig(
    math_mode=MathMode.PARANOID,
    precision_mode=PrecisionMode.DECIMAL,
    decimal_precision=200,
    enable_tracing=True,
    trace_all_operations=True,
)
```

## Méthodes de tracing

### 1. Utilisation basique

```python
from nuclear_add.tracing import NumericTracer

tracer = NumericTracer()

# ... effectuer des opérations ...
from nuclear_add import add
add(1e308, 1e308, overflow="inf")

# Obtenir le résumé
summary = tracer.get_summary()
print(summary)
```

### 2. Filtrage des événements

```python
from nuclear_add.tracing import ErrorType, ErrorSeverity

# Par type
overflow_events = tracer.get_by_type(ErrorType.OVERFLOW)

# Par sévérité minimale
errors = tracer.get_by_severity(ErrorSeverity.ERROR)
```

### 3. Export JSON

```python
json_data = tracer.to_json()
# Sauvegarder ou analyser
```

## Méthodes de backend

### 1. Sélection manuelle

```python
from nuclear_add.backends import get_backend

backend = get_backend("python")
result = backend.add(2, 3)

backend = get_backend("decimal", precision=100)
result = backend.add("0.1", "0.2")
```

### 2. Sélection automatique

```python
backend = get_backend("auto")  # Choisit le meilleur disponible
```

### 3. Liste des backends disponibles

```python
from nuclear_add.backends import list_available_backends

available = list_available_backends()
# ['python', 'numpy'] si NumPy est installé
```

## Méthodes avancées

### 1. Évaluation paresseuse

```python
from nuclear_add.types import LazyExpr

x = LazyExpr.var("x", 3.0)
y = LazyExpr.var("y", 4.0)
z = (x * x + y * y).sqrt()  # Pas encore calculé!

result = z.eval()  # 5.0 (calculé maintenant)
```

### 2. Graphe de calcul

```python
expr = x + y
graph = expr.to_graph()  # Format DOT
print(graph)
```

### 3. Valeurs tracées

```python
from nuclear_add.types import TracedValue

a = TracedValue(10.0)
b = TracedValue(5.0)
c = a + b
d = c * TracedValue(2.0)

print(d.get_full_trace())  # Historique complet
```

### 4. Arrondi stochastique

```python
from nuclear_add.types import StochasticValue

sv = StochasticValue(0.123456789, _rng_seed=42)
# Élimine le biais systématique dans les longues sommes
```

