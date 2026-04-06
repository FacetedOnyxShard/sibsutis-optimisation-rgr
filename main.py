from matrix import *
from sympy import Poly
import sympy as sp


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

    return equalities


def add_basis_vars(matrix, needed_vars, basis_list):
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


def artificial_variable_simplex(simplex_matrix):
    # симплекс метод с M строкой
    # выбираем столбец (самое большое отрицательное число среди коэффициентов)
    min_in_m = simplex_matrix[-1][1]
    min_ck = 1
    for ck in range(2, len(simplex_matrix[-1])):
        if simplex_matrix[-1][ck] < min_in_m:
            min_in_m = simplex_matrix[-1][ck]
            min_ck = ck

    # выбираем строку (самое маленькое симплексное отношение)
    sr = []
    for rk in range(
        len(simplex_matrix) - 2
    ):  # нужно сделать вычисление из другой матрицы
        sr.append(simplex_matrix[rk][0] / simplex_matrix[rk][min_ck])

    min_sr = sr[0]
    min_sr_idx = 0
    for i in range(1, len(sr)):
        if sr[i] < min_sr:
            min_sr = sr[i]
            min_sr_idx = i

    # выбранный элемент разрешающий делаем жорданово преобразование относительно его
    # если перменная ИБ вышла из базиса вычеркиваем столбец этой переменной
    # если M строка занулилась вычеркиваем M строку
    # если в M строке все коэффициенты положительны -> решение оптимально
    # если (решение_оптимально и не_вышла_из_базиса(переменная_ИБ)) система несовместна
    # если (нет_м_строки() и коэфициенты_з_положительны()) решение найдено
    # пока (есть_м_строка() или коэфициенты_з_положительны())
    pass


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

    # находим переменные которые уже образуют базис
    basis_list = find_basis_variables(MATRIX)

    # добавляем искусственные переменные в базис
    needed_vars = len(MATRIX) - len(basis_list)
    simplex_matrix = add_basis_vars(MATRIX, needed_vars, basis_list)

    # выводим базисные переменные через свободные
    basis_vars_equalities = derive_basis_vars(simplex_matrix)

    # выводим Z и M строку
    z_str_eq, m_str_eq = prepare_z_str(basis_vars_equalities, needed_vars, Z_STR)

    # готовим симплекс матрицу
    full_simplex_matrix = prepare_simplex_matrix(simplex_matrix, z_str_eq, m_str_eq)

    # решаем симплекс методом с M строкой
    artificial_variable_simplex(full_simplex_matrix)

    # print_matrix(MATRIX)

    # answer_obj, intermediate_matrices = solve_linear_system(MATRIX)

    # full_answer = {}
    # for matrix in intermediate_matrices:
    #     key, value = convert_matrix_to_json_field(matrix)
    #     full_answer[key] = value
    # full_answer["solution"] = answer_obj

    # write_answer_to_file(ANSWERS_FILEPATH, full_answer)


if __name__ == "__main__":
    main()
