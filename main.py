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
from sympy import (
    Eq,
    solve,
    sympify,
    symbols,
    Integer,
    Rational,
    Matrix,
    pprint,
)
import os


def move_column(matrix, from_idx, to_idx):
    for row in matrix:
        col = row.pop(from_idx)
        row.insert(to_idx, col)
    return matrix


def sympy_to_frac(n):
    return Fraction(int(n))


def prepare_matrix(matrix):
    normalized_matrix = [row for row in matrix if row != []]
    return normalized_matrix


def is_basis_col(ck, matrix):
    row_sum = Fraction(0)
    for rk in range(len(matrix)):
        if matrix[rk][ck] == Fraction(1):
            row_sum += abs(matrix[rk][ck])
            if row_sum > Fraction(1):
                return False
        elif matrix[rk][ck] != Fraction(0):
            return False
    return row_sum == Fraction(1)


def find_basis_variables_in_simplex(matrix):
    basis_vars = []

    for ck in range(1, len(matrix[0])):
        if matrix[0][ck] != Fraction(1) and matrix[0][ck] != Fraction(0):
            continue

        basis_var = is_basis_col(ck, matrix)

        if not basis_var:
            continue
        basis_vars.append(ck)

    return basis_vars


def find_basis_variables(matrix):
    basis_vars = []

    for ck in range(len(matrix[0]) - 1):
        if matrix[0][ck] != Fraction(1) and matrix[0][ck] != Fraction(0):
            continue

        basis_var = is_basis_col(ck, matrix)

        if not basis_var:
            continue
        basis_vars.append(ck)

    return basis_vars


def derive_basis_vars(matrix):
    # ищем столбцы с базисными переменными
    basis_cols = [0] * len(matrix)

    print_matrix(matrix)

    for ck in range(len(matrix[0]) - 1):
        if not (matrix[0][ck] == Fraction(0) or matrix[0][ck] == Fraction(1)):
            continue

        if is_basis_col(ck, matrix):
            for rk in range(len(matrix)):
                if matrix[rk][ck] == Fraction(1):
                    basis_cols[rk] = ck
                    break

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

    print_matrix(matrix)

    # находит строки на которых распологаются базисные значения
    for ck in basis_list:
        for rk in range(len(matrix)):
            if matrix[rk][ck] == Fraction(1):
                basis_rows.append(rk)
                break

    print_matrix(matrix)

    #
    basis_set = set(basis_rows)

    missing_basis_rows = [i for i in range(len(matrix)) if i not in basis_set]
    current_idx_in_missing = 0
    for i in range(needed_vars):
        col = [Fraction(0)] * len(matrix)
        col[missing_basis_rows[current_idx_in_missing]] = Fraction(1)
        current_idx_in_missing += 1

        for j in range(len(matrix)):
            matrix[j].append(col[j])

    print_matrix(matrix)
    matrix = move_column(matrix, -(needed_vars + 1), len(matrix[0]))
    print_matrix(matrix)

    #
    simplex_matrix = copy_matrix(matrix)
    return simplex_matrix


