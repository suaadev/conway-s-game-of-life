import numpy as np
import pygame
from math import ceil


class Board(pygame.Surface):
    def __init__(self, width, height, game_engine):
        super().__init__((width, height))

        self.BACKGROUND_COLOR = (15, 15, 15)
        self.CELL_ALIVE_COLOR = (198, 229, 245)
        self.CELL_DEAD_COLOR = (0, 0, 0)

        self.CELL_WIDTH = 10
        self.CELL_HEIGHT = 10

        self.height = height
        self.width = width
        self.fill(self.BACKGROUND_COLOR)
        self.cell_border = 0
        self.game_engine = game_engine
        self.simulation = False
        self.build()
        self.alive_cells = set()
        self.alive_cells_memory = set()

    def build(self):
        self.max_rows = ceil(self.height / self.CELL_HEIGHT)
        self.max_columns = ceil(self.width / self.CELL_WIDTH)
        print(self.cell_border)
        cell_rects = []
        for i in range(0, self.height, self.CELL_HEIGHT):
            for j in range(0, self.width, self.CELL_WIDTH):
                rect = pygame.rect.Rect(j, i, self.CELL_WIDTH, self.CELL_HEIGHT)
                pygame.draw.rect(self, self.CELL_DEAD_COLOR, rect, self.cell_border)
                cell_rects.append(rect)
        print(
            (self.max_rows, self.max_columns), self.height, self.width, len(cell_rects)
        )
        self.board = np.zeros((self.max_rows, self.max_columns))

        self.cell_rects = cell_rects
        return self.board

    def resize(self, width, height):
        super().__init__((width, height))
        self.height = height
        self.width = width
        self.build()

    def switch_cell_border(self):
        self.cell_border = 0 if self.cell_border == 1 else 1
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                cell_value = self.board[i][j]
                self.update_rect(i, j, cell_value)

    def set_cell_status(self, coord_x: int, coord_y: int, status: bool) -> tuple[int]:
        j = coord_x // self.CELL_WIDTH  # columns
        i = coord_y // self.CELL_HEIGHT  # rows
        before_cell_value = self.board[i][j]
        new_cell_value = 1 if status else 0
        self.board[i][j] = new_cell_value
        # optimization  only render the cell that have change
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
        cell_rect = self.cell_rects[i * len(self.board[0]) + j]
        color = self.CELL_ALIVE_COLOR if new_cell_value == 1 else self.CELL_DEAD_COLOR
        border = 0 if new_cell_value == 1 else 1
        border *= self.cell_border

        if border == 1:
            pygame.draw.rect(self, self.BACKGROUND_COLOR, cell_rect, 0)

        pygame.draw.rect(self, color, cell_rect, border)

    def clear(self):
        self.stop_simulation()
        for i, j in self.alive_cells:
            self.board[i][j] = 0
            self.update_rect(i, j, 0)

        self.alive_cells_memory = set()
        self.alive_cells = set()

    def next_generation(self):
        next_alive_cells = set()

        board_copy = self.board.copy() if self.simulation else self.board
        explored_cells = {}
        for i, j in self.alive_cells:
            row_min_i = max(0, i - 2)
            row_max_i = min(self.max_rows, i + 3)

            col_min_i = max(0, j - 2)
            col_max_i = min(self.max_columns, j + 3)

            for k in range(row_min_i, row_max_i):
                for p in range(col_min_i, col_max_i):
                    if explored_cells.get((k, p)) is not None:
                        # print("POSICION EXPLORADA", (k, p))
                        continue
                    cell_value = self.board[k][p]

                    new_cell_value = self.game_engine.verify_cell(k, p, self.board)

                    if cell_value != new_cell_value:
                        self.update_rect(k, p, new_cell_value)
                        board_copy[k][p] = new_cell_value

                    if new_cell_value == 1:
                        next_alive_cells.add((k, p))
                    explored_cells[(k, p)] = True

        self.alive_cells = next_alive_cells
        self.board = board_copy
