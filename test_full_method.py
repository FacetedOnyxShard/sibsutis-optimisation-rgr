import json
import os
from pathlib import Path
import pytest

from main import (
    solve_matrix,
    read_matrix_from_file,
    all_prepares_for_matrix,
)


def run_solver(task_id):
    MATRIX_DIR = "0_zlp"
    DIR_FOR_ANSWERS = "answer"
    result_path = f"./{DIR_FOR_ANSWERS}/answer.json"

    MATRIX = read_matrix_from_file(f"{MATRIX_DIR}/{task_id}.txt")

    MATRIX, Z_STR, INITIAL_Z_STR, is_z_min_system = all_prepares_for_matrix(MATRIX)
    solve_matrix(MATRIX, Z_STR, INITIAL_Z_STR, result_path, is_z_min_system)

    with open(result_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_problem1():
    result = run_solver("pr_task1")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["1", "0", "2"],
        "z_value": "3",
    }
    assert result["solution"] == expected


def test_problem2():
    result = run_solver("pr_task2")
    expected = {"answer_comment": "Система ограничений не совместна"}
    assert result["solution"] == expected


def test_problem3():
    result = run_solver("pr_task3")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["3", "0", "1", "3"],
        "z_value": "2",
    }
    assert result["solution"] == expected


def test_problem4():
    result = run_solver("pr_task4")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["0", "2", "4", "1", "0"],
        "z_value": "-4",
    }
    assert result["solution"] == expected


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


def test_problem7():
    result = run_solver("pr_task7")
    expected = {"answer_comment": "Система ограничений не совместна"}
    assert result["solution"] == expected


def test_problem8():
    result = run_solver("pr_task8")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["5/2", "5/2", "5/2", "0"],
        "z_value": "15",
    }
    assert result["solution"] == expected


def test_problem9():
    result = run_solver("pr_task9")
    expected = {
        "answer_comment": "единственное решение",
        "answer": "[7*lambda/4 + 5/4, 7*lambda/4 + 21/4, 7/2 - 7*lambda/2, 7*lambda/2 + 35/2, 7*lambda, 0]",
        "z_value": "4",
    }
    assert result["solution"] == expected


def test_problem10():  # нельзя выбрать СО
    result = run_solver("pr_task10")
    expected = {"answer_comment": "Система ограничений не совместна"}
    assert result["solution"] == expected


def test_pr07_problem7():
    result = run_solver("pr07_task7")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["2", "0", "0", "0", "3", "0", "0"],
        "z_value": "3",
    }
    assert result["solution"] == expected


def test_pr07_problem8():
    result = run_solver("pr07_task8")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["3", "1", "0", "0", "0", "0", "0"],
        "z_value": "14",
    }
    assert result["solution"] == expected


def test_pr07_problem9():
    result = run_solver("pr07_task9")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["5", "0", "4", "0", "0", "0"],
        "z_value": "14",
    }
    assert result["solution"] == expected


def test_pr07_problem10():
    result = run_solver("pr07_task10")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["4", "3", "0", "0", "0", "0", "0"],
        "z_value": "7",
    }
    assert result["solution"] == expected


def test_pr08_problem1():
    result = run_solver("pr08_task1")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["20", "0", "23", "65", "0"],
        "z_value": "20",
    }
    assert result["solution"] == expected


def test_pr08_problem2():
    result = run_solver("pr08_task2")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["0", "4", "2", "2", "0", "0"],
        "z_value": "12",
    }
    assert result["solution"] == expected


def test_pr08_problem3():
    result = run_solver("pr08_task3")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["0", "10", "0", "0", "10", "20"],
        "z_value": "20",
    }
    assert result["solution"] == expected


def test_pr08_problem4():
    result = run_solver("pr08_task4")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["20", "0", "0", "16", "48", "0"],
        "z_value": "20",
    }
    assert result["solution"] == expected


def test_pr08_problem5():
    result = run_solver("pr08_task5")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["0", "12", "0", "54", "40", "0"],
        "z_value": "12",
    }
    assert result["solution"] == expected


def test_pr08_problem6():
    result = run_solver("pr08_task6")
    expected = {
        "answer_comment": "единственное решение",
        "answer": ["0", "0", "15", "0", "76", "96"],
        "z_value": "15",
    }
    assert result["solution"] == expected
