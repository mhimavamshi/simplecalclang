# parsers: shunting yard, recursive descent, custom idea

from AST import AST, Node

precedence = {
    "operator.plus": 1,
    "operator.minus": 1,
    "operator.divide": 2,
    "operator.multiply": 2,
}


class RecursivePrecedenceReduction:
    """
    Idea:
        to recurse down to base of expression inside parentheses first
        so we only consider them first, for eg. 1 + (2 * 3) we first go to 2 * 3 and then go up recursively
        we scan it and tag all the operators with their position
        we sort them by precedence (we do higher precedence first)
        we sort them by left-to-right positions (left to right associativity)
        then we bracket and reduce - 1 + 2 * 3 => (1 + (2 * 3)) => (1 + 6)
        maybe we bracket the base case and then again recurse? or we bracket all at the beginning and then recurse?
        we will take the sorted positions
        from first to last: make them a node, then take that node and make it child of next node and so on
        operation, left is the first value, right is the node which is a value or another AST

        optional enhancement:
        check distance between lower precedence operators and distance to next one, then parallely build them
    """

    @classmethod
    def get_all_brackets(cls, tokens):
        stack = []
        pairs = []

        for i, token in enumerate(tokens):
            if isinstance(token, Node):
                continue

            token_type, _, _ = token

            if token_type == "lparen":
                stack.append(i)

            elif token_type == "rparen":
                start = stack.pop()
                pairs.append((start, i))

        if stack:
            raise ValueError("Unmatched opening parenthesis")

        return pairs

    @classmethod
    def parse(cls, tokens, tree, depth=0):
        indent = "  " * depth

        print(f"{indent}PARSE CALL")
        print(f"{indent}Tokens: {tokens}")

        brackets = cls.get_all_brackets(tokens)
        print(f"{indent}Brackets: {brackets}")

        if brackets:
            start, end = brackets[-1]

            print(f"{indent}Reducing bracket ({start}, {end})")

            inner = tokens[start + 1 : end]
            print(f"{indent}Inner: {inner}")

            cls.parse(inner, tree, depth + 1)

            node = tree.last_node()

            tokens = tokens[:start] + [node] + tokens[end + 1 :]

            return cls.parse(tokens, tree, depth)

        operator_tokens = sorted(
            [
                (i, t)
                for i, t in enumerate(tokens)
                if not isinstance(t, Node) and t[0].startswith("operator")
            ],
            key=lambda x: (precedence[x[1][0]], x[0]),
        )

        print(f"{indent}Operators: {operator_tokens}")

        if not operator_tokens:
            return

        idx, first = operator_tokens[0]
        left = tokens[idx - 1]
        right = tokens[idx + 1]

        tree.add_node(first, left, right)

        print(f"{indent}Created: {left} {first} {right}")

        for idx, op in operator_tokens[1:]:
            left = tokens[idx - 1]
            right = tree.last_node()

            tree.add_node(op, left, right)

            print(f"{indent}Chained: {left} {op} {right}")

        return

    @classmethod
    def reduce_once(cls, tokens):
        stack = []
        for i, t in enumerate(tokens):
            if isinstance(t, Node):
                continue

            ttype = t[0]
            if ttype == "lparen":
                stack.append(i)
            elif ttype == "rparen":
                start = stack.pop()
                inner_node = cls.parse_efficient(tokens[start + 1 : i])
                tokens[start : i + 1] = [inner_node]
                return True

        best_idx = None
        best_prec = None

        for i, t in enumerate(tokens):
            if isinstance(t, Node):
                continue
            if not t[0].startswith("operator"):
                continue

            prec = precedence[t[0]]

            if best_idx is None or (prec, i) > (best_prec, best_idx):
                best_idx = i
                best_prec = prec

        if best_idx is None:
            return False

        op = tokens[best_idx]
        left = tokens[best_idx - 1]
        right = tokens[best_idx + 1]

        if not isinstance(left, Node):
            left = Node("value", left)
        if not isinstance(right, Node):
            right = Node("value", right)

        new_node = Node("operation", op, left, right)

        tokens[best_idx - 1 : best_idx + 2] = [new_node]

        return True

    @classmethod
    def parse_efficient(cls, tokens):
        tokens = list(tokens)

        while cls.reduce_once(tokens):
            pass

        if len(tokens) != 1:
            raise ValueError(f"Invalid expression: {tokens}")

        result = tokens[0]
        if not isinstance(result, Node):
            result = Node("value", result)

        return result

class PrattParser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        t = self.peek()
        self.pos += 1
        return t

    def parse(self):
        return self.expression(0)


    def expression(self, min_bindp=0):
        # first token
        # figure out what it is
        # if its int, make a int node
        # if its minus its unary and put high bp and recurse forward
        # if its paren, recurse and expect right paren at the end

        token = self.advance()
        if token is None:
            raise ValueError("end of input")

        if token[0] == "int":
            left = Node(AST.VALUE_TYPE, token)
        elif token[0] == "lparen":
            left = self.expression(0)
            self.advance()
        # you can add unary here
        # or a sin function by and funcname token and gathering arguments and making it a left node 
        else:
            raise ValueError(f"Unexpected token: {token}")                

        # base case:
        # check if next is op
        # get the binding power as its the first op
        # if its operator, check its power against min_bindp
        # if its greater than or equal add it as an operation node, and recurse again forward with min_bindp + 1 for left associativity
        # else return back
        # update right to be the recursed above
        # create new node with curr left, op, right 
        # update left to include the new node

        while True:
            op = self.peek()
            if op is None or not op[0].startswith("operator"):
                break

            prec = precedence[op[0]]
            lbp, rbp = prec, prec + 1 # + 1 so left is stronger than right even if same precedence
            # for right associativity (^ operator, dont increment)
            if lbp < min_bindp:
                break

            self.advance()

            right = self.expression(min_bindp=rbp)
            left = Node(AST.OPERATION_TYPE, op, left, right)

        return left


def parse(tokens, method):
    tree = AST()

    if method == "RecursivePrecedenceReduction":
        root = RecursivePrecedenceReduction.parse_efficient(tokens)
        tree._last_node = root
        return tree

    if method == "PrattParser":
        parser = PrattParser(tokens)
        root = parser.parse()
        tree._last_node = root 
        return tree