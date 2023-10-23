import types
from typing import TypeAlias, Any

a: type = list
b: type[int] = bool
c: type[bool] = int

d: tuple[int, str] = (1, "")

#a: TypeAlias =
#a: TypeAlias =

type_dict: dict[tuple[type, tuple[type | Any]], type] = dict()


def get_type(base_cls: type[T], type_args: tuple[type | Any]) -> type[T]:
    k = (base_cls, type_args)

    if k in type_dict:
        return type_dict[k]
    else:
        t = new_type(base_cls, type_args)
        type_dict[k] = t
        return t

from typing import Protocol
class RT(Protocol)


def new_type(cls: type[T], params: tuple) -> type[Reified, T]:
    #class ntype(base_cls):
    #    typeargs = key
    reified2 = types.new_class(
        name=cls.__name__,
        bases=(cls,),
        exec_body=(lambda ns: ns)
    )

    return reified2


def tuplize_class_getitem_params(params: Any) -> tuple:
    if isinstance(params, tuple):
        return params
    else:
        return (params,)
