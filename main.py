import CFG2CNF
import CYK 
def readSyntax(Terminals, languages):
    syntax = languages
    syntax.replace("\t", " ") 
    syntax.replace("\n", " NEWLINE ")
    syntax = syntax.split(" ")
    for x in range (syntax.count('')):
        syntax.remove('')
    for i in range(len(syntax)):
        if syntax[i] not in Terminals and len(syntax[i]) > 0:
            syntax[i] = "NAME"
    return syntax


Terminals, CNF = CFG2CNF.CFG2CNF("model.txt")
languages = open("syntax.txt").read()
languages = readSyntax(Terminals, languages)
print(languages)
# for x in CNF:
#     print(x)
CYK.CYK(CNF, 'S0', languages)
