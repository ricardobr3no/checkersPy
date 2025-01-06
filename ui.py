import arcade.gui


class Ui(arcade.View):
    def __init__(self):
        super().__init__()

        self.ui_manager = arcade.gui.UIManager(auto_enable=True)

        # indicative turn
        self.p1 = arcade.gui.UILabel(text="P1", text_color=arcade.color.WHITE, font_size=30, bold=True)
        self.p2 = arcade.gui.UILabel(text="P2", text_color=arcade.color.RED, font_size=30, bold=True)
        h_box = arcade.gui.UIBoxLayout(x=450, y=400, vertical=False)
        h_box.add(self.p1)
        h_box.add(self.p2)
        h_box._space_between = 30

        # buttons
        start_button = arcade.gui.UIFlatButton(width=100, height=40, text="START")
        exit_button = arcade.gui.UIFlatButton(width=100, height=40, text="EXIT")

        v_box = arcade.gui.UIBoxLayout( x=450, y=200,)
        v_box.add(h_box)
        v_box.add(start_button)
        v_box.add(exit_button)
        v_box._space_between = 20

        self.ui_manager.add(v_box)
        
        @start_button.event("on_click")
        def start_button_click(event):
            self.window.setup()

        @exit_button.event("on_click")
        def exit_button_click(event):
            self.window.close()

    
    def update_turn(self, turn: str):
        return 
        if turn == "W":
            self.p1.label.font_size = 35
            self.p2.label.font_size = 30
        if turn == "R":
            self.p1.label.font_size = 30
            self.p2.label.font_size = 35

        print(turn)


    def on_draw(self):
        arcade.start_render()
        self.ui_manager.draw()



