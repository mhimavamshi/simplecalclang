# parsers: shunting yard, recursive descent, custom idea

from AST import AST, Node

precedence = {
    "operator.plus": 2,
    "operator.minus": 2,
    "operator.divide": 1,
    "operator.multiply": 1,
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

            if best_idx is None or (prec, i) < (best_prec, best_idx):
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


def parse(tokens, method):
    if method == "RecursivePrecedenceReduction":
        root = RecursivePrecedenceReduction.parse_efficient(tokens)
        tree = AST()
        tree._last_node = root
        return tree
