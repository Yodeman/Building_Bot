import heapq

def next_move(posr, posc, board):
    c = CleanDirt((posr, posc), board)
    actions = c.solve()
    print(actions)

class Node():
    def __init__(self, state, parent, action):
        self.state = state[0]
        self.parent = parent
        self.action = action
        self.path_cost = parent.path_cost + state[2] if parent else state[2]

class PriorityQueueWithFunction():
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes.The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction
        self.q = []

    def put(self, item):
        entry = (item, self.priorityFunction(item))
        heapq.heappush(self.q, entry)

    def get(self):
        (item, _) = heapq.heappop(self.q)
        return item

    def isEmpty(self):
        return len(self.q)==0

    def contain_state(self, state):
        return any(item[1].state==state for item in self.q)

class CleanDirt():
    """
    A Search problem associated with cleaning all the dirts in a grid.
    """
    def __init__(self, bot_pos, board):
        self.bot_pos = bot_pos
        self.board = board
        #self.board_grid = self.board_to_grid()
        self.height = self.width = len(board)

    def get_dirts(self, board):
        dirts = []
        for i, row in enumerate(board):
            if 'd' in ''.join(row):
                for j, col in enumerate(row):
                    if col == 'd':
                        dirts.append((i,j))
        return dirts

    def board_grid(self, board):
        return [[i for i in j] for j in board]
    
    def getStartState(self):
        #return (self.bot_pos, tuple(self.board_grid(self.board)))
        return (self.bot_pos)

    def isGoalState(self, state):
        return len(self.get_dirts(state[1]))==0

    def neighbors(self, state):
        row, col = state[0]
        candidate = [
            ("UP", (row - 1, col)),
            ("DOWN", (row + 1, col)),
            ("LEFT", (row, col - 1)),
            ("RIGHT", (row, col + 1))
        ]
        neighbors = []
        for action,(r,c) in candidate:
            if 0<=r<=self.height and 0<=c<=self.width:
                nextState = state[1].copy()
                nextState[r][c] = '-'
                neighbors.append((((r,c), tuple(nextState)), action, 1))
        return neighbors

    def manhattanDistance(self, pos1, pos2):
        return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

    def heuristic(self, state):
        dist = 0
        bot_pos, grid = state
        dirts = self.get_dirts(grid)
        if len(dirts)==0:
            return 0
        for i in range(len(dirts)):
            nextDirt = dirts[i]
            dirt_dist = self.manhattanDistance(bot_pos, nextDirt)
            if dirt_dist > dist:
                dist = dirt_dist
        return dist

    def solve(self):
        """
        Solve the problem using astar search.
        """
        func = lambda item:item.path_cost + self.heuristic(item.state)
        node = Node((self.getStartState(), None, 0), None, None)
        frontier = PriorityQueueWithFunction(func)
        explored_states = set()
        frontier.put(node)
        while True:
            if frontier.isEmpty():
                return []
            node = frontier.get()
            if self.isGoalState(node.state):
                path = []
                while node.parent:
                    path.insert(0, node.action)
                    node = node.parent
                return path
            print(node.state)
            explored_states.add(node.state)
            for successor in self.neighbors(node.state):
                child = Node(successor, node, successor[1])
                if child.state not in explored_states and not frontier.contain_state(child.state):
                    frontier.put(child)

    
        
if __name__ == "__main__":
    #posr, posc = map(int, input().strip().split())
    posr, posc = 0, 0
    #board = []
    board = ['b---d', '-d--d', '--dd-', '--d--', '----d']
    #for i in range(5):
    #    board.append(input())

    next_move(posr, posc, board)
