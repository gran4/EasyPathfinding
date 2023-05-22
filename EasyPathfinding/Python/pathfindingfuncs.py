

__all__ = (
    "heuristic",
    "move_cost",
    "get_dist"
)

def heuristic(start:tuple, goal:tuple):
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


def move_cost(a:int, b:int):

    if a[0] == b[0] or a[1] == b[1]:
        return 1*5
    else:
        return 1.42*5


def get_dist(pos, pos2):
    return math.sqrt((pos[0]-pos2[0])**2+(pos[1]- pos2[1])**2)
