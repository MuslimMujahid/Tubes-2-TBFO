def loadModel(modelPath):
    file = open(modelPath).read()
    K = file.split("Variables:\n")[0].replace("Terminals:\n", "").replace("\n", "")
    V = file.split("Variables:\n")[1].split("Productions:\n")[0].replace("Variables", "").replace("\n", "")
    P = file.split("Productions:\n")[1]
    return cleanAlphabet(K), cleanAlphabet(V), cleanProduction(P)

def writeResult(productions):
    i = 0
    for rule in sorted(productions):
        i+=1
        print(rule)
    print(i)

def cleanAlphabet(expression):
    return expression.split()

def cleanProduction(expression):
    result = []
    rules = expression.split('\n')
    for rule in rules:
        rule = rule.replace(';', '').split(' -> ')
        left, rights = rule
        if left == 'SEMI_COLON':
            rights = ';'
        elif left == 'NEWLINE':
            rights = '\n'
        rights = rights.split(' | ')
        for right in rights:
            newRight = right.split(' ')
            for x in range(newRight.count('')):
                newRight.remove('')
            result.append((left, newRight))

    return result

def isExistNullProduction(productions, variables):
    for rule in productions:
        left, right = rule
        if "e" in right:
            return True
    return False

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
    paths = []
    while True:
        unreachable = True
        for ruleS in productions:
            leftS, rightS = ruleS
            if left in rightS and not(left == leftS) and ruleS not in paths:
                paths.append(ruleS)
                left = leftS
                unreachable = False
                break
        if unreachable:
            break

    return left is not "S0"


def isVariablesMoreThan2(variables, rule):
    left, right = rule
    countVar = 0
    for v in right:
        if v in variables:
            countVar += 1
            if countVar > 2:
                return True
    return False

def replaceMoreThan2Var(variables, rule, Vars):
    result = []
    left, right = rule
    while isVariablesMoreThan2(variables, rule):
        variables.append(Vars.pop(0))  
        leftS = variables[-1]
        result.append((leftS, [right.pop(-2)]+[right.pop(-1)]))
        right.append(leftS)

    # print(result)
    return result+[(left, right)], variables, Vars

def replaceTerms(productions, variables, Vars):
    result = []
    for i in range(len(productions)):
        left, right = productions[i]
        for j in range(len(right)):
            if right[j] not in variables and len(right[j]) > 1:
                leftS = Vars.pop(0)
                variables.append(leftS)
                result.append((leftS, [right[j]]))
                right[j] = variables[-1]
        productions[i] = (left, right)
    
    return productions+result, variables, Vars


def isTermProduction(variables, rule):
    left, right = rule
    return len(right) == 2 and right[0] not in variables and right[1] in variables

def getNotUsedVariables(usedVariables, Vars):
    for var in usedVariables:
        if var in Vars:
            Vars.remove(var)

    return Vars

def replaceTermProduction(productions, variables, rule, Vars):

    result = []
    left, right = rule
    variables.append(Vars.pop(0))
    newLeft = variables[-1]
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
    return productions, variables, Vars
