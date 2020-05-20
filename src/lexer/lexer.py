from src.lexer.token.token import Token
from src.lexer.token.token_type import TokenType


class Lexer:
    code: str
    tokens: [Token]

    def __init__(self, code=""):
        self.code = code
        self.tokens = []

    def read_from_file(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as fin:
            self.code = fin.read()

    def tokenize(self) -> list:
        buffer = ""
        record_string = False
        for i, sym in enumerate(self.code):
            if sym == "\"":
                record_string = not record_string
            if self.is_sep(sym):
                if buffer != "":
                    self.tokens.append(Token(buffer))
                    buffer = ""
                if record_string or (sym != " " and sym != '\n' and sym != '\t'):
                    self.tokens.append(Token(sym))
            else:
                buffer += sym

        if buffer != "":
            self.tokens.append(Token(buffer))

        self.adj_sub()
        return self.tokens

    def adj_sub(self):
        hatch_tokens = []
        i = 0
        while i < len(self.tokens):
            if i < len(self.tokens) - 2 and self.is_adj_decimal(self.tokens[i], self.tokens[i + 1]):
                token = Token(self.tokens[i].lexeme + self.tokens[i + 1].lexeme + self.tokens[i + 2].lexeme)
                hatch_tokens.append(token)
                i += 3
            elif i < len(self.tokens) - 1 and self.is_adj_operator(self.tokens[i], self.tokens[i + 1]):
                token = Token(self.tokens[i].lexeme + self.tokens[i + 1].lexeme)
                hatch_tokens.append(token)
                i += 2
            elif self.tokens[i].type == TokenType.LEFT_STRING:
                buffer = self.tokens[i].lexeme
                adj_half = self.get_adj_half(self.tokens[i])
                print('im her')
                i += 1
                while i < len(self.tokens):
                    buffer += self.tokens[i].lexeme
                    if self.tokens[i].type == adj_half or \
                            (len(self.tokens[i].lexeme) == 1 and self.tokens[i].type == TokenType.STRING_CONST):
                        token = Token(buffer)
                        hatch_tokens.append(token)
                        break
                    i += 1
                else:
                    raise Exception("[RIGHT HALF OF ADJUSTABLE OPERATOR" + str(adj_half) + "EXPECTED]")
                i += 1
            else:
                hatch_tokens.append(Token(self.tokens[i].lexeme))
                i += 1

        self.tokens = hatch_tokens

    def print(self):
        print('------- Token Table -------')

        for token in self.tokens:
            print(token)

    @staticmethod
    def is_adj_decimal(first: Token, second: Token) -> bool:
        return first.type == TokenType.NUMBER_CONST and second.type == TokenType.POINT

    @staticmethod
    def get_adj_half(first: Token) -> TokenType:
        if first.type == TokenType.LEFT_STRING:
            return TokenType.RIGHT_STRING
        if first.type == TokenType.LEFT_MULTI_LINE_COMMENT:
            return TokenType.RIGHT_MULTI_LINE_COMMENT
        return TokenType.NONE

    @staticmethod
    def is_adj_operator(first: Token, second: Token) -> bool:
        return (first.lexeme in "<>=+-*/:!" and second.lexeme == "=") or \
               (first.lexeme == "+" and second.lexeme == "+") or \
               (first.lexeme == "-" and second.lexeme == "-") or \
               (first.lexeme == "/" and second.lexeme == "*") or \
               (first.lexeme == "*" and second.lexeme == "/") or \
               (first.lexeme == "&" and second.lexeme == "&") or \
               (first.lexeme == "|" and second.lexeme == "|")

    @staticmethod
    def is_sep(sym) -> bool:
        return sym in " ()+-*/[]<>{}=!:;.,\n\t\r"
