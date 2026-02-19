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

## Installation

```sh
pip install reification
```

## License

WTFPL

Copyright (C) 2023 curegit
