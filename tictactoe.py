import pygame

pygame.init()

# Set up window
game_display = pygame.display.set_mode((450, 450))
pygame.display.set_caption('Tic Tac Toe')

# Set up game board
game_board = [[None, None, None], [None, None, None], [None, None, None]]
white = (255, 255, 255)
black = (0, 0, 0)
game_display.fill(black)
pygame.draw.line(game_display, white, (150, 0), (150, 450), 3)
pygame.draw.line(game_display, white, (300, 0), (300, 450), 3)
pygame.draw.line(game_display, white, (0, 150), (450, 150), 3)
pygame.draw.line(game_display, white, (0, 300), (450, 300), 3)


# Center positions for each tile
TILE_POS = [[(75, 75), (225, 75), (375, 75)], [(75, 225), (225, 225),
                                               (375, 225)], [(75, 375), (225, 375), (375, 375)]]


# Find tile position from click postion and update game board
def find_tile(pos):
    if pos[0] < 150:
        if pos[1] < 150:
            return (0, 0)
        elif pos[1] > 150 and pos[1] < 300:
            return (1, 0)
        elif pos[1] > 300 and pos[1] < 450:
            return (2, 0)
    elif pos[0] > 150 and pos[0] < 300:
        if pos[1] < 150:
            return (0, 1)
        elif pos[1] > 150 and pos[1] < 300:
            return (1, 1)
        elif pos[1] > 300 and pos[1] < 450:
            return (2, 1)
    elif pos[0] > 300 and pos[0] < 450:
        if pos[1] < 150:
            return (0, 2)
        elif pos[1] > 150 and pos[1] < 300:
            return (1, 2)
        elif pos[1] > 300 and pos[1] < 450:
            return (2, 2)


# Draw X in tile
def draw_x(pos):
    tile = find_tile(pos)
    # print(f"Tile: {tile}")
    if game_board[tile[0]][tile[1]] is None:
        game_board[tile[0]][tile[1]] = 0
        tile_x = TILE_POS[tile[0]][tile[1]][0]
        tile_y = TILE_POS[tile[0]][tile[1]][1]
        pygame.draw.line(game_display, white, (tile_x - 60,
                                               tile_y - 60), (tile_x + 60, tile_y + 60), 3)
        pygame.draw.line(game_display, white, (tile_x - 60,
                                               tile_y + 60), (tile_x + 60, tile_y - 60), 3)
        return True
    return False


# Draw O in tile
def draw_o(pos):
    tile = find_tile(pos)
    # print(f"Tile: {tile}")
    if game_board[tile[0]][tile[1]] is None:
        game_board[tile[0]][tile[1]] = 1
        tile = TILE_POS[tile[0]][tile[1]]
        pygame.draw.circle(game_display, white, tile, 60)
        return True
    return False


# Check rows of board for win
def check_rows(board=game_board):
    for row in board:
        if None in row:
            continue
        if (len(set(row)) == 1):
            return True
    return False


# Check columns of board for win
def check_columns():
    # Transpose game board
    columns = [[None, None, None], [None, None, None], [None, None, None]]
    for i in range(3):
        for j in range(3):
            columns[i][j] = game_board[j][i]
    return check_rows(columns)  # Check rows of transposed game board


# Ugly PEP8 E501
def check_diagonals():
    return ((game_board[0][0] is not None and game_board[1][1] is not None and game_board[2][2] is not None) and (game_board[0][0] == game_board[1][1] == game_board[2][2])) or ((game_board[2][0] is not None and game_board[1][1] is not None and game_board[0][2] is not None) and (game_board[2][0] == game_board[1][1] == game_board[0][2]))


# Check if there is a win
def check_win():
    return check_rows() or check_columns() or check_diagonals()


def check_draw():
    for row in game_board:
        if None in row:
            return False
    return True


# Game loop
player = 0
crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if player == 0:
                # Prevent tile overriding
                tile_drawn = draw_x(pygame.mouse.get_pos())
                # print(f"Drawn: {tile_drawn}")
                # print(game_board)
                if tile_drawn:
                    if check_win():
                        print(f"Player {player} wins!")
                        crashed = True
                    elif check_draw():
                        print("Tie! Nobody wins!")
                        crashed = True
                    player = 1  # Next turn
            else:
                # Prevent tile overriding
                tile_drawn = draw_o(pygame.mouse.get_pos())
                # print(f"Drawn: {tile_drawn}")
                # print(game_board)
                if tile_drawn:
                    if check_win():
                        print(f"Player {player} wins!")
                        crashed = True
                    elif check_draw():
                        print("Tie! Nobody wins!")
                        crashed = True
                    player = 0  # Next turn

    pygame.display.update()

pygame.quit()
quit()
