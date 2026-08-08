# def print_matriz(matriz):
#     for i in matriz:
#         for j in i:
#             print(j, end="  ")
#         print()
#     print()


def merge_matrices(old_matriz, new_matriz, callback=lambda i, j: j) -> list[list[int]]:

    len_old_matriz_rows = len(old_matriz)
    len_old_matriz_columns = len(old_matriz[0])

    len_new_matriz_rows = len(new_matriz)
    len_new_matriz_columns = len(new_matriz[0])

    matriz_min_rows = min(len_old_matriz_rows, len_new_matriz_rows)
    matriz_min_columns = min(len_old_matriz_columns, len_new_matriz_columns)

    matriz_max_rows = max(len_old_matriz_rows, len_new_matriz_rows)
    matriz_max_columns = max(len_old_matriz_columns, len_new_matriz_columns)

    difference_rows = (matriz_max_rows - matriz_min_rows) // 2
    difference_columns = (matriz_max_columns - matriz_min_columns) // 2

    diff_i_new = 0
    diff_i_old = 0

    diff_j_new = 0
    diff_j_old = 0

    if len_new_matriz_rows > len_old_matriz_rows:
        diff_i_new += difference_rows
    else:
        diff_i_old += difference_rows

    if len_new_matriz_columns > len_old_matriz_columns:
        diff_j_new += difference_columns
    else:
        diff_j_old += difference_columns

    for i in range(matriz_min_rows):
        for j in range(matriz_min_columns):
            value = old_matriz[i + diff_i_old][j + diff_j_old]
            new_matriz[i + diff_i_new][j + diff_j_new] = value
            callback(i + diff_i_new, j + diff_j_new, value)

    return new_matriz


# old_matriz = [[1 for _ in range(10)] for _ in range(6)]  # new matriz

# new_matriz = [[0 for _ in range(6)] for _ in range(10)]  # new matriz

# print_matriz(old_matriz)

# print_matriz(new_matriz)

# print_matriz(merge_matrices(old_matriz, new_matriz))
