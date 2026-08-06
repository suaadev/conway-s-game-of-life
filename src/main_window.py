from sys import exit

import pygame

from board import Board
from game_egine import GameEngine


class MainWindow:
    def __init__(self, width: int, heigth: int, game_engine: GameEngine):
        self.FRAME_RATE = 60
        self.heigth = heigth
        self.width = width
        pygame.init()
        pygame.display.set_caption("jhon conway's game of life")
        self.display = pygame.display.set_mode(
            (self.width, self.heigth), pygame.RESIZABLE
        )
        self.game_engine = game_engine
        self.clock = pygame.time.Clock()
        self.board = Board(self.width, self.heigth, self.game_engine)

    def run(self):
        while True:
            events = pygame.event.get()
            mouse_position = pygame.mouse.get_pos()
            # print(mouse_position)
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()
                    print(f"resized: {size} ")
                    self.board.resize(size[0], size[1])

                if event.type == pygame.MOUSEBUTTONUP:
                    self.board.release_alive_cells_memory()

                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_s]:
                        if not self.board.simulation:
                            self.board.start_simulation()
                        else:
                            self.board.stop_simulation()

                    if keys[pygame.K_c]:
                        self.board.clear()

                    if keys[pygame.K_b]:
                        self.board.switch_cell_border()

            mouse_pressed = pygame.mouse.get_pressed()

            if mouse_pressed[0]:
                mouse_position = pygame.mouse.get_pos()
                self.board.set_cell_status(mouse_position[0], mouse_position[1], True)
            elif mouse_pressed[2]:
                mouse_position = pygame.mouse.get_pos()
                self.board.set_cell_status(mouse_position[0], mouse_position[1], False)

            if self.board.simulation:
                self.board.next_generation()

            self.display.blit(self.board, (0, 0))

            pygame.display.update()
            self.clock.tick(self.FRAME_RATE)
