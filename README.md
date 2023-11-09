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

## Requirements

- Python >= 3.12

This library is written in pure Python and does not require any external modules.

## Install

```sh
pip3 install reification
```

## API

The public API is defined under the root of the `reification` package.

### `Reified` (class)

Usage: `from reification import Reified`

`Reified` is a Mixin class designed to facilitate the creation of new types based on reified type parameters.

This class is thread-safe so that inheriting classes can be used in multiple threads.

You cannot directly instantiate this class.

#### `targ: type | tuple[type | Any, ...] | Any` (class property)

This class property represents the type argument(s) specified for the reified generic class.
If there's more than one type argument, `targ` will be a tuple containing each given type or type-like value.
If a type argument is not specified, it may return `Any`.

#### `type_args: tuple[type | Any, ...]` (class property)

This is another class property that carries the type argument(s) provided for the reified generic class.
Unlike `targ`, `type_args` always returns a tuple of the specified type arguments, even when there's only one type argument.
If no type arguments are given, it may contain a single `Any`.

#### `__class_getitem__(cls, params: type | tuple[type | Any, ...] | Any) -> type` (special class method, for Mixin)

This method, which the class overrides, is used for creating new types each time it is called with distinct type arguments.
It serves a key role in handling parameterized generic classes, enabling the different identities on different type arguments of the same base class.

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
stack.push(42)  # raise TypeError
```

The `ReifiedStack` class created here is generic and derived from the `Reified` base class, and implements a simple stack with `push` and `pop` methods.

In the `push` method, we are checking at runtime if the item being pushed is of the specified generic type (this type is accessible via the `targ` attribute inherited from `Reified`).
If the type of the item does not match, a `TypeError` is raised.

In the example usage, we create an instance of the ReifiedStack class with a type argument as string. When we try to push a string `"spam"`, the item is accepted since it matches with the stack's specified type argument.
However, when we try to push an integer `42`, a `TypeError` is raised because the type of item does not match with the stack's type argument.

This demonstrates the use of reified generics in Python where we can have runtime access to the type parameters, enabling us to type check dynamically at runtime.
This is useful in situations where we need to enforce type safety in our code or use type information at runtime.

## Typing

With `Reified` generic types, type parameters are considered for understanding and respecting the typing semantics as much as possible.

Python's native `isinstance` function works seamlessly with reified generic types.

In context of reified generics:

```py
>>> isinstance(ReifiedList[int](), ReifiedList[int])
True
```

The above expression returns `True` as a `ReifiedList` object of integer type is indeed an instance of a `ReifiedList` of integer type.

On the other hand:

```py
>>> isinstance(ReifiedList[str](), ReifiedList[int])
False
```

This returns `False` because, while both the objects are instances of the `ReifiedList` class, their type parameters are different (string vs integer).

### Type Equivalence

It treats two instances of the `Reified` derived same class as equivalent only if the type parameters provided in their instantiation are exactly the same.
That is, `ReifiedClass[T, ...] == ReifiedClass[S, ...]` if and only if `(T, ...) == (S, ...)`.

```py
>>> ReifiedList[float] == ReifiedList[float]
True
>>> ReifiedList[float] == ReifiedList[int]
False
>>> ReifiedList[tuple[int, str]] == ReifiedList[tuple[int, str]]
True
>>> ReifiedList[tuple[int, str]] == ReifiedList[tuple[int, float]]
False
>>> ReifiedList[ReifiedList[int]] == ReifiedList[ReifiedList[int]]
True
>>> ReifiedList[ReifiedList[int]] == ReifiedList[ReifiedList[str]]
False
```

### Subtyping

The `Reified` Mixin supports nominal subtyping.

Let type `A` and `B` be `Reified` derived class.
Type `A` is a subtype of type `B` if `A == B` or `A` is directly derived from `B`.

A `Reified` derived class with type parameters is considered a subtype of the same class without type parameters.
This means that `ReifiedClass[T, ...]` is a subtype of `ReifiedClass`.

```py
>>> issubclass(ReifiedList[int], ReifiedList[int])
True
>>> issubclass(ReifiedList, ReifiedList[int])
False
>>> issubclass(ReifiedList[int], ReifiedList)
True
>>> issubclass(ReifiedList[str], ReifiedList[int])
False
>>> class ReifiedListSub(ReifiedList[int]):
...     pass
...
>>> issubclass(ReifiedListSub, ReifiedList[int])
True
```

#### Type Variance

`Reified` Mixin only considers direct equivalence of type parameters for subtyping and does not cater for type variance.

```py
>>> issubclass(bool, int)
True
>>> class ReifiedTuple[T](Reified, tuple[T]):
...     pass
...
>>> issubclass(ReifiedTuple[bool], ReifiedTuple[int])
False
```

## License

WTFPL
