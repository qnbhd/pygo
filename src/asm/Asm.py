import random
from enum import Enum, auto
from src.parser.ast.ast import AST as Ast
from src.parser.ast.node import Node
from src.parser.ast.node_type import NodeType
from src.parser.variable.variable import Variable

from src.asm.AsmConstants import *


class AsmPlace(Enum):
    DATA = auto(),
    BEFORE_MAIN = auto(),
    MAIN = auto()


class AsmPlaceString:
    value: str

    def __init__(self):
        self.value = ''

    def append(self, string: str):
        self.value += string


class Asm:
    ast: Ast

    filename: str

    # asm places
    data: AsmPlaceString
    before_main: AsmPlaceString
    main: AsmPlaceString
    current_place_for_writing: AsmPlaceString

    byte_on_stack: int

    def __init__(self, filename: str, ast: Ast):
        self.ast = ast
        self.filename = filename

        self.data: AsmPlaceString = AsmPlaceString()
        self.before_main: AsmPlaceString = AsmPlaceString()
        self.main: AsmPlaceString = AsmPlaceString()

        self.current_place_for_writing = self.main
        self.byte_on_stack = 8

        self.file = open(filename, 'w')

        self.count_compare = 0

    def generate(self):
        self.init_variables()
        self.init_operands_for_division()

        self.init_print_function()

        self.block_to_asm()


        self.write(asm_header)
        self.write(start_data)
        self.write(self.data.value)
        self.write(end_data)
        self.write(text_start)
        self.write(self.before_main.value)
        self.write(label_start)
        self.write(proc_prolog + str(len(self.ast.variables.table) * 4 + 8) + ", 0")
        self.write(self.main.value)
        self.write(proc_epilogue)
        self.write(function_return)
        self.write(text_end)
        self.write(label_end)

        self.file.close()

    def init_print_function(self):
        self.set_place_for_writing(AsmPlace.DATA)
        self.raw(tab + "print_format db \"%d \", 0\n")
        self.set_place_for_writing(AsmPlace.BEFORE_MAIN)

        self.raw("print PROC\n   enter 0, 0\n")

        self.push(eax)
        self.push(ebx)
        self.push(ecx)
        self.push(edx)

        self.mov(eax, "[ebp + 8]")
        self.raw(tab + "invoke crt_printf, offset print_format, eax\n")

        self.pop(eax)
        self.pop(ebx)
        self.pop(ecx)
        self.pop(edx)

        self.raw("   leave \n   ret 4\nprint ENDP")

        self.set_place_for_writing(AsmPlace.MAIN)

    def init_variables(self):
        for variable in self.ast.variables.table:
            self.stack_variable(variable)

    def init_operands_for_division(self):
        self.set_place_for_writing(AsmPlace.DATA)
        self.raw(tab + "div_op_1 dd 0\n")
        self.raw(tab + "div_op_2 dd 0\n")
        self.set_place_for_writing(AsmPlace.MAIN)


    def block_to_asm(self):
        self.block_to_asm_recursive(self.ast.tree)

    def block_to_asm_recursive(self, current_node: Node):
        if current_node is None:
            return

        if current_node.type == NodeType.SET:
            op1: Node = current_node.op1
            op2: Node = current_node.op2

            if op1.type == NodeType.USING_VARIABLE or op1.type == NodeType.VARIABLE_DECLARATION:
                variable_name: str = op1.value
                self.expression_recursive(op2)
                self.pop(eax)
                self.mov(self.local_var(variable_name), eax)
                return

        elif Node.is_comparison_operator(current_node.type):
            self.relation_expression_recursive(current_node)
            return
        elif current_node.type == NodeType.IF or current_node.type == NodeType.IF_ELSE:
            condition: Node = current_node.op1
            statement: Node = current_node.op2
            elseStatement: Node = current_node.op3

            randId: int = random.randint(0, 1000000)

            startLabel: str = "_if_start_" + str(randId)
            endLabel: str = "_if_end_" + str(randId)
            elseLabel: str = "_if_else_" + str(randId)

            self.block_to_asm_recursive(condition)
            self.pop(eax)
            self.cmp(eax, null)

            endOrElseLabel: str = endLabel

            if current_node.type == NodeType.IF_ELSE:
                endOrElseLabel = elseLabel

            self.je(endOrElseLabel)

            if current_node.type == NodeType.IF_ELSE:
                self.label(startLabel)
                self.block_to_asm_recursive(statement)
                self.jmp(endLabel)
                self.label(elseLabel)
                self.block_to_asm_recursive(elseStatement)
                self.label(endLabel)
            elif current_node.type == NodeType.IF:
                self.label(startLabel)
                self.block_to_asm_recursive(statement)
                self.label(endLabel)

            return

        elif current_node.type == NodeType.FOR:
            prevention: Node = current_node.op1
            condition: Node = current_node.op2
            aftereffects: Node = current_node.op3
            statement: Node = current_node.op4

            randId: int = random.randint(0, 1000000)

            startLabel: str = "_loop_start_" + str(randId)
            endLabel: str = "_loop_end_" + str(randId)
            aftereffectsLabel: str = "_loop_aftereffects_" + str(randId)

            self.block_to_asm_recursive(prevention)
            self.label(startLabel)
            self.block_to_asm_recursive(condition)
            self.pop(eax)
            self.cmp(eax, null)
            self.je(endLabel)
            self.block_to_asm_recursive(statement)
            self.label(aftereffectsLabel)
            self.block_to_asm_recursive(aftereffects)
            self.jmp(startLabel)
            self.label(endLabel)

            return

        elif current_node.type == NodeType.EXPRESSION:
            self.block_to_asm_recursive(current_node.op1)
            return
        elif current_node.type == NodeType.PRINT:
            self.expression_recursive(current_node.op1)
            self.pop(eax)
            self.push(eax)
            self.raw(tab + "call print\n")
            return

        self.block_to_asm_recursive(current_node.op1)
        self.block_to_asm_recursive(current_node.op2)
        self.block_to_asm_recursive(current_node.op3)
        self.block_to_asm_recursive(current_node.op4)

    def expression_recursive(self, current_node: Node):
        if current_node is None:
            return

        if current_node.type == NodeType.ADD:
            self.expression_recursive(current_node.op1)
            self.expression_recursive(current_node.op2)
            self.pop(eax)
            self.pop(ebx)
            self.add(eax, ebx)
            self.push(eax)
        elif current_node.type == NodeType.SUB:
            self.expression_recursive(current_node.op1)
            self.expression_recursive(current_node.op2)
            self.pop(ebx)
            self.pop(eax)
            self.sub(eax, ebx)
            self.push(eax)
        elif current_node.type == NodeType.MUL:
            self.expression_recursive(current_node.op1)
            self.expression_recursive(current_node.op2)
            self.pop(eax)
            self.pop(ebx)
            self.imul(eax, ebx)
            self.push(eax)
        elif current_node.type == NodeType.DIV:
            self.expression_recursive(current_node.op1)
            self.expression_recursive(current_node.op2)
            self.pop(ebx)
            self.pop(eax)
            self.mov("div_op_1", eax)
            self.mov("div_op_2", ebx)
            self.finit()
            self.fild("div_op_2")
            self.fild("div_op_1")
            self.fdiv("st(0)", "st(1)")
            self.fist("div_op_1")
            self.push("div_op_1")
        elif current_node.type == NodeType.UNARY_MINUS:
            self.expression_recursive(current_node.op1)
            self.pop(eax)
            self.imul(eax, minus_one)
            self.push(eax)
        elif current_node.type == NodeType.INTEGER_CONST:
            numberValue: str = current_node.value
            self.push(numberValue)
        elif current_node.type == NodeType.USING_VARIABLE:
            variableName: str = current_node.value
            self.push(self.local_var(variableName))
        elif Node.is_comparison_operator(current_node.type):
            self.relation_expression_recursive(current_node)
        elif current_node.type == NodeType.EXPRESSION:
            self.expression_recursive(current_node.op1)

    def relation_expression_recursive(self, current_node: Node):
        if current_node is None:
            return

        if current_node.type == NodeType.INTEGER_CONST:
            value_ = int(current_node.value)

            if value_ == 0:
                self.push(null)
            else:
                self.push(one)

        elif current_node.type == NodeType.USING_VARIABLE:
            self.count_compare += 1

            label_if_not_equal: str = "_compare_not_equal" + str(self.count_compare)
            label_compare_end: str = "_compare_end" + str(self.count_compare)

            variable_name = current_node.value
            self.cmp(self.local_var(variable_name), null)
            self.jne(label_if_not_equal)
            self.push(null)
            self.jmp(label_compare_end)
            self.label(label_if_not_equal)
            self.push(one)
            self.label(label_compare_end)

        elif current_node.type == NodeType.EXPRESSION:
            self.relation_expression_recursive(current_node.op1)
            return
        else:
            self.count_compare += 1
            op1 = current_node.op1
            op2 = current_node.op2
            self.expression_recursive(op1)
            self.pop(ecx)
            self.expression_recursive(op2)
            self.pop(edx)
            self.cmp(ecx, edx)

            label_if_not_equal = "_compare_not_equal" + str(self.count_compare)
            label_compare_end = "_compare_end" + str(self.count_compare)

            if current_node.type == NodeType.LESS:
                self.jge(label_if_not_equal)
            elif current_node.type == NodeType.LESS_EQUAL:
                self.jg(label_if_not_equal)
            elif current_node.type == NodeType.GREATER:
                self.jle(label_if_not_equal)
            elif current_node.type == NodeType.GREATER_EQUAL:
                self.jl(label_if_not_equal)
            elif current_node.type == NodeType.EQUAL:
                self.jne(label_if_not_equal)
            elif current_node.type == NodeType.NOT_EQUAL:
                self.je(label_if_not_equal)

            self.push(one)
            self.jmp(label_compare_end)
            self.label(label_if_not_equal)
            self.push(null)
            self.label(label_compare_end)

            return

    def set_place_for_writing(self, place: AsmPlace):
        if place == AsmPlace.DATA:
            self.current_place_for_writing = self.data
        elif place == AsmPlace.BEFORE_MAIN:
            self.current_place_for_writing = self.before_main
        elif place == AsmPlace.MAIN:
            self.current_place_for_writing = self.main

    def write(self, string: str):
        self.file.write(string + '\n')

    def local_var(self, name: str):
        return name + "_variable[ebp]"

    def stack_variable(self, variable: Variable):
        variable_name = variable.name
        self.before_main.append(variable_name + "_variable = " + "-" + str(self.byte_on_stack) + "\n")
        self.byte_on_stack += 4

    def push(self, value: str):
        self.current_place_for_writing.append(tab + "push " + value + "\n")

    def pop(self, value: str):
        self.current_place_for_writing.append(tab + "pop " + value + "\n")

    def add(self, value1: str, value2: str):
        self.current_place_for_writing.append(tab + "add " + value1 + ", " + value2 + "\n")

    def sub(self, value1: str, value2: str):
        self.current_place_for_writing.append(tab + "sub " + value1 + ", " + value2 + "\n")

    def imul(self, value1: str, value2: str):
        self.current_place_for_writing.append(tab + "imul " + value1 + ", " + value2 + "\n")

    def mov(self, value1: str, value2: str):
        self.current_place_for_writing.append(tab + "mov " + value1 + ", " + value2 + "\n")

    def raw(self, value: str):
        self.current_place_for_writing.append(value)

    def cmp(self, value1: str, value2: str):
        self.current_place_for_writing.append(tab + "cmp " + value1 + ", " + value2 + "\n")

    def jmp(self, value: str):
        self.current_place_for_writing.append(tab + "jmp " + value + "\n")

    def je(self, value: str):
        self.current_place_for_writing.append(tab + "je " + value + "\n")

    def jne(self, value: str):
        self.current_place_for_writing.append(tab + "jne " + value + "\n")

    def jl(self, value: str):
        self.current_place_for_writing.append(tab + "jl " + value + "\n")

    def jle(self, value: str):
        self.current_place_for_writing.append(tab + "jle " + value + "\n")

    def jg(self, value: str):
        self.current_place_for_writing.append(tab + "jg " + value + "\n")

    def jge(self, value: str):
        self.current_place_for_writing.append(tab + "jge " + value + "\n")

    def label(self, value: str):
        self.current_place_for_writing.append(value + ":\n")

    def finit(self):
        self.current_place_for_writing.append(tab + "finit\n")

    def fild(self, value: str):
        self.current_place_for_writing.append(tab + "fild " + value + "\n")

    def fdiv(self, value1: str, value2: str):
        self.current_place_for_writing.append(tab + "fdiv " + value1 + ", " + value2 + "\n")

    def fist(self, value: str):
        self.current_place_for_writing.append(tab + "fist " + value + "\n")
