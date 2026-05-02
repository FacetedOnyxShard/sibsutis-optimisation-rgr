import json
import sys
from pathlib import Path
import pytest

import os
from main import (
    solve_matrix,
    prepare_matrix,
    copy_arr,
    read_matrix_from_file,
    create_or_truncate_file,
)


def test_simplex_solution(tmp_path, monkeypatch):
    """
    Проверяет, что для заданной входной матрицы программа формирует
    правильный объект 'solution' в выходном JSON-файле.
    """

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

    solve_matrix(MATRIX, Z_STR, INITIAL_Z_STR)

    result_path = "./answer/answer.json"
    assert os.path.exists(result_path), "Файл answer.json не создан"
    with open(result_path, "r", encoding="utf-8") as f:
        result = json.load(f)

    expected_solution = {
        "answer_comment": "единственное решение",
        "answer": ["3", "0", "1", "3"],
        "z_value": "2",
    }

    assert "solution" in result, "В ответе отсутствует ключ 'solution'"
    assert result["solution"] == expected_solution, (
        f"Несовпадение решения: получено {result['solution']}, "
        f"ожидалось {expected_solution}"
    )
