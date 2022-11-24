import argparse
import json

UNASSIGNED = 0


def is_safe(matrix: list, row: int, col: int, num: int) -> bool:

    # Check if it can be placed in this row
    if num in matrix[row]:
        return False

    # Check if it can be placed in this col
    if num in [row_data[col] for row_data in matrix]:
        return False

    # Check if it can be placed in this box
    row_start_index = row - (row % SUDOKU_BOX_SIZE)
    col_start_index = col - (col % SUDOKU_BOX_SIZE)
    for tmp_row_index in range(SUDOKU_BOX_SIZE):
        tmp_row = [matrix[row_start_index + tmp_row_index][col_start_index + tmp_col_index]
                   for tmp_col_index in range(SUDOKU_BOX_SIZE)]
        if num in tmp_row:
            return False

    return True


def is_completed(matrix: list) -> bool:
    for row_data in matrix:
        if UNASSIGNED in row_data:
            return False
    return True


def sudoku_solve() -> bool:
    global SUDOKU_MATRIX
    matrix = SUDOKU_MATRIX
    # BEGIN_YOUR_CODE
    change = True
    while change:
        change = False
        for row in range(MAX_NUMBER):
            for col in range(MAX_NUMBER):
                if matrix[row][col] == UNASSIGNED:
                    result = [is_safe(matrix, row, col, num) for num in range(1, MAX_NUMBER + 1)]
                    if result.count(True) == 1:
                        matrix[row][col] = result.index(True) + 1
                        change = True
        for num in range(1, MAX_NUMBER+1):
            for row in range(SUDOKU_BOX_SIZE): # 0, 1, 2
                for col in range(SUDOKU_BOX_SIZE): # 0, 1, 2
                    result = []
                    for box_row in range(row*SUDOKU_BOX_SIZE,row*SUDOKU_BOX_SIZE+SUDOKU_BOX_SIZE): # [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
                        for box_col in range(col*SUDOKU_BOX_SIZE, col*SUDOKU_BOX_SIZE+SUDOKU_BOX_SIZE): # [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
                            result.append(is_safe(matrix, box_row, box_col, num))
                    if result.count(True) == 1:
                        matrix[row*SUDOKU_BOX_SIZE + result.index(True)//3][col*SUDOKU_BOX_SIZE+result.index(True)%3] = num
                        change = True
    # END_YOUR_CODE
    return is_completed(matrix)

def sudoku_solver() -> list:
    global SUDOKU_MATRIX
    matrix = SUDOKU_MATRIX
    if sudoku_solve():
        return matrix
    return ["No Result"]


if __name__ == '__main__':
    SUDOKU_MATRIX = []
    SUDOKU_BOX_SIZE = 0
    MAX_NUMBER = 0

    parser = argparse.ArgumentParser()
    parser.add_argument('--sudoku_file_path', '-f', type=str, default='q1_sample_input.json')

    args = parser.parse_args()
    with open(args.sudoku_file_path, "r+") as fs:
        sudoku_info = json.load(fs)
        SUDOKU_MATRIX = sudoku_info['matrix']
        SUDOKU_BOX_SIZE = sudoku_info['box_size']
        MAX_NUMBER = SUDOKU_BOX_SIZE**2

    sudoku_result = sudoku_solver()

    print("Answer:")
    for result in sudoku_result:
        print(result)

    result_dict = {
        "result": sudoku_result
    }

    with open('sudoku_solver_result.json', 'w+') as fs:
        fs.write(json.dumps(result_dict, indent=4))
