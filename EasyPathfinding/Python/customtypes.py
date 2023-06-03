from __future__ import annotations
from typing import Union, Tuple, Generic

__all__ = [
    "number",
    "Point",
    "BarrierType"
]

number = Union[float, int]
Point = Tuple[number, number]

BarrierType = Generic()
