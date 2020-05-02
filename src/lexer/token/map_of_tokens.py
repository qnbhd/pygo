from src.lexer.token.token_type import token_type as t


class TokensMap:
    map = {
        "package": t.PACKAGE,
        "import" : t.IMPORT,
        "func" : t.FUNC,
        "main": t.MAIN,
        
        "var": t.VAR,
        "int": t.INT,
        "float32": t.FLOAT32,
        "bool": t.BOOL,
        "string": t.STRING,
        "complex64": t.COMPLEX64,
    
        "+": t.PLUS,
        "-": t.MINUS,
        "*": t.STAR,
        "/": t.SLASH,
        "+=": t.ADD_ASSIGN,
        "-=": t.SUB_ASSIGN,
        "*=": t.MUL_ASSIGN,
        "/=": t.DIV_ASSIGN,
        "++": t.INCREMENT,
        "--": t.DECREMENT,

        "for": t.FOR,
        "if": t.IF,
        "switch": t.SWITCH,

        "type": t.TYPE,
        "struct": t.STRUCT,
        "nil": t.NIL,

        "(": t.LPAREN,
        ")": t.RPAREN,
        "[": t.LSQ,
        "]": t.RSQ,
        "{": t.LBRA,
        "}": t.RBRA,
        ":": t.COLON,
        ";": t.SEMICOLON,

        "return": t.RETURN,
        "continue": t.CONTINUE,
        "break": t.BREAK,

        "=": t.ASSIGN,
        "<": t.LESS,
        ">": t.GREATER,

        "==": t.EQUAL,
        "<=": t.LESS_OR_EQUAL,
        ">=": t.GREATER_OR_EQUAL,

        ":=": t.COLON_ASSIGN,

        ".": t.POINT,
        "!": t.EXCLAMATION,
        "?": t.QUESTION,
        ",": t.COMMA

    }
