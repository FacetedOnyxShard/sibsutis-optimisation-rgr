from matrix import *


def prepare_matrix(matrix):
    normalized_matrix = [row for row in matrix if row != []]
    return normalized_matrix


def find_basis_variables(matrix):
    basis_vars = []

    for ck in range(len(matrix[0])):
        basis_var = True
        row_sum = 0
        for rk in range(len(matrix)):
            row_sum += matrix[rk][ck]
            if row_sum > 1:
                basis_var = False
                break

        if not basis_var:
            continue
        basis_vars.append(ck)

    return basis_vars


def artificial_variable_technique():
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
    # находим переменные которые уже образуют базис
    basis_list = find_basis_variables(MATRIX)
    # отнимаем искусственные переменные от Z
    # выводим базисные переменные через свободные
    # подставляем выведенные переменные в Z строку

    # решаем симплекс методом с M строкой
    artificial_variable_technique()

    print_matrix(MATRIX)

    # answer_obj, intermediate_matrices = solve_linear_system(MATRIX)

    # full_answer = {}
    # for matrix in intermediate_matrices:
    #     key, value = convert_matrix_to_json_field(matrix)
    #     full_answer[key] = value
    # full_answer["solution"] = answer_obj

    # write_answer_to_file(ANSWERS_FILEPATH, full_answer)


if __name__ == "__main__":
    main()
