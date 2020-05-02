from src.lexer.token.token import Token
from src.lexer.lexer import Lexer
from src.parser.ast.ast import AST
from src.parser.ast.node import Node
from src.parser.ast.node_type import NodeType
from src.parser.parser import Parser

if __name__ == "__main__":
    parser = Parser("src/example.go")
    ss = parser.parse()

