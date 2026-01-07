# Diagrammes et schémas

## Architecture système (Mermaid)

```mermaid
graph TB
    User[Utilisateur] --> API[API Layer]
    API --> add[add function]
    API --> sum_safe[sum_safe function]
    API --> gradient[gradient function]
    
    add --> Engine[NuclearEngine]
    sum_safe --> Engine
    gradient --> Engine
    
    Engine --> Config[NuclearConfig]
    Engine --> Backend[Backend Selection]
    Engine --> Tracer[NumericTracer]
    
    Backend --> Python[PythonBackend]
    Backend --> NumPy[NumPyBackend]
    Backend --> CuPy[CuPyBackend]
    Backend --> Numba[NumbaBackend]
    Backend --> Decimal[DecimalBackend]
    
    Engine --> Types[Type System]
    Types --> Interval[Interval]
    Types --> DualNum[DualNumber]
    Types --> Lazy[LazyExpr]
    Types --> Traced[TracedValue]
    
    Tracer --> Analyzer[PrecisionAnalyzer]
    Tracer --> Detector[OverflowDetector]
```

## Flux d'exécution d'une addition

```mermaid
flowchart TD
    Start[add a b] --> CheckTypes{Types spéciaux?}
    CheckTypes -->|Interval| IntervalAdd[Addition Interval]
    CheckTypes -->|DualNumber| DualAdd[Addition Dual]
    CheckTypes -->|LazyExpr| LazyAdd[Addition Lazy]
    CheckTypes -->|Normal| Validate[Valider inputs]
    
    Validate --> Promote[Promouvoir types]
    Promote --> PreCheck{Vérification pré-op}
    PreCheck -->|Overflow?| OverflowPolicy{Politique}
    OverflowPolicy -->|RAISE| RaiseError[OverflowError]
    OverflowPolicy -->|INF| Continue[Continuer]
    PreCheck -->|OK| Compute[Calculer]
    
    Compute --> Backend{Backend}
    Backend -->|Python| PythonOp[Opération Python]
    Backend -->|NumPy| NumPyOp[Opération NumPy]
    Backend -->|GPU| GPUOp[Opération GPU]
    
    PythonOp --> PostCheck[Vérification post-op]
    NumPyOp --> PostCheck
    GPUOp --> PostCheck
    
    PostCheck --> CheckNaN{NaN?}
    CheckNaN -->|Oui| NaNPolicy{Politique}
    NaNPolicy -->|RAISE| RaiseNaN[ArithmeticError]
    NaNPolicy -->|REPLACE| Replace[0.0]
    NaNPolicy -->|PROPAGATE| Continue
    
    CheckNaN -->|Non| CheckInf{Inf?}
    CheckInf -->|Oui| InfPolicy{Politique}
    InfPolicy -->|RAISE| RaiseInf[OverflowError]
    InfPolicy -->|SATURATE| Saturate[MAX_FLOAT]
    
    CheckInf -->|Non| Paranoid{Mode PARANOID?}
    Paranoid -->|Oui| PrecisionCheck[Vérifier précision]
    Paranoid -->|Non| Return[Retourner résultat]
    
    PrecisionCheck --> Trace[Logger dans Tracer]
    Trace --> Return
    
    IntervalAdd --> Return
    DualAdd --> Return
    LazyAdd --> Return
    Replace --> Return
    Saturate --> Return
```

## Hiérarchie des types

```mermaid
classDiagram
    class Number {
        <<abstract>>
    }
    
    class Interval {
        +low: float
        +high: float
        +midpoint()
        +width()
        +__add__()
        +__mul__()
    }
    
    class DualNumber {
        +real: float
        +dual: float
        +variable()
        +constant()
        +exp()
        +log()
    }
    
    class LazyExpr {
        +op: str
        +args: tuple
        +eval()
        +grad()
        +to_graph()
    }
    
    class TracedValue {
        +value: Any
        +trace: List
        +get_full_trace()
    }
    
    class StochasticValue {
        +value: float
        +precision: int
    }
    
    Number <|-- Interval
    Number <|-- DualNumber
    Number <|-- LazyExpr
    Number <|-- TracedValue
    Number <|-- StochasticValue
```

## Architecture des backends

```mermaid
classDiagram
    class Backend {
        <<abstract>>
        +name: str
        +capabilities: BackendCapabilities
        +add()
        +add_many()
        +kahan_sum()
        +is_available()
    }
    
    class PythonBackend {
        +kahan_sum()
        +neumaier_sum()
        +pairwise_sum()
    }
    
    class NumPyBackend {
        +vectorized_add()
        +kahan_sum()
    }
    
    class CuPyBackend {
        +to_gpu()
        +to_cpu()
    }
    
    class NumbaBackend {
        +_compile_functions()
    }
    
    class DecimalBackend {
        +precision: int
    }
    
    Backend <|-- PythonBackend
    Backend <|-- NumPyBackend
    Backend <|-- CuPyBackend
    Backend <|-- NumbaBackend
    Backend <|-- DecimalBackend
```

