import readline
from tokenizer import tokenize

def process(expression):
    tokens = tokenize(expression)    
    return tokens

def main():
    while True:
        expression = input("> ")
        result = process(expression)
        print(result)

if __name__ == "__main__":
    main()

