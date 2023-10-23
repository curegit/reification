from typing import TypeVar, Any
from .utils import get_type, tuplize_class_getitem_params

T = TypeVar("T")

# TODO: Reified[T]
# Reified = type[T] & Reified
def reify(base_type: type[T]) -> type[T]:
    #@cache しないといけない

    # Generic を継承する？
    class _Reified(base_type):

        def __class_getitem__(cls, params: Any):

            if hasattr(super(), "__class_getitem__"):
                super().__class_getitem__(params)


            param_tuple = tuplize_class_getitem_params(params)
            t = get_type(cls, param_tuple)
            t.type_args = params
            return t
    return _Reified
