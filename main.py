import arcade, os
from board import Board
from piece import Piece
from config import WIN_WIDHT, WIN_HEIGHT, SQUARE_SIZE
import arcade.gui
from ui import Ui


class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, center_window=True)
        self.board = Board()
        self.selected_piece = None
        self.player_turn = 0
        self.mouse_pos = (0, 0)
        arcade.set_background_color(arcade.color.AMAZON)
        self.ui = Ui()
        self.is_killing = False


    def turn_controller(self):
        self.player_turn = "R" if self.player_turn == "W" else "W"
        print("current turn: ", self.player_turn)
        self.ui.update_turn(self.player_turn)


    def setup(self):
        os.system("clear" if os.name != "nt" else "cls")
        self.board.create_board()
        self.player_turn = 0
        self.turn_controller()


    def on_draw(self):
        self.clear()

        self.ui.on_draw()

        self.board.draw_squares()
        self.board.pieces.draw()

        # show crowns and changing scale
        for piece in self.board.pieces:
            if piece.letra == self.player_turn:
                piece.change_scale(self.mouse_pos)

            if piece.is_king:
                piece.show_crown()

        # show how piece is selected
        if self.selected_piece and self.selected_piece.letra == self.player_turn:
            # draw outline in selected piece
            arcade.draw_circle_outline(self.selected_piece.center_x, self.selected_piece.center_y,
                                      self.selected_piece.radius*1.1, arcade.color.GOLD, border_width=3)
            self.board.draw_guides(self.selected_piece)



    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = x, y


    def on_mouse_release(self, x, y, button, modifiers):

        if x > WIN_HEIGHT:
            return

        # if self.board.game_over:
        #     self.setup()


        row, col = int(y/SQUARE_SIZE),  int(x/SQUARE_SIZE)
        get_piece = self.board.get_piece(row, col)

        print(get_piece, row, col)
        print("current turn:", self.player_turn)

        if not self.selected_piece and get_piece == 0:
            return


        if not self.selected_piece:
            # pode selectionar um piece
            if isinstance(get_piece, Piece):
                self.selected_piece = get_piece


        elif self.selected_piece.letra == self.player_turn and (row, col) in self.board.get_piece_valid_moves(self.selected_piece)[0]: # updade to in valid position!!
            # se tiver selecionado e clicar em posicao VALIDA, pode mover
            jump_is_kill_jump = self.board.get_piece_valid_moves(self.selected_piece)[1]
            self.board.move_piece(self.selected_piece, row, col)
            has_kill_moves = self.board.get_piece_valid_moves(self.selected_piece)[1]
            self.is_killing = True if jump_is_kill_jump and has_kill_moves else False

            if not jump_is_kill_jump or not has_kill_moves:
                # logica dos pulos consecutivos
                self.selected_piece = None
                self.turn_controller()
                self.is_killing = False


        elif isinstance(get_piece, Piece) and get_piece.letra == self.player_turn:
            # se tiver selecionado e tiver clicado em posicao com outra piece do mesmo time, troca a selected_piece
            if not self.is_killing: # nao pode trocar de piece se estiver em matança
                self.selected_piece = get_piece
                print("change piece to :", get_piece, row, col)

        else:
            self.selected_piece = None


        # print(self.is_killing)



def main():
    game = Game(WIN_WIDHT, WIN_HEIGHT, "checkersPy")
    game.setup()
    game.run()
    

if __name__ == "__main__":
    main()
