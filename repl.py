import readline
import traceback
from tokenizer import tokenize
from parser import parse


def process(expression):
    tokens = tokenize(expression)
    AST = parse(tokens, method="PrattParser")
    AST.print_tree()
    return AST.evaluate()


def main():
    while True:
        try:
            expression = input("> ")
            result = process(expression)
            print(result)
        except EOFError:
            break
        except Exception as e:
            traceback.print_exc()
            continue


if __name__ == "__main__":
    main()
