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
