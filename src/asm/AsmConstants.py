

asmHeader = ".586\n" + \
             ".model flat, stdcall\n\n" + \
             "include <\\masm32\\include\\msvcrt.inc>\n" + \
             "include <\\masm32\\include\\kernel32.inc>\n" + \
             "includelib <\\masm32\\lib\\msvcrt.lib>\n" + \
             "includelib <\\masm32\\lib\\kernel32.lib>\n"

startData = "data segment\n"
endData = "data ends\n"
textStart = "text segment\n"
textEnd = "text ends\n"
labelStart = "__start:\n"
labelEnd = "end __start\n"
procProlog = "   enter "
procEpilogue = "   leave\n"
functionReturn = "   ret\n"
tab = "   "

eax = "eax"
ebx = "ebx"
ecx = "ecx"
edx = "edx"
esi = "esi"
null = "0"
one = "1"
minus_one = "-1"
