from src.parser.ast.node_type import NodeType


class Node:

    def __init__(self, type, value="", op1=None, op2=None, op3=None, op4=None):
        self.type_ = type
        self.value_ = value
        self.child_nodes_ = list()
        self.child_nodes_.append(op1)
        if op2 is not None:
            self.child_nodes_.append(op2)
        if op3 is not None:
            self.child_nodes_.append(op3)
        if op4 is not None:
            self.child_nodes_.append(op4)

    def hangup_child(self, child):
        if child is not None and child != self:
            self.child_nodes_.append(child)
