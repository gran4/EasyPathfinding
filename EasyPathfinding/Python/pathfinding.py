from pathfindingfuncs import *
from customMaps import *

__all__ = (
    "AStarSearch",
    "SearchTilesAround"
)


def AStarSearch(Map:LivingMap, start:tuple, end:tuple, allow_diagonal_movement:bool=True, movelist=[], min_dist=0):
    tilesize = Map.tilesize
    length = Map.length
    height = Map.height

    start = (int(start[0]/tilesize), int(start[1]/tilesize))
    end = (int(end[0]/tilesize), int(end[1]/tilesize))

    G = {}  # Actual movement cost to each position from the start position
    F = {}  # Estimated movement cost of start to end going via this position

    graph = Map.graph
    max_iterations = len(graph[0]) * len(graph)

    # Initialize starting values
    G[start] = 0
    F[start] = heuristic(start, end)

    closed_vertices = set()
    open_vertices = set([start])
    came_from = {}

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    count = 0
    while len(open_vertices) > 0:
        count += 1
        if count > max_iterations:
            break

        # Get the vertex in the open list with the lowest F score
        current = None
        current_fscore = None
        for pos in open_vertices:
            if current is None or F[pos] < current_fscore:
                current_fscore = F[pos]
                current = pos

        # Check if we have reached the goal
        dist = get_dist(current, end)*tilesize
        if dist <= min_dist:
            # Retrace our route backward
            path = [[current[0]*tilesize, current[1]*tilesize]]
            while current in came_from:
                current = came_from[current]
                path.append([current[0]*tilesize, current[1]*tilesize])
            path.reverse()

            return path  # Done!

        # Mark the current vertex as closed
        open_vertices.remove(current)
        closed_vertices.add(current)

        neighbours = []
        for new_position in adjacent_squares: # Adjacent squares
            neighbours.append((current[0] + new_position[0], current[1] + new_position[1]))

        # Update scores for vertices near the current position
        for neighbour in neighbours:
            if neighbour in closed_vertices:
                continue  # We have already processed this node exhaustively
            elif neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= 100 or neighbour[1] >= 100:
                continue

            if not graph[neighbour[0]][neighbour[1]] in movelist:
                continue


            candidate_g = G[current] + move_cost(current, neighbour)

            if not neighbour in open_vertices:
                open_vertices.add(neighbour)  # Discovered a new vertex
            elif candidate_g >= G[neighbour]:
                continue  # This G score is worse than previously found

            # Adopt this G score
            came_from[neighbour] = current
            G[neighbour] = candidate_g
            h = heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + h

    # Out-of-bounds
    return []


def SearchTilesAround(Map:LivingMap, start:tuple, allow_diagonal_movement:bool=True, movelist=[]):
    tilesize = Map.tilesize
    length = Map.length
    height = Map.height

    start = (int(start[0]/tilesize), int(start[1]/tilesize))

    graph = Map.graph

    closed_vertices = set()
    open_vertices = set([start])

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    count = 0
    while len(open_vertices) > 0:
        count += 1
        if count > 100:
            break

        #get first element in the set
        for current in open_vertices:
            break
        open_vertices.remove(current)
        closed_vertices.add(current)

        neighbours = []
        for new_position in adjacent_squares: # Adjacent squares
            neighbours.append((current[0] + new_position[0], current[1] + new_position[1]))

        # Update scores for vertices near the current position
        for neighbour in neighbours:
            if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= length or neighbour[1] >= height:
                continue

            if not graph[neighbour[0]][neighbour[1]] in movelist:
                continue
            if neighbour in closed_vertices:
                continue

            if not neighbour in open_vertices:
                open_vertices.add(neighbour)  


    # Out-of-bounds
    return count




def AStarWDict(Map:BarrierDict, start:tuple, end:tuple, allow_diagonal_movement:bool=True, movelist=[], min_dist=0):
    tilesize = Map.tilesize
    length = Map.length
    height = Map.height

    start = (int(start[0]/tilesize), int(start[1]/tilesize))
    end = (int(end[0]/tilesize), int(end[1]/tilesize))

    G = {}  # Actual movement cost to each position from the start position
    F = {}  # Estimated movement cost of start to end going via this position

    graph = Map.barrier_dict
    max_iterations = len(Map.length) * len(Map.height)

    # Initialize starting values
    G[start] = 0
    F[start] = heuristic(start, end)

    closed_vertices = set()
    open_vertices = set([start])
    came_from = {}

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    count = 0
    while len(open_vertices) > 0:
        count += 1
        if count > max_iterations:
            break

        # Get the vertex in the open list with the lowest F score
        current = None
        current_fscore = None
        for pos in open_vertices:
            if current is None or F[pos] < current_fscore:
                current_fscore = F[pos]
                current = pos

        # Check if we have reached the goal
        dist = get_dist(current, end)*50
        if dist <= min_dist:
            # Retrace our route backward
            path = [[current[0]*tilesize, current[1]*tilesize]]
            while current in came_from:
                current = came_from[current]
                path.append([current[0]*tilesize, current[1]*tilesize])
            path.reverse()

            return path  # Done!

        # Mark the current vertex as closed
        open_vertices.remove(current)
        closed_vertices.add(current)

        neighbours = []
        for new_position in adjacent_squares: # Adjacent squares
            neighbours.append((current[0] + new_position[0], current[1] + new_position[1]))

        # Update scores for vertices near the current position
        for neighbour in neighbours:
            if neighbour in closed_vertices:
                continue  # We have already processed this node exhaustively
            elif neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= length or neighbour[1] >= height:
                continue

            if not graph[neighbour[0]][neighbour[1]] in movelist:
                continue


            candidate_g = G[current] + move_cost(current, neighbour)

            if not neighbour in open_vertices:
                open_vertices.add(neighbour)  # Discovered a new vertex
            elif candidate_g >= G[neighbour]:
                continue  # This G score is worse than previously found

            # Adopt this G score
            came_from[neighbour] = current
            G[neighbour] = candidate_g
            h = heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + h

    # Out-of-bounds
    return []


def SearchAroundWDict(Map:BarrierDict, start:tuple, allow_diagonal_movement:bool=True, movelist=[]):
    tilesize = Map.tilesize
    length = Map.length
    height = Map.height

    start = (int(start[0]/tilesize), int(start[1]/tilesize))

    graph = Map.barrier_dict

    closed_vertices = set()
    open_vertices = set([start])

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    count = 0
    while len(open_vertices) > 0:
        count += 1
        if count > 100:
            break

        #get first element in the set
        for current in open_vertices:
            break
        open_vertices.remove(current)
        closed_vertices.add(current)

        neighbours = []
        for new_position in adjacent_squares: # Adjacent squares
            neighbours.append((current[0] + new_position[0], current[1] + new_position[1]))

        # Update scores for vertices near the current position
        for neighbour in neighbours:
            if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= length or neighbour[1] >= hegiht:
                continue

            if not graph[neighbour[0]][neighbour[1]] in movelist:
                continue
            if neighbour in closed_vertices:
                continue

            if not neighbour in open_vertices:
                open_vertices.add(neighbour)  


    # Out-of-bounds
    return count

