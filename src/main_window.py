from sys import exit

import pygame

from game_egine import GameEngine
from simulation import Simulation


class MainWindow:
    FPS_RATE = 60
    MAX_WINDOW_MS_TO_SIMULATE = 200
    MIN_WINDOW_MS_TO_SIMULATE = 10

    def __init__(self, width: int, heigth: int, game_engine: GameEngine):

        self.heigth = heigth
        self.width = width
        pygame.init()
        pygame.display.set_caption("Conway's Game of Life")
        self.display = pygame.display.set_mode(
            (self.width, self.heigth), pygame.RESIZABLE
        )
        self.game_engine = game_engine
        self.clock = pygame.time.Clock()
        self.simulation = Simulation(self.game_engine, self.display)

        self.generation_font: pygame.font.SysFont = pygame.font.SysFont("arial", 15)

    def run(self):

        last_time = pygame.time.get_ticks()
        current_window_to_simulate = 30

        while True:
            events = pygame.event.get()
            mouse_position = pygame.mouse.get_pos()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.VIDEORESIZE:
                    size = pygame.display.get_window_size()

                    self.simulation.resize(size[0], size[1])

                if self.simulation.simulation and event.type == pygame.MOUSEBUTTONUP:
                    self.simulation.release_cells_memory()

                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_s]:
                        if not self.simulation.simulation:
                            self.simulation.start()
                        else:
                            self.simulation.stop()

                    if keys[pygame.K_c]:
                        self.simulation.clear()

                    if keys[pygame.K_b]:
                        self.simulation.switch_cell_border()

                    if (
                        keys[pygame.K_m]
                        and current_window_to_simulate < self.MAX_WINDOW_MS_TO_SIMULATE
                    ):
                        current_window_to_simulate += 10

                    if (
                        keys[pygame.K_n]
                        and current_window_to_simulate > self.MIN_WINDOW_MS_TO_SIMULATE
                    ):
                        current_window_to_simulate -= 10

            mouse_pressed = pygame.mouse.get_pressed()

            if mouse_pressed[0]:
                mouse_position = pygame.mouse.get_pos()
                self.simulation.set_cell_status(
                    mouse_position[0], mouse_position[1], True
                )
            elif mouse_pressed[2]:
                mouse_position = pygame.mouse.get_pos()
                self.simulation.set_cell_status(
                    mouse_position[0], mouse_position[1], False
                )

            current_time = pygame.time.get_ticks()

            if (
                self.simulation.simulation
                and current_time - last_time >= current_window_to_simulate
            ):
                self.simulation.next_generation()
                last_time = current_time

            self.display.blit(self.simulation.surface, self.simulation.surface_rect)

            pygame.display.update()
            self.clock.tick(self.FPS_RATE)
