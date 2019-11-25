varContainer = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

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

    return productions

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
    return len(right) == 1 and right[0] in variables and not (left == "S0")

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

def isRuleUnreachable(productions, variables, rule):
    left, right = rule
    while True:
        for ruleS in productions:
            leftS, rightS = ruleS
            if left in rightS:
                left = leftS
                break
        break

    return left is not "S0"


def REMOVE_UNIT_PRODUCTIONS(productions, variables):

    while isExistUnitProduct(productions, variables):
        unitProductions = []
        for rule in productions:            
            if isUnitProduct(rule, variables):
                unitProductions.append(rule)
                productions.remove(rule)
        for unitProduction in unitProductions:
            productions += replaceUnitProduct(productions + unitProductions, unitProduction)

    CopyProductions = productions.copy()
    for rule in CopyProductions:
        if isRuleUnreachable(productions, variables, rule):
            productions.remove(rule)

    return productions

def isVariablesMoreThan2(variables, rule):
    left, right = rule
    countVar = 0
    for v in right:
        if v in variables:
            countVar += 1
            if countVar > 2:
                return True
        else:
            return False

def replaceMoreThan2Var(variables, rule, Vars):
    result = []
    left, right = rule
    while isVariablesMoreThan2(variables, rule):
        result.append((Vars.pop(0),[right.pop(-1)]))

    # print(result)
    return Vars, result+[(left, right)]


def REMOVE_MORE_THAN_2_VARIABLES_PRODUCTION(productions, variables, Vars):
    CopyProductions = productions.copy()
    for rule in CopyProductions:
        if isVariablesMoreThan2(variables, rule):
            productions.remove(rule)
            Vars, newRules =  replaceMoreThan2Var(variables, rule, Vars)
            productions += newRules
    
    return Vars, productions

def isTermProduction(variables, rule):
    left, right = rule
    return len(right) == 2 and right[0] not in variables and right[1] in variables

def getNotUsedVariables(usedVariables, Vars):
    for V in  usedVariables:
        Vars.remove(V)
    return Vars

def replaceTermProduction(variables, rule, Vars):
    result = []
    left, right = rule
    leftS = Vars.pop(0)
    rightS = [right[0]]
    result += [(leftS, rightS)]
    right[0] = leftS
    result += [(left, right)]

    return Vars, result

def REMOVE_TERM_PRODUCTION(productions, variables, Vars):
    CopyProductions = productions.copy()
    for rule in CopyProductions:
        left, right = rule
        if isTermProduction(variables, rule):
            productions.remove(rule)
            Vars, newRule = replaceTermProduction(variables, rule, Vars)
            productions += newRule
    return Vars, productions

K, V, Productions = loadModel("model4.txt")
varContainer = getNotUsedVariables(V, varContainer)

Productions = START(Productions, V)
Productions = REMOVE_NULL_PRODUCTIONS(Productions, V)
# Productions = REMOVE_UNIT_PRODUCTIONS(Productions, V)
# varContainer, Productions = REMOVE_MORE_THAN_2_VARIABLES_PRODUCTION(Productions, V, varContainer)
# varContainer, Productions = REMOVE_TERM_PRODUCTION(Productions, V, varContainer) 

for rule in Productions:
    print(rule)
