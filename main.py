from fraction import Fraction
from matrix import (
    create_linear_expression,
    frac_to_sympy,
    copy_matrix,
    create_linear_expression_with_start,
    create_x_map,
    transform_matrix,
    print_matrix,
    read_matrix_from_file,
    calculate_elements_all_dir,
    create_or_truncate_file,
    copy_arr,
    write_answer_to_file,
    solve_linear_system,
    convert_matrix_to_json_field,
)
from sympy import Eq, solve, sympify, symbols, Integer, Rational
import os


def prepare_matrix(matrix):
    normalized_matrix = [row for row in matrix if row != []]
    return normalized_matrix


def is_basis_col(ck, matrix):
    row_sum = Fraction(0)
    for rk in range(len(matrix)):
        row_sum += abs(matrix[rk][ck])
        if row_sum > Fraction(1):
            return False
    return True


def find_basis_variables(matrix):
    basis_vars = []

    for ck in range(len(matrix[0]) - 1):
        if matrix[0][ck] != Fraction(0):
            continue

        basis_var = is_basis_col(ck, matrix)

        if not basis_var:
            continue
        basis_vars.append(ck)

    return basis_vars


def derive_basis_vars(matrix):
    # ищем столбцы с базисными переменными
    basis_cols = []

    for ck in range(len(matrix[0]) - 1):
        if not (matrix[0][ck] == Fraction(0) or matrix[0][ck] == Fraction(1)):
            continue

        if is_basis_col(ck, matrix):
            basis_cols.append(ck)

    # выводим
    equalities = []
    for bk in basis_cols:
        for rk in range(len(matrix)):
            if matrix[rk][bk] != Fraction(1):
                continue
            # нужная строка, из нее можно вывести x_{bk + 1}
            expression = create_linear_expression(len(matrix[rk]) - 1)
            equation = Eq(expression, frac_to_sympy(matrix[rk][-1]))

            for j, value in enumerate(matrix[rk]):
                equation = equation.subs(f"k{j + 1}", frac_to_sympy(value))

            solution = solve(equation, f"x{bk + 1}")
            equalities.append({"base": f"x{bk + 1}", "equation": solution})
            break

    return equalities, basis_cols


def add_basis_vars(const_matrix, needed_vars, basis_list):
    matrix = copy_matrix(const_matrix)

    # найти строки для которых уже есть переменная в базисе
    basis_rows = []

    for ck in basis_list:
        for rk in len(matrix):
            if matrix[rk][ck] == Fraction(1):
                basis_rows.append(rk)
                break

    #
    basis_set = set(basis_rows)

    #
    cur_var_idx = 0
    addition_rows = []
    for i in range(len(matrix)):
        row = []
        for var_idx in range(needed_vars):
            if i not in basis_set and cur_var_idx == var_idx:
                row.append(Fraction(1))
            else:
                row.append(Fraction(0))

        r_eq_elem = matrix[i].pop()
        row.append(r_eq_elem)
        cur_var_idx += 1
        addition_rows.append(row)

    #
    simplex_matrix = copy_matrix(matrix)
    for rk in range(len(matrix)):
        simplex_matrix[rk].extend(addition_rows[rk])

    return simplex_matrix


