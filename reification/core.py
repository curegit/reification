from typing import Any
from .utils import get_reified_type, tuplize_class_getitem_params


class Reified:
    """Mixin class designed to facilitate the creation of new types based on reified type parameters"""

    targ: type | tuple[type | Any, ...] | Any = Any
    """
    This class property represents the type argument(s) that were specified when the reified generic class was instantiated.
    If there is more than one type argument, `targ` will be a tuple containing each given type.
    If no type argument is specified, `Any` will be returned.

    Returns:
        type | tuple[type | Any, ...] | Any: The type argument(s) given when the class was instantiated.
        If no type argument was given, `Any` will be returned.
    """

    type_args: tuple[type | Any, ...] = (Any,)
    """
    This class property holds the type argument(s) provided for the reified generic class.
    Unlike `targ`, `type_args` always returns a tuple of the specified type arguments, even when there's only one type argument.
    If no type arguments are given, it contains `Any`.

    Returns:
        tuple[type | Any, ...]: A tuple containing the type argument(s) given when the class was instantiated.
        If no type argument was given, the returned tuple contains `Any`.
    """

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
