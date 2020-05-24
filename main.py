from src.parser.parser import Parser
from src.asm.Asm import Asm
import os
import shutil
import sys


def make(to_file):
    fin = open("gen.bat", 'w')

    fin.write("""
            ml /c /coff {0}.asm
            link /subsystem:console {0}.obj""".format(to_file))

    fin.close()

    os.system("gen.bat")
    os.remove("gen.bat") 

    shutil.move(to_file + '.asm', 'bin\\' + to_file + '.asm')
    shutil.move(to_file + '.obj', 'bin\\' + to_file + '.obj')
    shutil.move(to_file + '.exe', 'bin\\' + to_file + '.exe')

if __name__ == "__main__":

    print(len(sys.argv))

    if len(sys.argv) != 3:
        raise Exception("Not all arguments entered. Stopping ...")

    source_code = sys.argv[1]
    to_file = sys.argv[2]

    parser: Parser = Parser(source_code)
    ss = parser.parse()

    asm: Asm = Asm(to_file + '.asm', parser.ast)
    asm.generate()

    make(to_file)

    print("Compiled successfull! {0}.exe placed ast bin-folder".format(to_file))







