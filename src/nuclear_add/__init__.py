"""
Nuclear Add - The Most Overkill Addition Ever Made

A paranoid numerical addition engine with:
- Kahan summation for precision
- Interval arithmetic with error bounds
- Automatic differentiation
- Multiple computation backends (NumPy, CuPy, Numba)
- Numeric error tracing
- And much more...

For 99.9% of cases: just use +
For the remaining 0.1%: now you know this exists.
"""

from .core import (
    add,
    NuclearEngine,
    NuclearConfig,
    sum_safe,
    add_with_error,
    gradient,
    get_engine,
    set_engine,
)
from .types import (
    Interval,
    TracedValue,
    LazyExpr,
    DualNumber,
    StochasticValue,
)
from .backends import (
    get_backend,
    Backend,
    list_available_backends,
)
from .tracing import (
    NumericTracer,
    ErrorEvent,
    ErrorType,
    ErrorSeverity,
)

__version__ = "1.0.0"

__all__ = [
    # Core functions
    "add",
    "sum_safe",
    "add_with_error",
    "gradient",
    "get_engine",
    "set_engine",
    # Engine & Config
    "NuclearEngine",
    "NuclearConfig",
    # Types
    "Interval",
    "TracedValue",
    "LazyExpr",
    "DualNumber",
    "StochasticValue",
    # Backends
    "get_backend",
    "Backend",
    "list_available_backends",
    # Tracing
    "NumericTracer",
    "ErrorEvent",
    "ErrorType",
    "ErrorSeverity",
]

