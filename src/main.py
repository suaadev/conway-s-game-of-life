from game_egine import GameEngine
from main_window import MainWindow


def main():
    game_engine = GameEngine()
    main_window = MainWindow(1000, 1000, game_engine)
    main_window.run()


if __name__ == "__main__":
    main()
