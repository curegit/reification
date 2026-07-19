from typing import ClassVar, Any
from .utils import get_reified_type, tuplize_class_getitem_params


class Reified:
    """Mixin class designed to facilitate the creation of new types based on reified type parameters.
    In most cases, this class should be placed before the normal generic class in the class inheritance list.

    ```python
    >>> from reification import Reified
    >>> class ReifiedList[T](Reified, list[T]):
    ...     pass
    >>> xs = ReifiedList[int](range(10))
    >>> xs.targ
    <class 'int'>

    ```

    Attributes:
        targ: The cached representative of the type argument(s) used to create the reified class.
        type_args: A tuple containing the cached representative of the type arguments.
    """

    targ: ClassVar[type | tuple[type | Any, ...] | Any] = Any
    """The type argument(s) that were specified when the reified generic class was instantiated.

    If there is more than one type argument, `targ` will be a tuple containing each given type.
    If a generic reified class is used without specifying its own type arguments, `Any` will be returned.
    A non-generic subclass of a specialized reified class inherits the specialized value instead.

    Equivalent type arguments share the same reified class. This attribute is initialized when that
    class is first created, so an equivalent later subscription does not replace the cached value.
    """

    type_args: ClassVar[tuple[type | Any, ...]] = (Any,)
    """A tuple containing the type argument(s) provided for the reified generic class.

    Unlike `targ`, `type_args` always returns a tuple of the specified type arguments,
    even when there's only one type argument. If a generic reified class is used without specifying
    its own type arguments, it contains a single `Any`. A non-generic subclass of a specialized
    reified class inherits the specialized tuple instead.

    Equivalent type arguments share the same reified class. This attribute is initialized when that
    class is first created, so an equivalent later subscription does not replace the cached value.
    """

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        own_type_params = cls.__dict__.get("__type_params__", ())
        own_parameters = cls.__dict__.get("__parameters__", ())
        if own_type_params or own_parameters:
            cls.targ = Any
            cls.type_args = (Any,)

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

        All type arguments must be hashable and follow Python's normal hash contract so that they
        can be used as stable cache keys. Typing constructs such as `Annotated` are not treated
        specially; their metadata must therefore also be hashable.

        Raises:
            TypeError: If this class is `Reified` itself or any type argument is not hashable.
        """
        # Prohibit from instantiating directly
        if cls is Reified:
            raise TypeError("Cannot instantiate 'Reified' class directly.")
        # Returns a separated reified type
        param_tuple = tuplize_class_getitem_params(params)
        return get_reified_type(cls, param_tuple)
