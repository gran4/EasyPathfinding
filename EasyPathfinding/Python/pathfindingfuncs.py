from __future__ import annotations

from customtypes import number, Point
from typing import Tuple
import math


__all__ = (
    "heuristic",
    "move_cost",
    "get_dist",
    "collapse",
)

def heuristic(start: Tuple, goal: Tuple) -> float:
        """
        Gets the Heuristic of the 2 points
        """
        # Use Chebyshev distance heuristic if we can move one square either
        # adjacent or diagonal
        d = 1
        d2 = 1
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return d * (dx + dy) + (d2 - 2 * d) * min(dx, dy)


def move_cost(a: number, b: number) -> float:
    if a[0] == b[0] or a[1] == b[1]:
        return 1*5
    else:
        return 1.42*5


def get_dist(pos: number, pos2: number) -> float:
    return math.sqrt((pos[0]-pos2[0])**2+(pos[1]- pos2[1])**2)


def collapse(point: Point, tilesize: int) -> Point:
    return point[0]/tilesize, point[1]/tilesize
