# Reification (Python library)


```py
from reification import Reified

class ReifiedList[T](Reified): pass

l = ReifiedList[int]([1, 2, 3])

print(l.types) # int
```

## Requirements

Python >= 3.12

Any non-builtin modules are NOT required.

## Install

```sh
pip3 install reification
```

## Usage

```py
>>> from reification import reify
>>> a = reify[list[int]]([1, 2, 3])
>>> a.type
list[int]
```

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

## License

[WTFPL](LICENSE)
