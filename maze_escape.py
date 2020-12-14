import pickle

def next_move(ID, board):
	m = Maze_Escape(board)
	print(m.solve())

class Maze_Escape():
    def __init__(self, board):
        self.board = [list(line) for line in board]
        mem_board = None
        self.bot_pos = (1,1)
        try:
            with open(filename, 'rb') as f:
                mem_board = pickle.load(f)
        except:
            self.new_board = self.rotate(self.board, 'LEFT')
        if mem_board:
            board,action = mem_board
            self.new_board = self.rotate(self.board, self.decide(action))
            for i in [0, 1, 2]:
                for j in [0, 1, 2]:
                    if board[i][j]=='#' and self.new_board[i][j]=='-':
                        self.new_board[i][j]='#'
            self.board = self.rotate(self.new_board, self.bot_orient(action))
        print(self.new_board)

    def maze_orient(self, action):
        if action=='RIGHT':
            return 'DOWN'
        

    def bot_orient(self, action):
        if action=='UP':
            return 'UP'
        elif action == 'DOWN':
            return 'DOWN'
        elif action == 'RIGHT':
            return 'LEFT'
        else:
            return 'RIGHT'
        

    def get_walls(self):
        gate = None
        walls = []
        for i,row in enumerate(self.board):
            if 'e' in row or '#' in row:
                for j, col in enumerate(row):
                    if col=='#':
                        walls.append((i,j))
                    if col=='e':
                        gate = (i,j)
        return walls, gate
    
    def rotate(self, board, direction):
        board = [list(line) for line in board]
        if direction == 'UP':
            return board
        elif direction == 'RIGHT':
            return [list(i) for i in list(reversed(list(zip(*board))))]
        elif direction == 'DOWN':
            return [list(reversed(args)) for args in reversed(board)]
        elif direction == 'LEFT':
            return [list(reversed(args)) for args in zip(*board)]

    def neighbors(self):
        walls, gate = self.get_walls()
        row,col = self.bot_pos
        actions = [
            ("RIGHT", (row, col + 1)),
            ("LEFT", (row, col - 1)),
            ("UP", (row - 1, col)),
            ("DOWN", (row + 1, col))
        ]
        neighbors = []
        for action, (r,c) in actions:
            if (0<=r<3 and 0<=c<3) and (r,c) not in walls:
                neighbors.append((action, (r,c)))

        # sort neighbors according to their distances from bot position or gate.
        if gate:
            neighbors = sorted(neighbors, key=lambda action:abs(action[1][0]-gate[0])+
                               abs(action[1][1]-gate[1]))
        else:
            neighbors = sorted(neighbors, key=lambda action:abs(action[1][0]-row)+
                               abs(action[1][1]-col))
        with open(filename, 'wb') as f:
            pickle.dump((self.new_board, neighbors[0][0]), f)
        #print(self.new_board)
        return neighbors

    def solve(self):
    	actions = self.neighbors()
    	return actions[0][0]

if __name__ == "__main__":
    filename = 'memory.txt'
    player = int(input())
    board = [[j for j in input().strip()] for i in range(3)]
    next_move(player, board)
