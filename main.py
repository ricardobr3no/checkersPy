import arcade, os
from board import Board
from piece import Piece
from config import WIN_WIDHT, WIN_HEIGHT, SQUARE_SIZE


def in_matrix(e, matrix: [list, tuple]):
    """verifica se extiste algum elemento (e) na matrix"""
    for row in matrix:
        if row.count(e) > 0:
            return True
    return False


class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, center_window=True)
        self.board = Board()
        self.selected_piece = None
        self.player_turn = 0
        self.mouse_pos = (0, 0)


    def turn_controller(self):
        if self.player_turn == "W":
            self.player_turn = "R"
        else:
            self.player_turn = "W"

        print("current turn: ", self.player_turn)
        return self.player_turn


    def setup(self):
        os.system("clear" if os.name != "nt" else "cls")
        self.board.create_board()
        self.player_turn = 0
        self.turn_controller()


    def on_draw(self):
        self.clear()
        self.board.draw_squares()

        if self.selected_piece and self.selected_piece.letra == self.player_turn:
            # draw outline in selected piece
            arcade.draw_circle_filled(self.selected_piece.center_x, self.selected_piece.center_y,
                                      self.selected_piece.radius*1.1, arcade.color.GOLD)
            self.board.draw_guides(self.selected_piece)

        self.board.pieces.draw()


    def on_mouse_release(self, x, y, button, modifiers):
        row, col = int(y/SQUARE_SIZE),  int(x/SQUARE_SIZE)
        get_piece = self.board.get_piece(row, col)

        print(get_piece, row, col)
        print("current turn:", self.player_turn)

        if not self.selected_piece and get_piece == 0:
            return


        if not self.selected_piece:
            # pode selectionar um piece
            self.selected_piece = get_piece

        elif self.selected_piece.letra == self.player_turn and (row, col) in self.board.get_piece_valid_moves(self.selected_piece)[0]: # updade to in valid position!!
            # se tiver selecionado e clicar em posicao VALIDA, pode mover
            jump_is_kill_jump = self.board.get_piece_valid_moves(self.selected_piece)[1]
            self.board.move_piece(self.selected_piece, row, col)
            has_kill_moves = self.board.get_piece_valid_moves(self.selected_piece)[1]

            if not jump_is_kill_jump or not has_kill_moves:
                # se o primeiro pulo foi normal
                self.selected_piece = None
                self.turn_controller()


        elif isinstance(get_piece, Piece) and get_piece.letra == self.player_turn:
            # se tiver selecionado e tiver clicado em posicao com outra piece do mesmo time, troca a selected_piece
            self.selected_piece = get_piece
            print("change piece to :", get_piece, row, col)

        else:
            self.selected_piece = None



def main():
    game = Game(WIN_HEIGHT, WIN_HEIGHT, "checkersPy")
    game.setup()
    game.run()
    

if __name__ == "__main__":
    main()
