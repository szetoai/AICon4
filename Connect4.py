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

Credits:
Functions adapted from CS50's Introduction to Artificial Intelligence with Python Week 0 - Tic-Tac-Toe Project
"""

# Board Variables
R = "R"
Y = "Y"
EMPTY = None
v = 0

# Functions

def initial_state():
    board = [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],]
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
    moves = []
    for i in range(6):
        for j in range(7):
            if i == 5:   
                if board[i][j] == EMPTY:
                    moves.append([i, j])
            else:
                if board[i][j] == EMPTY and board[i + 1][j] != EMPTY:
                    moves.append([i, j])
    return moves

def result(board, action):
    turn = player(board)
    newboard = [row[:] for row in board]
    if newboard[action[0]][action[1]] == EMPTY:
        newboard[action[0]][action[1]] = turn
    else:
        pass
    return newboard

def utility(board):
    """
    Returns 1 if Red has won the game, -1 if Yellow has won, 0 otherwise.
    """
    
    for color in [R, Y]:
        # Horizontal Check
        for row in range(6):
            for col in range(4):  # Only need to start check up to the 4th column
                if all(board[row][col + k] == color for k in range(4)):
                    return 1 if color == R else -1
        
        # Vertical Check
        for col in range(7):
            for row in range(3):  # Only need to start check up to the 3rd row from bottom
                if all(board[row + k][col] == color for k in range(4)):
                    return 1 if color == R else -1
        
        # Positive Diagonal Check (bottom left to top right)
        for row in range(3, 6):
            for col in range(4):
                if all(board[row - k][col + k] == color for k in range(4)):
                    return 1 if color == R else -1
        
        # Negative Diagonal Check (top left to bottom right)
        for row in range(3):
            for col in range(4):
                if all(board[row + k][col + k] == color for k in range(4)):
                    return 1 if color == R else -1
                    
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
    taken = 0
    if utility(board) != 0:
        return True
    for i in range(6):
        try:
            if board[i].index(EMPTY) > -1:
                break
        except ValueError:
            taken += 1
            continue
    if taken == 6:
        return True
    else:
        return False

def maxi(board, depth, depth_limit):
    if terminal(board) or depth == depth_limit:
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, mini(result(board, action), depth + 1, depth_limit))
    return v

def mini(board, depth, depth_limit):
    if terminal(board) or depth == depth_limit:
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, maxi(result(board, action), depth + 1, depth_limit))
    return v

def minimax(board):
    empty_cells = sum(row.count(EMPTY) for row in board)
    depth_limit = min(empty_cells, 5)
    if terminal(board):
        return None

    best_action = None
    if player(board) == R:
        best_value = -math.inf
        for action in actions(board):
            value = mini(result(board, action), 1, depth_limit)
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = math.inf
        for action in actions(board):
            value = maxi(result(board, action), 1, depth_limit)
            if value < best_value:
                best_value = value
                best_action = action

    return best_action

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
        title = font.render("Connect 4", True, red)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        subtitle = font.render("vs", True, white)
        subtitleRect = subtitle.get_rect()
        subtitleRect.center = ((width / 2), 100)
        subtitle1 = font.render("A.I.", True, yellow)
        subtitleRect1 = subtitle.get_rect()
        subtitleRect1.center = ((width / 2) - 10, 160)
        window.blit(title, titleRect)
        window.blit(subtitle, subtitleRect)
        window.blit(subtitle1, subtitleRect1)

        # Draw buttons
        playRedButton = pygame.Rect((width / 3.08), (height / 2.75), 350, 50)
        playRed = font.render("Play as Red", True, red)
        playRedRect = playRed.get_rect()
        playRedRect.center = playRedButton.center
        pygame.draw.rect(window, blue, playRedButton)
        window.blit(playRed, playRedRect)

        playYellowButton = pygame.Rect((width / 3.3), (height / 2), 400, 50)
        playYellow = font.render("Play as Yellow", True, yellow)
        playYellowRect = playYellow.get_rect()
        playYellowRect.center = playYellowButton.center
        pygame.draw.rect(window, blue, playYellowButton)
        window.blit(playYellow, playYellowRect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playRedButton.collidepoint(mouse):
                time.sleep(0.5)
                user = R
            elif playYellowButton.collidepoint(mouse):
                time.sleep(0.5)
                board[5][3] = R
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
            victor = winner(board)
            if victor is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over:   wins."
                letter1 = f"{victor}"
                if victor == R:
                    ROY = red
                else:
                    ROY = yellow
                letter1 = font.render(letter1, True, ROY)
                letter1Rect = letter1.get_rect()
                letter1Rect.center = ((width / 1.715), 30)
                window.blit(letter1, letter1Rect)
        elif user == Player:
            title = f"Play as"
            letter = f"{user}"
            if user == R:
                ROY = red
            else:
                ROY = yellow
            letter = font.render(letter, True, ROY)
            letterRect = letter.get_rect()
            letterRect.center = ((width / 1.59), 30)
            window.blit(letter, letterRect)
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
