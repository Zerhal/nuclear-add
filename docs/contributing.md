# Guide de contribution

## Structure du projet

```
nuclear_add/
├── src/nuclear_add/     # Code source principal
├── tests/               # Tests unitaires
├── docs/                # Documentation
└── .github/workflows/   # CI/CD
```

## Workflow de développement

### 1. Setup

```bash
# Cloner le projet
git clone <repo-url>
cd nuclear_add

# Installer les dépendances
uv sync --extra dev

# Installer le module en mode développement
uv pip install -e .
```

### 2. Développement

```bash
# Lancer les tests
uv run pytest

# Vérifier le linting
uv run ruff check src/ tests/
uv run black --check src/ tests/
uv run mypy src/nuclear_add

# Formater le code
uv run black src/ tests/
uv run ruff check --fix src/ tests/
```

### 3. Tests

- Écrire des tests pour toute nouvelle fonctionnalité
- Maintenir la couverture de code > 60%
- Tests dans `tests/` avec préfixe `test_`

### 4. Documentation

- Mettre à jour la docstring pour toute nouvelle fonction/classe
- Ajouter des exemples dans `docs/methods_guide.md` si nécessaire
- Mettre à jour `docs/api_reference.md` pour les nouvelles APIs

## Standards de code

### Type hints

Toutes les fonctions doivent avoir des type hints :

```python
def my_function(a: float, b: float) -> float:
    """Description."""
    return a + b
```

### Docstrings

Format Google style :

```python
def add(a: Any, b: Any) -> Any:
    """
    Add two numbers safely.
    
    Args:
        a: First operand
        b: Second operand
    
    Returns:
        Sum of a and b
    
    Raises:
        TypeError: If inputs are not numeric
    """
```

### Naming

- Classes : `PascalCase`
- Fonctions/méthodes : `snake_case`
- Constantes : `UPPER_SNAKE_CASE`
- Privé : préfixe `_`

## Ajouter un nouveau backend

1. Créer une classe héritant de `Backend`
2. Implémenter toutes les méthodes abstraites
3. Ajouter au registre dans `backends.py`
4. Ajouter des tests dans `tests/test_backends.py`

Exemple :

```python
class MyBackend(Backend):
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

## Ajouter un nouveau type

1. Créer la classe dans `types.py`
2. Ajouter la gestion dans `NuclearEngine._handle_special_types()`
3. Ajouter des tests
4. Documenter dans `docs/api_reference.md`

## Processus de PR

1. Créer une branche depuis `main`
2. Faire les modifications
3. Ajouter des tests
4. Vérifier que tous les tests passent
5. Mettre à jour la documentation
6. Créer une PR avec description claire

## Checklist avant PR

- [ ] Tous les tests passent
- [ ] Couverture de code maintenue
- [ ] Code formaté (black, ruff)
- [ ] Type hints complets
- [ ] Docstrings à jour
- [ ] Documentation mise à jour
- [ ] Pas de warnings mypy
- [ ] Exemples fonctionnels

