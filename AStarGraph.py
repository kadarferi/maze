# https://rosettacode.org/wiki/A*_search_algorithm#Python

from __future__ import print_function


class AStarGraph(object):
    # Define a class board like grid with two barriers

    def __init__(self):
        self.barriers = []
        self.barriers.append(
            [(2, 4), (2, 5), (2, 6), (3, 6), (4, 6), (5, 6), (5, 5), (5, 4), (5, 3), (5, 2), (4, 2), (3, 2)])
        self.nrow = 7
        self.ncol = 7
        print(self.barriers)

    def heuristic(self, start, goal):
        # Use Chebyshev distance heuristic if we can move one square either
        # adjacent or diagonal
        D = 1
        D2 = 2  # Manhattan distance  (instead of 1 Chebyshev)
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    def get_vertex_neighbours(self, pos):
        n = []
        # Moves allow link a chess king
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
#        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            x2 = pos[0] + dx
            y2 = pos[1] + dy
            if x2 < 0 or x2 > self.ncol-1 or y2 < 0 or y2 > self.nrow-1:
                continue
            n.append((x2, y2))
        return n

    def move_cost(self, a, b):
        for barrier in self.barriers:
            if b in barrier:
                return 9999  # Extremely high cost to enter barrier squares
        return 1  # Normal movement cost


