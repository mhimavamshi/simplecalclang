# tests/test_evaluate.py

from tokenizer import tokenize
from parser import parse

def eval_expr(expr):
    tokens = tokenize(expr)
    tree = parse(tokens, method="RecursivePrecedenceReduction")
    return tree.evaluate()

def test_simple_add():
    assert eval_expr("1 + 2") == 3

def test_precedence():
    assert eval_expr("1 + 2 * 3") == 7

def test_parentheses():
    assert eval_expr("(1 + 2) * 3") == 9

def test_nested_parentheses():
    assert eval_expr("1 + (2 * (3 + 4))") == 15

def test_multiple_ops():
    assert eval_expr("10 - 2 * 3") == 4

def test_single_number():
    assert eval_expr("42") == 42

def test_nested():
    assert eval_expr("((2+3)*4)") == 20

def test_negative_literal():
    assert eval_expr("-3") == -3

def test_negative_addition():
    assert eval_expr("-3 + 5") == 2

def test_negative_multiplication():
    assert eval_expr("-3 * 2") == -6

def test_negative_inside_parentheses():
    assert eval_expr("(-3 + 5)") == 2

def test_nested_negative():
    assert eval_expr("1 + (-2 * (3 + 4))") == -13

def test_double_negative():
    assert eval_expr("-3 + -2") == -5

def test_subtract_negative():
    assert eval_expr("5 - -3") == 8

def test_negative_parentheses_multiplication():
    assert eval_expr("2 * (-3 + 1)") == -4