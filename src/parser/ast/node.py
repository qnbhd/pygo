from src.parser.ast.node_type import NodeType


class Node:
    type: NodeType
    value: str
    child_nodes: list

    def __init__(self, type_: NodeType, value_: str = "", op1=None, op2=None, op3=None, op4=None):
        self.type = type_
        self.value = value_

        self.op1 = op1
        self.op2 = op2
        self.op3 = op3
        self.op4 = op4

    def hangup_child1(self, child):
        if child is not None and child != self:
            self.child_nodes.append(child)
