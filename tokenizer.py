operators = {"+": "plus", "-": "minus", "*": "multiply", "/": "divide"}

def infer_type(pre):
    if pre.isdigit(): return "int"
    if pre in operators: return f"operator.{operators[pre]}"
    if pre.isspace(): return "space"
    if pre == ")": return "rparen"
    if pre == "(": return "lparen"
    return None

def can_accumulate(pre, post):
    if pre == "operator.minus" and post == "int":
        return True
    if pre == "int" and post == "int":
        return True
    return False


def merge(state, chars):
    return (state, "".join(chars))

def tokenize(expression):
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
        accumulate = can_accumulate(curr_type, next_type) 


        if not accumulate:
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
