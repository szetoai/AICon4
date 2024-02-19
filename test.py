Y = "Y"
EMPTY = ""
boardd = [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, Y, EMPTY, Y, EMPTY, EMPTY],
            [EMPTY, Y, Y, EMPTY, Y, EMPTY, EMPTY],]
def actions(board):
    # in: board state, out: all possible actions
    moves = []
    # row itterator
    for i in range(6):
        # column itterator
        for j in range(7):
            if i == 5:   
                if board[i][j] == EMPTY:
                    moves.append([i, j])
            else:
                if board[i][j] == EMPTY and board[i + 1][j] != EMPTY:
                    moves.append([i, j])
    return moves

def main():
    print(f"{actions(boardd)}")

main()