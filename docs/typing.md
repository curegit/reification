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

## Type Equivalence

It treats two instances of the same `Reified`-derived class as equivalent only if the type parameters provided in their instantiation are exactly the same.
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
