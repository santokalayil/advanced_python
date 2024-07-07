from typing import Callable, ParamSpec, TypeVar
from functools import wraps


P = ParamSpec("P")
R = TypeVar("R")


def log(level: str = "INFO") -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"The function/method '{fn.__name__}' started")
            print(f"{level=}")
            try:
                return fn(*args, **kwargs)
            finally:
                print(f"The function/method '{fn.__name__}' is completed")
        
        return wrapper
    return decorator

@log("DEBUG")
def do_something(name: str) -> None:
    print(f"Doing something with {name=}")


do_something("Santo")




