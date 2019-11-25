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
        if isNullProduct(rule):
            NullVariables.append(left)
            productions.remove(rule)

    for NullVariable in NullVariables:
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

def isNullProduct(rule):
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

def isUnitProduct(rule, variables):
    left, right = rule
    return len(right) == 1 and right[0] in variables

def isExistUnitProduct(productions, variables):
    exist = False
    for rule in productions:
        if isUnitProduct(rule, variables):
            exist = True
            break
    return exist

def replaceUnitProduct(productions, rule):
    left, right = rule
    for ruleS in productions:
        leftS, rightS = ruleS
        if leftS == right[0]:
            return [(left, rightS)]

def isUnreachableRule(productions, variables, rule):
    left, right = rule
    while True:
        for ruleS in productions:
            leftS, rightS = ruleS
            if left in rightS:
                left = leftS
                break
        break
        
    return not (left == "S")


def REMOVE_UNIT_PRODUCTIONS(productions, variables):

    while isExistUnitProduct(productions, variables):
        unitProductions = []
        for rule in productions:            
            if isUnitProduct(rule, variables):
                unitProductions.append(rule)
                productions.remove(rule)
        for unitProduction in unitProductions:
            productions += replaceUnitProduct(productions + unitProductions, unitProduction)

    for rule in productions:
        if isUnreachableRule(productions, variables, rule):
            productions.remove(rule)

    return sorted(productions, reverse=True)


# replaceNullVar(("A",["a", "B", "a", "B", "B", "c", "B"]), "B")
# replaceNullVar(("A",["a", "B", "c", "B", "d", "B", "f", "B", "g"]), "B")

K, V, Productions = loadModel("model2.txt")
# Productions = START(Productions, V)
# Productions = REMOVE_NULL_PRODUCTIONS(Productions, V)
# print(Productions)
# for rule in Productions:
#     if isUnitProduct(rule, V):
#         print(rule)
print(REMOVE_UNIT_PRODUCTIONS(Productions, V))
# REMOVE_UNIT_PRODUCTIONS(Productions, V)