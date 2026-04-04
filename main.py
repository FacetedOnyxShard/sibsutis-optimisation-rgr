from matrix import *


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

    for ck in range(len(matrix[0])):
        if matrix[0][ck] != Fraction(0):
            continue

        if is_basis_col(ck, matrix):
            basis_cols.append(ck)

    # выводим
    equalities = []
    for bk in basis_cols:
        for rk in range(len(matrix)):
            if matrix[rk][bk] == Fraction(1):
                # нужная строка, из нее можно вывести x_{bk + 1}

                break

    return equalities


def add_basis_vars(matrix, z_str, needed_vars, basis_list):
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

        cur_var_idx += 1
        addition_rows.append(row)

    #
    simplex_matrix = copy_matrix(matrix)
    for rk in range(len(matrix)):
        simplex_matrix[rk].extend(addition_rows[rk])

    return simplex_matrix


def artificial_variable_simplex():
    # симплекс метод с M строкой
    # выбираем столбец (самое большое отрицательное число среди коэффициентов)
    # выбираем строку (самое маленькое симплексное отношение)
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
    Z_STR = [MATRIX.pop()]  # перевод списка в массив

    # находим переменные которые уже образуют базис
    basis_list = find_basis_variables(MATRIX)

    # добавляем искусственные переменные в базис
    needed_vars = len(MATRIX) - len(basis_list)
    simplex_matrix = add_basis_vars(MATRIX, Z_STR, needed_vars, basis_list)

    # выводим базисные переменные через свободные
    basis_vars_equalities = derive_basis_vars(simplex_matrix)

    # подставляем выведенные переменные в Z строку

    # отнимаем искусственные переменные от Z и добаляем их в матрицу
    # simplex_matrix, simplex_z_str, simplex_m_str = prepare_for_simplex(
    #     MATRIX, Z_STR, needed_vars, basis_list
    # )

    # решаем симплекс методом с M строкой
    artificial_variable_simplex()

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
