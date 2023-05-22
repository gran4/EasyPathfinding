from types import Point


__all__ = (
    "CustomList",
    "LivingMap"
    "BarrierDict"
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
        "__weakref__"
    )

    def __init__(self, x_length:int, y_length:int,  
                    size:int, *args, tilesize:int=50
                    ) -> None:
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

    def change(self, x:int, y:int, barrier:bool) -> None:
        x = int(x/50)
        y = int(y/50)

        if barrier:
            self.graph[x][y] = 1
        else:
            self.graph[x][y] = 0

    def __getitem__(self, i):
        return self.graph[i]

    def __setitem__(self, x, y, val):
        self.graph[x][y] = val




class ObservablePoint(list):
    """
    A List that represents a point that moves

    Use when you use AStarBarrierDict
    """
    def __setitem__(self, index, item):
        self.changed = True
        super().__setitem__(int(index), int(item))
    def __getitem__(self, __name):
        return super().__getitem__(int(__name))
    def __len__(self) -> int:
        return 2

class BarrierObject:
    def __init__(self, barrier, layer=0, bellow: List[Sprite] = []):
        self.barrier = barrier
        self.bellow = bellow
        self.layer = layer
    def get_bellow(self):
        if not self.bellow:
            return None
        self.barrier = self.bellow.pop()
        return self.barrier
    def push(self, barrier):
        if self.barrier:
            self.bellow.append(self.barrier)
        self.barrier = barrier
    def remove_top():
        obj = self.barrier
        self.barrier = self.bellow.pop()
        return obj
    def remove(barrier):
        if not barrier in self.layers:
            return None
        self.layers.remove(barrier)
    def __eq__(self, other: BarrierObject) -> bool:
        return self.layer == other.layer


class BarrierDict:
    """
    Class that manages a dict of barriers 
    that can be encountered during
    A* path finding.
    """
    def __init__(self,
                 blocking_sprites: Point,
                 tilesize: int,
                 left: int,
                 right: int,
                 bottom: int,
                 top: int,
                 moving_barriers: Optional[List[Point]] = None,
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

        self.static_barriers = blocking_sprites
        self.moving_barriers = moving_barriers
        self.barrier_dict = {}

        self.set_up_dict()

    def set_up_dict(self):
        for cx in range(self.left, self.right + 1):
            self.barrier_dict[cx] = {}
            for cy in range(self.bottom, self.top + 1):
                self.barrier_dict[cx][cy] = BarrierObject(None)
        for barrier in self.static_barriers:
            x, y = _collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y].push(barrier)
        for barrier in self.moving_barriers:
            x, y = _collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y].push(barrier)

    def recalculate(self):
        for barrier in self.static_barriers:
            x, y = _collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y].barrier = barrier
        for barrier in self.moving_barriers:
            x, y = _collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y].barrier = barrier

    def recalculate_moving():
        for barrier in self.moving_barriers:
            x, y = _collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y].barrier = barrier

    def add_static_barrier(self, barrier):
        self.static_barriers.append(barrier)
        x, y = _collapse(barrier.position, self.tilesize)
        self.barrier_dict[x][y].barrier = barrier
    
    def add_moving_barrier(self, barrier):
        self.moving_barriers.append(barrier)
        x, y = _collapse(barrier.position, self.tilesize)
        self.barrier_dict[x][y].barrier = barrier
    
    def remove_static(self, barrier = Union[int, Point]):
        if isinstance(barrier, int):
            return self.static_barriers.pop(int)
        elif isinstance(barrier, Point):
            temp = self.barrier_dict[barrier[0]][barrier[1]]
            self.barrier_dict[barrier[0]][barrier[1]] = None
            return temp

    def remove_moving(self, index: Union[int, Point]):
        if isinstance(barrier, int):
            return self.moving_barriers.pop(int)
        elif isinstance(barrier, Point):
            temp = self.barrier_dict[barrier[0]][barrier[1]]
            self.barrier_dict[barrier[0]][barrier[1]] = None
            return temp

class LayeredBarrierDict:
    """
    Class that manages a dict of barriers 
    that can be encountered during
    A* path finding.
    """
    def __init__(self,
                 blocking_sprites: Point,
                 tilesize: int,
                 left: int,
                 right: int,
                 bottom: int,
                 top: int,
                 moving_barriers: Optional[List[Point]] = None,
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

        self.static_barriers = blocking_sprites
        self.moving_barriers = moving_barriers
        self.barrier_dict = {}

        self.set_up_dict()

    def set_up_dict(self):
        for cx in range(self.left, self.right + 1):
            self.barrier_dict[cx] = {}
            for cy in range(self.bottom, self.top + 1):
                self.barrier_dict[cx][cy] = BarrierObject(None)
        for barrier in self.static_barriers:
            x, y = _collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y].push(barrier)
        for barrier in self.moving_barriers:
            x, y = _collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y].push(barrier)

    def recalculate(self):
        for barrier in self.static_barriers:
            x, y = _collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y].barrier = barrier
        for barrier in self.moving_barriers:
            x, y = _collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y].barrier = barrier

    def recalculate_moving():
        for barrier in self.moving_barriers:
            x, y = _collapse(barrier.position, self.tilesize)
            self.barrier_dict[x][y].barrier = barrier

    def add_static_barrier(self, barrier):
        self.static_barriers.append(barrier)
        x, y = _collapse(barrier.position, self.tilesize)
        self.barrier_dict[x][y].barrier = barrier
    
    def add_moving_barrier(self, barrier):
        self.moving_barriers.append(barrier)
        x, y = _collapse(barrier.position, self.tilesize)
        self.barrier_dict[x][y].barrier = barrier
    
    def remove_static(self, barrier = Union[int, Point, "Any barrier"]):
        if isinstance(barrier, int):
            return self.static_barriers.pop(int)
        elif isinstance(barrier, Point):
            return self.barrier_dict[barrier[0]][barrier[1]].remove_top()
        else:
            return self.barrier_dict[barrier[0]][barrier[1]].remove(barrier)

    def remove_moving(self, index: Union[int, Point, "Any barrier"]):
        if isinstance(barrier, int):
            return self.moving_barriers.pop(int)
        elif isinstance(barrier, Point):
            return self.barrier_dict[barrier[0]][barrier[1]].remove_top()
        else:
            return self.barrier_dict[barrier[0]][barrier[1]].remove(barrier)


# Example usage
N, M = input().split()
N, M = int(N), int(M)
breeds = input()

roads = []
for i in range(N-1):
    road = input()
    start, end = road.split(" ")
    start, end = int(start), int(end)

friends = []
for i in range(M):
    visit = input()
    start, end, person = visit.split(" ")
    start, end, person = int(start), int(end), int(person)




print(output)



#USE Weak refs(arcade as example)