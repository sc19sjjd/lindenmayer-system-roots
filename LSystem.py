import numpy as np

# get the parameter arguments from a string of the form:
# V(p1, p2, p3, ..., pn), where V is the variable character and p1-pn are the parameters
def getArgs(v: str) -> list:
    args = v[2:-1]
    args = args.split(',')
    return args

# parse a set of parameter arguments using pythons eval function
# evaluate the contents of each parameter argument using the globals dictionary 
def parseArgs(args: list, globals: dict) -> list:
    p_args = []
    for arg in args:
        new_arg = eval(arg, globals)
        p_args.append(new_arg)

    return p_args

# parse a paramaterised variable into the following structure:
# ['variable character', 'parameter 1', 'parameter 2', ..., 'paramater n']
def parseVariable(v: str, globals: dict={}) -> list:
    var = []
    args = getArgs(v)
    if globals != {}:
        args = parseArgs(args, globals)
    var.append(v[0])
    for a in args:
        var.append(a)

    return var

# parse a string sentence into a list where each list element is either:
# a parsed variable, ['variable character', 'parameter 1', 'parameter 2', ...]
# or a non variable character, ['character']
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

# parse the supplied rules dictionary into the following structure:
# { 'variable character': ( [variable parameters], [([rule likelihood, [parsed sentence]), (more rule 2-tuples) ] ) }
def parseRules(rules: dict, variables: list) -> dict:
    p_rules = {}
    keys = list(rules.keys())
    for key in keys:
        var = parseVariable(key)

        multi_rules = []
        for rule in rules[key]:
            prob = rule[0]
            rhs = parseSentence(rule[1], variables)
            multi_rules.append((
                prob,
                rhs
            ))
        
        p_rules[var[0]] = (var[1:], multi_rules)

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


# Parameterised L-System Class
# ----------- Constructor Arguments --------------#
#   variables: a list of variables and placeholder parameters **Do not use any spaces in the variables
#   constants: a dictionary of variables that can be applied in any of the rule parameters
#   axiom: the starting sentence in string form **No spaces
#   rule: a dictionary of rules with each key value pair in the following form:
#       'V': [(p1, "S1"), (p2, "S2"), ..., (pn, "Sn")]
#       Where V is a variable with parameters placeholders, p is a probability weight and S the string to replace V with
#       The probability weights can be any number > 0 and rule selection is performed via roulette wheel
#   iterations: integer value above 0, the amount of iterations of the L-System to be performed
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

    # select a random matching rule with roulette wheel like selection
    def selectRule(self, var):
        if not var in self.parsed_rules.keys():
            return None, None
        
        var_rules = self.parsed_rules[var]
        parameters = var_rules[0]
        total = 0.0

        for rule in var_rules[1]:
            total += rule[0]

        rand = np.random.uniform(0.0, total)
        curr = 0.0
        for rule in var_rules[1]:
            if rand < curr + rule[0]:
                return rule, parameters
            else:
                curr += rule[0]

        return None, None
    
    def applyRule(self, rule: str, globals: dict) -> list:
        res = []
        for substr in rule[1]:
            if len(substr) >  1:
                new_var = [substr[0]]

                for param in substr[1:]:
                    new_var.append(str(eval(param, globals)))

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
                    rule, params = self.selectRule(substr[0])

                    if rule is None:
                        p_next.append(substr)
                        continue
                    
                    # match the rule's parameter keys with values
                    globals = {}
                    j = 1
                    for param in params:
                        globals[param] = float(substr[j])
                        j += 1

                    # join the rule parameters with the constants for parameter evaluation
                    globals = globals | self.constants
                    p_next.extend(self.applyRule(rule, globals))

                else:
                    p_next.append(substr)

            self.parsed_system.append(p_next)
            self.system.append(parsedSentenceToString(p_next))


# simple LSystem class from Lindenmayer Systems python module
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