import itertools
from typing import Any, Callable, Generator, TypeVar

T = TypeVar("T")


def sequence(func: Callable[[int], T]) -> Generator[T, None, None]:
    """
    Generates a sequence of values from a sequence of integers starting at zero,
    passed through the callable, which must take an integer argument.
    """
    return (func(n) for n in itertools.count())


class _Auto:
    """
    Sentinel value indicating an automatic default will be used.
    """

    def __bool__(self) -> bool:
        # Allow `Auto` to be used like `None` or `False` in boolean expressions
        return False


Auto: Any = _Auto()
