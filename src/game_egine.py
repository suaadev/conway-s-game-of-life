class GameEngine:
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
