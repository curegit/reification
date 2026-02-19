# Reification (Python library)

Reified generics in Python to get type parameters at runtime

```py
from reification import Reified


class ReifiedList[T](Reified, list[T]):
    pass


xs = ReifiedList[int](range(10))
print(xs)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(xs.targ)  # <class 'int'>
```

See the detailed documentation at <https://curegit.github.io/reification/>.

## Requirements

- Python >= 3.12

This library is written in pure Python and does not require any external modules.

## Installation

```sh
pip install reification
```

## Example Usage: Type-Checked Generic Stack

```py
from reification import Reified


class ReifiedStack[T](Reified):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[T] = []

    def push(self, item: T) -> None:
        # We can do runtime check
        if isinstance(item, self.targ):
            self.items.append(item)
        else:
            raise TypeError()

    def pop(self) -> T:
        if self.items:
            return self.items.pop()
        else:
            raise IndexError("pop from empty stack")


stack = ReifiedStack[str]()
stack.push("spam")  # OK
stack.push(42)  # raises TypeError
```

The `ReifiedStack` class created here is generic and derived from the `Reified` base class, and implements a simple stack with `push` and `pop` methods.

In the `push` method, we are checking at runtime if the item being pushed is of the specified generic type (this type is accessible via the `targ` attribute inherited from `Reified`).
If the type of the item does not match, a `TypeError` is raised.

In the example usage, we create an instance of the ReifiedStack class with `str` as the type argument. When we try to push a string `"spam"`, the item is accepted since it matches the stack's specified type argument.
However, when we try to push an integer `42`, a `TypeError` is raised because the type of the item does not match the stack's type argument.

This demonstrates the use of reified generics in Python where we can have runtime access to the type parameters, enabling us to type check dynamically at runtime.
This is useful in situations where we need to enforce type safety in our code or use type information at runtime.

## API

See the full API reference at <https://curegit.github.io/reification/reference/>.

## License

WTFPL

Copyright (C) 2023 curegit
