class GameEngine:

    def verify_cell(self, i, j, board) -> int:

        cell = board[i][j]

        neighboorhods_count = self.calculateNeighboorhods(board, i, j)

        if cell == 0 and neighboorhods_count == 3:
            cell = 1

        elif cell == 1 and neighboorhods_count < 2 or neighboorhods_count > 3:
            cell = 0

        return cell

    def calculateNeighboorhods(self, board: list[list[int]], i: int, j: int) -> int:
        neighboorhods_count = 0
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

                neighboorhods_count += 1 if board[ni][nc] > 0 else 0

        return neighboorhods_count
