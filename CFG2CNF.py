import math

def loadModel(modelPath):
    file = open(modelPath).read()
    K = file.split("Variables:\n")[0].replace("Terminals:\n", "").replace("\n", "")
    V = file.split("Variables:\n")[1].split("Productions:\n")[0].replace("Variables", "").replace("\n", "")
    P = file.split("Productions:\n")[1]
    return cleanAlphabet(K), cleanAlphabet(V), cleanProduction(P)

def cleanAlphabet(expression):
    return expression.split()

def cleanProduction(expression):
    result = []
    rawRules = expression.replace("\n", "").split(";")[:-1]
    # print(rawRules)
    for rule in rawRules:
        leftside = rule.split(" -> ")[0]
        rightTerms = rule.split(" -> ")[1].split(" | ")
        for term in rightTerms:
            result.append((leftside, term.split(" ")))
    return result

def START(productions, variables):
    variables.append("S0")
    return [("S0", [variables[0]])] + productions

def REMOVE_NULL_PRODUCTIONS(productions, variables):
    NullVariables = []
    for rule in productions:
        left, right = rule
        if isRuleNull(rule):
            NullVariables.append(left)
            productions.remove(rule)

    for NullVariable in NullVariables:
        # NullVariablesRemoved = [].copy()
        NullVariablesRemoved = []
        for rule in productions:
            left, right = rule
            if isExistNullVar(rule, NullVariable):
                NullVariablesRemoved += replaceNullVar(rule, NullVariable)
        for rule in NullVariablesRemoved:
            if rule not in productions:      
                productions.append(rule)

    return sorted(productions, reverse=True)

def getNullVarIndex(rule, NullVar):
    indexPosList = []
    indexPos = 0

    left, right = rule
    while True:
        try:
            indexPos = right.index(NullVar, indexPos)
            indexPosList.append(indexPos)
            indexPos += 1
        except ValueError as e:
            break
    return indexPosList

def isRuleNull(rule):
    left, right = rule
    return "e" in right

def isExistNullVar(rule, NullVar):
    left, right = rule
    return NullVar in right

def replaceNullVar(rule, NullVar):
    result = []
    left, right = rule
    NullVarIndex =  getNullVarIndex(rule, NullVar)
    for i in range(len(NullVarIndex)):
        for j in range(i, len(NullVarIndex)):
            for k in range(j, len(NullVarIndex)):
                ReplacingIndex = NullVarIndex[i:j+1] + NullVarIndex[k+1:]
                NewRight = right.copy()
                for l in sorted(ReplacingIndex, reverse=True):
                    NewRight.pop(l)
                if (left, NewRight) not in result:
                    result.append((left, NewRight))
    return result


# replaceNullVar(("A",["a", "B", "a", "B", "B", "c", "B"]), "B")
# replaceNullVar(("A",["a", "B", "c", "B", "d", "B", "f", "B", "g"]), "B")

K, V, Productions = loadModel("model.txt")
Productions = START(Productions, V)
Productions = REMOVE_NULL_PRODUCTIONS(Productions, V)
print(Productions)