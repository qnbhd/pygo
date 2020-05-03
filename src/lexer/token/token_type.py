from enum import Enum, auto


class token_type(Enum):
    NUMBER_CONST = auto(),
    STRING_CONST = auto(),

    PACKAGE = auto(),
    IMPORT = auto(),
    FUNC = auto(),
    MAIN = auto(),

    VAR = auto(),
    INT = auto(),
    FLOAT32 = auto(),
    BOOL = auto(),
    STRING = auto(),
    COMPLEX64 = auto(),

    PLUS = auto(),
    MINUS = auto(),
    STAR = auto(),
    SLASH = auto(),

    ADD_ASSIGN = auto(),
    SUB_ASSIGN = auto(),
    MUL_ASSIGN = auto(),
    DIV_ASSIGN = auto(),

    INCREMENT = auto(),
    DECREMENT = auto(),

    FOR = auto(),
    IF = auto(),
    ELSE = auto(),
    SWITCH = auto(),

    TYPE = auto(),
    STRUCT = auto(),
    NIL = auto(),

    LPAREN = auto(),
    RPAREN = auto(),

    LSQ = auto(),
    RSQ = auto(),

    LBRA = auto(),
    RBRA = auto(),

    COLON = auto(),
    SEMICOLON = auto(),

    IDENTIFIER = auto(),

    RETURN = auto(),
    BREAK = auto(),
    CONTINUE = auto(),

    ASSIGN = auto(),  # =
    LESS = auto(),  # <
    GREATER = auto(),  # >

    EQUAL = auto(),  # ==
    NOT_EQUAL = auto(),
    LESS_OR_EQUAL = auto(),  # <=
    GREATER_OR_EQUAL = auto(),  # >=

    COLON_ASSIGN = auto(),  # :=

    POINT = auto()

    COMMA = auto(),
    QUESTION = auto(),
    EXCLAMATION = auto()

    LEFT_STRING = auto(),
    RIGHT_STRING = auto(),

    EOF = auto()

    ONE_LINE_COMMENT = auto(),
    LEFT_MULTI_LINE_COMMENT = auto(),
    RIGHT_MULTI_LINE_COMMENT = auto()
