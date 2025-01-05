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

    def move(self, row, col):
        self.row, self.col = row, col
        self.position = self.col * SQUARE_SIZE + SQUARE_SIZE//2, self.row * SQUARE_SIZE + SQUARE_SIZE//2

        if self.row in [0, 7]:
            self.is_king = True


    def update(self, mouse_pos: tuple):
        if self.collides_with_point(mouse_pos):
            pass


    def __repr__(self):
        return self.letra

