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

b_variable = -8
c1_variable = -12
i_variable = -16
print PROC
   enter 0, 0
   push eax
   push ebx
   push ecx
   push edx
   mov eax, [ebp + 8]
   invoke crt_printf, offset print_format, eax
   pop eax
   pop ebx
   pop ecx
   pop edx
   leave 
   ret 4
print ENDP
__start:

   enter 20, 0
   push 5
   pop eax
   mov b_variable[ebp], eax
   push 6
   pop eax
   mov c1_variable[ebp], eax
   push 100
   pop eax
   mov b_variable[ebp], eax
   push b_variable[ebp]
   pop ecx
   push 100
   pop edx
   cmp ecx, edx
   jne _compare_not_equal1
   push 1
   jmp _compare_end1
_compare_not_equal1:
   push 0
_compare_end1:
   pop eax
   cmp eax, 0
   je _if_else_97041
_if_start_97041:
   push 0
   pop eax
   mov i_variable[ebp], eax
_loop_start_362521:
   push i_variable[ebp]
   pop ecx
   push 10
   pop edx
   cmp ecx, edx
   jg _compare_not_equal2
   push 1
   jmp _compare_end2
_compare_not_equal2:
   push 0
_compare_end2:
   pop eax
   cmp eax, 0
   je _loop_end_362521
   push b_variable[ebp]
   push i_variable[ebp]
   pop eax
   pop ebx
   add eax, ebx
   push eax
   pop eax
   mov b_variable[ebp], eax
   push b_variable[ebp]
   pop eax
   push eax
   call print
_loop_aftereffects_362521:
   push i_variable[ebp]
   push 1
   pop eax
   pop ebx
   add eax, ebx
   push eax
   pop eax
   mov i_variable[ebp], eax
   jmp _loop_start_362521
_loop_end_362521:
   jmp _if_end_97041
_if_else_97041:
   push b_variable[ebp]
   pop ecx
   push 100
   pop edx
   cmp ecx, edx
   jge _compare_not_equal3
   push 1
   jmp _compare_end3
_compare_not_equal3:
   push 0
_compare_end3:
   push c1_variable[ebp]
   pop ecx
   push 5
   pop edx
   cmp ecx, edx
   jne _compare_not_equal4
   push 1
   jmp _compare_end4
_compare_not_equal4:
   push 0
_compare_end4:
   pop eax
   cmp eax, 0
   je _if_else_686621
_if_start_686621:
   push 1000
   pop eax
   mov b_variable[ebp], eax
   jmp _if_end_686621
_if_else_686621:
   push b_variable[ebp]
   pop ecx
   push 100
   pop edx
   cmp ecx, edx
   jge _compare_not_equal5
   push 1
   jmp _compare_end5
_compare_not_equal5:
   push 0
_compare_end5:
   push c1_variable[ebp]
   pop ecx
   push 6
   pop edx
   cmp ecx, edx
   jne _compare_not_equal6
   push 1
   jmp _compare_end6
_compare_not_equal6:
   push 0
_compare_end6:
   pop eax
   cmp eax, 0
   je _if_end_25880
_if_start_25880:
   push 2000
   pop eax
   mov b_variable[ebp], eax
_if_end_25880:
_if_end_686621:
_if_end_97041:
   push c1_variable[ebp]
   push b_variable[ebp]
   pop eax
   pop ebx
   add eax, ebx
   push eax
   pop eax
   push eax
   call print

   leave

   ret

text ends

end __start

