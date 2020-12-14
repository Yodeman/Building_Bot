def next_move(posr, posc, board):
    agent = CleanDirt((posr, posc), board)
    action = agent.solve()
    print(action)

class CleanDirt():
    def __init__(self, bot_pos, board):
        self.board = board
        self.bot_pos = bot_pos
        self.height = self.width = 5

    def get_dirt(self):
        for i, row in enumerate(self.board):
            if 'd' in row:
                for j, col in enumerate(row):
                    if col == 'd':
                        return (i,j)

    #def closest_dirt(self):
    #    position = self.bot_pos
    #    i, j = min(self.get_dirts(),
    #           key=lambda dirt_pos:abs(position[0]-dirt_pos[0])+abs(position[1]-dirt_pos[1])
    #           )
    #    return (i,j)

    def neighbors(self):
        """
        Find the closest dirt to the bot using the manhattan distance.
        """
        dirt_pos = self.get_dirt()
        if dirt_pos==(-1,-1):
            raise Exception("Board is already cleaned")
        row, col = self.bot_pos
        candidate = [
            ("CLEAN", (row, col))
            ("UP", (row - 1, col)),
            ("DOWN", (row + 1, col)),
            ("LEFT", (row, col - 1)),
            ("RIGHT", (row, col + 1))
        ]
        neighbors = []
        for action,(r,c) in candidate:
            if 0<=r<=self.height and 0<=c<=self.width:
                neighbors.append((action, (r,c)))
        #neighbors = sorted(neighbors,
        #                    key=lambda action: abs(action[1][0]-dirt_pos[0])+abs(action[1][1]-dirt_pos[1])
        #                )
        #if dirt_pos==self.bot_pos:
        #    neighbors.insert(0, ("CLEAN", (row, col)))
        return neighbors

    def solve(self):
        percepts = self.neighbors()
        return percepts[0][0]

if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)