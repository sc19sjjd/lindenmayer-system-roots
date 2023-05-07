import re

def findBetween(s, l, r) -> str:
    result = re.search(f'{l}.*{r}', s)
    return result

def getArgs(v: str) -> list:
    args = v[2:-1]
    args = args.split(',')
    return args

def parseArgs(args: list, globals: dict) -> list:
    p_args = []
    for arg in args:
        new_arg = eval(arg, globals)
        p_args.append(new_arg)

    return p_args

def parseVariable(v: str, globals: dict={}) -> list:
    var = []
    args = getArgs(v)
    if globals != {}:
        args = parseArgs(args, globals)
    var.append(v[0])
    for a in args:
        var.append(a)

    return var

def parseSentence(s: str, variables: list, globals: dict={}) -> list:
    sentence = []
    i = 0
    while i < len(s):
        if s[i] in variables:            
            var_end = s.find(')', i)
            var = parseVariable(s[i:var_end+1], globals)
            sentence.append(var)

            i = var_end

        else: 
            sentence.append([s[i]])

        i += 1

    return sentence

def parseRules(rules: dict, variables: list) -> dict:
    p_rules = {}
    keys = list(rules.keys())
    for key in keys:
        var = parseVariable(key)
        rhs = parseSentence(rules[key], variables)
        p_rules[var.pop(0)] = [
            var,
            rhs
        ]
        
    return p_rules

def parsedVarToString(var: list) -> str:
    s = var[0] + '('
    for i in range(1,len(var)):
        s += var[i] + ','
    s = s[:-1] + ')'

    return s

def parsedSentenceToString(ps: str) -> str:
    s = ""
    for e in ps:
        if len(e) <= 1:
            s += e[0]
        else:
            s += parsedVarToString(e)

    return s


class ParamLSystem():
    def __init__(self, variables, constants, axiom, rules, iterations=0):
        
        self.parsed_variables = []
        self.variables = []
        for v in variables:
            p_var  = parseVariable(v)
            self.parsed_variables.append(p_var)
            self.variables.append(p_var[0])

        self.parsed_axiom = parseSentence(axiom, self.variables)
        self.parsed_rules = parseRules(rules, self.variables)
        self.parsed_system = [self.parsed_axiom]
        
        self.constants = constants
        self.axiom = axiom
        self.rules = rules
        self.system = [self.axiom]
        
        for i in range(iterations):
            self.iterate()

    def __repr__(self):
        return str(self.system)
    
    def __applyRule(self, rule: str, globals: dict) -> list:
        res = []
        #print(f"globals: {globals}")
        for substr in rule[1]:
            if len(substr) >  1:
                #print(f"substr: {substr}")
                new_var = [substr[0]]
                for param in substr[1:]:
                    #print(f"param: {param}")
                    new_var.append(str(eval(param, globals)))
                    #print(f"new_var:  {new_var}")

                res.append(new_var)
            else:
                res.append(substr)

        return res

    def iterate(self, iterations: int=1):
        for i in range(iterations):
            p_current = self.parsed_system[-1]

            p_next = []
            for substr in p_current:
                if len(substr) > 1:
                    if not substr[0] in self.parsed_rules.keys():
                        p_next.append(substr)
                        continue

                    rule = self.parsed_rules[substr[0]]
                    globals = {}
                    i = 1
                    for gvar in rule[0]:
                        globals[gvar] = float(substr[i])
                        i += 1

                    globals = globals | self.constants
                    p_next.extend(self.__applyRule(rule, globals))

                else:
                    p_next.append(substr)

            #print(f"p_next: {p_next}")
            self.parsed_system.append(p_next)
            self.system.append(parsedSentenceToString(p_next))


class LSystem:
    def __init__(self, variables, constants, axiom, rules, iterations=0):
        self.variables = variables
        self.constants = constants
        self.axiom = axiom
        self.rules = rules
        self.system = [self.axiom]
        for i in range(iterations):
            self.iterate()

    def __repr__(self):
        return str(self.system)

    def iterate(self, iterations=1):
        for i in range(iterations):
            nxt = self.system[-1]
            rep={} # replacements
            count=1
            for var in self.rules.keys():
                repstr = str(chr(count))
                nxt=repstr.join( nxt.split(var) )
                rep[repstr] = var
                count=count+1
            for var in rep.keys():
                nxt = self.rules[rep[var]].join(nxt.split(var))

            self.system.append(nxt)