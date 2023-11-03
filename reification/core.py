from typing import Any
from .utils import get_reified_type, tuplize_class_getitem_params


class Reified:
    targ: Any = type | Any

    type_args: tuple[type | Any, ...] = (Any,)

    def __new__(cls, *args, **kwargs):
        # Prohibit from instantiating directly
        if cls is Reified:
            raise RuntimeError("Cannot instantiate 'Reified' class directly.")
        return super().__new__(cls, *args, **kwargs)

    # Return type should be inferred
    def __class_getitem__(cls, params: type | tuple[type | Any, ...] | Any):
        # Prohibit from instantiating directly
        if cls is Reified:
            raise RuntimeError("Cannot instantiate 'Reified' class directly.")
        # Returns a separated reified type
        param_tuple = tuplize_class_getitem_params(params)
        rt = get_reified_type(cls, param_tuple)
        rt.targ = params
        rt.type_args = param_tuple
        return rt
