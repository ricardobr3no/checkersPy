import arcade, os, time
import arcade.gui

from .board import Board
from .piece import Piece
from .config import WIN_WIDHT, WIN_HEIGHT, SQUARE_SIZE

from random import choice


class Game(arcade.View):

    def __init__(self, mode: int = 1):
        super().__init__()
        
        self.mode = mode

        self.board = Board()
        self.selected_piece = None
        self.player_turn = 0
        self.mouse_pos = (0, 0)
        self.is_killing = False

        arcade.set_background_color(arcade.color.AMAZON)
        self.ui_init() # iniciar ui
        self.setup()


    def ui_init(self):
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # label winner
        self.label_winner = arcade.Text(text="P1 WIN", start_x=100, start_y=200,
                                        font_size=40, bold=True, font_name="comic sans MS")

        # indicative turn
        label_px, label_py = 480, 250
        self.p1 = arcade.Text(text="P1", start_x=label_px, start_y=label_py,
                              color=arcade.color.WHITE, font_size=30, bold=True)
        self.p2 = arcade.Text(text="P2", start_x=label_px, start_y=label_py,
                              color=arcade.color.RED, font_size=30, bold=True)

        # buttons
        start_button = arcade.gui.UIFlatButton(width=100, height=40, text="START")
        exit_button = arcade.gui.UIFlatButton(width=100, height=40, text="MENU")

        v_box = arcade.gui.UIBoxLayout( x=450, y=200,)
        # v_box.add(h_box)
        v_box.add(start_button)
        v_box.add(exit_button)
        v_box._space_between = 20

        self.ui_manager.add(v_box)
        
        @start_button.event("on_click")
        def start_button_click(event):
            # restart
            game = Game(mode=1 if self.mode == 1 else 2)
            self.window.show_view(game)

        @exit_button.event("on_click")
        def exit_button_click(event):
            # exit or Menu
            menu = Menu()
            self.window.show_view(menu)


    def ui_update_turn(self):
        is_game_over, ganhador = self.board.check_game_over()
        if is_game_over:
            if ganhador == "W":
                self.label_winner.text = "P1 WIN !!"
            elif ganhador == "R":
                self.label_winner.text = "P2 WIN !!"
            self.label_winner.draw()

        if self.player_turn == "W":
            self.p1.draw()
        elif self.player_turn == "R":
            self.p2.draw()


    def turn_controller(self):
        self.player_turn = "R" if self.player_turn == "W" else "W"
        print("current turn: ", self.player_turn)
        # self.ui_update_turn()


    def setup(self):
        os.system("clear" if os.name != "nt" else "cls")
        self.board.create_board()
        self.player_turn = 0
        self.turn_controller()


    def on_draw(self):
        self.clear()

        # draws board and pieces
        self.board.draw_squares()
        self.board.pieces.draw()

        # show crowns and changing scale
        for piece in self.board.pieces:
            if self.mode == 1:
                if piece.letra == self.player_turn:
                    piece.change_scale(self.mouse_pos)
            else:
                if piece.letra == "W":
                    piece.change_scale(self.mouse_pos)

            if piece.is_king:
                piece.show_crown()

        # show how piece is selected
        if self.selected_piece and self.selected_piece.letra == self.player_turn:
            # draw outline in selected piece
            arcade.draw_circle_outline(self.selected_piece.center_x, self.selected_piece.center_y,
                                      self.selected_piece.radius*1.1, arcade.color.GOLD, border_width=3)
            self.board.draw_guides(self.selected_piece)

        # draw ui
        self.ui_manager.draw()
        self.ui_update_turn()


    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = x, y


    def ia_move(self):
        ia_team = [p for p in self.board.pieces if p.letra == self.player_turn]
        ia_valid_moves = []

        if not ia_team:
            return

        if self.mode == 2 and self.player_turn == "R":

            for piece in ia_team:
                ia_moves, ia_has_kill_move = self.board.get_piece_valid_moves(piece)
                if ia_moves:
                    ia_valid_moves.append({"piece": piece, "moves": ia_moves})

            choiced = choice(ia_valid_moves)
            choiced_piece = choiced["piece"]
            choiced_move_row, choiced_move_col = choice(choiced["moves"])

            # print(choiced_piece, choiced_move_row, choiced_move_col)
            jump_is_kill_jump = self.board.diags(choiced_piece)[1]
            self.board.move_piece(choiced_piece, choiced_move_row, choiced_move_col)
            has_kill_moves = self.board.diags(choiced_piece)[1]

            if jump_is_kill_jump:
                while has_kill_moves: # vai entrar como True ou False
                    print("entrou")
                    moves, has_kill_moves = self.board.diags(choiced_piece)
                    row, col = choice(moves)
                    self.board.move_piece(choiced_piece, row, col)
                    moves, has_kill_moves = self.board.diags(choiced_piece)

                    if not has_kill_moves:
                        break

            self.turn_controller()


    def on_mouse_release(self, x, y, button, modifiers):
        if x > WIN_HEIGHT or y > WIN_HEIGHT:
            return

        # human logic
        row, col = int(y/SQUARE_SIZE),  int(x/SQUARE_SIZE)
        get_piece = self.board.get_piece(row, col)

        print(get_piece, row, col)
        print("current turn:", self.player_turn)

        if not self.selected_piece:
            # pode selectionar um piece
            if isinstance(get_piece, Piece):
                self.selected_piece = get_piece

        elif self.selected_piece.letra == self.player_turn and (row, col) in self.board.get_piece_valid_moves(self.selected_piece)[0]: 
            # se tiver selecionado e clicar em posicao VALIDA, pode mover
            jump_is_kill_jump = self.board.diags(self.selected_piece)[1]
            self.board.move_piece(self.selected_piece, row, col)
            has_kill_moves = self.board.diags(self.selected_piece)[1]
            self.is_killing = True if jump_is_kill_jump and has_kill_moves else False

            if not jump_is_kill_jump or not has_kill_moves and not self.is_killing:
                # logica dos pulos consecutivos
                self.selected_piece = None
                self.turn_controller()
                self.is_killing = False
                # ia here
                self.ia_move()
            print(self.is_killing)

        elif isinstance(get_piece, Piece) and get_piece.letra == self.player_turn:
            # se tiver selecionado e tiver clicado em posicao com outra piece do mesmo time, troca a selected_piece
            if not self.is_killing: # nao pode trocar de piece se estiver em matança
                self.selected_piece = get_piece
                print("change piece to :", get_piece, row, col)

        else:
            self.selected_piece = None


class Menu(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AMAZON)
        
        self.ui = arcade.gui.UIManager()
        self.ui.enable()
        # buttons
        b_mode_1 = arcade.gui.UIFlatButton(width=200, text="P1 vs P2")
        b_mode_2 = arcade.gui.UIFlatButton(width=200, text="P1 vs COMP")
        b_exit = arcade.gui.UIFlatButton(width=200, text="EXIT")

        # layout
        v_box = arcade.gui.UIBoxLayout(align="center")
        v_box.add(b_mode_1)
        v_box.add(b_mode_2)
        v_box.add(b_exit)
        v_box._space_between = 20
        anchor = arcade.gui.UIAnchorWidget(anchor_x="center", anchor_y="center", child=v_box)
        self.ui.add(anchor)

        @b_mode_1.event("on_click")
        def on_click_b1(event):
            game_view = Game(mode=1)
            self.ui.disable()
            self.window.show_view(game_view)
            
        @b_mode_2.event("on_click")
        def on_click_b2(event):
            game_view = Game(mode=2)
            self.ui.disable()
            self.window.show_view(game_view)

        @b_exit.event("on_click")
        def on_click_exit(event):
            self.window.close()
        

    def on_draw(self):
        self.clear()
        self.ui.draw()

