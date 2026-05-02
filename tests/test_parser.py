# tests/test_parser.py

from tokenizer import tokenize
from parser import parse

def test_root_operator():
    tokens = tokenize("1 + 2 * 3")
    tree = parse(tokens, method="RecursivePrecedenceReduction")
    root = tree._last_node

    assert root.value[0] == "operator.plus"
    assert root.right.value[0] == "operator.multiply"

def test_negative_literal_root():
    tokens = tokenize("-3")
    tree = parse(tokens, method="RecursivePrecedenceReduction")
    root = tree._last_node

    assert root.nodetype == "value"
    assert root.value[1] == "-3"


def test_negative_addition_structure():
    tokens = tokenize("-3 + 5")
    tree = parse(tokens, method="RecursivePrecedenceReduction")
    root = tree._last_node

    assert root.value[0] == "operator.plus"
    assert root.left.value[1] == "-3"
    assert root.right.value[1] == "5"


def test_negative_multiplication_structure():
    tokens = tokenize("-3 * 2")
    tree = parse(tokens, method="RecursivePrecedenceReduction")
    root = tree._last_node

    assert root.value[0] == "operator.multiply"
    assert root.left.value[1] == "-3"
    assert root.right.value[1] == "2"


def test_negative_inside_parentheses_structure():
    tokens = tokenize("(-3 + 5)")
    tree = parse(tokens, method="RecursivePrecedenceReduction")
    root = tree._last_node

    assert root.value[0] == "operator.plus"
    assert root.left.value[1] == "-3"
    assert root.right.value[1] == "5"


def test_subtract_negative_structure():
    tokens = tokenize("5 - -3")
    tree = parse(tokens, method="RecursivePrecedenceReduction")
    root = tree._last_node

    assert root.value[0] == "operator.minus"
    assert root.left.value[1] == "5"
    assert root.right.value[1] == "-3"