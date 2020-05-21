from src.parser.parser import Parser
from src.asm.Asm import Asm

if __name__ == "__main__":
    parser: Parser = Parser("example.go")
    ss = parser.parse()

    asm: Asm = Asm('test.asm', parser.ast)
    asm.generate()
