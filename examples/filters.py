from typing import List, Tuple, Sequence
from typing import Callable, ParamSpec, TypeVar
from functools import wraps
import pandas as pd


P = ParamSpec("P")
R = TypeVar("R")


def log(filter_name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"Applying filter '{filter_name}' to data'")
            ret = fn(*args, **kwargs)
            print(f"Applying '{filter_name}' completed'")
            return ret
        return wrapper
    return decorator

@log()
def apply_filter(df: pd.Dataframe, col: str, filt: Sequence[bool]) -> pd.DataFrame:
    df[col] = pd.Series(filt).astype(int)
    return df


df = pd.DataFrame({"name": ["Santo", "Sajan", "Saly", "Thomas"]})

# defining filters
filters: List[Tuple[str, str, Sequence[bool]]] = [
    ("S filter", "starts_with_S", df["name"].str.startswith("S")),
    
]

# applying filters
for filt_name, col, filt in filters:
    df = apply_filter(df, col, filt)

print(df)