def prepare_z_str(basis_vars_equalities, needed_vars, z_str):
    m_basis = []
    for i in range(needed_vars):
        m_basis.append(basis_vars_equalities[-(i + 1)])

    # составляем из Z sympy
    expression = create_linear_expression(len(z_str) - 1)
    z_str_equation = Eq(expression, frac_to_sympy(z_str[-1]))

    for j, value in enumerate(z_str):
        z_str_equation = z_str_equation.subs(f"k{j + 1}", frac_to_sympy(value))

    for i in range(len(basis_vars_equalities) - needed_vars):
        z_str_equation = z_str_equation.subs(
            sympify(basis_vars_equalities[i]["base"]),
            basis_vars_equalities[i]["equation"],
        )

    var_terms = sum(
        [term for term in z_str_equation.lhs.as_ordered_terms() if term.free_symbols]
    )
    const_terms = sum(
        [
            term
            for term in z_str_equation.lhs.as_ordered_terms()
            if not term.free_symbols
        ]
    )
    z_str_equation = Eq(-var_terms, const_terms)

    # преобразуем m строку
    first_idx = int(m_basis[-1]["base"][1:])
    last_idx = int(m_basis[0]["base"][1:])
    m_str_equation = create_linear_expression_with_start(first_idx, last_idx)
    for i in range(len(m_basis)):
        m_str_equation = m_str_equation.subs(
            m_basis[i]["base"], m_basis[i]["equation"][0]
        )

    m_str_equation = Eq(m_str_equation, 0)

    var_terms = sum(
        [term for term in m_str_equation.lhs.as_ordered_terms() if term.free_symbols]
    )
    const_terms = sum(
        [
            term
            for term in m_str_equation.lhs.as_ordered_terms()
            if not term.free_symbols
        ]
    )

    m_str_equation = Eq(var_terms, -const_terms)

    return z_str_equation, m_str_equation


def move_column(matrix, from_idx, to_idx):
    for row in matrix:
        col = row.pop(from_idx)
        row.insert(to_idx, col)
    return matrix


def sympy_to_frac(n):
    return Fraction(int(n))


def prepare_simplex_matrix(simplex_matrix, z_str_eq, m_str_eq):
    z_row = []
    m_row = []

    z_row.append(sympy_to_frac(z_str_eq.rhs))
    m_row.append(sympy_to_frac(m_str_eq.rhs))

    z_coeffs = []
    m_coeffs = []

    x_map = create_x_map(len(simplex_matrix[0]) - 1)
    for var in x_map:
        z_coeffs.append(sympy_to_frac(z_str_eq.lhs.coeff(var)))
        m_coeffs.append(sympy_to_frac(m_str_eq.lhs.coeff(var)))

    z_row.extend(z_coeffs)
    m_row.extend(m_coeffs)

    full_simplex_matrix = copy_matrix(simplex_matrix)

    move_column(full_simplex_matrix, -1, 0)
    full_simplex_matrix.append(z_row)
    full_simplex_matrix.append(m_row)

    return full_simplex_matrix


# добавить базисную переменную из исходной матрицы
def artificial_variable_simplex(simplex_matrix, len_src_matrix, basis_cols):
    simplex_matrix_copy = copy_matrix(simplex_matrix)
    len_simplex_values = len(simplex_matrix[0]) - 1

    intermediate_matrices = []
    intermediate_matrices.append(simplex_matrix)

    answer = basis_cols

    while True:
        # условие выхода (нужна проверка Z строки) и другие проверки для M строки
        all_zeroes = True
        for i in range(len_src_matrix):
            if simplex_matrix_copy[-1][i] != Fraction(0):
                all_zeroes = False
                break

        if all_zeroes:
            break

        # симплекс метод с M строкой
        # выбираем столбец (самое большое отрицательное число среди коэффициентов)
        min_in_m = simplex_matrix_copy[-1][1]
        min_ck = 1
        for ck in range(2, len(simplex_matrix_copy[-1])):
            if simplex_matrix_copy[-1][ck] < min_in_m:
                min_in_m = simplex_matrix_copy[-1][ck]
                min_ck = ck

        # выбираем строку (самое маленькое симплексное отношение)
        sr = []
        for rk in range(
            len(simplex_matrix_copy) - 2
        ):  # нужно сделать вычисление из другой матрицы
            if simplex_matrix_copy[rk][min_ck] == Fraction(0):
                sr.append(float("inf"))
                continue
            if (
                abs(simplex_matrix_copy[rk][0] / simplex_matrix_copy[rk][min_ck])
                != simplex_matrix_copy[rk][0] / simplex_matrix_copy[rk][min_ck]
            ):
                sr.append(float("inf"))
                continue

            sr.append(simplex_matrix_copy[rk][0] / simplex_matrix_copy[rk][min_ck])

        min_sr = sr[0]
        min_rk = 0
        for i in range(1, len(sr)):
            if sr[i] < min_sr:
                min_sr = sr[i]
                min_rk = i

        answer[min_rk] = min_ck

        # выбранный элемент разрешающий делаем жорданово преобразование относительно его
        new_simplex_matrix = transform_matrix(simplex_matrix_copy, min_rk, min_ck)
        calculate_elements_all_dir(
            simplex_matrix_copy, new_simplex_matrix, min_rk, min_ck
        )

        intermediate_matrices.append(new_simplex_matrix)

        simplex_matrix_copy = copy_matrix(new_simplex_matrix)

    # если перменная ИБ вышла из базиса вычеркиваем столбец этой переменной
    # если M строка занулилась вычеркиваем M строку
    # если в M строке все коэффициенты положительны -> решение оптимально
    # если (решение_оптимально и не_вышла_из_базиса(переменная_ИБ)) система несовместна
    # если (нет_м_строки() и коэфициенты_з_положительны()) решение найдено
    # пока (есть_м_строка() или коэфициенты_з_положительны())
    return simplex_matrix_copy, answer, intermediate_matrices


