import readline

operators = {"+", "-", "*", "/"}

def infer_type(pre):
    if pre.isdigit(): return "int"
    if pre in operators: return "operator"
    if pre.isspace(): return "space"
    if pre == ")": return "rparen"
    if pre == "(": return "lparen"
    return None

def merge(state, chars):
    return (state, "".join(chars))

def tokenize(expression):
    """
    state machine
    with a stack 

    number, current state is number, and next char is number
    keep accumulating
    if its another thing, stop accumulating and transition to another state

    """
    tokens = [] 
    store = []  
    zeroed_length = len(expression) - 1

    for index, char in enumerate(expression):
        store.append(char)

        # look ahead instead of current character
        next_char = expression[index+1] if index+1 <= zeroed_length else None
        if not next_char:
            break
  
        curr_type = infer_type(char)
        next_type = infer_type(next_char)
        same = (curr_type == next_type) 


        if not same:
            if not (curr_type == "space"):
                token = merge(curr_type, store)
                tokens.append(token)
            store = []
    
    if store:
        curr_type = infer_type(store[-1])
        if not (curr_type == "space"):
            tokens.append(merge(curr_type, store))
        store = []
   
    return tokens


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

