import numpy as np  # noqa: I001
from merge_matrices import merge_matrices


class GameEngine:
    def __init__(self, max_rows=1000, max_columns=1000):
        self.max_rows = max_rows
        self.max_columns = max_columns

        self.reset()
        self.scanning_limit()

    def scanning_limit(self, rows=None, columns=None):

        col_resolved = columns if columns is not None else self.max_columns
        row_resolved = rows if rows is not None else self.max_rows

        print(col_resolved, row_resolved)
        diff_col = (self.max_columns - col_resolved) // 2
        diff_row = (self.max_rows - row_resolved) // 2

        self.scaning_min_j = diff_col
        self.scaning_max_j = self.max_columns - diff_col - 1

        self.scaning_min_i = diff_row
        self.scaning_max_i = self.max_rows - diff_row - 1

        print(
            (
                self.scaning_max_i - self.scaning_min_i,
                self.scaning_max_j - self.scaning_min_j,
            ),
            (self.scaning_min_i, self.scaning_min_j),
            (self.scaning_max_i, self.scaning_max_j),
        )

    def resize(self, max_rows, max_columns):
        self.cells_memory = set()
        self.alive_cells = set()
        self.max_rows = max_rows
        self.max_columns = max_columns
        self.generation = merge_matrices(
            self.generation,
            np.zeros((max_rows, max_columns)),
            lambda i, j, v: self.alive_cells.add((i, j)) if v == 1 else None,
        )
        return self.generation

    def set_value_cell(self, i, j, status, in_memo=False):
        i_ = i + self.scaning_min_i
        j_ = j + self.scaning_min_j
        before_cell_value = self.generation[i_][j_]

        new_cell_value = 1 if status else 0

        self.generation[i_][j_] = new_cell_value

        if in_memo:
            self.cells_memory.add((i_, j_))
        else:
            self.alive_cells.add((i_, j_))

        return (new_cell_value, before_cell_value)

    def release_cells_memory(self):
        self.alive_cells = self.alive_cells.union(self.cells_memory)

    def reset(self):
        self.alive_cells = set()
        self.cells_memory = set()
        self.current_generation = 0
        self.generation = np.zeros((self.max_rows, self.max_columns))

    def next_generation(self, callback: lambda: (int, int, int)):
        next_alive_cells = set()

        generation_copy = self.generation.copy()

        explored_cells = {}

        for i, j in self.alive_cells:  # n
            positions_ = [
                (i, j),
                (i, (j + 1) % self.max_columns),
                (i, (j - 1) % self.max_columns),
                ((i + 1) % self.max_rows, (j + 1) % self.max_columns),
                ((i + 1) % self.max_rows, (j - 1) % self.max_columns),
                ((i + 1) % self.max_rows, j),
                ((i - 1) % self.max_rows, (j - 1) % self.max_columns),
                ((i - 1) % self.max_rows, (j + 1) % self.max_columns),
                ((i - 1) % self.max_rows, j),
            ]

            for k, p in positions_:
                if explored_cells.get((k, p)) is not None:
                    continue

                cell_value = self.generation[k][p]

                new_cell_value = self.verify_cell(k, p, self.generation)  # 3x3

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

    def get_generation_value(self, i, j):
        return self.generation[i + self.scaning_min_i][j + self.scaning_min_j]

    def get_total_neighbors(self, board: list[list[int]], i: int, j: int) -> int:
        total_neighbors = 0

        for k in [1, 0, -1]:
            for p in [1, 0, -1]:
                # se obtiene el residudio de multiplicar la posicion con el limite para que sea toloideal
                ni = (i + k) % self.max_rows
                nc = (j + p) % self.max_columns

                if ni == i and nc == j:
                    continue

                total_neighbors += 1 if board[ni][nc] > 0 else 0

        return total_neighbors
