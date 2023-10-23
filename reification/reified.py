from typing import Generic, TypeVar, Any
from abc import ABC, abstractmethod


T = TypeVar("T", covariant=True)


type[T & protocol]



from typing import Protocol

# Reified<T> : T
class Reified:
    #@abstractmethod
    def type_args(cls) -> Any:
        pass
