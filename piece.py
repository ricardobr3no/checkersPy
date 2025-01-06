import arcade
from config import SQUARE_SIZE

class Piece(arcade.SpriteCircle):
    def __init__(self, color: arcade.Color, row_col: tuple):
        super().__init__(color=color, radius=int(0.9 * SQUARE_SIZE //2))
        self.row, self.col = row_col
        self.color = color
        self.position = self.col * SQUARE_SIZE + SQUARE_SIZE//2, self.row * SQUARE_SIZE + SQUARE_SIZE//2
        self.letra = "W" if self.row < 3 else "R"
        self.is_king = False
        self.radius = int(0.9 * SQUARE_SIZE // 2)
        self.crown = arcade.SpriteSolidColor(int(SQUARE_SIZE/2), int(SQUARE_SIZE/2), arcade.color.GOLD)
        self.directions_y = [1] if self.letra == "W" else [-1]

    def move(self, row, col):
        self.row, self.col = row, col
        self.position = self.col * SQUARE_SIZE + SQUARE_SIZE//2, self.row * SQUARE_SIZE + SQUARE_SIZE//2

        if self.row in [0, 7]:
            self.is_king = True
            self.directions_y = [-1, 1]


    def show_crown(self):
        self.crown.position = self.position
        self.crown.draw()


    def change_scale(self, mouse_pos: tuple):
        self.scale = 1.1 if self.collides_with_point(mouse_pos) else 1


    def __repr__(self):
        return self.letra

