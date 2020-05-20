from enum import Enum, auto


class NodeType(Enum):
    IDENTIFIER = auto(),

    VARIABLE_DECLARATION = auto(),
    USING_VARIABLE = auto(),

    NUMBER_CONST = auto(),

    STRING_CONST = auto(),

    # math
    ADD = auto(),
    SUB = auto(),
    MUL = auto(),
    DIV = auto(),

    UNARY_MINUS = auto(),

    # setter
    SET = auto(),

    LESS = auto(),  # <
    GREATER = auto(),  # >
    EQUAL = auto(),  # ==
    NOT_EQUAL = auto(),  # !=
    LESS_EQUAL = auto(),  # <=
    GREATER_EQUAL = auto(),  # >=

    # cycles
    FOR = auto(),

    # conditions
    IF = auto(),
    IF_ELSE = auto(),

    # expression
    EXPRESSION = auto(),

    STATEMENT = auto(),
    SEQ_STATEMENT = auto(),
    STATEMENT_LIST = auto(),

    PROGRAM = auto(),

    OR = auto(),
    AND = auto(),

    BRACKET_BLOCK = auto(),
    PACKAGE = auto(),
    IMPORT = auto()
