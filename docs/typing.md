# Typing

## Typing Basis

With `Reified` generic types, type parameters are taken into account, respecting the typing semantics as much as possible.

Python's native `isinstance` function works seamlessly with reified generic types.

In the context of reified generics:

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

This returns `False` because, while both objects are instances of the `ReifiedList` class, their type parameters are different (string vs integer).

## Hashable Type Arguments

All type arguments passed to a `Reified`-derived class must be hashable and must follow Python's normal hash contract: their hash value and equality must remain stable while they are used.
Reified types use their type arguments as dictionary keys to cache the generated classes.

`Annotated` is not treated specially.
Its metadata is preserved as part of the type argument, so the metadata must also be hashable.
Strings, tuples containing only hashable items, and frozen dataclass instances whose fields are hashable can be used normally.

```py
>>> from typing import Annotated
>>> HashableInt = Annotated[int, ("unit", "ms")]
>>> ReifiedList[HashableInt].targ == HashableInt
True
>>> UnhashableInt = Annotated[int, []]
>>> ReifiedList[UnhashableInt]
Traceback (most recent call last):
    ...
TypeError: Reified type arguments must be hashable.
```

## Unparameterized Generic Classes

A generic `Reified`-derived class used without its own type arguments exposes `Any`, including when it inherits from another generic reified class.
Once parameterized, it exposes the supplied argument.

```py
>>> from typing import Any
>>> class ReifiedListSub[T](ReifiedList[T]):
...     pass
>>> ReifiedListSub().targ is Any
True
>>> ReifiedListSub[int]().targ is int
True
```

A non-generic subclass of an already specialized reified class instead inherits that specialization.

```py
>>> class ReifiedIntList(ReifiedList[int]):
...     pass
>>> ReifiedIntList().targ is int
True
```

## Type Equivalence

It treats two instances of the same `Reified`-derived class as equivalent only if the type parameters provided in their instantiation are exactly the same.
That is, `ReifiedClass[T, ...] == ReifiedClass[S, ...]` if and only if `(T, ...) == (S, ...)`.

Equivalent type arguments reuse the same generated class.
The class-level `targ` and `type_args` attributes are initialized when that class is first created and are not replaced by an equivalent later subscription.
They therefore contain an equivalent cached representative, which is not necessarily the same object or spelling used by a later subscription.

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
>>> ReifiedList[int] is ReifiedList[int,]
True
>>> ReifiedList[int,].targ is int
True
```

## Subtyping

The `Reified` Mixin supports nominal subtyping.

Let types `A` and `B` be `Reified`-derived classes.
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

### Generic Inheritance Limitation

Type arguments supplied to a generic subclass are reified for that subclass only.
They are not substituted into parameterized base classes.
Consequently, generic inheritance through a type variable is not reflected in runtime subclass checks.

```py
>>> class ReifiedBase[T](Reified):
...     pass
>>> class ReifiedSub[T](ReifiedBase[T]):
...     pass
>>> ReifiedSub[int].type_args
(<class 'int'>,)
>>> issubclass(ReifiedSub[int], ReifiedBase[int])
False
```

This differs from inheriting an already specialized reified class.
A non-generic subclass directly inherits that specialization and remains its runtime subclass.

```py
>>> class ReifiedIntSub(ReifiedBase[int]):
...     pass
>>> ReifiedIntSub.type_args
(<class 'int'>,)
>>> issubclass(ReifiedIntSub, ReifiedBase[int])
True
```

### Type Variance

The `Reified` Mixin only considers direct equivalence of type parameters for subtyping and does not account for type variance.

```py
>>> issubclass(bool, int)
True
>>> class ReifiedTuple[T](Reified, tuple[T]):
...     pass
...
>>> issubclass(ReifiedTuple[bool], ReifiedTuple[int])
False
```
