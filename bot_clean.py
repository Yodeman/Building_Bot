from math import sqrt

def next_move(posr, posc, board):
    agent = CleanDirt((posr, posc), board)
    action = agent.solve()
    print(action)

class CleanDirt():
    def __init__(self, bot_pos, board):
        self.board = board
        self.bot_pos = bot_pos
        self.height = self.width = 5

    def get_dirts(self):
        dirts = []
        for i, row in enumerate(self.board):
            if 'd' in row:
                for j, col in enumerate(row):
                    if col == 'd':
                        dirts.append((i,j))
        return dirts

    def closest_dirt(self):
        position = self.bot_pos
        i, j = min(self.get_dirts(),
               key=lambda dirt_pos:sqrt((position[0]-dirt_pos[0])**2+(position[1]-dirt_pos[1])**2)
               )
        return (i,j)

    def neighbors(self):
        """
        Find the closest dirt to the bot using the manhattan distance.
        """
        dirt_pos = self.closest_dirt()
        row, col = self.bot_pos
        candidate = [
            ("CLEAN", (row, col)),
            ("UP", (row - 1, col)),
            ("DOWN", (row + 1, col)),
            ("LEFT", (row, col - 1)),
            ("RIGHT", (row, col + 1))
        ]
        neighbors = []
        for action,(r,c) in candidate:
            if 0<=r<=self.height and 0<=c<=self.width:
                neighbors.append((action, (r,c)))
        neighbors = sorted(neighbors,
                            key=lambda action: sqrt((action[1][0]-dirt_pos[0])**2+(action[1][1]-dirt_pos[1])**2)
                        )
        #if dirt_pos==self.bot_pos:
        #    neighbors.insert(0, ("CLEAN", (row, col)))
        return neighbors

    def solve(self):
        percepts = self.neighbors()
        return percepts[0][0]

def to_str(board):
    str_board = []
    for i in board:
        s = ''
        for j in i:
            s += j
        str_board.append(s)
    return str_board

def solve(bot_pos, board):
    print("Search and clean dirt on the grid:\n'b'-bot, 'd'-dirt")
    print("\nInitial state:")
    print('\n'.join(board))
    num_move = 0
    done = False
    while not done:
        board = [[i for i in j] for j in board]
        c = CleanDirt(bot_pos, board)
        percept = c.neighbors()[0]
        print('\nAfter performing action: '+str(percept))
        if percept[0]=="CLEAN":
            num_move += 1
            board[bot_pos[0]][bot_pos[1]] = '-'
        else:
            num_move += 1
            board[bot_pos[0]][bot_pos[1]] = '-'
            if board[percept[1][0]][percept[1][1]] != 'd':
                board[percept[1][0]][percept[1][1]] = 'b'
        bot_pos = percept[1]
        print(''.join('\n'.join(to_str(board))))
        if ''.join(to_str(board)).count('d')==0:
            done = True
    print(f"{num_move} total moves")

if __name__ == "__main__":
    pos = (0,0)
    board = ['b---d', '-d--d', '--dd-', '--d--', '----d']
    #c = CleanDirt(pos, board)
    #print(c.bot_pos)
    #print(c.neighbors())
    #next_move(pos[0], pos[1], board)
    solve(pos, board)