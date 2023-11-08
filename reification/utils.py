import types
from typing import Any
from threading import RLock


_type_dict: dict[tuple[type, tuple[type | Any, ...]], type] = dict()


_lock = RLock()


def get_reified_type[T](base_cls: type[T], type_args: tuple[type | Any, ...]) -> type[T]:
    key = (base_cls, type_args)
    with _lock:
        if key in _type_dict:
            return _type_dict[key]
        else:
            new_type = clone_type(base_cls)
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
