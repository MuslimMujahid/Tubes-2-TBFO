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
languages = open("syntax.txt").read()
languages = readSyntax(Terminals, languages)

if ( CYK.CYK(CNF, 'S0', languages) ):
    print("Compile success .... ")
else :
    print("Syntax error!")
