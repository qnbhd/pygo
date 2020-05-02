from src.parser.ast import ast
from src.lexer.lexer import Lexer
from src.lexer.token.token_type import token_type
from src.lexer.token.token import Token

from src.parser.ast.node import Node
from src.parser.ast.node import NodeType

debug = False


class Parser:

    def __init__(self, file_path):
        self.lex_ = Lexer()
        self.lex_.read_from_file(file_path)
        self.ast_ = ast.AST()
        self.tokens_ = self.lex_.tokenize()
        self.pos_ = 0
        self.size_ = len(self.tokens_)

    def parse(self):
        result = list()
        """while not self.match(token_type.EOF):
            result.append(self.program())"""
        self.ast_.tree = self.program()
        self.ast_.print()

    def get(self, relative_position) -> Token:
        position = self.pos_ + relative_position
        if position >= self.size_:
            return Token('\0')
        return self.tokens_[position]

    def match(self, type: token_type) -> bool:
        current = self.get(0)
        if type != current.type_:
            return False
        self.pos_ += 1
        return True

    def program(self):
        if debug:
            print("[*] program")
        statement_node = self.statement()
        return statement_node

    def statement(self):
        if debug:
            print("[*] statement")
        expression_node = self.expression()
        return expression_node

    def expression(self):
        if debug:
            print("[*] expression")
        add_node = self.add()
        return add_node

    def add(self):
        if debug:
            print("[*] add")

        multy_node = self.multy()

        while True:
            if self.match(token_type.PLUS):
                temp_node = self.add()
                new_node = Node(NodeType.ADD, '', multy_node, temp_node)
                return new_node
            if self.match(token_type.MINUS):
                temp_node = self.add()
                new_node = Node(NodeType.SUB, '', multy_node, temp_node)
                return new_node
            break

        return multy_node

    def multy(self):
        if debug:
            print("[*] multy")

        unary_node = self.unary()

        while True:
            if self.match(token_type.STAR):
                temp_node = self.multy()
                new_node = Node(NodeType.MUL, '', unary_node, temp_node)
                return new_node
            if self.match(token_type.SLASH):
                temp_node = self.multy()
                new_node = Node(NodeType.DIV, '', unary_node, temp_node)
                return new_node
            break

        return unary_node

    def unary(self):
        if debug:
            print("[*] unary")

        if self.match(token_type.MINUS):
            temp_node = self.primary()
            new_node = Node(NodeType.UNARY_MINUS, '', temp_node)
            return new_node

        temp_node = self.primary()

        return temp_node

    def primary(self):
        if debug:
            print("[*] primary")
        current = self.get(0)
        #print("BBB", current)
        if self.match(token_type.NUMBER_CONST):
            number_node = Node(NodeType.NUMBER_CONST, current.lexeme_)
            return number_node
        if self.match(token_type.STRING_CONST):
            string_node = Node(NodeType.STRING_CONST, current.lexeme_)
            return string_node
        if self.match(token_type.LPAREN):
            expr_node = self.expression()
            if not self.match(token_type.RPAREN):
                raise Exception("RIGHT PAREN WAS EXCEPTED")
            return expr_node

        raise Exception("[UNKNOWN TOKEN]")
