__version__ = "0.1.1"

from .reify import reify
from .reific import Reific
from .reified import ReifiedType

__all__ = ["reify", "Reific", "ReifiedType"]



#a: type[int] = bool
#b: type[bool] = int #NG

e: type[bool] = bool

#c: type[bool] = a # NG
d: type[int] = e #OK

f: list[bool] = []
m: list[int] = f
