def next_move(posr, posc, board):
    height = len(board)
    width = max([len(i) for i in board])
    def dirts_pos(board):
        dirts = []
        for i, row in enumerate(board):
            if 'd' in row:
                for j, col in enumerate(row):
                    if col == 'd':
                        dirts.append((i,j))
        return dirts

    # determine the closest dirt
    i, j = min(dirts_pos(board),
               key=lambda dirt_pos:abs(posr-dirt_pos[0])+abs(posc-dirt_pos[1])
               )

##    if i > posr: print('DOWN')
##    elif i < posr: print('UP')
##    elif j < posc: print('LEFT')
##    elif j > posc: print('RIGHT')
##    else: print('CLEAN')

    print(
        'LEFT' if j < posc else 'RIGHT' if j > posc else 'UP' if i < posr
        else 'DOWN' if i > posr else 'CLEAN'
        )


posr, posc = map(int, input().strip().split())
board = []
for i in range(5):
    board.append(input())

next_move(posr, posc, board)
