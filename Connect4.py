import pygame
import sys
import time
import math
pygame.init()

"""
Run on Python 3.7.9 64 bit
Requirements:
    pygame ("pip install pygame" in cmd window)
    ttf file (can download from sites such as https://www.fontsquirrel.com/fonts/lato)
"""

# Board Variables
R = "R"
Y = "Y"
EMPTY = None
v = 0

# Functions
class inputerror(Exception):
    # raises exception if occupied square clicked
    print("Invalid cell.")
    pass

def initial_state():
    # initial board state
    board = [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],]
    # the first EMPTY in that list is [0][0] and is the top left of the board - meaning bottom right is [5][6]
    return board


def player(board):
    # returns which turn it is
    rcount = 0
    ycount = 0
    # rows
    for i in range(6):
        # columns
        for j in range(7):
            if board[i][j] == R:
                rcount += 1
            elif board[i][j] == Y:
                ycount += 1
    if rcount == ycount:
        return R
    if rcount > ycount:
        return Y
    
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

def result(board, action):
    # in: board state + action, out: resulting board
    turn = player(board)
    newboard = [row[:] for row in board]
    if newboard[action[0]][action[1]] == EMPTY:
        newboard[action[0]][action[1]] = turn
    else:
        raise inputerror
    return newboard

def utility(board):
    """
    Returns 1 if Red has won the game, -1 if Yellow has won, 0 otherwise.
    """
    for c in [R, Y]:
        # Check rows and columns
        for i in range(4):
            if all(cell == c for cell in board[i]) or all(board[j][i] == c for j in range(4)):
                return 1 if c == R else -1
        # Check diagonals
        if all(board[i][i] == c for i in range(4)) or all(board[i][2 - i] == c for i in range(4)):
            return 1 if c == Y else -1
    return 0
        

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if utility(board) != 0:
        if utility(board) == 1:
            return R
        else:
            return Y
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    taken = 0
    if utility(board) != 0:
        return True
    for i in range(6):
        try:
        # if there's an available spot in this row
            if board[i].index(EMPTY) > -1:
                break
        # if there isnt
        except ValueError:
            taken += 1
            continue
    if taken == 6:
        return True
    else:
        return False

def maxi(board):
    if terminal(board) == True:
        return utility(board)
    v = -2
    # for each action possible
    for i in range(len(actions(board))):
        v = max(v, mini(result(board, actions(board)[i])))
    return v
    
def mini(board):
    if terminal(board) == True:
        return utility(board)
    v = 2
    # for each action possible
    for j in range(len(actions(board))):
        v = min(v, maxi(result(board, actions(board)[j])))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    bestaction = (0, 0)
    if player(board) == R:
        bestvalue = float('inf')     
    else:
        bestvalue = float('-inf')
    turn = player(board)
    if terminal(board) == True:
        return None
    # R wants to maximize win value
    if turn == R:
        bestvalue = maxi(board)
        # for each action possible on this board
        for i in range(len(actions(board))):
            # if the best max value equals the best min value for this action
            if bestvalue == mini(result(board, actions(board)[i])):
                bestaction = actions(board)[i]
                break
    # Y wants to minimize win value
    else:
        bestvalue = mini(board)
        # for each action possible on this board
        for j in range(len(actions(board))):
            # if the best original min value equals the best max value for this action
            if bestvalue == maxi(result(board, actions(board)[j])):
                bestaction = actions(board)[j]
                break

    return bestaction

"""""
MAIN GAME LOOP STARTS HERE
"""""

# Colors
yellow = (255, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 43, 255)
# Window
dimensions = width, height = (1000, 600)
window = pygame.display.set_mode(dimensions)
# font (font file, size)
font = pygame.font.Font("Roboto-Bold.ttf", 60)
# initialize game
user = None
board = initial_state()
ai_turn = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    window.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = font.render("Connect 4 VS AI", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        window.blit(title, titleRect)

        # Draw buttons
        playRedButton = pygame.Rect((width / 8), (height / 2), 350, 50)
        playRed = font.render("Play as Red", True, black)
        playRedRect = playRed.get_rect()
        playRedRect.center = playRedButton.center
        pygame.draw.rect(window, white, playRedButton)
        window.blit(playRed, playRedRect)

        playYellowButton = pygame.Rect(4 * (width / 8), (height / 2), 400, 50)
        playYellow = font.render("Play as Yellow", True, black)
        playYellowRect = playYellow.get_rect()
        playYellowRect.center = playYellowButton.center
        pygame.draw.rect(window, white, playYellowButton)
        window.blit(playYellow, playYellowRect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playRedButton.collidepoint(mouse):
                time.sleep(0.2)
                user = R
            elif playYellowButton.collidepoint(mouse):
                time.sleep(0.2)
                user = Y

    else:

        # Draw game board
        tile_size = 80
        board_width, board_height = 7 * tile_size, 6 * tile_size
        tile_origin = ((width - board_width) / 2,
                       (height - board_height) / 2 + 20)
        tiles = []
        for i in range(6):
            row = []
            for j in range(7):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(window, blue, rect, 3)

                if board[i][j] != EMPTY:
                    if board[i][j] == R:
                        ROY = red
                    else:
                        ROY = yellow
                    move = font.render(board[i][j], True, ROY)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    window.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = terminal(board)
        Player = player(board)

        # Show title
        if game_over:
            winner = winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == Player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = font.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        window.blit(title, titleRect)

        # Check for AI move
        if user != Player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = minimax(board)
                board = result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == Player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(6):
                for j in range(7):
                    if (tiles[i][j].collidepoint(mouse)):
                        # PROBLEM
                        for k in range(5, -1, -1):
                            try:
                                checker = actions(board).index([k, j])
                                board = result(board, (k, j))
                                break
                            except ValueError:
                                continue
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = font.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(window, white, againButton)
            window.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = initial_state()
                    ai_turn = False

    pygame.display.flip()
