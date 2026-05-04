from fraction import Fraction
from operator import itemgetter
from sympy import symbols, sympify, Add, solve, Eq
from enum import Enum
import json
import os


def read_matrix_from_file(filename: str) -> list[list[Fraction]]:
    with open(filename) as file:
        matrix = []
        for line in file:
            matrix.append(list(map(Fraction.to_fraction, line.split())))

    return matrix


def print_matrix(matrix: list[list[Fraction]]) -> None:
    for row in matrix:
        print(" ".join(f"{str(fraction):>10}" for fraction in row))
    print()


def transform_matrix(
    matrix: list[list[Fraction]], row: int, col: int
) -> list[list[Fraction]]:
    transformed_matrix = copy_matrix(matrix)
    enabling_element = matrix[row][col]

    for j in range(len(matrix[row])):
        transformed_matrix[row][j] = matrix[row][j] / enabling_element

    for i in range(len(matrix)):
        if i == row:
            continue
        transformed_matrix[i][col] = Fraction(0)

    return transformed_matrix


def find_enabling_element(a_matrix: list[list[Fraction]], current_row: int) -> int:
    column = -1

    for j in range(len(a_matrix[current_row])):
        if a_matrix[current_row][j] != Fraction(0):
            column = j
            break

    return column


def copy_arr(arr: list):
    return arr[:]


