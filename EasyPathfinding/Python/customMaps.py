from __future__ import annotations

from customtypes import Point, BarrierType
from typing import Union, Optional, List
from pathfindingfuncs import *


__all__ = (
    "CustomList",
    "LivingMap",
    "BarrierObject",
    "BarrierDict",
    "LayeredBarrierDict"
)


class CustomList(list):
    """
    A List that allows floats when getting or setting something
    """
    def __setitem__(self, index, item):
        super().__setitem__(int(index), int(item))

    def __getitem__(self, __name):
        return super().__getitem__(int(__name))


class LivingMap(object):
    """Custom Map"""

    __slots__ = (
        "size",
        "tilesize",
        "graph",
        "length",
        "height",
        "__weakref__"
    )

    def __init__(self, x_length: int, y_length: int,  
                    size: int, *args, tilesize: int=50
                    ) -> None:
        self.length = x_length
        self.height = y_length
        self.size = size
        self.tilesize = tilesize

        self.graph = CustomList()#[[0 for tile in range(y_length)] for tiles in range(x_length)]
        for tiles in range(x_length):
            self.graph.append(CustomList())
            for tile in range(y_length):
                self.graph[tiles].append(0)

        count = 1
        for barrierlist in args:
            for barrier in barrierlist:
                x = int(barrier.center_x/50)
                y = int(barrier.center_y/50)
                self.graph[x][y] = count
            count += 1

    def change(self, x:int, y:int, barrier: int) -> None:
        x = int(x/50)
        y = int(y/50)

        self.graph[x][y] = barrier

    def __getitem__(self, i):
        return self.graph[i]

    def __setitem__(self, x, y, val):
        self.graph[x/self.tilesize][y/self.tilesize] = val

class ObservablePoint(list):
    """
    A List that represents a point that moves

    Use when you use AStarBarrierDict
    """
    __slots__ = ("changed")
    def __setitem__(self, index, item):
        self.changed = True
        super().__setitem__(int(index), int(item))
    def __getitem__(self, __name):
        return super().__getitem__(int(__name))
    def __len__(self) -> int:
        return 2

class BarrierObject:
    __slots__ = (
        "barrier",
        "bellow",
        "layer",
        "base"
    )
    def __init__(self, layer=0, bellow: List[Point] = [], base = None):
        self.barrier = base
        self.bellow = bellow
        self.layer = layer
        self.base = base
    def get_bellow(self):
        if not self.bellow:
            return self.base
        self.barrier = self.bellow.pop()
        return self.barrier
    def push(self, barrier):
        if self.barrier:
            self.bellow.append(self.barrier)
        self.barrier = barrier
    def remove_top(self):
        obj = self.barrier
        self.barrier = self.bellow.pop()
        return obj
    def remove(self, barrier):
        if not barrier in self.layers:
            return self.base
        self.layers.remove(barrier)
    def __eq__(self, other: BarrierObject) -> bool:
        return self.layer == other.layer

class BarrierDict:
    """
    Class that manages a dict of barriers
    that can be encountered during A* path finding.
    Accessing elements is much faster, but start is slower.
    """
    __slots__ = (
        "tilesize",
        "bottom",
        "left",
        "right",
        "top",
        "length",
        "height",
        "static_barriers",
        "moving_barriers",
        "barrier_dict"
    )
    def __init__(self,
                 tilesize: int,
                 left: int,
                 right: int,
                 bottom: int,
                 top: int,
                 moving_barriers: Optional[List[Point]] = None,
                 base = None
                 ):
        """
        :param Sprite moving_sprite: Sprite that will be moving
        :param SpriteList blocking_sprites: Sprites that can block movement
        :param int tilesize: Size of the grid, in pixels
        :param int left: Left border of playing field
        :param int right: Right border of playing field
        :param int bottom: Bottom of playing field
        :param int top: Top of playing field
        """

        self.tilesize = tilesize
        self.bottom = int(bottom // tilesize)
        self.top = int(top // tilesize)
        self.left = int(left // tilesize)
        self.right = int(right // tilesize)

        self.length = int(self.top - self.bottom)
        self.height = int(self.right - self.left)

        self.moving_barriers = moving_barriers
        self.barrier_dict = {}
        self.base = base

        self.set_up_dict()

    def set_up_dict(self):
        for cx in range(self.left, self.right + 1):
            self.barrier_dict[cx] = {}
            for cy in range(self.bottom, self.top + 1):
                self.barrier_dict[cx][cy] = self.base
        for barrier in self.moving_barriers:
            x, y = collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y] = barrier

    def recalculate(self):
        for barrier in self.moving_barriers:
            if not barrier.moved:
                continue
            x, y = collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y] = barrier

    def recalculate_moving(self):
        for barrier in self.moving_barriers:
            x, y = collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y] = barrier

    def add(self, barrier):
        self.moving_barriers.append(barrier)
        x, y = collapse(barrier.position, self.tilesize)
        self.barrier_dict[x][y] = barrier

    def remove(self, barrier: Union[int, Point]):
        if isinstance(barrier, int):
            return self.moving_barriers.pop(int)
        elif isinstance(barrier, Point):
            temp = self.barrier_dict[barrier[0]][barrier[1]]
            self.barrier_dict[barrier[0]][barrier[1]] = self.base
            return temp

class LayeredBarrierDict(BarrierDict):
    """
    Subtly different from `BarrierDict`, same idea but uses `Barrier`
    objects. Instead, barriers can be over each other,
    only the one on top takes precedence.

    ... Example:
        Earth bellow floor bellow walls
        
        something that goes through this tile has to go through the wall,
        thus, ensuring that tiles bellow are save so when the walls are broken,
        there is the floor underneath(only certian things can go on the floor),
        then when the floor breaks, it is dirt(self.base).
        NOTE: (This can also be used for diff speeds on diff substance)
    """

    def __init__(self,
                 tilesize: int,
                 left: int,
                 right: int,
                 bottom: int,
                 top: int,
                 moving_barriers: Optional[List[Point]] = None,
                 base = None
                 ):
        """
        :param Sprite moving_sprite: Sprite that will be moving
        :param SpriteList blocking_sprites: Sprites that can block movement
        :param int tilesize: Size of the grid, in pixels
        :param int left: Left border of playing field
        :param int right: Right border of playing field
        :param int bottom: Bottom of playing field
        :param int top: Top of playing field
        """
        super().__init__(
            tilesize, left, right, bottom,
            top, moving_barriers=moving_barriers, base=base
        )

    def set_up_dict(self):
        for cx in range(self.left, self.right + 1):
            self.barrier_dict[cx] = {}
            for cy in range(self.bottom, self.top + 1):
                self.barrier_dict[cx][cy] = BarrierObject(self.base)
        for barrier in self.moving_barriers:
            x, y = collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y].push(barrier)

    def recalculate(self):
        for barrier in self.moving_barriers:
            if not barrier.moved:
                continue
            x, y = collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y].barrier = barrier

    def add(self, barrier):
        self.moving_barriers.append(barrier)
        x, y = collapse(barrier.position, self.tilesize)
        self.barrier_dict[x][y].push(barrier)

    def remove(self, barrier: Union[int, Point, BarrierType]):
        if isinstance(barrier, int):
            barrier = self.moving_barriers.pop(int)
            self.barrier_dict[barrier.center_x][barrier.center_y]
            return barrier
        elif isinstance(barrier, Point):
            return self.barrier_dict[barrier[0]][barrier[1]].remove_top()
        else:
            return self.barrier_dict[barrier.center_x][barrier.center_y].remove(barrier)


#USE Weak refs(arcade as example)