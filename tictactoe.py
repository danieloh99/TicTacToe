#!/usr/bin/env python3

class Player:
    def __init__(self, game_world, id):
        """Player is initialized w/ its ID (X or O) and the game it is in."""
        self.id = id
        self.game_world = game_world

    def move(self):
        """Announce player's turn and get a move. Repeat until valid move
        is received.
        """
        while True:
            print("Player %s's Turn." %self.id)
            move = self.get_move()
            if move != -1:
                return move


    def get_move(self):
        """Ask for a move from player. Returns -1 on invalid move."""
        try:
            spot = int(input("Where would you like to move [0-8]?: "))
        except ValueError:
            print("Error. Invalid move.\n")
            return -1

        if spot<0 or spot>8:
            print("Error. Invalid move.\n")
            return -1
        elif self.game_world.board[spot] != '_':
            print("Error. Spot is taken.\n")
            return -1
        return spot

class AI(Player):
    """Derived class from Player. Used when user wants to play
    against Computer.
    """

    def __init__(self, game_world, id):
        """AI Constructor. Keeps track of its own board for future computation
        and the opponent's ID.
        """
        Player.__init__(self, game_world, id)
        self.opponent = 'X' if id == 'O' else 'O'
        self.board = self.game_world.board

    def minimax(self, board, depth, ai_turn):
        """Algorithm to determine a move's value by recursively going through
        all possible future board setups based on the current board.

        Returns +1 if move leads to AI's victory, -1 if leads to Human's,
        0 if tie.

        Assumes player will play optimally.
        """
        # First checks current state of the board. If the opponent won,
        # return -1. If the AI won, return +1. If the board is tied, return 0.
        if self.game_world.check_win(board) == self.opponent:
            return -1
        if self.game_world.check_win(board) is not 'None':
            return 1
        if self.game_world.board_is_full(board):
            return 0

        if ai_turn:  # Maximizer: AI wants to choose the best move for itself.
            best_score = -2
            for index in range(9):
                if self.board[index] != '_':
                    continue
                board[index] = self.id
                best_score = max(best_score,
                                self.minimax(board, depth + 1, False))
                board[index] = '_'
            return best_score
        else:  # Minimizer: AI computes which move is best for human to make.
            best_score = 2
            for index in range(9):
                if board[index] != '_':
                    continue
                board[index] = 'X' if self.id == 'O' else 'O'
                best_score = min(best_score,
                                self.minimax(board, depth + 1, True))
                board[index] = '_'
            return best_score

    def get_move_helper(self, board):
        """Determine the best move for the AI to make, given a board.
        Calls minimax algorithm on each possible move to determine the best move
        currently possible, and returns that move.
        """

        best_move = None  # the index for where the move should be made
        best_value = -1  # used to check if a move is better

        # Loop over all indices in the board, skipping the full spots.
        for index in range(9):
            if board[index] != '_':
                continue

            # At each spot in the board, fill it w/ the AI's move, and see if
            # the move is better than the current best move, by comparing the
            # return value of the minimax function with the current best_value
            board[index] = self.id
            move_value = self.minimax(board, 0, False)
            board[index] = '_'

            # Keep track of the best move, and return it at the end.
            if move_value > best_value:
                best_move = index
                best_value = move_value
        return best_move

    def get_move(self):
        return self.get_move_helper(self.board)


class Game:
    win_conditions = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6))

    def __init__(self):
        self.board = ['_', '_', '_', '_', '_', '_', '_', '_', '_']
        self.moves_count = 0
        self.playerX = Player(self, 'X')
        self.playerO = None
        self.turn = 'X'

    def print_board(self):
        print("")
        for row in [0, 3, 6]:
            print(self.board[row], self.board[row + 1], self.board[row + 2])
        print("")

    def update_board(self, turn, location):
        self.board[location] = self.turn
        self.turn = 'O' if self.turn == 'X' else 'X'

    def get_move_and_update_board(self):
        location = self.playerX.move() \
                    if self.turn == 'X' else self.playerO.move()
        self.update_board(self.turn, location)
        self.moves_count += 1

    def check_win(self, board):
        for win_order in self.win_conditions:
            if board[win_order[0]] == board[win_order[1]] \
                    == board[win_order[2]] == 'X':
                return 'X'
            elif board[win_order[0]] == board[win_order[1]] \
                    == board[win_order[2]] == 'O':
                return 'O'
        return 'None'

    def board_is_full(self, board):
        """Goes through board checking if it is full."""
        for index in range(9):
            if board[index] == '_':
                    return False
        return True

    def welcome(self):
        print("Welcome to Tic-Tac-Toe!")
        while True:
            type_of_opponent = input("Would you like to play against another "
                                     "player or a computer? [p or c]: ")
            if type_of_opponent == 'p':
                self.playerO = Player(self, 'O')
                return
            elif type_of_opponent == 'c':
                self.playerO = AI(self, 'O')
                return
            else:
                print("Error. Invalid input.\n")

    def game_over(self, who_won):
        self.print_board()
        if who_won == 'X':
            print("Player X won! Thanks for playing!")
        elif who_won == 'O':
            print("Player O won! Thanks for playing!")
        else:
            print("It was a tie! Thanks for playing!")

    def play(self):
        self.welcome()

        gameOver = False
        while not gameOver:
            self.print_board()
            self.get_move_and_update_board()
            who_won = self.check_win(self.board)
            if who_won is not 'None' or self.moves_count==9:
                gameOver = True

        self.game_over(who_won)


obj = Game()
obj.play()
input("Press ENTER to close...")
