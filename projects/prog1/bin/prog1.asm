.586
.model flat, stdcall

include <\masm32\include\msvcrt.inc>
include <\masm32\include\kernel32.inc>
includelib <\masm32\lib\msvcrt.lib>
includelib <\masm32\lib\kernel32.lib>

data segment

   div_op_1 dd 0
   div_op_2 dd 0
   print_format db "%d ", 0

data ends

text segment

a_variable = -8
b_variable = -12
D_variable = -16
print PROC
   enter 0, 0
   mov eax, [ebp + 8]
   invoke crt_printf, offset print_format, eax
   leave 
   ret 4
print ENDP
__start:

   enter 20, 0
   push 1
   pop eax
   mov a_variable[ebp], eax
   push 2
   pop eax
   imul eax, -1
   push eax
   pop eax
   mov b_variable[ebp], eax
   push 100
   pop eax
   mov D_variable[ebp], eax
   push a_variable[ebp]
   pop ecx
   push b_variable[ebp]
   pop edx
   cmp ecx, edx
   jge _compare_not_equal1
   push 1
   jmp _compare_end1
_compare_not_equal1:
   push 0
_compare_end1:
   pop eax
   cmp eax, 0
   je _if_else_345355
_if_start_345355:
   push 1
   pop eax
   push eax
   call print
   jmp _if_end_345355
_if_else_345355:
   push 0
   pop eax
   push eax
   call print
_if_end_345355:

   leave

   ret

text ends

end __start

