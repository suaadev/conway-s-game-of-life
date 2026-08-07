import numpy as np


class GameEngine:
    def __init__(self, max_rows=100, max_columns=100):
        self.max_rows = max_rows
        self.max_columns = max_columns
        self.generation = np.zeros((self.max_rows, self.max_columns))
        self.alive_cells = set()
        self.cells_memory = set()
        self.current_generation = 0

    def build(self, max_rows, max_columns):
        self.max_rows = max_rows
        self.max_columns = max_columns
        self.generation = np.zeros((self.max_rows, self.max_columns))
        self.alive_cells = set()
        self.cells_memory = set()
        self.current_generation = 0

    def set_value_cell(self, i, j, status, in_memo=False):
        before_cell_value = self.generation[i][j]

        new_cell_value = 1 if status else 0

        self.generation[i][j] = new_cell_value

        if in_memo:
            self.cells_memory.add((i, j))
        else:
            self.alive_cells.add((i, j))

        return (new_cell_value, before_cell_value)

    def release_cells_memory(self):
        self.alive_cells = self.alive_cells.union(self.cells_memory)

    def reset(self):
        self.generation = np.zeros((self.max_rows, self.max_columns))
        self.alive_cells = set()

    def next_generation(self, callback: lambda: (int, int, int)):
        next_alive_cells = set()

        generation_copy = self.generation.copy()

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

                    new_cell_value = self.verify_cell(k, p, self.generation)

                    if cell_value != new_cell_value:
                        generation_copy[k][p] = new_cell_value
                        callback(k, p, new_cell_value)

                    if new_cell_value == 1:
                        next_alive_cells.add((k, p))

                    explored_cells[(k, p)] = True

        self.current_generation += 1
        self.alive_cells = next_alive_cells
        self.generation = generation_copy
        return self.generation

    def verify_cell(self, i, j, board) -> int:
        cell = board[i][j]

        total_neighbors = self.get_total_neighbors(board, i, j)

        if cell == 0 and total_neighbors == 3:
            cell = 1

        elif cell == 1 and total_neighbors < 2 or total_neighbors > 3:
            cell = 0

        return cell

    def get_total_neighbors(self, board: list[list[int]], i: int, j: int) -> int:
        total_neighbors = 0
        rows = len(board)
        columns = len(board[0])

        for k in [1, 0, -1]:
            for p in [1, 0, -1]:
                ni = i + k
                nc = j + p

                if (
                    ni == i
                    and nc == j
                    or ni < 0
                    or ni >= rows
                    or nc < 0
                    or nc >= columns
                ):
                    continue

                total_neighbors += 1 if board[ni][nc] > 0 else 0

        return total_neighbors
