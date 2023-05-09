import types
from typing import Generic, TypeVar, TypeVarTuple, Any

Ts = TypeVarTuple("Ts")

class Reific(Generic[*Ts]):

    def __class_getitem__(cls, key):
        if key in type_dict:
            return type_dict[key]
        class rei(cls):
            pass
        reified = types.new_class(
            name=cls.__name__,
            bases=(cls,),
            exec_body=(lambda ns: ns)
        )
        if isinstance(key, type):
            reified.type_arg = key
            type_dict[key] = reified
        return reified
