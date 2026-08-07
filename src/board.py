from math import ceil

import numpy as np
import pygame


class Board:
    BACKGROUND_COLOR = (15, 15, 15)
    CELL_ALIVE_COLOR = (198, 229, 245)
    CELL_DEAD_COLOR = (0, 0, 0)
    CELL_SIZE = 10

    def __init__(self, game_engine, parent_surface: pygame.Surface):
        parent_surface_size = parent_surface.get_size()
        self.parent_surface = parent_surface
        self.surface = pygame.Surface(parent_surface_size)
        self.surface_width = parent_surface_size[0]
        self.surface_height = parent_surface_size[1]
        self.surface.fill(self.BACKGROUND_COLOR)
        self.surface_rect = self.surface.get_rect(topleft=(0, 0))

        self.cell_border = 0
        self.game_engine = game_engine
        self.simulation = False
        self.build()
        self.alive_cells = set()
        self.alive_cells_memory = set()

    def build(self):
        self.max_rows = ceil(self.surface_height / self.CELL_SIZE)
        self.max_columns = ceil(self.surface_width / self.CELL_SIZE)

        cell_rects: list[list[pygame.Rect]] = []

        for i in range(0, self.surface_height, self.CELL_SIZE):
            column_cell_rects = []
            for j in range(0, self.surface_width, self.CELL_SIZE):
                rect = pygame.rect.Rect(j, i, self.CELL_SIZE, self.CELL_SIZE)

                pygame.draw.rect(
                    self.surface, self.CELL_DEAD_COLOR, rect, self.cell_border
                )

                column_cell_rects.append(rect)
            cell_rects.append(column_cell_rects)

        self.generation = np.zeros((self.max_rows, self.max_columns))
        self.cell_rects = cell_rects
        return self.generation

    def resize(self, width, heigth):
        self.surface_height = heigth
        self.surface_width = width
        self.surface = pygame.Surface((width, heigth))
        self.surface.fill(self.BACKGROUND_COLOR)
        self.surface_rect = self.surface.get_rect(topleft=(0, 0))
        self.build()

    def switch_cell_border(self):
        self.cell_border = 0 if self.cell_border == 1 else 1
        for i in range(len(self.generation)):
            for j in range(len(self.generation[0])):
                cell_value = self.generation[i][j]
                self.update_rect(i, j, cell_value)

    def set_cell_status(self, coord_x: int, coord_y: int, status: bool) -> tuple[int]:
        j = coord_x // self.CELL_SIZE  # columns
        i = coord_y // self.CELL_SIZE  # rows
        before_cell_value = self.generation[i][j]
        new_cell_value = 1 if status else 0
        self.generation[i][j] = new_cell_value

        # Optimization  only render the cell that have change
        if before_cell_value != new_cell_value:
            self.update_rect(i, j, new_cell_value)

        if new_cell_value == 1:
            if self.simulation:
                self.alive_cells_memory.add((i, j))
            else:
                self.alive_cells.add((i, j))

        return (i, j)

    def release_alive_cells_memory(self):
        for i in self.alive_cells_memory:
            self.alive_cells.add(i)
        self.alive_cells_memory = set()

    def start_simulation(self):
        self.simulation = True

    def stop_simulation(self):
        self.simulation = False

    def update_rect(self, i, j, new_cell_value):
        cell_rect = self.cell_rects[i][j]
        color = self.CELL_ALIVE_COLOR if new_cell_value == 1 else self.CELL_DEAD_COLOR
        border = 0 if new_cell_value == 1 else 1
        border *= self.cell_border

        if border == 1:
            pygame.draw.rect(self.surface, self.BACKGROUND_COLOR, cell_rect, 0)

        pygame.draw.rect(self.surface, color, cell_rect, border)

    def clear(self):
        self.stop_simulation()
        for i, j in self.alive_cells:
            self.generation[i][j] = 0
            self.update_rect(i, j, 0)

        self.alive_cells_memory = set()
        self.alive_cells = set()

    def next_generation(self):
        next_alive_cells = set()

        board_copy = self.generation.copy() if self.simulation else self.generation
        explored_cells = {}
        for i, j in self.alive_cells:
            row_min_i = max(0, i - 1)
            row_max_i = min(self.max_rows, i + 2)

            col_min_i = max(0, j - 1)
            col_max_i = min(self.max_columns, j + 2)

            for k in range(row_min_i, row_max_i):
                for p in range(col_min_i, col_max_i):
                    if explored_cells.get((k, p)) is not None:
                        continue

                    cell_value = self.generation[k][p]

                    new_cell_value = self.game_engine.verify_cell(k, p, self.generation)

                    if cell_value != new_cell_value:
                        self.update_rect(k, p, new_cell_value)
                        board_copy[k][p] = new_cell_value

                    if new_cell_value == 1:
                        next_alive_cells.add((k, p))
                    explored_cells[(k, p)] = True

        self.alive_cells = next_alive_cells
        self.generation = board_copy
