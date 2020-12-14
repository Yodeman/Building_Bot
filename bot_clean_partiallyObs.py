import pickle
def next_move(posr, posc, board):
    agent = CleanDirt((posr, posc), board)
    action = agent.solve()
    print(action)

class Node():
    def __init__(self, state, action):
        self.state = state
        self.action = action

class Frontier():
    def __init__(self):
        self.f = []

    def put(self, node):
        self.f.append(node)

    def get(self):
        node = self.f[-1]
        return node.state

    def contain_state(self, state):
        return any(node.state==state for node in self.f)
    def get_actions(self, state):
        return [node.action for node in self.f if node.state==state]

class CleanDirt():
    def __init__(self, bot_pos, board):
        self.board = board
        mem_board = []
        self.bot_pos = bot_pos
        #self.height = self.width = 5
        try:
            with open(filename, 'rb') as f:
                self.frontier = pickle.load(f)
                mem_board = self.frontier.get()
        except:
            self.frontier = Frontier()
        if mem_board:
            for i in [0,1,2,3,4]:
                for j in [0,1,2,3,4]:
                    if mem_board[i][j]=='-' and self.board[i][j]=='o':
                        self.board[i][j]='-'
                    if mem_board[i][j]=='d' and self.board[i][j]=='o':
                        self.board[i][j] = 'd'


    def get_dirts(self, row, col):
        dirts = []
        directions = {(1,0), (-1,0), (0,-1), (0, 1), (1,1),
                      (-1,-1), (1,-1), (-1,1), (0,0)}
        for dr, dc in directions:
            if 0<=(row+dr)<5 and 0<=(col+dc)<5:
                if self.board[row+dr][col+dc]=='d':
                    dirts.append((row+dr,col+dc))
        #for i, row in enumerate(self.board):
        #    if 'd' in row:
        #        for j, col in enumerate(row):
        #            if col == 'd':
        #                dirts.append((i,j))
        return dirts

    def get_unobserved(self):
        unobserved = []
        for i, row in enumerate(self.board):
            if 'o' in row:
                for j,col in enumerate(row):
                    if col=='o':
                        unobserved.append((i,j))
        return unobserved

    def closest_unobserved(self):
        position = self.bot_pos
        unobserved = self.get_unobserved()
        if unobserved:
            i,j = min(unobserved,
                key=lambda pos:((position[0]-pos[0])**2+(position[1]-pos[1])**2)**0.5
                )
            return i,j

    def closest_dirt(self):
        """
        Find the closest dirt to the bot using the euclidean distance.
        """
        position = self.bot_pos
        dirts = self.get_dirts(position[0],position[1])
        if dirts:
            i, j = min(dirts,
                key=lambda dirt_pos:((position[0]-dirt_pos[0])**2+(position[1]-dirt_pos[1])**2)**0.5
                )
            return (i,j)

    def neighbors(self):
        """
        Get the closest box to the dirt using the euclidean distance.
        """
        dirt_pos = self.closest_dirt()
        row, col = self.bot_pos
        if dirt_pos:
            actions = [
                ("UP", (row - 1, col)),
                ("DOWN", (row + 1, col)),
                ("LEFT", (row, col - 1)),
                ("RIGHT", (row, col + 1)),
                ("CLEAN", (row, col))
            ]  
            neighbors = []
            for action,(r,c) in actions:
                if (0<=r<5 and 0<=c<5):
                    neighbors.append((action, (r,c)))
        
            sorted_neighbors = sorted(neighbors,
                            key=lambda action: ((action[1][0]-dirt_pos[0])**2+
                                            (action[1][1]-dirt_pos[1])**2)**0.5
                            )
            #if dirt_pos==self.bot_pos:
            #    neighbors.insert(0, ("CLEAN", (row, col)))
            return sorted_neighbors
        else:
            unobserved = self.closest_unobserved()
            if unobserved:
                actions = [
                ("RIGHT", (row, col + 1)),
                ("LEFT", (row, col - 1)),
                ("UP", (row - 1, col)),
                ("DOWN", (row + 1, col))
                ]  
                neighbors = []
                for action,(r,c) in actions:
                    if 0<=r<5 and 0<=c<5:
                        neighbors.append((action, (r,c)))
                sorted_neighbors = sorted(neighbors,
                                key=lambda action: ((action[1][0]-unobserved[0])**2+
                                                    (action[1][1]-unobserved[1])**2)**0.5
                            )
                
                if self.frontier.contain_state(self.board):
                    for i,action in enumerate(sorted_neighbors):
                        if action[0] in self.frontier.get_actions(self.board):
                            sorted_neighbors.pop(i)
                self.frontier.put(Node(self.board, sorted_neighbors[0][0]))
                with open(filename, 'wb') as f:
                    pickle.dump(self.frontier, f)
                return sorted_neighbors

    def solve(self):
        percepts = self.neighbors()
        return percepts[0][0]

if __name__ == "__main__":
    filename = 'board.txt'
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)
