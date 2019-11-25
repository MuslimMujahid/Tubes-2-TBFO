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

# REMOVE USELESS SYMBOLS
def isGenerateTerminalOrV1Element(aturan, terminals, V1):
    # Algoritme
    for simbol in aturan[1]:
        if (simbol in terminals or simbol in V1):
            return True
    return False

def semuaVariablesAdaDiVx(aturan, variables, Vx):
    # Algoritme
    if aturan[0] not in Vx:
        return False
    for simbol in aturan[1]:
        if simbol in variables and simbol not in Vx:
            return False
    return True

def semuaTerminalsAdaDiVx(aturan, terminals, Tx):
    # Algoritme
    for simbol in aturan[1]:
        if simbol in terminals and simbol not in Tx:
            return False
    return True

def langkahPertama(terminals, variables, initial, rules):
    # Inisialisasi
    V1 = set()
    P1 = set()

    # Algoritme
    while True:
        oldLenV1 = len(V1)
        for aturan in rules:
            if isGenerateTerminalOrV1Element(aturan, terminals, V1):
                V1.add(aturan[0])
        if not (len(V1) > oldLenV1):
            break
    for aturan in rules:
        if semuaVariablesAdaDiVx(aturan, variables, V1):
            P1.add(aturan)
    return langkahKedua(terminals, V1, initial, P1)

def langkahKedua(terminals, variables, initial, rules):
    # Inisialisasi
    T2 = set()
    V2 = initial.copy()
    P2 = set()

    # Algoritme
    while True:
        oldLenT2 = len(T2)
        oldLenV2 = len(V2)
        for aturan in rules:
            if aturan[0] in V2:
                for simbol in aturan[1]:
                    if simbol in variables:
                        V2.add(simbol)
                    elif simbol in terminals:
                        T2.add(simbol)
        if not (len(V2) > oldLenV2 and len(T2) > oldLenT2):
            break
    for aturan in rules:
        if semuaVariablesAdaDiVx(aturan, variables, V2):
            if semuaTerminalAdaDiVx(aturan, terminals, T2):
                P2.add(aturan)
    return (T2, V2, initial, P2)

def menghapusUselesssimbols(terminals, variables, initial, rules):
    return langkahPertama(terminals, variables, initial, rules)

# replaceNullVar(("A",["a", "B", "a", "B", "B", "c", "B"]), "B")
# replaceNullVar(("A",["a", "B", "c", "B", "d", "B", "f", "B", "g"]), "B")

K, V, Productions = loadModel("model.txt")
Productions = START(Productions, V)
Productions = REMOVE_NULL_PRODUCTIONS(Productions, V)
print(Productions)
