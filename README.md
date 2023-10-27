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
