from src.parser.ast import ast
from src.lexer.lexer import Lexer
from src.lexer.token.token_type import token_type
from src.lexer.token.token import Token

from src.parser.ast.node import Node
from src.parser.ast.node import NodeType
from src.parser.packages import Packages

debug = True


class Parser:

    def __init__(self, file_path):
        self.lex_ = Lexer()
        self.lex_.read_from_file(file_path)
        self.ast_ = ast.AST()
        self.tokens_ = self.lex_.tokenize()
        self.pos_ = 0
        self.size_ = len(self.tokens_)
        self.packages_map = Packages()

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

    def consume(self, type):
        current = self.get(0)
        if type != current.type_:
            raise RuntimeError("Token " + str(current) + "doesn't match" + str(type))
        self.pos_ += 1
        return current

    def parse(self):

        self.ast_.tree = Node(NodeType.PROGRAM)
        statements = self.program()
        for statement in statements:
            self.ast_.tree.hangup_child(statement)
        self.ast_.print()

    def program(self):
        if debug:
            print("[*] program")
        statements_nodes = list()
        while not self.match(token_type.EOF):
            statements_nodes.append(self.statement())
        return statements_nodes

    def statement(self):
        if debug:
            print("[*] statement")
        if self.match(token_type.IF):
            return self.if_else_block()
        if self.match(token_type.FOR):
            return self.for_block()
        assignment_statement_node = self.assignment_statement()
        return assignment_statement_node

    def if_else_block(self):
        condition = self.expression()

        if_block_statement = self.bracket_expression()
        else_block = None
        if self.match(token_type.ELSE):
            else_block = self.bracket_expression()

        if_else_node = Node(NodeType.IF if else_block is None else NodeType.IF_ELSE, '',
                            condition, if_block_statement, else_block)

        return if_else_node

    def for_block(self):
        initialization = self.assignment_statement()
        self.consume(token_type.SEMICOLON)
        termination = self.expression()
        self.consume(token_type.SEMICOLON)
        increment = self.assignment_statement()
        statement = self.statement_or_block()
        return Node(NodeType.FOR, '', initialization, termination, increment, statement)

    def statement_or_block(self):
        if self.get(0).type_ == token_type.LBRA:
            return self.bracket_expression()
        return self.statement()

    def bracket_expression(self):
        if self.match(token_type.LBRA):
            statement = self.statement()
            if not self.match(token_type.RBRA):
                raise Exception("RIGHT BLOCK-BRACKET WAS EXCEPTED")
            return statement
        else:
            raise Exception("LEFT BLOCK-BRACKET WAS EXCEPTED")

    def assignment_statement(self):
        if debug:
            print("[*] assignment statement")
        current = self.get(0)
        if current.type_ == token_type.IDENTIFIER and self.get(1).type_ == token_type.COLON_ASSIGN:
            self.consume(token_type.IDENTIFIER)
            variable = current.lexeme_
            self.consume(token_type.COLON_ASSIGN)
            return Node(NodeType.VARIABLE_DECLARATION, variable, self.expression())

        expression_node = self.expression()
        return expression_node

    def expression(self):
        if debug:
            print("[*] expression")
        add_node = self.conditional()
        return add_node

    def conditional(self):
        if debug:
            print("[*] conditional")

        add_node = self.add()
        current = self.get(0)

        if current.type_ in [token_type.EQUAL, token_type.NOT_EQUAL, token_type.LESS, token_type.GREATER,
                             token_type.LESS_OR_EQUAL, token_type.GREATER_OR_EQUAL]:
            self.match(current.type_)
            temp_node = self.conditional()
            new_node = Node(current.type_, '', add_node, temp_node)
            return new_node

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
                temp_node = self.unary()
                new_node = Node(NodeType.MUL, '', unary_node, temp_node)
                return new_node
            if self.match(token_type.SLASH):
                temp_node = self.unary()
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

        if self.match(token_type.PLUS):
            temp_node = self.primary()
            new_node = Node(NodeType.UNARY_PLUS, '', temp_node)
            return new_node

        temp_node = self.primary()

        return temp_node

    def primary(self):
        if debug:
            print("[*] primary")
        current = self.get(0)
        if debug:
            print("CURRENT ->", current)
        if self.match(token_type.NUMBER_CONST):
            number_node = Node(NodeType.NUMBER_CONST, current.lexeme_)
            return number_node
        if self.match(token_type.STRING_CONST):
            string_node = Node(NodeType.STRING_CONST, current.lexeme_)
            return string_node
        if self.match(token_type.IDENTIFIER):
            package = current.lexeme_
            if package in self.packages_map.default_packages_space:
                if self.get(0).type_ == token_type.POINT:
                    identifier = self.get(1).lexeme_
                    print(identifier)
                    if self.get(1).type_ == token_type.IDENTIFIER and \
                            identifier in self.packages_map.default_packages_space[package]:
                        self.match(token_type.POINT)
                        pckg_type = self.packages_map.default_packages_space[package][identifier]
                        self.match(token_type.IDENTIFIER)
                        if pckg_type == NodeType.PRINT_OPERATOR:
                            if self.match(token_type.LPAREN):
                                arg = self.expression()
                                print(arg.type_)
                                if arg.type_ not in [NodeType.STRING_CONST, NodeType.NUMBER_CONST]:
                                    raise Exception("STRING OR NUMBER WAS EXPECTED IN PRINT OPERATOR")

                                print(self.get(0))
                                if not self.match(token_type.RPAREN):
                                    raise Exception("RIGHT PAREN WAS EXCEPTED")
                                return Node(NodeType.PRINT_OPERATOR, '', arg)
                            else:
                                raise Exception("LEFT PAREN WAS EXPECTED")
                        else:
                            raise Exception("OPERATOR IS EXISTED BUT NOT IMPLEMENTED IN COMPILER")
                    else:
                        raise Exception("IDENTIFIER IN PACKAGE <" + package + "> WASN'T FINDED OR INCORRECT")
                else:
                    raise Exception("POINT BEFORE 2 INDENTIFIER EXPECTED")

        if current.type_ == token_type.LPAREN:
            return self.par_expression()

        raise Exception("[UNKNOWN TOKEN]")

    def par_expression(self):
        if not self.match(token_type.LPAREN):
            raise Exception("LEFT PAREN WAS EXCEPTED")
        expr_node = self.expression()
        if not self.match(token_type.RPAREN):
            raise Exception("RIGHT PAREN WAS EXCEPTED")
        return expr_node
