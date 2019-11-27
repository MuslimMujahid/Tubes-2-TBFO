import CFG2CNF
import CYK 

def readSyntax(Terminals, languages):
    syntax = languages
    syntax = syntax.replace("\t", "") 
    syntax = syntax.replace("\n", " ENDL ")
    syntax = syntax.replace("' '", " UNKNOWN ")
    syntax = syntax.split(" ")
    for x in range (syntax.count('')):
        syntax.remove('')
    for i in range(len(syntax)):
        if syntax[i] not in Terminals and len(syntax[i]) > 0:
            syntax[i] = "UNKNOWN"
    return syntax

Terminals, CNF = CFG2CNF.CFG2CNF("model2.txt")
languages = open("tc2.txt").read()

tokens = [':', '.', '+', '-', '*', '/', '<', '>', '<=', '>=', '==', '(', ')', '[', ']', ',', "'"]
languages = open("syntax.txt").read() + '\nqwertyuiop'

for token in tokens:
    read = len(token)
    for i in range(len(languages)-read):
        CC = languages[i:i+read]
        if CC == token:
            if not (languages[i-1] == " "):
                print(languages[i:])
                languages = languages[:i] + " " + languages[i:]
            elif not (languages[i+read+1] == " "):
                languages = languages[:i+read] + " " + languages[i+read:]

languages = languages[:len(languages)-11]

languages = readSyntax(Terminals, languages)

if ( CYK.CYK(CNF, 'S0', languages) ):
    print("Compile success .... ")
else :
    print("Syntax error!")
