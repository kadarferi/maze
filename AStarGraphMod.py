from AStarGraph import *
import numpy as np

ch_barrier = '#'
ch_mine    = '%'
ch_free    = '.'
ch_start   = 'X'
ch_route   = '*'

class AStarGraphMod(AStarGraph):

    def __init__(self, file):

        self.barriers = []         # positions of barriers or walls
        self.mines = []            # positions of mines
        self.start_point = (0, 0)  # position of start point
        self.end_points = []       # positions of exit points
        self.nrow = 0              # vertical size
        self.ncol = 0              # horizontal size
        self.mine_cost = 9999

        with open(file, "rt") as infile:
            matrix = np.matrix([list(line.strip()) for line in infile.readlines()])
            self.nrow = matrix.shape[0]
            self.ncol = matrix.shape[1]
            self.matrix = matrix

            # identify barriers, mines, start and end points
            barriers = []
            for y in range(self.nrow):
                #print(matrix[y])
                for x in range(self.ncol):
                    ch = matrix[y, x]
                    if ch == ch_barrier:
                        barriers.append((x, y))
                    elif ch == ch_mine:
                        self.mines.append((x, y))
                    elif ch == ch_start:
                        self.start_point = (x, y)
            self.barriers.append(barriers)

            # End points: "." at row=0,max or col=0,max
            for y in range(self.nrow):
                for x in [0, self.ncol-1]:
                    if matrix[y, x] == '.':
                        self.end_points.append((x, y))
            for x in range(self.ncol):
                for y in [0, self.nrow-1]:
                    if matrix[y, x] == '.':
                        self.end_points.append((x, y))

            #print("\nBarriers: ", self.barriers)
            #print("\nMines: ", self.mines)
            #print("\nStart: ", self.start_point)
            #print("\nEnd points: ", self.end_points)

    def move_cost(self, a, b):
        c = 1
        is_mine = 0
        for barrier in self.barriers:
            if b in barrier:
                c = np.inf  # Extremely high cost to enter barrier squares
                #c = np.inf
                # ezeket igazítsuk a mátrix méretéhez!

        if b in self.mines:
            c = self.mine_cost

        return c

    def is_mine(self, b):
        if b in self.mines:
            return 1
        return 0



    def matrix_to_file(self, file='Output.txt'):
        with open(file, "wt") as outfile:
            for r in range(self.nrow):
                for c in range(self.ncol):
                    outfile.write(str(self.matrix[r, c]))
                outfile.write('\n')

    def update_matrix_with_route(self, route):
        for x, y in route[1:]:
            self.matrix[y, x] = ch_route

# --------------------------------------------------------------------------------------------
def AStarSearch(start, end, graph: AStarGraphMod):
    G = {}  # Actual movement cost to each position from the start position
    F = {}  # Estimated movement cost of start to end going via this position

    # Initialize starting values
    G[start] = 0
    F[start] = graph.heuristic(start, end)

    closedVertices = set()
    openVertices = {start}
    cameFrom = {}

    actual_path = []

    while len(openVertices) > 0:
        # Get the vertex in the open list with the lowest F score
        current = None
        currentFscore = None
        for pos in openVertices:
            if current is None or F[pos] < currentFscore:
                currentFscore = F[pos]
                current = pos
                actual_path.append(current)

        # Check if we have reached the goal
        if current == end:
            # Retrace our route backward
            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            return path, F[end]  # Done!

        # Mark the current vertex as closed
        openVertices.remove(current)
        closedVertices.add(current)

        # Update scores for vertices near the current position
        for neighbour in graph.get_vertex_neighbours(current):
            if neighbour in closedVertices:
                continue  # We have already processed this node exhaustively
            candidateG = G[current] + graph.move_cost(current, neighbour)    # cost

            if neighbour not in openVertices:
                openVertices.add(neighbour)  # Discovered a new vertex
            elif candidateG >= G[neighbour]:
                continue  # This G score is worse than previously found

            # Adopt this G score
            cameFrom[neighbour] = current
            G[neighbour] = candidateG
            H = graph.heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + H
            actual_path.append(current)

    raise RuntimeError("A* failed to find a solution")