# бесконечно много решений, когда под свободной переменной в Z или M строке 0
# нет решений, когда мы не можем выбрать строку или столбец
def get_answer_from_matrix(answer_matrix, z_str_eq, answer_idxs, initial_z_str):
    values = []
    for rk in range(len(answer_matrix) - 2):
        values.append(answer_matrix[rk][0])

    k = 0
    answer = [Fraction(0)] * (len(initial_z_str) - 1)
    for val in values:
        answer[answer_idxs[k] - 1] = val
        k += 1

    answer.append(answer_matrix[-2][0])

    return answer


def solve_matrix(MATRIX, Z_STR, INITIAL_Z_STR, ANSWERS_FILEPATH="./answer/answer.json"):
    # находим переменные которые уже образуют базис
    basis_list = find_basis_variables(MATRIX)

    # добавляем искусственные переменные в базис
    needed_vars = len(MATRIX) - len(basis_list)
    simplex_matrix = add_basis_vars(MATRIX, needed_vars, basis_list)

    # выводим базисные переменные через свободные
    basis_vars_equalities, basis_cols = derive_basis_vars(simplex_matrix)

    # выводим Z и M строку
    z_str_eq, m_str_eq = prepare_z_str(basis_vars_equalities, needed_vars, Z_STR)

    # готовим симплекс матрицу
    full_simplex_matrix = prepare_simplex_matrix(simplex_matrix, z_str_eq, m_str_eq)

    # решаем симплекс методом с M строкой
    answer_matrix, answer_idxs, intermediate_matrices = artificial_variable_simplex(
        full_simplex_matrix, len(MATRIX[0]), basis_cols
    )

    # получаем ответ,
    # одна строка последний элемент, то чему равно Z
    answer = get_answer_from_matrix(answer_matrix, z_str_eq, answer_idxs, INITIAL_Z_STR)
    z_value = answer.pop()

    answer_object = {
        "answer_comment": "единственное решение",
        "answer": answer,
        "z_value": z_value,
    }

    full_answer = {}
    for matrix in intermediate_matrices:
        key, value = convert_matrix_to_json_field(matrix)
        full_answer[key] = value
    full_answer["solution"] = answer_object

    write_answer_to_file(ANSWERS_FILEPATH, full_answer)


def main() -> None:
    MATRIX_DIR = "0_zlp"
    TASK_ID = "pr_task3"

    MATRIX = read_matrix_from_file(f"{MATRIX_DIR}/{TASK_ID}.txt")

    DIR_FOR_ANSWERS = "answer"
    ANSWERS_FILEPATH = f"./{DIR_FOR_ANSWERS}/answer.json"

    os.makedirs(DIR_FOR_ANSWERS, exist_ok=True)
    create_or_truncate_file(ANSWERS_FILEPATH)

    MATRIX = prepare_matrix(MATRIX)
    Z_STR = MATRIX.pop()
    INITIAL_Z_STR = copy_arr(Z_STR)

    solve_matrix(MATRIX, Z_STR, INITIAL_Z_STR, ANSWERS_FILEPATH)


if __name__ == "__main__":
    main()