## Système de tracing

```mermaid
sequenceDiagram
    participant User
    participant Engine
    participant Tracer
    participant Analyzer
    participant Detector
    
    User->>Engine: add(a, b)
    Engine->>Detector: will_overflow_add()
    Detector-->>Engine: True/False
    
    Engine->>Engine: compute_add()
    Engine->>Analyzer: check_addition()
    Analyzer-->>Engine: ErrorEvent or None
    
    Engine->>Tracer: log_error()
    Tracer->>Tracer: Store event
    
    Engine-->>User: result
    
    User->>Tracer: get_summary()
    Tracer-->>User: Summary dict
```

## Sélection de backend

```mermaid
flowchart TD
    Start[get_backend name] --> Check{name == auto?}
    Check -->|Non| Direct[Retourner backend spécifique]
    Check -->|Oui| Precision{Précision requise?}
    
    Precision -->|Oui| Decimal[DecimalBackend]
    Precision -->|Non| Size{Taille données}
    
    Size -->|Petit < 100| Python[PythonBackend]
    Size -->|Grand| GPU{GPU disponible?}
    
    GPU -->|Oui| PreferGPU{Préférer GPU?}
    PreferGPU -->|Oui| CuPy[CuPyBackend]
    PreferGPU -->|Non| Numba{Numba disponible?}
    
    GPU -->|Non| Numba
    Numba -->|Oui| NumbaBackend[NumbaBackend]
    Numba -->|Non| NumPy{NumPy disponible?}
    
    NumPy -->|Oui| NumPyBackend[NumPyBackend]
    NumPy -->|Non| Python
    
    Direct --> Return[Retourner backend]
    Decimal --> Return
    Python --> Return
    CuPy --> Return
    NumbaBackend --> Return
    NumPyBackend --> Return
```

## Schéma ASCII simple

```
┌─────────────────────────────────────────────────────────┐
│                    USER APPLICATION                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   nuclear_add.add()   │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │   NuclearEngine       │
         │  ┌─────────────────┐  │
         │  │ NuclearConfig   │  │
         │  └─────────────────┘  │
         └───────────┬───────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    ▼                ▼                ▼
┌─────────┐    ┌──────────┐    ┌──────────┐
│ Backend │    │  Types   │    │ Tracing  │
│         │    │          │    │          │
│ Python  │    │ Interval │    │ Tracer   │
│ NumPy   │    │ DualNum  │    │ Analyzer │
│ CuPy    │    │ LazyExpr │    │ Detector │
│ Numba   │    │ Traced   │    └──────────┘
│ Decimal │    │ Stochastic│
└─────────┘    └──────────┘
```

## États de configuration

```mermaid
stateDiagram-v2
    [*] --> STRICT: strict()
    [*] --> FAST: fast()
    [*] --> PARANOID: paranoid()
    [*] --> SCIENTIFIC: scientific()
    
    STRICT --> STRICT: Toutes vérifications
    FAST --> FAST: Moins de vérifications
    PARANOID --> PARANOID: Toutes vérifications + tracing
    SCIENTIFIC --> SCIENTIFIC: Haute précision
    
    STRICT: Overflow: RAISE
    STRICT: NaN: RAISE
    STRICT: Tracing: ON
    
    FAST: Overflow: INF
    FAST: NaN: PROPAGATE
    FAST: Tracing: OFF
    
    PARANOID: Overflow: RAISE
    PARANOID: NaN: RAISE
    PARANOID: Tracing: ALL
    PARANOID: Precision: INTERVAL
    
    SCIENTIFIC: Precision: DECIMAL
    SCIENTIFIC: Decimal prec: 100+
    SCIENTIFIC: Kahan: ON
```

## Flux de données avec types spéciaux

```mermaid
flowchart LR
    A[Input a, b] --> B{Type check}
    
    B -->|Interval| I[Interval Arithmetic]
    B -->|DualNumber| D[Automatic Diff]
    B -->|LazyExpr| L[Lazy Evaluation]
    B -->|TracedValue| T[Value Tracing]
    B -->|Normal| N[Normal Addition]
    
    I --> R[Result Interval]
    D --> R2[Result DualNumber]
    L --> R3[Result LazyExpr]
    T --> R4[Result TracedValue]
    N --> R5[Result Number]
    
    R --> Out[Output]
    R2 --> Out
    R3 --> Out
    R4 --> Out
    R5 --> Out
```

