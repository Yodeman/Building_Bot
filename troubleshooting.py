def rotate(board, direction):
    new_board = None
    board = [list(line) for line in board]
    if direction == 'UP':
        new_board = board
    elif direction == 'RIGHT':
        new_board = reversed(list(zip(*board)))
    elif direction == 'DOWN':
        new_board = [reversed(args) for args in reversed(board)]
    elif direction == 'LEFT':
        new_board = [reversed(args) for args in zip(*board)]

    return to_string(new_board)

def to_string(board):
    b = []
    for i in board:
        s = ''
        for j in i:
            s += str(j)
        b.append(s)
    return '\n'.join(b)

if __name__ == "__main__":
    board = [[0,3,8],[4,1,7],[2,6,5]]
    #board = ['###', '#--', '###']
    #board = [('#', '-', '-'), ('#', '-', '-'), ('#', '#', '#')]
    print(to_string(board))
    #print(rotate(board, 'LEFT'))
##    direction = ['RIGHT', 'UP', 'LEFT', 'DOWN']
##    for d in direction:
##        print(d+':')
##        print(rotate(board, d))
##        print()
