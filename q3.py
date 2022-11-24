import json
import argparse
from copy import deepcopy

ASSIGNED = 1
UNASSIGNED = 0



def is_safe(matrix: list, row: int, col: int) -> bool:
    n = len(matrix)

    # Check if it can be placed in this row
    row_data = matrix[row]
    if ASSIGNED in row_data:
        return False

    # Check if it can be placed in this col
    col_data = [temp_row_data[col] for temp_row_data in matrix]
    if ASSIGNED in col_data:
        return False

    # Check if it can be placed on this diagonal
    diff_count = min(row, col)
    row_start_index = row - diff_count
    col_start_index = col - diff_count
    diagonal_data_1 = [matrix[row_index][col_index] for row_index, col_index in
                       zip(range(row_start_index, n, 1), range(col_start_index, n, 1))]
    if ASSIGNED in diagonal_data_1:
        return False

    diff_count = min(n - row - 1, col)
    row_start_index = row + diff_count
    col_start_index = col - diff_count
    diagonal_data_2 = [matrix[row_index][col_index] for row_index, col_index in
                       zip(range(row_start_index, -1, -1), range(col_start_index, n, 1))]
    if ASSIGNED in diagonal_data_2:
        return False

    return True


def n_queen_solve(row: int) -> None:
    global puzzle_matrix
    global n_queen_result
    matrix = puzzle_matrix
    n = len(puzzle_matrix)
    # BEGIN_YOUR_CODE
    def solve_queen(matrix, row, num):
        if num == n: # stop, because found result
            n_queen_result.append(matrix)
            return
        for col in range(n):
            if is_safe(matrix, row, col): # put queen, go next row
                matrix[row][col] = ASSIGNED
                solve_queen(deepcopy(matrix), row+1, num+1)
                matrix[row][col] = UNASSIGNED # backtracking, try next col

    solve_queen(matrix, row, 0)
    # END_YOUR_CODE


if __name__ == '__main__':
    puzzle_matrix = []
    n_queen_result = []

    parser = argparse.ArgumentParser()
    parser.add_argument('--puzzle_file_path', '-f', type=str, default='q3_sample_input.json')

    args = parser.parse_args()
    with open(args.puzzle_file_path, "r+") as fs:
        n_queen_info = json.load(fs)
        n_size = n_queen_info['n']
        n_size = 8

    # Create Puzzle
    for i in range(n_size):
        puzzle_matrix.append([0] * n_size)

    # Solve n Queen Problem
    n_queen_solve(0)
    # print(solve_queen(puzzle_matrix, 0, 0, 0, n_size))

    for index, result in enumerate(n_queen_result):
        print('=', f'{index + 1:02d}', '='*10)
        for row_result in result:
            print(row_result)
        print()

    result_dict = {
        "length": len(n_queen_result),
        "result": n_queen_result
    }

    with open('n_queen_result.json', "w+") as fs:
        fs.write(json.dumps(result_dict, indent=4))
