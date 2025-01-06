import arcade
from config import ROWS, COLS, SQUARE_SIZE, WIN_HEIGHT
from piece import Piece
# from rich import print


class Board:

    def __init__(self):
        self.board = []
        self.pieces = arcade.SpriteList()
        self.game_over = False

    def setup(self):
        self.create_board()
        self.player_turn = 0
        self.turn_controller()


    def mostrar_board(self):
        for row in self.board:
            print(row)

    def create_board(self):
        self.board.clear() # restart board
        self.pieces.clear()
         
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
			    # se tiver nas primeiras rows, colocar as peças brancas
                if row < 3 and col%2 == (row+1) % 2:
                    self.board[row].append(1)
			    # se tiver nas primeiras rows, colocar as peças vermelhas
                elif row > 4 and col%2 == (row+1) % 2:
                    self.board[row].append(2)
			    # nas demais, colocar ZERO simplesmente
                else:
                    self.board[row].append(0)

        # colocar as pieces nas posicoes de inicio
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != 0:
                    color_piece = arcade.color.WHITE if self.board[row][col] == 1 else arcade.color.RED
                    new_piece = Piece(color=color_piece, row_col=(row,col))
                    new_piece.row, new_piece.col = row, col # start row col
                    # new_piece.turn = 1 if row < 3 else 2 # start turn
                    self.board[row][col] = new_piece
                    self.pieces.append(new_piece)

        self.mostrar_board()
			    
        
    def draw_squares(self):
        # draw background
        arcade.draw_rectangle_filled(WIN_HEIGHT//2, WIN_HEIGHT//2, WIN_HEIGHT, WIN_HEIGHT, arcade.color.BLACK)

        # draw squares
        for row in range(ROWS):
            for col in range(row % 2, COLS, +2):
                arcade.draw_rectangle_filled(row * SQUARE_SIZE + SQUARE_SIZE / 2,
                                             col * SQUARE_SIZE + SQUARE_SIZE / 2,
                                             SQUARE_SIZE, SQUARE_SIZE,
                                             arcade.color.BROWN)


    def get_piece(self, row:int, col:int):
        return self.board[row][col]


    def move_piece(self, piece: Piece, row: int, col: int):
        moves, has_kill_move = self.get_piece_valid_moves(piece)
         
        if (row, col) in moves:
            if abs(row - piece.row) > 1:
                media: int = lambda a, b: (a + b) // 2
                obstaculo = self.board[media(piece.row, row)][media(piece.col, col)]
                obstaculo.kill() # remover sprite do meio
                self.board[media(piece.row, row)][media(piece.col, col)] = 0

            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
            piece.move(row, col)
            # self.mostrar_board()
        self.check_game_over()


    def get_piece_valid_moves(self, piece: Piece) -> list:
        dir_y = 1 if piece.letra == "W" else -1
        moves, has_kill_move = self.diags(piece)
        return moves, has_kill_move


    def diags(self, piece: Piece) -> tuple:
        """dir_x e dir_y recebem -1 para left/down or +1 para right/up"""
        simple_moves = []
        kill_moves = []
        has_kill_move = False
        next_pos = next_2_pos = 0

        for dir_y in piece.directions_y:
            for dir_x in [-1, 1]:
                can_check_simple_move = (0 <= piece.row + dir_y <= 7) and (0 <= piece.col + dir_x <=7)
                can_check_kill_move = (0 <= piece.row + 2*dir_y <= 7) and (0 <= piece.col + 2*dir_x <=7) 

                if can_check_simple_move:
                    next_pos = self.board[piece.row + dir_y][piece.col + dir_x]
                    # check for simple moves
                    if next_pos == 0 and not has_kill_move:
                        simple_moves.append((piece.row+dir_y, piece.col+dir_x))

                if can_check_kill_move:
                    next_2_pos = self.board[piece.row + 2*dir_y][piece.col + 2*dir_x]
                    # check for kill moves
                    if isinstance(next_pos, Piece) and next_pos.letra != piece.letra and next_2_pos == 0:
                        has_kill_move = True
                        kill_moves.append((piece.row+2*dir_y, piece.col+2*dir_x))

        return (kill_moves, has_kill_move) if kill_moves else (simple_moves, has_kill_move)


    def draw_guides(self, piece: Piece):
        for (row, col) in self.get_piece_valid_moves(piece)[0]:
            arcade.draw_circle_filled(col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2,
                                      piece.radius//2, arcade.color.BLUE)


    def check_game_over(self):
        white_pieces = [p for p in self.pieces if p.letra == "W"]
        red_pieces = [p for p in self.pieces if p.letra == "R"]
    
        if not white_pieces or not red_pieces:
            print("GAME_OVER")
            self.game_over = True
            return True
        return False
