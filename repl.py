import readline
from tokenizer import tokenize
from parser import parse
from AST import print_AST, evaluate_AST

def process(expression):
    tokens = tokenize(expression)    
    AST = parse(tokens)
    print_AST(AST)
    result = evaluate_AST(AST)
    return result

def main():
    while True:
        expression = input("> ")
        result = process(expression)
        print(result)

if __name__ == "__main__":
    main()

