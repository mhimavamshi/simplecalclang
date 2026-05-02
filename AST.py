# AST Node classes, print AST function, evaluate AST


class Node:
    def __init__(self, nodetype, value, left=None, right=None):
        self.nodetype = nodetype
        self.value = value
        self.left = left
        self.right = right

    # def __str__(self):
    #     return f"Node [{id(self)}]: {self.nodetype}, {self.value} and left: {self.left} [{id(self.left) if self.left else None}], right: {self.right} [{id(self.right) if self.right else None}]"

    def __str__(self):
        if self.nodetype == "value" and isinstance(self.value, tuple):
            val = self.value[1]  # ('int', '1', 0) → '1'
        else:
            val = self.value

        left_id = id(self.left) if self.left else None
        right_id = id(self.right) if self.right else None

        return f"Node(id={id(self)}, type={self.nodetype}, value={val}, left_id={left_id}, right_id={right_id})"


class AST:
    
    OPERATION_TYPE = "operation"
    VALUE_TYPE = "value"

    def __init__(self):
        self.nodes = []
        self.root = None
        self._last_node = None



    def add_node(self, operation, left, right):
        if not isinstance(left, Node):
            left = Node(self.VALUE_TYPE, left)
        self.nodes.append(left)
        if not isinstance(right, Node):
            right = Node(self.VALUE_TYPE, right)
        self.nodes.append(right)
        node = Node(self.OPERATION_TYPE, operation, left, right)
        self.nodes.insert(0, node)
        self._last_node = self.nodes[0]

    def last_node(self):
        return self._last_node

    def evaluate(self, node=None):
        if node is None:
            node = self._last_node

        # --- Leaf node ---
        if node.nodetype == self.VALUE_TYPE:
            if isinstance(node.value, tuple):
                return int(node.value[1])
            return int(node.value)

        # --- Operation node ---
        left_val = self.evaluate(node.left)
        right_val = self.evaluate(node.right)

        op_type = node.value[0]

        if op_type == "operator.plus":
            return left_val + right_val
        elif op_type == "operator.minus":
            return left_val - right_val
        elif op_type == "operator.multiply":
            return left_val * right_val
        elif op_type == "operator.divide":
            return left_val / right_val

        raise ValueError(f"Unknown operator: {op_type}")

    def print_tree(self, node=None, indent="", is_left=True):
        if node is None:
            node = self._last_node
            if node is None:
                print("Empty tree")
                return

        prefix = "├── " if is_left else "└── "
        print(indent + prefix + f"{node.nodetype}: {node.value[1]}")

        child_indent = indent + ("│   " if is_left else "    ")

        if node.left:
            self.print_tree(node.left, child_indent, True)
        if node.right:
            self.print_tree(node.right, child_indent, False)
