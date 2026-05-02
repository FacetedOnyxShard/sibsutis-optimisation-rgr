import json
import os
from pathlib import Path
import pytest

from main import (
    solve_matrix,
    prepare_matrix,
    copy_arr,
    read_matrix_from_file,
    create_or_truncate_file,
)

MATRIX_DIR = "0_zlp"
DIR_FOR_ANSWERS = "answer"


def setup_answer_dir():
    os.makedirs(DIR_FOR_ANSWERS, exist_ok=True)
    create_or_truncate_file(f"./{DIR_FOR_ANSWERS}/answer.json")


def run_solver(task_id):
    MATRIX = read_matrix_from_file(f"{MATRIX_DIR}/{task_id}.txt")
    setup_answer_dir()
    MATRIX = prepare_matrix(MATRIX)
    Z_STR = MATRIX.pop()
    INITIAL_Z_STR = copy_arr(Z_STR)
    solve_matrix(MATRIX, Z_STR, INITIAL_Z_STR)
    result_path = f"./{DIR_FOR_ANSWERS}/answer.json"
    with open(result_path, "r", encoding="utf-8") as f:
        return json.load(f)


# def test_problem1():
#     result = run_solver("pr_task1")
#     expected = {
#         "answer_comment": "единственное решение",
#         "answer": ["1", "0", "2"],
#         "z_value": "3",
#     }
#     assert result["solution"] == expected


# def test_problem2():
#     result = run_solver("pr_task2")
#     expected = {"answer_comment": "Система ограничений не совместна"}
#     assert result["solution"] == expected


def test_problem3():
    result = run_solver("pr_task3")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["3", "0", "1", "3"],
        "z_value": "2",
    }
    assert result["solution"] == expected


# def test_problem4():
#     result = run_solver("pr_task4")
#     expected = {
#         "answer_comment": "единственное решение",
#         "answer": ["0", "2", "4", "1", "0"],
#         "z_value": "-4",
#     }
#     assert result["solution"] == expected


def test_problem5():
    result = run_solver("pr_task5")
    expected = {"answer_comment": "Система ограничений не совместна"}
    assert result["solution"] == expected


def test_problem6():
    result = run_solver("pr_task6")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["0", "6", "0", "4"],
        "z_value": "42",
    }
    assert result["solution"] == expected


# def test_problem7():
#     result = run_solver("pr_task7")
#     expected = {"answer_comment": "Система ограничений не совместна"}
#     assert result["solution"] == expected


def test_problem8():
    result = run_solver("pr_task8")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["5/2", "5/2", "5/2", "0"],
        "z_value": "15",
    }
    assert result["solution"] == expected
