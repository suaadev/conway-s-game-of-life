from math import ceil

import numpy as np
import pygame

from game_egine import GameEngine

## TODO: CORREGIR PROBLEMA DE TOLIDE EN SCANING LIMITS DEL GAME ENGIME, DEJAR EL LIMITE POR LIMITE GENERAL O POR VENTANA DE SCANING
## TODO: corregir inserncion de valores


class Simulation:
    BACKGROUND_COLOR = (85, 15, 15)
    CELL_ALIVE_COLOR = (198, 229, 245)
    CELL_DEAD_COLOR = (0, 0, 0)
    CELL_SIZE = 10

    def __init__(self, parent_surface: pygame.Surface):
        parent_surface_size = parent_surface.get_size()
        self.parent_surface = parent_surface
        self.surface = pygame.Surface(parent_surface_size)
        self.surface_width = parent_surface_size[0]
        self.surface_height = parent_surface_size[1]
        self.surface.fill(self.BACKGROUND_COLOR)
        self.surface_rect = self.surface.get_rect(topleft=(0, 0))
        self.cell_border = 0
        self.simulation = False
        self.build_simulation()

    def build_simulation(self):
        self.max_window_rows = ceil(self.surface_height / self.CELL_SIZE)
        self.max_window_columns = ceil(self.surface_width / self.CELL_SIZE)
        display_width, display_heignt = pygame.display.get_desktop_sizes()[0]

        max_rows_engine = ceil(display_heignt / self.CELL_SIZE)
        max_cols_engine = ceil(display_width / self.CELL_SIZE)

        self.game_engine = GameEngine(max_rows_engine, max_cols_engine)
        self.game_engine.scanning_limit(self.max_window_rows, self.max_window_columns)
        self.build_rects()

    def build_rects(self):
        cell_rects = []

        for py in range(0, self.surface_height, self.CELL_SIZE):
            column_cell_rects = []
            for px in range(0, self.surface_width, self.CELL_SIZE):
                rect = pygame.rect.Rect(px, py, self.CELL_SIZE, self.CELL_SIZE)

                i = py // self.CELL_SIZE
                j = px // self.CELL_SIZE

                value = self.game_engine.get_generation_value(i, j)

                if value == 1:
                    pygame.draw.rect(self.surface, self.CELL_ALIVE_COLOR, rect)
                else:
                    pygame.draw.rect(
                        self.surface, self.CELL_DEAD_COLOR, rect, self.cell_border
                    )

                column_cell_rects.append(rect)

            cell_rects.append(np.array(column_cell_rects))

        self.cell_rects = np.array(cell_rects)

    def update_rect(self, i, j, new_cell_value):
        if i >= self.max_window_rows or j >= self.max_window_columns or i < 0 or j < 0:
            return

        cell_rect = self.cell_rects[i][j]

        color = self.CELL_ALIVE_COLOR if new_cell_value == 1 else self.CELL_DEAD_COLOR

        border = 0 if new_cell_value == 1 else 1

        border *= self.cell_border

        if border == 1:
            pygame.draw.rect(self.surface, self.BACKGROUND_COLOR, cell_rect, 0)

        pygame.draw.rect(self.surface, color, cell_rect, border)

    def resize(self, width, heigth):
        self.surface_height = heigth
        self.surface_width = width
        self.surface = pygame.Surface((width, heigth))
        self.surface_rect = self.surface.get_rect(topleft=(0, 0))
        self.surface.fill(self.BACKGROUND_COLOR)
        self.max_window_rows = ceil(self.surface_height / self.CELL_SIZE)
        self.max_window_columns = ceil(self.surface_width / self.CELL_SIZE)
        self.game_engine.scanning_limit(self.max_window_rows, self.max_window_columns)
        self.build_rects()

    def switch_cell_border(self):
        self.cell_border = 0 if self.cell_border == 1 else 1
        ## Sole le coloque border a los rects que estan en la ventana
        for i in range(self.max_window_rows):
            for j in range(self.max_window_columns):
                cell_value = self.game_engine.get_generation_value(i, j)
                self.update_rect(i, j, cell_value)

    def set_cell_status(self, coord_x: int, coord_y: int, status: bool) -> tuple[int]:
        j = coord_x // self.CELL_SIZE  # columns
        i = coord_y // self.CELL_SIZE  # rows

        (new_cell_value, before_cell_value) = self.game_engine.set_value_cell(
            i,
            j,
            status,
            in_memo=self.simulation,
        )

        # Optimization  only render the cell that have change
        if before_cell_value != new_cell_value:
            self.update_rect(i, j, new_cell_value)

        return (i, j)

    def release_cells_memory(self):
        self.game_engine.release_cells_memory()

    def start(self):
        self.simulation = True

    def stop(self):
        self.simulation = False

    def clear(self):
        self.stop()
        self.game_engine.reset()
        for i in range(self.max_window_rows):
            for j in range(self.max_window_columns):
                self.update_rect(i, j, 0)

    def next_generation(self):
        self.game_engine.next_generation(
            lambda i, j, v: self.update_rect(
                i - self.game_engine.scaning_min_i,
                j - self.game_engine.scaning_min_j,
                v,
            )
        )
