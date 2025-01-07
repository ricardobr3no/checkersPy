import arcade, os
import arcade.gui

from .board import Board
from .piece import Piece
from .config import WIN_WIDHT, WIN_HEIGHT, SQUARE_SIZE


class Game(arcade.View):

    def __init__(self):
        super().__init__()
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

        # indicative turn
        self.p1 = arcade.gui.UILabel(text="P1", text_color=arcade.color.WHITE, font_size=30, bold=True)
        self.p2 = arcade.gui.UILabel(text="P2", text_color=arcade.color.RED, font_size=30, bold=True)
        h_box = arcade.gui.UIBoxLayout(x=450, y=400, vertical=False)
        h_box.add(self.p1)
        h_box.add(self.p2)
        h_box._space_between = 30

        # buttons
        start_button = arcade.gui.UIFlatButton(width=100, height=40, text="START")
        exit_button = arcade.gui.UIFlatButton(width=100, height=40, text="MENU")

        v_box = arcade.gui.UIBoxLayout( x=450, y=200,)
        v_box.add(h_box)
        v_box.add(start_button)
        v_box.add(exit_button)
        v_box._space_between = 20

        self.ui_manager.add(v_box)
        
        @start_button.event("on_click")
        def start_button_click(event):
            # restart
            game = Game()
            self.window.show_view(game)

        @exit_button.event("on_click")
        def exit_button_click(event):
            # exit or Menu
            menu = Menu()
            self.window.show_view(menu)


    def ui_update_turn(self):
        # update in future, not working for now
        return
        if self.player_turn == "W":
            self.p1.label.font_size = 35
            self.p2.label.font_size = 30
        elif self.player_turn == "R":
            self.p1.label.font_size = 30
            self.p2.label.font_size = 35
         

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

        self.ui_manager.draw()
        self.ui_update_turn()

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
            game_view = Game()
            self.ui.disable()
            self.window.show_view(game_view)
            
        @b_mode_2.event("on_click")
        def on_click_b2(event):
            print("oi")

        @b_exit.event("on_click")
        def on_click_exit(event):
            self.window.close()
        

    def on_draw(self):
        self.clear()
        self.ui.draw()

