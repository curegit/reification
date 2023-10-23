from typing import Generic, TypeVarTuple, Any
from .utils import get_type, tuplize_class_getitem_params




Ts = TypeVarTuple("Ts")


class Reific(Generic[*Ts]):

    # TODO: Reified[Self]
    def __class_getitem__(cls, params: Any) -> type[Self]:

        #
        super().__class_getitem__(params)

        #
        param_tuple = tuplize_class_getitem_params(params)
        t = get_type(cls, param_tuple)
        #
        #t.key =
        return t
