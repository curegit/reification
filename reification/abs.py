from typing import ClassVar, Any
from .utils import get_reified_type, tuplize_class_getitem_params


class Reified:
    """Mixin class designed to facilitate the creation of new types based on reified type parameters.
    In most cases, this class should be placed before the normal generic class in the class inheritance list.

    Example:
        >>> from reification import Reified
        >>> class ReifiedList[T](Reified, list[T]):
        ...     pass
        >>> xs = ReifiedList[int](range(10))
        >>> xs.targ
        <class 'int'>

    Attributes:
        targ: The type argument(s) that were specified when the reified generic class was instantiated.
        type_args: A tuple containing the type argument(s) provided for the reified generic class.
    """

    targ: ClassVar[type | tuple[type | Any, ...] | Any] = Any
    """The type argument(s) that were specified when the reified generic class was instantiated.

    If there is more than one type argument, `targ` will be a tuple containing each given type.
    If no type argument is specified, `Any` will be returned.
    """

    type_args: ClassVar[tuple[type | Any, ...]] = (Any,)
    """A tuple containing the type argument(s) provided for the reified generic class.

    Unlike `targ`, `type_args` always returns a tuple of the specified type arguments,
    even when there's only one type argument. If no type arguments are given, it contains a single `Any`.
    """

    def __init__(self, *args, **kwargs):
        # Prohibit from instantiating directly
        if type(self) is Reified:
            raise TypeError("Cannot instantiate 'Reified' class directly.")
        super().__init__(*args, **kwargs)

    # Return type should be inferred
    def __class_getitem__(cls, params: type | tuple[type | Any, ...] | Any):
        """This dunder method, which the class overrides, is used for creating a new type each time it is called with distinct type arguments.
        It serves a key role in handling parameterized generic classes, enabling different identities for different type arguments of the same base class.

        Note that this custom method violates Python's convention that `__class_getitem__` should return an instance of `GenericAlias`.
        """
        # Prohibit from instantiating directly
        if cls is Reified:
            raise TypeError("Cannot instantiate 'Reified' class directly.")
        # Returns a separated reified type
        param_tuple = tuplize_class_getitem_params(params)
        rt = get_reified_type(cls, param_tuple)
        rt.targ = params
        rt.type_args = param_tuple
        return rt
