def displayPathtoPrincess(n, grid):
    g = Grid(n, grid)
    g.solve()
    #solution = g.solution
    print('\n'.join(g.solution))


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class Queue():
    def __init__(self):
        self.q = []

    def put(self, node):
        self.q.append(node)

    def get(self):
        if self.is_empty():
            raise Exception("empty queue")
        return self.q.pop(0)

    def contain_state(self, state):
        return any(node.state==state for node in self.q)

    def is_empty(self):
        return len(self.q)==0

class Grid():
    def __init__(self, n, grid):
        self.height = n
        self.width = n
        str_grd = ''.join(grid)

        #validate start and goal
        if str_grd.count('m') != 1:
            raise Exception("grid must have exactly one player")
        if str_grd.count('p') != 1:
            raise Exception("grid must have exactly one princess")

        # Get princess and player position
        for i in range(self.height):
            for j in range(self.width):
                if grid[i][j] == 'm':
                    self.start = i, j
                elif grid[i][j] == 'p':
                    self.goal = i, j
        self.solution = None

    def neighbors(self, state):
        row, col = state
        candidate = [
            ("UP", (row - 1, col)),
            ("DOWN", (row + 1, col)),
            ("LEFT", (row, col - 1)),
            ("RIGHT", (row, col + 1))
        ]
        neighbors = []
        for action,(r,c) in candidate:
            if 0<=r<=self.height and 0<=c<=self.width:
                neighbors.append((action, (r,c)))
        return neighbors

    def solve(self):
        """Find the princess"""
        start = Node(self.start, None, None)
        frontier = Queue()
        frontier.put(start)

        self.explored = set()

        while True:
            # If nothing is left in the frontier, then no path
            if frontier.is_empty():
                raise Exception("no solution")

            node = frontier.get()
            # check if node is the goal state
            if node.state == self.goal:
                actions = []
                #actions.append()
                while node.parent:
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                self.solution = actions
                break

            self.explored.add(node.state)
            
            # add neighbors to the frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contain_state(state) and state not in self.explored:
                    child = Node(state, node, action)
                    frontier.put(child)
m = int(input())
grid = []
for i in range(0, m):
    grid.append(input().strip())
displayPathtoPrincess(m, grid)
