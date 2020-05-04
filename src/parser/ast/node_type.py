from enum import Enum, auto


class NodeType(Enum):
    IDENTIFIER = auto(),

    VARIABLE_DECLARATION = auto(),
    USING_VARIABLE = auto(),
    VARIABLE_TYPE = auto(),

    CONSTANT_DECLARATION = auto(),
    USING_CONSTANT = auto(),
    NUMBER_CONST = auto(),
    BOOLEAN_CONST = auto(),
    STRING_CONST = auto(),

    # math
    ADD = auto(),
    SUB = auto(),
    MUL = auto(),
    DIV = auto(),

    BEFORE_INC = auto(),
    BEFORE_DEC = auto(),

    AFTER_INC = auto(),
    AFTER_DEC = auto(),

    UNARY_PLUS = auto(),
    UNARY_MINUS = auto(),
    UNARY_EXCLAMATION = auto(),

    # logical
    LOGICAL_AND = auto(),
    LOGICAL_OR = auto(),

    # setter
    SET = auto(),

    LESS = auto(),  # <
    GREATER = auto(),  # >
    EQUAL = auto(),  # ==
    NOT_EQUAL = auto(),  # !=
    LESS_EQUAL = auto(),  # <=
    GREATER_EQUAL = auto(),  # >=

    # cycles
    DO_WHILE = auto(),
    FOR = auto(),
    WHILE = auto(),
    #
    BREAK = auto(),
    CONTINUE = auto(),

    # conditions
    IF = auto(),
    IF_ELSE = auto(),

    INDEX_CAPTURE = auto(),

    # function
    FUNCTION_CALL = auto(),
    FUNCTION_ARGS = auto(),
    FUNCTION_ARG = auto(),

    RETURN = auto(),

    FUNCTION_IMPLEMENTATION = auto(),
    FUNCTION_IMPLEMENTATION_ARG = auto(),
    FUNCTION_IMPLEMENTATION_ARGS = auto(),
    FUNCTION_IMPLEMENTATION_RETURN_TYPE = auto(),

    # expression
    EXPRESSION = auto(),
    CONST_EXPRESSION = auto(),

    STATEMENT = auto(),
    SEQ_STATEMENT = auto(),
    STATEMENT_LIST = auto(),

    INITIALIZER = auto(),
    INITIALIZER_LIST = auto(),

    NEW = auto(),

    PROGRAM = auto(),

    DECLARATION_TYPE = auto(),

    FUNCTION_IMPLEMENTATION_NEW = auto(),
    FUNCTION_IMPLEMENTATION_NEW_ARGS = auto(),
    FUNCTION_IMPLEMENTATION_NEW_ARG = auto(),

    PRINT_OPERATOR = auto(),

    OR = auto(),
    AND = auto(),

    BRACKET_BLOCK = auto(),
    PACKAGE = auto(),
    IMPORT = auto()

