asm_header = ".586\n" + \
             ".model flat, stdcall\n\n" + \
             "include <\\masm32\\include\\msvcrt.inc>\n" + \
             "include <\\masm32\\include\\kernel32.inc>\n" + \
             "includelib <\\masm32\\lib\\msvcrt.lib>\n" + \
             "includelib <\\masm32\\lib\\kernel32.lib>\n"

start_data = "data segment\n"
end_data = "data ends\n"
text_start = "text segment\n"
text_end = "text ends\n"
label_start = "__start:\n"
label_end = "end __start\n"
proc_prolog = "   enter "
proc_epilogue = "   leave\n"
function_return = "   ret\n"
tab = "   "

eax = "eax"
ebx = "ebx"
ecx = "ecx"
edx = "edx"
esi = "esi"
null = "0"
one = "1"
minus_one = "-1"
