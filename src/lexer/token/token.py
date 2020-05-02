from src.lexer.token.token_type import token_type
from src.lexer.token.map_of_tokens import TokensMap


class Token:
    lexeme_ = ""
    type_ = token_type.IDENTIFIER

    def __init__(self, lexeme: str):
        self.lexeme_ = lexeme
        self.type_ = self.wto(lexeme)

    def wto(self, lexeme: str) -> token_type:
        if self.is_string(lexeme):
            return token_type.STRING_CONST
        if self.is_left_string(lexeme):
            return token_type.LEFT_STRING
        if self.is_right_string(lexeme):
            return token_type.RIGHT_STRING

        temporary = TokensMap.map.get(lexeme)
        if temporary is not None:
            return temporary
        if self.is_number(lexeme):
            return token_type.NUMBER_CONST

        return token_type.IDENTIFIER

    @staticmethod
    def is_number(lexeme: str) -> bool:
        for sym in lexeme:
            if not sym.isdigit() and sym != '.':
                return False
        return True

    @staticmethod
    def is_left_string(lexeme: str) -> bool:
        return lexeme[0] == "\""

    @staticmethod
    def is_right_string(lexeme: str) -> bool:
        return lexeme[-1] == "\""

    @staticmethod
    def is_string(lexeme: str) -> bool:
        if lexeme[0] == "\"" and lexeme[-1] == "\"":
            return True
        return False

    def __str__(self):
        return "(" + str(self.type_) + ", " + self.lexeme_ + ")"
