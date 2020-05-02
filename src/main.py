from src.lexer.token.token import Token
from src.lexer.lexer import Lexer

if __name__ == "__main__":
    lex = Lexer()
    lex.read_from_file("src/example.go")
    z = lex.tokenize()
    for token in z:
        print(token)