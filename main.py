import arcade
from checkers.config import WIN_WIDHT, WIN_HEIGHT, WIN_TITLE
from checkers.screens import Menu


def main():
    janela = arcade.Window(WIN_WIDHT, WIN_HEIGHT, WIN_TITLE, center_window=True)
    menu_view = Menu()
    janela.show_view(menu_view)
    janela.run()

if __name__ == "__main__":
    main()
