import CFG

def START(productions, variables, Vars):
    variables.append("S0")
    return [("S0", [variables[0]])] + productions, variables, Vars

def REMOVE_NULL_PRODUCTIONS(productions, variables, Vars):
    
    while ( CFG.isExistNullProduction(productions, variables) ):
        NullVariables = []
        CopyProductions = productions.copy()
        for rule in CopyProductions:
            left, right = rule
            if CFG.isNullProduct(rule): 
                NullVariables.append(left)
                productions.remove(rule)
                
        for NullVariable in NullVariables:
            NullVariablesRemoved = []
            for rule in productions:
                left, right = rule
                if CFG.isExistNullVar(rule, NullVariable):
                    NullVariablesRemoved += CFG.replaceNullVar(rule, NullVariable)
            for rule in NullVariablesRemoved:
                if rule not in productions:
                    left, right = rule 
                    if len(right) == 0:
                        right.append("e")
                    productions.append(rule)

    return productions, variables, Vars

def REMOVE_UNIT_PRODUCTIONS(productions, variables, Vars):
    
    CopyProductions = productions.copy()
    for rule in CopyProductions:            
        if CFG.isUnitProduct(rule, variables) and rule in productions:
            newRules = CFG.replaceUnitProduct(productions, variables, rule)
            productions.remove(rule)
            for newRule in newRules:
                if newRule not in productions:
                    productions.append(newRule)
            
    CopyProductions = productions.copy()
    for rule in CopyProductions:
        if CFG.isRuleUnreachable(productions, variables, rule):
            productions.remove(rule)

    return productions, variables, Vars

def REMOVE_MORE_THAN_2_VARIABLES_PRODUCTION(productions, variables, Vars):
    
    productions, variables, Vars = CFG.replaceTerms(productions, variables, Vars)

    CopyProductions = productions.copy()
    for rule in CopyProductions:
        if CFG.isVariablesMoreThan2(variables, rule):
            newRules, variables, Vars = CFG.replaceMoreThan2Var(variables, rule, Vars)
            productions.remove(rule)
            productions += newRules
    return productions, variables, Vars

def REMOVE_TERM_PRODUCTION(productions, variables, Vars):
    CopyProductions = productions.copy()
    for rule in productions:
        left, right = rule
        if CFG.isTermProduction(variables, rule):
            productions, variables, Vars = CFG.replaceTermProduction(productions, variables, rule, Vars)
    return productions, variables, Vars