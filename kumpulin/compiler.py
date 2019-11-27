import sys
import CFG2CNF
import CYK 

tokens = [':', '.', '+', '-', '*', '/', '<', '>', '<=', '>=', '==', '(', ')', '[', ']', ',', "' '", "'", "\""]
languages = open("syntax.txt").read()
# print(languages)

def readSyntax(Terminals, languages):
    syntax = languages   
    if syntax[-1] == ")":
        syntax = syntax[:-1] + " )"
    syntax = syntax.replace("  ", " ")
    # print(syntax)
    syntax = syntax.replace("\t", "") 
    syntax = syntax.replace("\n", " ENDL ")
    syntax = syntax.replace("' '", " UNKNOWN ")
    syntax = syntax.replace("\" \"", " UNKNOWN ")
    syntax = syntax.split(" ")
    for x in range (syntax.count('')):
        syntax.remove('')
    # print(syntax)
    for i in range(len(syntax)):
        if syntax[i] not in Terminals and len(syntax[i]) > 0:
            syntax[i] = "UNKNOWN"
    # print(syntax)
    return syntax

Terminals, CNF = CFG2CNF.CFG2CNF("model.txt")
languages = open(sys.argv[1]).read()

# print(languages)
for token in tokens:
    read = len(token)
    for i in range(len(languages)-read+1):
        CC = languages[i:i+read]
        if CC == token:
            # print(CC)
            if not (languages[i-1] == " "):
                # print("[i:]", languages[i:])
                languages = languages[:i] + " " + languages[i:]
            elif not ( i == len(languages)-2):
                if not (languages[i+read+1] == " "):
                    languages = languages[:i+read] + " " + languages[i+read:]
# print(languages)
languages = readSyntax(Terminals, languages)
# print(languages)
# remove endl in end of syntax
if languages[-1] == "ENDL":
    languages = languages[:-1]

print(languages)
if ( CYK.CYK(CNF, 'S0', languages) ):
    print("Compile success .... ")
else :
    print("Syntax error!")