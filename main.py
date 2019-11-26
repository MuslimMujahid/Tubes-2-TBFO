import CFG2CNF
import CYK

def readSyntax(Terminals, languages):
    syntax = languages
    syntax.replace("\t", " ") 
    syntax.replace("\n", " NEWLINE ")
    syntax = syntax.split(" ")
    for i in range(len(syntax)):
        if syntax[i] not in Terminals and len(syntax[i]) > 0:
            syntax[i] = "NAME"
    return syntax


# Terminals, V, Productions = CFG.loadModel("newgrammar.txt")
# varContainer = CFG.getNotUsedVariables(V, varContainer)

Terminals, CNF = CFG2CNF.CFG2CNF("newgrammar.txt")
languages = "import what"
languages = readSyntax(Terminals, languages)
print(languages)
CYK.CYK(CNF, "S0", languages)