def copy_matrix(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    matrix_copy = [row[:] for row in matrix]
    return matrix_copy


def calculate_elements(a, a_hat, row: int, col: int):
    enabling_element = a[row][col]

    for crow in range(len(a)):
        koef = a[crow][col] / enabling_element

        for ccol in range(col, len(a[crow])):
            if crow == row:
                continue

            current_element = a[crow][ccol]

            a_hat[crow][ccol] = current_element - (koef * a[row][ccol])


def calculate_elements_all_dir(a, a_hat, row: int, col: int):
    enabling_element = a[row][col]

    for crow in range(len(a)):
        koef = a[crow][col] / enabling_element

        for ccol in range(len(a[crow])):
            if ccol == col:
                continue

            if crow == row:
                continue

            current_element = a[crow][ccol]

            a_hat[crow][ccol] = current_element - (koef * a[row][ccol])


def strike_zero_rows(matrix: list[list[Fraction]], row) -> list[list[Fraction]]:
    zero_rows = []
    for crow in range(row + 1, len(matrix)):
        is_zero = True
        for j in range(len(matrix[crow])):
            if matrix[crow][j] != Fraction(0):
                is_zero = False

        if is_zero:
            zero_rows.append(crow)

    new_matrix = []
    cur_zero_row_idx = 0
    for i, row in enumerate(matrix):
        if len(zero_rows) != 0 and i == zero_rows[cur_zero_row_idx]:
            if cur_zero_row_idx < len(zero_rows) - 1:
                cur_zero_row_idx += 1
            continue

        new_matrix.append(row)

    return new_matrix


def swap_rows(matrix, row1, row2):
    if not (0 <= row1 < len(matrix) and 0 <= row2 < len(matrix)):
        raise IndexError()

    temp = matrix[row1]
    matrix[row1] = matrix[row2]
    matrix[row2] = temp


def select_main_element(matrix, cur_row):
    ccol = 0
    ccol_abs_elem_and_idxs = []

    # колонки идут с начала строки,
    # можно сделать с предыдущей колонки + 1
    for ccol in range(len(matrix[0]) - 1):
        for crow in range(cur_row, len(matrix)):
            if matrix[crow][ccol] == Fraction(0):
                continue

            ccol_abs_elem_and_idxs.append((abs(matrix[crow][ccol]), crow))

        if len(ccol_abs_elem_and_idxs) == 0:
            continue

        max_abs_elem_and_idx = max(ccol_abs_elem_and_idxs, key=itemgetter(0))
        if max_abs_elem_and_idx[0] != Fraction(0):
            break

    last_col_idx = len(matrix[0]) - 2
    last_row_idx = len(matrix) - 1
    if ccol == last_col_idx and matrix[last_row_idx][ccol] == Fraction(0):
        ccol = -1
    else:
        swap_rows(matrix, cur_row, max_abs_elem_and_idx[1])

    return ccol


def counter(reset: bool = False):
    if not hasattr(counter, "count"):
        counter.count = 0
    if reset:
        counter.count = 0
    counter.count += 1
    return counter.count


def convert_matrix_to_json_field(matrix: list[list[Fraction]]):
    key = f"matrix {counter()}"
    value = []

    for i, row in enumerate(matrix):
        matrix_row = []
        for j, item in enumerate(matrix[i]):
            if j == 0:
                matrix_row.append(f"{str(item)}")
                continue

            matrix_row.append(f"{str(item):>12}")

        value.append("".join(matrix_row))

    return key, value


def Gauss_Jordan_elimination(original_matrix: list[list[Fraction]]):
    a = copy_matrix(original_matrix)
    intermediate_matrices_container = []

    for row in range(len(a)):
        if row >= len(a):
            break

        col = select_main_element(a, row)
        # col = find_enabling_element(a, row) # нужна если
        # # не используется select_main_element

        if col != -1:  # все элементы в левой части равны 0, правая - неизвестно
            a_hat = transform_matrix(a, row, col)
            calculate_elements(a, a_hat, row, col)

        a_hat = strike_zero_rows(a_hat, row)
        a = copy_matrix(a_hat)

        if col == -1 and matrices_are_equal(a, a_hat):
            continue
        intermediate_matrices_container.append(a)

    return a, intermediate_matrices_container


def have_incorrect_row(matrix: list[list[Fraction]]):
    res = False

    for i in range(len(matrix)):
        is_zero_row = True
        last_element_in_row = matrix[i][-1]
        for j in range(len(matrix[i]) - 1):
            if matrix[i][j] != Fraction(0):
                is_zero_row = False
                break

        if is_zero_row and last_element_in_row != Fraction(0):
            res = True
            break

    return res


def is_identity_matrix(matrix: list[list[Fraction]]):
    current_k = 0
    if len(matrix) != len(matrix[0]) - 1:
        return False

    for i in range(len(matrix)):
        for j in range(len(matrix[i]) - 1):
            if j == current_k:
                if not matrix[i][j] == Fraction(1):
                    return False
            else:
                if not matrix[i][j] == Fraction(0):
                    return False
        current_k += 1

    return True


def frac_to_sympy(n: Fraction):
    return sympify(str(n))


def find_common_solution(matrix: list[list[Fraction]]):
    solutions = []
    for i, row in enumerate(matrix):
        # можно создавать выражение только 1 раз
        expression = create_linear_expression(len(row) - 1)
        equation = Eq(expression, frac_to_sympy(row[-1]))
        base_var_idx = -1
        base_var_found = False

        for j, value in enumerate(row):
            if j == len(row) - 1:  # нужно для того, чтобы не включать расширенную часть
                continue  # можно написать break
            if not base_var_found and value == Fraction(1):
                base_var_idx = j + 1
                base_var_found = True

            equation = equation.subs(f"k{j + 1}", frac_to_sympy(value))

        solution = solve(equation, f"x{base_var_idx}")
        solutions.append((f"x{base_var_idx}", solution[0]))

    return solutions


class Answer(str, Enum):
    No = "нет решений"
    One = "одно решение"
    Infinity = "бесконечно много решений"


def find_system_solution(matrix: list[list[Fraction]]):
    answer = Answer.No
    answer_system = {}

    if have_incorrect_row(matrix):
        pass
    elif is_identity_matrix(matrix):
        answer = Answer.One
        for i, row in enumerate(matrix, start=1):
            key = f"x{i}"
            answer_system[key] = str(row[-1])
    else:
        answer = Answer.Infinity
        solutions = find_common_solution(matrix)
        for key, value in solutions:
            answer_system[key] = value

    return (answer, answer_system)


def write_answer_to_file(filepath: str, answer_object):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(answer_object, file, indent=2, default=str, ensure_ascii=False)


def solve_linear_system(matrix: list[list[Fraction]]) -> tuple:
    eliminated_matrix, intermediate_matrices = Gauss_Jordan_elimination(matrix)

    answer, answer_system = find_system_solution(eliminated_matrix)

    answer_object = {"answer": answer.value, "answer_system": answer_system}

    return answer_object, intermediate_matrices


def matrices_are_equal(
    matrix1: list[list[Fraction]], matrix2: list[list[Fraction]]
) -> bool:
    for i in range(len(matrix1)):
        for j in range(len(matrix2)):
            if matrix1[i][j] != matrix2[i][j]:
                return False

    return True


def create_linear_expression(n: int):
    var_symbols = symbols([f"x{i + 1}" for i in range(n)])
    coef_symbols = symbols([f"k{i + 1}" for i in range(n)])

    terms = [coef * var for coef, var in zip(coef_symbols, var_symbols)]
    expression = Add(*terms)
    return expression


def create_x_map(n: int):
    var_symbols = symbols([f"x{i + 1}" for i in range(n)])
    return var_symbols


def create_linear_expression_with_start(start: int, end: int):
    var_symbols = symbols([f"x{i + 1}" for i in range(start - 1, end)])
    expression = Add(*var_symbols)
    return expression


def create_or_truncate_file(filepath: str):
    with open(filepath, "w"):
        pass


def copy_from(arr, start: int, k: int):
    return [arr[i] for i in range(start, start + k)]


def make_seq(n: int):
    return [i + 1 for i in range(n)]


def combination_generation(n: int, k: int):
    if k == 0:
        return [[]]
    if n < k:
        return []

    p = k
    comb = make_seq(k)

    combinations = [comb.copy()]

    while p > 0:
        if comb[0] == n - k + 1:
            break

        comb = comb.copy()

        if comb[p - 1] >= n:
            j = 1

            while p > 0 and comb[p - 1] >= n - j:
                p -= 1

            comb[p - 1] += 1
            for i in range(p, k):
                comb[i] = comb[i - 1] + 1
            combinations.append(comb)

            p = k
            continue

        comb[p - 1] += 1
        combinations.append(comb)

    return combinations


def find_pivot_element(matrix: list[list[Fraction]], col, used_rows):
    rows = len(matrix)

    for row_idx in range(rows):
        if row_idx not in used_rows and matrix[row_idx][col] == Fraction(1):
            return row_idx

    for row_idx in range(rows):
        if row_idx not in used_rows and matrix[row_idx][col] != Fraction(0):
            return row_idx

    return -1


def find_basics_solutions(matrix):
    n = len(matrix[0]) - 1
    k = len(matrix)

    answers = []
    for var_list in combination_generation(n, k):
        a = copy_matrix(matrix)
        row_idxs = []
        answer = []
        used_rows = set()
        for i in range(len(var_list)):
            col = var_list[i] - 1
            row_idx = find_pivot_element(a, col, used_rows)
            row_idxs.append(row_idx)

            if row_idx == -1:
                answers.append(answer)
                break

            used_rows.add(row_idx)

            a_hat = transform_matrix(a, row_idx, col)
            calculate_elements(a, a_hat, row_idx, col)

            a = copy_matrix(a_hat)

            if i == len(var_list) - 1:
                for j in range(len(var_list)):
                    answer.append((f"x{var_list[j]}", a[row_idxs[j]][-1]))

                c = 0
                for j in range(len(a[0]) - 1):
                    if c < len(var_list) and j == (var_list[c] - 1):
                        c += 1
                        continue
                    answer.append((f"x{j + 1}", 0))

                answers.append(answer)

    return answers


def out_basics_solutions(answers):
    i = 1
    for row in answers:
        print(f"{i}:  ", end="")
        i += 1
        for items in row:
            print(f"{items[0]} {str(items[1]):<10}", end="")
        print()


def main() -> None:
    TASK_ID = "lr02_01"
    MATRIX_DIR = "test_matrix"

    MATRIX = read_matrix_from_file(f"{MATRIX_DIR}/{TASK_ID}_task.txt")

    DIR_FOR_ANSWERS = "answer"
    ANSWERS_FILEPATH = f"./{DIR_FOR_ANSWERS}/answer.json"

    os.makedirs(DIR_FOR_ANSWERS, exist_ok=True)
    create_or_truncate_file(ANSWERS_FILEPATH)

    answer_obj, intermediate_matrices = solve_linear_system(MATRIX)

    answers = find_basics_solutions(intermediate_matrices[-1])

    out_basics_solutions(answers)


if __name__ == "__main__":
    main()
