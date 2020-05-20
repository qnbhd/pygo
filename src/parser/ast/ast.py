from src.parser.ast.node import Node
from src.parser.ast.node_type import NodeType


class AST:
    tree: Node

    def __init__(self):
        self.tree = None

    def print_recursive(self, current_node: Node, level: int):
        if current_node is None:
            return

        for i in range(level):
            print('   ', end='')
        print("+-", end='')

        print(self.calculate_name(current_node.type), end=' ')

        if current_node.value != "":
            print("'" + current_node.value + "'")
        else:
            print("")

        self.print_recursive(current_node.op1, level + 1)
        self.print_recursive(current_node.op2, level + 1)
        self.print_recursive(current_node.op3, level + 1)
        self.print_recursive(current_node.op4, level + 1)

    def print(self):
        self.print_recursive(self.tree, 0)

    @staticmethod
    def calculate_name(node_type: NodeType) -> str:
        return str(node_type).split('.')[1].upper()
