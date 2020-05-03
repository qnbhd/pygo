# for small project
# to_do delete
from src.parser.ast.node_type import NodeType


class Packages:

    def __init__(self):
        self.default_packages_space = dict()
        self.default_packages_space['fmt'] = {'Println': NodeType.PRINT_OPERATOR}
