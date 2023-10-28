from typing import Any
from .utils import get_reified_type, tuplize_class_getitem_params


class Reified:
    targ: Any = type | Any

    type_args: tuple[type | Any, ...] = (Any,)

    # Return type should be inferred
    def __class_getitem__(cls, params: Any):
        param_tuple = tuplize_class_getitem_params(params)
        rt = get_reified_type(cls, param_tuple)
        rt.targ = params
        rt.type_args = param_tuple
        return rt
