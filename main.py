from src.parser.parser import Parser
from src.asm.Asm import Asm
import os
import shutil
import sys
import pathlib


def make(file):
    fin = open("gen.bat", 'w')

    fin.write("""
            ml /c /coff {0}.asm
            link /subsystem:console {0}.obj""".format(file))

    fin.close()

    os.system("gen.bat")
    os.remove("gen.bat")

    if not pathlib.Path('projects').exists():
        os.mkdir('projects')

    if not pathlib.Path('projects\\{0}'.format(file)).exists():
        os.mkdir('projects\\{0}'.format(file))

    if not pathlib.Path('projects\\{0}\\bin'.format(file)).exists():
        os.mkdir('projects\\{0}\\bin'.format(file))

    if not pathlib.Path('projects\\{0}\\logs'.format(file)).exists():
        os.mkdir('projects\\{0}\\logs'.format(file))

    shutil.move(file + '.asm', 'projects\\' + file + '\\bin\\' + file + '.asm')
    shutil.move(file + '.obj', 'projects\\' + file + '\\bin\\' + file + '.obj')
    shutil.move(file + '.exe', 'projects\\' + file + '\\bin\\' + file + '.exe')

    shutil.move("lex",  "projects\\{0}\\logs\\lex".format(file))
    shutil.move("ast",  "projects\\{0}\\logs\\ast".format(file))
    shutil.move("vars", "projects\\{0}\\logs\\vars".format(file))


if __name__ == "__main__":

    if len(sys.argv) != 3:
        raise Exception("Not all arguments entered. Stopping ...")

    source_code = sys.argv[1]
    to_file = sys.argv[2]

    parser: Parser = Parser(source_code)
    ss = parser.parse()

    asm: Asm = Asm(to_file + '.asm', parser.ast)
    asm.generate()

    make(to_file)

    print("Compiled successful! {0}.exe placed ast bin-folder".format(to_file))
