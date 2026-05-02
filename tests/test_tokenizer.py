# tests/test_tokenizer.py

from tokenizer import tokenize

def test_basic_tokens():
    tokens = tokenize("1 + 2")
    types = [t[0] for t in tokens]

    assert types == ["int", "operator.plus", "int"]

def test_parentheses():
    tokens = tokenize("(1 + 2)")
    types = [t[0] for t in tokens]

    assert types == ["lparen", "int", "operator.plus", "int", "rparen"]

def test_invalid_parentheses():
    import pytest
    with pytest.raises(ValueError):
        tokenize("(1 + 2")

def test_negative_number():
    tokens = tokenize("-3")
    assert tokens[0][0] == "int"
    assert tokens[0][1] == "-3"


def test_negative_after_operator():
    tokens = tokenize("5 + -3")
    values = [t[1] for t in tokens]
    assert values == ["5", "+", "-3"]


def test_double_negative():
    tokens = tokenize("-3 + -2")
    values = [t[1] for t in tokens]
    assert values == ["-3", "+", "-2"]


def test_multi_digit_numbers():
    tokens = tokenize("12 + 345")
    values = [t[1] for t in tokens]
    assert values == ["12", "+", "345"]


def test_no_spaces():
    tokens = tokenize("1+2*3")
    types = [t[0] for t in tokens]
    assert types == ["int", "operator.plus", "int", "operator.multiply", "int"]


def test_mixed_spacing():
    tokens = tokenize("  1   +   2 ")
    values = [t[1] for t in tokens]
    assert values == ["1", "+", "2"]


def test_nested_parentheses():
    tokens = tokenize("((1+2)*3)")
    types = [t[0] for t in tokens]
    assert types == [
        "lparen", "lparen", "int", "operator.plus", "int", "rparen",
        "operator.multiply", "int", "rparen"
    ]


def test_division_operator():
    tokens = tokenize("6 / 3")
    assert tokens[1][0] == "operator.divide"


def test_invalid_char():
    tokens = tokenize("1 + a")
    types = [t[0] for t in tokens]
    assert None in types  # current behavior