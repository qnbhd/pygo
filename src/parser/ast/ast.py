from src.parser.ast import node
from src.parser.ast.node import Node
from src.parser.ast.node_type import NodeType
from math import exp


class AST:

    def __init__(self):
        self.tree = None

    def r_traversal(self, current_node):
        if node is None:
            return

        # some actions

        self.r_traversal(current_node.op1_)
        self.r_traversal(current_node.op2_)
        self.r_traversal(current_node.op3_)
        self.r_traversal(current_node.op4_)

    def _print(self, current_node, level):
        if current_node is None:
            return

        # print(" " * level, end='')
        buffer = ""
        for i in range(level):
            buffer += '| '

        print(buffer, end='')

        print("[*] ", end='')
        print(self.calculate_name(current_node.type_), end=' ')
        if current_node.value_ != "":
            print("(" + current_node.value_ + ")")
        else:
            print()

        self._print(current_node.op1_, level + 1)
        self._print(current_node.op2_, level + 1)
        self._print(current_node.op3_, level + 1)
        self._print(current_node.op4_, level + 1)

    def print(self):
        self._print(self.tree, 0)

    @staticmethod
    def calculate_name(node_type: NodeType) -> str:
        return str(node_type).split('.')[1].upper()
