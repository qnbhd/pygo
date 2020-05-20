from src.parser.ast.ast import AST as Ast
from src.lexer.lexer import Lexer
from src.lexer.token.token_type import TokenType
from src.lexer.token.token import Token

from src.parser.ast.node import Node
from src.parser.ast.node import NodeType
from src.parser.packages import Packages


debug = True


class Parser:
    lexer: Lexer
    ast: Ast

    tokens: list
    pos: int

    tokens_count: int


    def __init__(self, file_path):
        self.lexer = Lexer()
        self.lexer.read_from_file(file_path)
        self.ast = Ast()
        self.tokens = self.lexer.tokenize()
        self.pos = 0

        self.lexer.print()

        self.tokens_count = len(self.tokens)
        self.packages_map = Packages()

        self.in_block_not_main = False

    def get(self, relative_position: int) -> Token:
        position = self.pos + relative_position
        if position >= self.tokens_count:
            return Token('\0')
        return self.tokens[position]

    def match(self, type_: TokenType) -> bool:
        current = self.get(0)

        if type_ != current.type:
            return False

        self.pos += 1
        return True

    def consume(self, type_: TokenType) -> Token:
        current = self.get(0)

        if type_ != current.type:
            raise RuntimeError("Token " + str(current) + "doesn't match" + str(type_))

        self.pos += 1
        return current

    def parse(self):
        self.ast.tree = Node(NodeType.PROGRAM)

        if not self.match(TokenType.PACKAGE):
            raise RuntimeError("PACKAGE NAME EXCEPTED")

        package_name = ''

        if self.get(0).type == TokenType.MAIN:
            package_name = 'main'
            self.consume(TokenType.MAIN)
        elif self.get(0).type == TokenType.IDENTIFIER:
            package_name = self.get(0)
            self.consume(TokenType.IDENTIFIER)

        package_node: Node = Node(NodeType.PACKAGE, package_name)

        # if self.match(TokenType.IMPORT):
        #
        #     self.consume(TokenType.LPAREN)
        #     import_node = Node(NodeType.IMPORT)
        #
        #     while not self.match(TokenType.RPAREN):
        #         import_node.hangup_child(self.primary())
        #
        #     package.hangup_child(import_node)

        self.consume(TokenType.FUNC)

        function_name_token: Token = self.get(0)

        if function_name_token.lexeme != package_name:
            raise RuntimeError("PACKAGE NAME AND INPUT POINT NAME ISN'T EQUAL")

        if function_name_token.lexeme == 'main':
            self.consume(TokenType.MAIN)
        else:
            self.consume(TokenType.IDENTIFIER)

        self.consume(TokenType.LPAREN)
        self.consume(TokenType.RPAREN)

        statement = self.bracket_expression()

        statement_list_package_node: Node = Node(NodeType.STATEMENT_LIST, '', package_node)
        statement_list_node: Node = Node(NodeType.STATEMENT_LIST, '', statement_list_package_node, statement)

        self.ast.tree.op1 = statement_list_node

        print("-------------AST TREE-------------")
        self.ast.print()
        print("----------VARIABLE TABLE----------")
        self.ast.variables.print()

    def bracket_expression(self) -> Node:

        self.consume(TokenType.LBRA)

        node = None

        while not self.match(TokenType.RBRA):
            statement_node = self.statement()
            node = Node(NodeType.STATEMENT_LIST, '', node, statement_node)

        return node

    def program(self) -> Node:
        node = None

        while not self.match(TokenType.EOF):
            statement_node = self.statement()
            node = Node(NodeType.STATEMENT_LIST, '', node, statement_node)

        return node

    def statement(self) -> Node:
        if self.match(TokenType.IF):
            return self.if_else_block()

        if self.match(TokenType.FOR):
            return self.for_block()

        return self.expression_statement()

    def if_else_block(self) -> Node:
        condition = self.expression()

        node_type = NodeType.IF

        if_block_statement = self.bracket_expression()

        else_block = None
        if self.match(TokenType.ELSE):
            node_type = NodeType.IF_ELSE
            self.match(TokenType.IF)
            else_block = self.if_else_block()

        return Node(node_type, '', condition, if_block_statement, else_block)

    def for_block(self) -> Node:
        initialization_node: Node = self.expression_statement()
        self.consume(TokenType.SEMICOLON)

        condition_node: Node = self.expression()
        self.consume(TokenType.SEMICOLON)

        aftereffect_node: Node = self.expression_statement()

        statement_node: Node = self.bracket_expression()

        return Node(NodeType.FOR, '', initialization_node, condition_node, aftereffect_node, statement_node)

    def declaration_statement(self) -> Node:
        current: Token = self.get(0)

        self.consume(TokenType.IDENTIFIER)
        variable_name: str = current.lexeme
        self.consume(TokenType.COLON_ASSIGN)

        self.ast.variables.add(variable_name)

        expression_node: Node = self.expression()
        variable_declaration_node: Node = Node(NodeType.VARIABLE_DECLARATION, variable_name)

        return Node(NodeType.SET, '', variable_declaration_node, expression_node)

    def expression_statement(self) -> Node:
        return self.expression()

    def expression(self) -> Node:
        return self.assignment_expression()

    def assignment_expression(self) -> Node:
        node: Node = self.logical_or()

        if self.match(TokenType.ASSIGN):

            assignment_expression_node: Node = self.assignment_expression()

            return Node(NodeType.SET, '', node, assignment_expression_node)

        return node

    def logical_or(self) -> Node:
        node: Node = self.logical_and()

        if self.match(TokenType.OR):
            return Node(NodeType.OR, '', node, self.logical_or())

        return node

    def logical_and(self) -> Node:
        node: Node = self.equality()

        if self.match(TokenType.AND):
            return Node(NodeType.AND, '', node, self.logical_and())

        return node

    def equality(self) -> Node:
        result: Node = self.conditional()

        if self.match(TokenType.EQUAL):
            return Node(NodeType.EQUAL, '', result, self.conditional())

        if self.match(TokenType.NOT_EQUAL):
            return Node(NodeType.NOT_EQUAL, '', result, self.conditional())

        return result

    def conditional(self) -> Node:
        result: Node = self.add()

        if self.match(TokenType.LESS):
            return Node(NodeType.LESS, '', result, self.add())

        if self.match(TokenType.GREATER):
            return Node(NodeType.GREATER, '', result, self.add())

        if self.match(TokenType.LESS_OR_EQUAL):
            return Node(NodeType.LESS_EQUAL, '', result, self.add())

        if self.match(TokenType.GREATER_OR_EQUAL):
            return Node(NodeType.GREATER_EQUAL, '', result, self.add())

        return result

    def add(self) -> Node:
        multy_node: Node = self.multy()

        if self.match(TokenType.PLUS):
            temp_node = self.add()
            return Node(NodeType.ADD, '', multy_node, temp_node)

        if self.match(TokenType.MINUS):
            temp_node = self.add()
            return Node(NodeType.SUB, '', multy_node, temp_node)

        return multy_node

    def multy(self) -> Node:
        unary_node: Node = self.unary()

        if self.match(TokenType.STAR):
            temp_node = self.multy()
            return Node(NodeType.MUL, '', unary_node, temp_node)

        if self.match(TokenType.SLASH):
            temp_node = self.multy()
            return Node(NodeType.DIV, '', unary_node, temp_node)

        return unary_node

    def unary(self) -> Node:
        if self.match(TokenType.MINUS):
            temp_node: Node = self.primary()
            return Node(NodeType.UNARY_MINUS, '', temp_node)

        return self.primary()

    def primary(self) -> Node:
        current: Token = self.get(0)

        if self.match(TokenType.NUMBER_CONST):
            number_node: Node = Node(NodeType.INTEGER_CONST, current.lexeme)
            return number_node

        if self.match(TokenType.STRING_CONST):
            string_node: Node = Node(NodeType.STRING_CONST, current.lexeme)
            return string_node

        if current.type == TokenType.IDENTIFIER and self.get(1).type == TokenType.COLON_ASSIGN:
            return self.declaration_statement()

        if self.match(TokenType.IDENTIFIER):
            identifier: str = current.lexeme

            if self.package_is_exists(identifier):
                return self.package_identifier(identifier)

            if self.ast.variables.contains(identifier):
                return Node(NodeType.USING_VARIABLE, identifier)

        if current.type == TokenType.LPAREN:
            return self.par_expression()

        return None

    def par_expression(self) -> Node:
        if not self.match(TokenType.LPAREN):
            raise Exception("LEFT PAREN WAS EXCEPTED")

        expr_node: Node = self.expression()

        if not self.match(TokenType.RPAREN):
            raise Exception("RIGHT PAREN WAS EXCEPTED")

        return expr_node

    def package_is_exists(self, identifier):
        return identifier in self.packages_map.default_packages_space

    def package_identifier(self, package):
        if self.get(0).type == TokenType.POINT:
            identifier = self.get(1).lexeme
            if self.get(1).type == TokenType.IDENTIFIER and \
                    identifier in self.packages_map.default_packages_space[package]:
                self.match(TokenType.POINT)
                pckg_type = self.packages_map.default_packages_space[package][identifier]
                self.match(TokenType.IDENTIFIER)
                if pckg_type == NodeType.PRINT_OPERATOR:
                    if self.match(TokenType.LPAREN):
                        arg = self.expression()
                        if arg.type not in [NodeType.STRING_CONST, NodeType.INTEGER_CONST]:
                            raise Exception("STRING OR NUMBER WAS EXPECTED IN PRINT OPERATOR")

                        if not self.match(TokenType.RPAREN):
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
