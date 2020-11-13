import pygame


class player(object):
    def __init__(self, window, board, id):
        self.id = id
        self.window = window
        self.board = board

    def move(self, board, pos):
        self.board = board
        tile_pos = self.find_tile(pos)
        print(tile_pos)
        self.board, status = tile(self.window, self.board, self.id,
                                  tile_pos[0], tile_pos[1]).display()
        return self.board, status

    # Find tile from mouse position
    def find_tile(self, pos):
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


class computer(object):
    def __init__(self, window, id):
        self.window = window
        self.id = id

    def move(self, board):
        bestScore = -100
        bestMove = None
        for i, row in enumerate(board):
            for j, column in enumerate(row):
                if column is None:
                    board[i][j] = self.id
                    score = self.minimax(board, 0, False)
                    board[i][j] = None
                    if score > bestScore:
                        bestScore = score
                        bestMove = [i, j]

        print(f"Best Move: {bestMove}")
        retBoard, status = tile(self.window, board, self.id,
                                bestMove[0], bestMove[1]).display()
        return retBoard

    def minimax(self, board, depth, isMaximizer):
        scores = {user.id: -1,
                  self.id: 1,
                  'draw': 0}
        result = check_win(board)
        if result is not None:
            # print(f"Result: {result}")
            return scores[result]

        if isMaximizer:
            bestScore = -100
            for i, row in enumerate(board):
                for j, column in enumerate(row):
                    if column is None:
                        board[i][j] = self.id
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = None
                        bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = 100
            for i, row in enumerate(board):
                for j, column in enumerate(row):
                    if column is None:
                        board[i][j] = next_turn[self.id]
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = None
                        bestScore = min(score, bestScore)
            return bestScore


class tile(object):
    def __init__(self, window, board, id, row, column):
        self.window = window
        self.board = board
        self.id = id
        self.TILE_POS = [[(75, 75), (225, 75), (375, 75)], [(75, 225), (225, 225),
                                                            (375, 225)], [(75, 375), (225, 375), (375, 375)]]
        self.row = row
        self.column = column
        self.x = self.TILE_POS[row][column][0]
        self.y = self.TILE_POS[row][column][1]

    def display(self):
        if self.board[self.row][self.column] is None:
            if self.id == 0:
                self.board[self.row][self.column] = 0
                self.draw_x()
                pygame.display.update()
                return self.board, True
            else:
                self.board[self.row][self.column] = 1
                self.draw_o()
                pygame.display.update()
                return self.board, True
        else:
            return self.board, False

    # Draw X in tile
    def draw_x(self):
        pygame.draw.line(self.window, (255, 255, 255), (self.x - 60,
                                                        self.y - 60), (self.x + 60, self.y + 60), 3)
        pygame.draw.line(self.window, (255, 255, 255), (self.x - 60,
                                                        self.y + 60), (self.x + 60, self.y - 60), 3)

    # Draw O in tile
    def draw_o(self):
        pygame.draw.circle(self.window, (255, 255, 255),
                           (self.x, self.y), 60, 3)


# Check rows of board for win
def check_rows(board):
    for i, row in enumerate(board):
        if None in row:
            continue
        elif len(set(row)) == 1:
            return board[i][0]
    return None


# Check columns of board for win
def check_columns(board):
    # Transpose game board
    columns = [[None, None, None], [None, None, None], [None, None, None]]
    for i in range(len(board)):
        for j in range(len(board[0])):
            columns[i][j] = board[j][i]
    return check_rows(columns)  # Check rows of transposed game board


# Check diagonals of board for win
def check_diagonals(board):
    # Ugly PEP8 E501 / does not work without 'is not None'?
    diagonal_1 = [board[0][0], board[1][1], board[2][2]]
    diagonal_2 = [board[0][2], board[1][1], board[2][0]]
    # print(f"Diagonal 1: {diagonal_1}")
    # print(f"Diagonal 2: {diagonal_2}")
    if (None not in diagonal_1) and (len(set(diagonal_1)) == 1):
        return diagonal_1[0]
    elif (None not in diagonal_2) and (len(set(diagonal_2)) == 1):
        return diagonal_2[0]
    else:
        return None


# Check if board is displayed
def check_draw(board):
    for row in board:
        if None in row:
            return None
    return "draw"


# Check if there is a win
def check_win(board):
    if check_rows(board) is not None:
        return check_rows(board)
    elif check_columns(board) is not None:
        return check_columns(board)
    elif check_diagonals(board) is not None:
        return check_diagonals(board)
    elif check_draw(board) is not None:
        return check_draw(board)
    else:
        return None


def user_turn(board, pos):
    game_board, displayed = user.move(board, pos)
    if not displayed:
        print("Not a valid move")
    else:
        print(f"Player moved. Game board:\n{game_board}")
        if check_win(game_board) == "draw":
            print("Draw! Nobody wins!")
            pygame.quit()
            quit()
        elif check_win(game_board) is not None:
            print("Player wins!")
            pygame.quit()
            quit()
    return game_board, displayed


def com_turn(board):
    game_board = com.move(board)
    print(f"Computer moved. Game board:\n{game_board}")
    if check_win(game_board) == "draw":
        print("Draw! Nobody wins!")
        pygame.quit()
        quit()
    elif check_win(game_board) is not None:
        print("Computer wins!")
        pygame.quit()
        quit()


pygame.init()
screen = pygame.display.set_mode((450, 450))
pygame.display.set_caption('Tic Tac Toe')

game_board = [[None, None, None], [None, None, None], [None, None, None]]
white = (255, 255, 255)
black = (0, 0, 0)
screen.fill(black)
pygame.draw.line(screen, white, (150, 0), (150, 450), 3)
pygame.draw.line(screen, white, (300, 0), (300, 450), 3)
pygame.draw.line(screen, white, (0, 150), (450, 150), 3)
pygame.draw.line(screen, white, (0, 300), (450, 300), 3)
pygame.display.update()

next_turn = {0: 1,
             1: 0}

user = player(screen, game_board, 0)
com = computer(screen, 1)
turn = user.id
crashed = False
if com.id == 0:
    com_turn(game_board)
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.MOUSEBUTTONUP and turn == user.id:
            game_board, displayed = user_turn(
                game_board, pygame.mouse.get_pos())
            if displayed:
                turn = next_turn[user.id]
            if turn == com.id:
                com_turn(game_board)
                turn = next_turn[com.id]

pygame.quit()
quit()
