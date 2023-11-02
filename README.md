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

Python >= 3.12

This library is written in pure Python and does NOT require any non-builtin modules.

## Install

```sh
pip3 install reification
```

## API

### `Reified` (class)

`Reified` is a Mixin class designed to facilitate the creation of new types based on reified type parameters.

This class is threadsafe so that inheriting classes can be used in multiple threads.

You cannot instantiate this class directly.

#### `targ: type | tuple[type | Any, ...] | Any` (class property)

This class property represents the type argument(s) specified for the reified generic class.
If there's more than one type argument, `targ` will be a tuple containing each given type or type-like values.
If type argument is not specified, it may return 'Any'.

#### `type_args: tuple[type | Any, ...]` (class property)

This is another class property that carries the type argument(s) provided for the reified generic class.
Unlike `targ`, `type_args` always returns a tuple of the specified type arguments, even when there's only one type argument.
If no type arguments are given, it may contain single 'Any'.

#### `__class_getitem__(cls, params: type | tuple[type | Any, ...] | Any) -> type` (special class method, for Mixin)

This method, which the class overrides, is used for creating new types each time it is called with distinct type arguments.
It serves a key role in handling parameterized generic classes, enabling the different identities on different type arguments of the same base class.

## Example usage: Type Checked Generic Stack

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

In the `push` method, we are checking at runtime if the item being pushed is of the specified generic type (this type is accessible via the 'targ' attribute inherited from Reified).
If the type of the item does not match, a `TypeError` is raised.

In the example usage, we create an instance of the ReifiedStack class with a type argument as string. When we try to push a string 'spam', the item is accepted since it matches with the stack's specified type argument. However, when we try to push an integer 42, a TypeError is raised because the type of item does not match with the stack's type argument.

This demonstrates the use of reified generics in Python where we can have runtime access to the type parameters, enabling us to type check dynamically at runtime. This is useful in situations where we need to enforce type safety in our code or use type information at runtime.

## Typing

```py
T = TypeVar("T")

class CheckedStack(Reific[T]):

```

```py
>>> int_stack = CheckedStack[int]()
>>> isinstance(int_stack, CheckedStack[int])
True
>>> isinstance(int_stack, CheckedStack[str])
False
```

subclass works as you expected.

```py
>>> issubclass(Reified[int], Reified[int])
>>> issubclass(Reified, Reified[int])
>>> issubclass(Reified[int], Reified)
>>> issubclass(Reified[str], Reified[int])
```
# Reification (Python library)

This value repr types.
Typ semantics are depends on each usage

## Install

```sh
pip3 install reification
```

## API

all public API is just below `reification` package

### `refiy` (function)

make defined normal generic class parameter-reified

`type_args` :

#### example

```py
>>> from reification import reify
>>> xs = reify(list)[int]([1, 2, 3])
>>> t, = xs.type_args
>>> t
int
```

```
reify(list)[int] is reify(list)[]
reify(list)[] is reify(list)[]
```

### `Reific` (class)

create type parameter-reified generics class


derives from base class
subtype nominaly, type eq when type parameter eq

```
MyStack[int]
```

## License

[WTFPL](LICENSE)