def prepare_z_str(basis_vars_equalities, needed_vars, z_str):
    m_basis = []
    sorted_basis_vars_equalities = sorted(
        basis_vars_equalities, key=lambda x: int(x["base"][1:])
    )
    for i in range(needed_vars):
        m_basis.append(sorted_basis_vars_equalities[-(i + 1)])

    # составляем из Z sympy
    expression = create_linear_expression(len(z_str) - 1)
    z_str_equation = Eq(expression, frac_to_sympy(z_str[-1]))

    # подставляем коэффициенты в Z
    for j in range(len(z_str) - 1):
        z_str_equation = z_str_equation.subs(f"k{j + 1}", frac_to_sympy(z_str[j]))

    print(z_str_equation)

    # выводим базисные переменные через свободные Z
    for i in range(len(sorted_basis_vars_equalities) - needed_vars):
        z_str_equation = z_str_equation.subs(
            sorted_basis_vars_equalities[i]["base"],
            sorted_basis_vars_equalities[i]["equation"][0],
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


def has_intersection(arr1, arr2):
    """Возвращает True, если есть общие элементы"""
    return bool(set(arr1) & set(arr2))


def remove_column(matrix, col_idx):
    """
    Удаляет столбец с индексом col_idx из матрицы (списка списков)
    """
    for row in matrix:
        del row[col_idx]
    return matrix


# добавить базисную переменную из исходной матрицы
def artificial_variable_simplex(
    simplex_matrix, len_src_matrix, basis_cols, needed_vars
):
    simplex_matrix_copy = copy_matrix(simplex_matrix)
    additional_basis = []
    sorted_basis_cols = sorted(basis_cols)
    for i in range(needed_vars):
        additional_basis.append(sorted_basis_cols[-(i + 1)])

    intermediate_matrices = []
    intermediate_matrices.append(simplex_matrix)
    print_matrix(simplex_matrix)

    answer = copy_arr(basis_cols)

    removed_cols_count = 0
    m_row_deleted = False
    is_correct = True
    second_matrix_found = False
    first_matrix = None
    second_matrix = None
    many_answers = False
    min_ck = None
    min_rk = None
    second_answer_idxs = None
    second_matrix_answer_idxs = None
    first_matrix_answer_idxs = None

    while True:
        # условия выхода
        all_zeroes = True
        if not m_row_deleted:
            for i in range(len(simplex_matrix_copy[-1])):
                if simplex_matrix_copy[-1][i] != Fraction(0):
                    all_zeroes = False
                    break

            if all_zeroes:
                del simplex_matrix_copy[-1]
                m_row_deleted = True
                intermediate_matrices.append(simplex_matrix_copy)

        if m_row_deleted:
            z_str_positive = True
            for i in range(1, len(simplex_matrix_copy[-1])):
                if simplex_matrix_copy[-1][i] < Fraction(0):
                    z_str_positive = False
                    break

        # проверяем на оптимальность
        optimal = True
        for ck in range(1, len(simplex_matrix_copy[-1])):
            if simplex_matrix_copy[-1][ck] < Fraction(0):
                optimal = False
                break

        if optimal:
            many_answers = False
            for ck in range(1, len_src_matrix):
                if ck in answer:
                    continue
                # if not m_row_deleted:
                #     if simplex_matrix_copy[-2][ck] == Fraction(0):
                #         many_answers = True
                #         break
                if simplex_matrix_copy[-1][ck] == Fraction(0):
                    many_answers = True
                    min_ck = ck
                    break

        if second_matrix_found:
            second_matrix = copy_matrix(simplex_matrix_copy)
            second_matrix_answer_idxs = copy_arr(answer)
            break

        if many_answers:
            second_matrix_found = False
            first_matrix = copy_matrix(simplex_matrix_copy)
            first_matrix_answer_idxs = copy_arr(answer)

        if optimal and not many_answers:
            break

        if m_row_deleted and z_str_positive and not many_answers:
            break

        if not many_answers:
            # симплекс метод с M строкой
            # выбираем столбец (самое большое отрицательное число среди коэффициентов)
            min_in_last_row = simplex_matrix_copy[-1][1]
            min_ck = 1
            for ck in range(2, len(simplex_matrix_copy[-1])):
                if simplex_matrix_copy[-1][ck] < min_in_last_row:
                    min_in_last_row = simplex_matrix_copy[-1][ck]
                    min_ck = ck
        else:
            pass  # столбец был выбран при проверки на множество решений

        # выбираем строку (самое маленькое симплексное отношение)
        sr = []
        matrix_height = len(simplex_matrix_copy) - 1  # отнимаем z строку
        if not m_row_deleted:
            matrix_height -= 1
        for rk in range(matrix_height):  # нужно сделать вычисление из другой матрицы
            element = simplex_matrix_copy[rk][min_ck]
            if element == Fraction(0):
                sr.append(float("inf"))
            elif simplex_matrix_copy[rk][0] < Fraction(0) and element >= Fraction(0):
                sr.append(float("inf"))
            elif simplex_matrix_copy[rk][0] >= Fraction(0) and element < Fraction(0):
                sr.append(float("inf"))
            elif simplex_matrix_copy[rk][0] / element < Fraction(0):
                sr.append(float("inf"))
            else:
                sr.append(simplex_matrix_copy[rk][0] / element)

        # поиск минимального симплексного отношения
        min_sr = sr[0]  # начальное значение
        if min_sr != float("inf"):
            min_sr += Fraction(1)
        min_rk = -1
        for i in range(len(sr)):
            if sr[i] < min_sr:
                min_sr = sr[i]
                min_rk = i

        # если не нашли ни одного подходящего СО
        if min_rk == -1:
            is_correct = False
            break

        col_to_remove = answer[min_rk]
        for column in answer:
            col = column
            if simplex_matrix_copy[min_rk][col] == Fraction(1):
                col_to_remove = col
                break
        if col_to_remove in additional_basis:
            for i in range(len(answer)):
                if col_to_remove <= answer[i]:
                    answer[i] -= 1

        answer[min_rk] = min_ck

        # выбранный элемент разрешающий делаем жорданово преобразование относительно его
        new_simplex_matrix = transform_matrix(simplex_matrix_copy, min_rk, min_ck)
        calculate_elements_all_dir(
            simplex_matrix_copy, new_simplex_matrix, min_rk, min_ck
        )

        if col_to_remove in additional_basis:
            remove_column(new_simplex_matrix, col_to_remove)
            removed_cols_count += 1

        intermediate_matrices.append(new_simplex_matrix)
        print_matrix(new_simplex_matrix)

        simplex_matrix_copy = copy_matrix(new_simplex_matrix)

        if many_answers and not second_matrix_found:
            second_matrix_found = True

    # проверка на остаток искусственных в базисе
    if is_correct:
        last_in_basis = find_basis_variables_in_simplex(simplex_matrix_copy)
        if has_intersection(additional_basis, last_in_basis):
            is_correct = False

    # для множества ответов
    second_answer_matrix = None
    if many_answers:
        simplex_matrix_copy = first_matrix
        second_answer_matrix = second_matrix
        answer = first_matrix_answer_idxs
        second_answer_idxs = second_matrix_answer_idxs

    # если перменная ИБ вышла из базиса вычеркиваем столбец этой переменной
    # если M строка занулилась вычеркиваем M строку
    # если в M строке все коэффициенты положительны -> решение оптимально
    # если (решение_оптимально и не_вышла_из_базиса(переменная_ИБ)) система несовместна
    # если (нет_м_строки() и коэфициенты_з_положительны()) решение найдено
    # пока (есть_м_строка() или коэфициенты_з_положительны())
    return (
        simplex_matrix_copy,
        answer,
        intermediate_matrices,
        is_correct,
        many_answers,
        second_answer_matrix,
        second_answer_idxs,
    )


# бесконечно много решений, когда под свободной переменной в Z или M строке 0
# нет решений, когда мы не можем выбрать строку или столбец
def get_answer_from_matrix(answer_matrix, answer_idxs, count_z_str_koeffs):
    values = []
    for rk in range(len(answer_matrix) - 1):
        values.append(answer_matrix[rk][0])

    k = 0
    answer = [Fraction(0)] * count_z_str_koeffs
    for val in values:
        answer[answer_idxs[k] - 1] = val
        k += 1

    answer.append(answer_matrix[len(values)][0])

    return answer


def get_answer_from_many_matricies(
    first_matrix,
    first_answer_idxs,
    second_matrix,
    second_answer_idxs,
    count_z_str_koeffs,
):
    first_answer = get_answer_from_matrix(
        first_matrix, first_answer_idxs, count_z_str_koeffs
    )
    second_answer = get_answer_from_matrix(
        second_matrix, second_answer_idxs, count_z_str_koeffs
    )
    z_value = first_answer.pop()
    second_answer.pop()

    print("X_n")
    print_matrix([first_answer])
    print("X_n+1")
    print_matrix([second_answer])

    first_sympy = [
        Rational(fraction.numerator, fraction.denominator) for fraction in first_answer
    ]
    second_sympy = [
        Rational(fraction.numerator, fraction.denominator) for fraction in second_answer
    ]

    lmbd = symbols("lambda")
    vec1 = Matrix(first_sympy)
    vec2 = Matrix(second_sympy)

    answer = (1 - lmbd) * vec1 + lmbd * vec2
    print(answer)

    simple_answer = sympify(answer)
    print("Simple:")
    print(simple_answer)
    print(str(list(simple_answer)))

    return str(list(simple_answer)), z_value


def is_z_min(z_row):
    if z_row[-1] == Fraction(1):
        return True
    return False


def prepare_for_z_min(matrix):
    prepared_matrix = copy_matrix(matrix)
    for i in range(len(prepared_matrix[-1]) - 1):
        prepared_matrix[-1][i] = -prepared_matrix[-1][i]
    prepared_matrix[-1][-1] = Fraction(0)
    return prepared_matrix


def solve_matrix(
    MATRIX,
    Z_STR,
    INITIAL_Z_STR,
    ANSWERS_FILEPATH="./answer/answer.json",
    is_z_min_system=False,
):
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

    # нужно изменить basis_cols, так как поменялась матрица
    for i in range(len(basis_cols)):
        basis_cols[i] += 1

    # решаем симплекс методом с M строкой
    (
        answer_matrix,
        answer_idxs,
        intermediate_matrices,
        is_correct,
        many_answers,
        second_answer_matrix,
        second_answer_idxs,
    ) = artificial_variable_simplex(
        full_simplex_matrix, len(MATRIX[0]), basis_cols, needed_vars
    )

    # получаем ответ,
    # одна строка последний элемент, то чему равно Z
    answer_object = None
    if many_answers:
        print("Первая матрица:")
        print_matrix(answer_matrix)
        print("Вторая матрица:")
        print_matrix(second_answer_matrix)

        answer, z_value = get_answer_from_many_matricies(
            answer_matrix,
            answer_idxs,
            second_answer_matrix,
            second_answer_idxs,
            len(INITIAL_Z_STR) - 1,
        )

        if is_z_min_system:
            z_value = -z_value

        answer_object = {
            "answer_comment": "единственное решение",
            "answer": answer,
            "z_value": z_value,
        }
    elif is_correct:
        print_matrix(answer_matrix)
        answer = get_answer_from_matrix(
            answer_matrix, answer_idxs, len(INITIAL_Z_STR) - 1
        )
        z_value = answer.pop()

        if is_z_min_system:
            z_value = -z_value

        answer_object = {
            "answer_comment": "единственное решение",
            "answer": answer,
            "z_value": z_value,
        }
    else:
        answer_object = {"answer_comment": "Система ограничений не совместна"}

    full_answer = {}
    for matrix in intermediate_matrices:
        key, value = convert_matrix_to_json_field(matrix)
        full_answer[key] = value
    full_answer["solution"] = answer_object

    write_answer_to_file(ANSWERS_FILEPATH, full_answer)


def all_prepares_for_matrix(MATRIX):
    matrix_z_row = MATRIX[-1]
    is_z_min_system = is_z_min(matrix_z_row)
    if is_z_min_system:
        MATRIX = prepare_for_z_min(MATRIX)

    MATRIX = prepare_matrix(MATRIX)
    Z_STR = MATRIX.pop()
    INITIAL_Z_STR = copy_arr(Z_STR)

    return MATRIX, Z_STR, INITIAL_Z_STR, is_z_min_system


def main() -> None:
    MATRIX_DIR = "0_zlp"
    TASK_ID = "pr07_task8"

    MATRIX = read_matrix_from_file(f"{MATRIX_DIR}/{TASK_ID}.txt")

    DIR_FOR_ANSWERS = "answer"
    ANSWERS_FILEPATH = f"./{DIR_FOR_ANSWERS}/answer.json"

    os.makedirs(DIR_FOR_ANSWERS, exist_ok=True)
    create_or_truncate_file(ANSWERS_FILEPATH)

    MATRIX, Z_STR, INITIAL_Z_STR, is_z_min_system = all_prepares_for_matrix(MATRIX)

    solve_matrix(MATRIX, Z_STR, INITIAL_Z_STR, ANSWERS_FILEPATH, is_z_min_system)


if __name__ == "__main__":
    main()
