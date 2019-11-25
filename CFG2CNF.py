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

def isExistNullProduction(productions, variables):
    for rule in productions:
        left, right = rule
        if "e" in right:
            return True
    return False

def START(productions, variables):
    variables.append("S0")
    return [("S0", [variables[0]])] + productions

def REMOVE_NULL_PRODUCTIONS(productions, variables):

    while ( isExistNullProduction(productions, variables) ):
        NullVariables = []
        CopyProductions = productions.copy()
        for rule in CopyProductions:
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
                    left, right = rule 
                    if len(right) == 0:
                        right.append("e")
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
    return len(right) == 1 and right[0] in variables

def isExistUnitProduct(productions, variables):
    exist = False
    for rule in productions:
        if isUnitProduct(rule, variables):
            exist = True
            break
    return exist

def replaceUnitProduct(productions, variables, rule):
    result = []
    left, right = rule
    for ruleS in productions:
        leftS, rightS = ruleS
        if leftS == right[0] and not isUnitProduct(ruleS, variables):
            result.append((left, rightS))

    return result

def isRuleUnreachable(productions, variables, rule):
    left, right = rule
    while True:
        unreachable = True
        for ruleS in productions:
            leftS, rightS = ruleS
            if left in rightS and not(left == leftS):
                left = leftS
                unreachable = False
                break
        if unreachable:
            break

    return left is not "S0"


def REMOVE_UNIT_PRODUCTIONS(productions, variables):

    CopyProductions = productions.copy()
    for rule in CopyProductions:            
        if isUnitProduct(rule, variables) and rule in productions:
            if rule in productions:
                productions.remove(rule)
            newRules = replaceUnitProduct(productions, variables, rule)
            for newRule in newRules:
                if newRule not in productions:
                    productions.append(newRule)
            
                

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
        leftS = Vars.pop(0)
        result.append((leftS, [right.pop(-2)]+[right.pop(-1)]))
        right.append(leftS)

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

def replaceTermProduction(productions, variables, rule, Vars):

    result = []
    left, right = rule
    newLeft = Vars.pop(0)
    result.append((newLeft,[right[0]]))

    CopyProductions = productions.copy()
    for ruleS in CopyProductions:
        leftS, rightS = ruleS
        if len(rightS) == 2 and rightS[0] == right[0]:
            newRule = (leftS, [newLeft,rightS[0]])
            if newRule not in productions:
                result.append((leftS, [newLeft,rightS[0]]))
                productions.remove(ruleS)

    productions += result
    return Vars, productions

def REMOVE_TERM_PRODUCTION(productions, variables, Vars):
    CopyProductions = productions.copy()
    for rule in productions:
        left, right = rule
        if isTermProduction(variables, rule):
            Vars, productions = replaceTermProduction(productions, variables, rule, Vars)
    return Vars, productions

K, V, Productions = loadModel("model4.txt")
varContainer = getNotUsedVariables(V, varContainer)

Productions = START(Productions, V)
Productions = REMOVE_NULL_PRODUCTIONS(Productions, V)
Productions = REMOVE_UNIT_PRODUCTIONS(Productions, V)
varContainer, Productions = REMOVE_MORE_THAN_2_VARIABLES_PRODUCTION(Productions, V, varContainer)
varContainer, Productions = REMOVE_TERM_PRODUCTION(Productions, V, varContainer) 

for rule in Productions:
    print(rule)
