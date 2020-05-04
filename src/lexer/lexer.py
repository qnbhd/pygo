from src.lexer.token.token import Token
from src.lexer.token.token_type import token_type


class Lexer:
    code_ = ""
    tokens_ = []

    def __init__(self, code=""):
        self.code_ = code
        self.tokens_ = []

    def read_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as fin:
            self.code_ = fin.read()

    def tokenize(self):
        buffer = ""
        record_string = False
        for i, sym in enumerate(self.code_):
            if sym == "\"":
                record_string = not record_string
            if self.is_sep(sym):
                if buffer != "":
                    self.tokens_.append(Token(buffer))
                    buffer = ""
                if record_string or (sym != " " and sym != '\n' and sym != '\t'):
                    self.tokens_.append(Token(sym))
            else:
                buffer += sym

        if buffer != "":
            self.tokens_.append(Token(buffer))

        self.adj_sub()
        return self.tokens_

    def adj_sub(self):
        hatch_tokens = []
        i = 0
        while i < len(self.tokens_):
            if i < len(self.tokens_) - 2 and self.is_adj_decimal(self.tokens_[i], self.tokens_[i + 1]):
                token = Token(self.tokens_[i].lexeme_ + self.tokens_[i + 1].lexeme_ + self.tokens_[i + 2].lexeme_)
                hatch_tokens.append(token)
                i += 3
            elif i < len(self.tokens_) - 1 and self.is_adj_operator(self.tokens_[i], self.tokens_[i + 1]):
                token = Token(self.tokens_[i].lexeme_ + self.tokens_[i + 1].lexeme_)
                hatch_tokens.append(token)
                i += 2
            elif self.tokens_[i].type_ == token_type.LEFT_STRING:
                buffer = self.tokens_[i].lexeme_
                adj_half = self.get_adj_half(self.tokens_[i])
                print('im her')
                i += 1
                while i < len(self.tokens_):
                    buffer += self.tokens_[i].lexeme_
                    if self.tokens_[i].type_ == adj_half or \
                            (len(self.tokens_[i].lexeme_) == 1 and self.tokens_[i].type_ == token_type.STRING_CONST):
                        token = Token(buffer)
                        hatch_tokens.append(token)
                        break
                    i += 1
                else:
                    raise Exception("[RIGHT HALF OF ADJUSTABLE OPERATOR" + str(adj_half) + "EXPECTED]")
                i += 1
            else:
                hatch_tokens.append(Token(self.tokens_[i].lexeme_))
                i += 1

        self.tokens_ = hatch_tokens

    @staticmethod
    def is_adj_decimal(first: Token, second: Token) -> bool:
        return first.type_ == token_type.NUMBER_CONST and second.type_ == token_type.POINT

    @staticmethod
    def get_adj_half(first: Token):
        if first.type_ == token_type.LEFT_STRING:
            return token_type.RIGHT_STRING
        if first.type_ == token_type.LEFT_MULTI_LINE_COMMENT:
            return token_type.RIGHT_MULTI_LINE_COMMENT
        return None

    @staticmethod
    def is_adj_operator(first: Token, second: Token) -> bool:
        return (first.lexeme_ in "<>=+-*/:!" and second.lexeme_ == "=") or \
               (first.lexeme_ == "+" and second.lexeme_ == "+") or \
               (first.lexeme_ == "-" and second.lexeme_ == "-") or \
               (first.lexeme_ == "/" and second.lexeme_ == "*") or \
               (first.lexeme_ == "*" and second.lexeme_ == "/") or \
               (first.lexeme_ == "&" and second.lexeme_ == "&") or \
               (first.lexeme_ == "|" and second.lexeme_ == "|")

    @staticmethod
    def is_sep(sym):
        return sym in " ()+-*/[]<>{}=!:;.,\n\t\r"
