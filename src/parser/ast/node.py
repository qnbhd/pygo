from src.parser.ast.node_type import NodeType


class Node:

    def __init__(self, type, value="", op1=None, op2=None, op3=None, op4=None):
        self.type_ = type
        self.value_ = value
        self.op1_, self.op2_, self.op3_, self.op4_ = op1, op2, op3, op4

    def print(self):
        pass
