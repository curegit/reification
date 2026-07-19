import types
from typing import Any
from threading import RLock

_type_dict: dict[tuple[type, tuple[type | Any, ...]], type] = dict()


_lock = RLock()


def _require_hashable_type_args(type_args: tuple[type | Any, ...]) -> None:
    try:
        hash(type_args)
    except TypeError:
        raise TypeError("Reified type arguments must be hashable.") from None


def get_reified_type[T](base_cls: type[T], type_args: tuple[type | Any, ...]) -> type[T]:
    _require_hashable_type_args(type_args)
    key = (base_cls, type_args)
    with _lock:
        if key in _type_dict:
            return _type_dict[key]
        else:
            new_type = clone_type(base_cls)
            setattr(new_type, "targ", type_args[0] if len(type_args) == 1 else type_args)
            setattr(new_type, "type_args", type_args)
            _type_dict[key] = new_type
            return new_type


def clone_type[T](cls: type[T]) -> type[T]:
    name = cls.__name__
    reified = types.new_class(name=name, bases=(cls,))
    return reified


def tuplize_class_getitem_params(params: type | tuple[type | Any, ...] | Any) -> tuple[type | Any, ...]:
    if isinstance(params, tuple):
        return params
    else:
        return (params,)
