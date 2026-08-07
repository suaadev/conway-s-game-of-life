from math import ceil

import pygame


class Simulation:
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
        self.build_simulation()

    def build_simulation(self):
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

        self.game_engine.build(self.max_rows, self.max_columns)

        self.cell_rects = cell_rects

    def resize(self, width, heigth):
        self.surface_height = heigth
        self.surface_width = width
        self.surface = pygame.Surface((width, heigth))
        self.surface.fill(self.BACKGROUND_COLOR)
        self.surface_rect = self.surface.get_rect(topleft=(0, 0))
        self.build_simulation()

    def switch_cell_border(self):
        self.cell_border = 0 if self.cell_border == 1 else 1
        for i in range(self.game_engine.max_rows):
            for j in range(self.game_engine.max_columns):
                cell_value = self.game_engine.generation[i][j]
                self.update_rect(i, j, cell_value)

    def set_cell_status(self, coord_x: int, coord_y: int, status: bool) -> tuple[int]:
        j = coord_x // self.CELL_SIZE  # columns
        i = coord_y // self.CELL_SIZE  # rows

        (new_cell_value, before_cell_value) = self.game_engine.set_value_cell(
            i, j, status, in_memo=self.simulation
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
        for i in range(self.game_engine.max_rows):
            for j in range(self.game_engine.max_rows):
                self.update_rect(i, j, 0)

    def next_generation(self):
        self.game_engine.next_generation(lambda i, j, v: self.update_rect(i, j, v))

    def update_rect(self, i, j, new_cell_value):
        cell_rect = self.cell_rects[i][j]
        color = self.CELL_ALIVE_COLOR if new_cell_value == 1 else self.CELL_DEAD_COLOR
        border = 0 if new_cell_value == 1 else 1
        border *= self.cell_border

        if border == 1:
            pygame.draw.rect(self.surface, self.BACKGROUND_COLOR, cell_rect, 0)

        pygame.draw.rect(self.surface, color, cell_rect, border)
