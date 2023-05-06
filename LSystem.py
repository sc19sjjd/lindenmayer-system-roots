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
            count=1;
            for var in self.rules.keys():
                repstr = str(chr(count))
                nxt=repstr.join( nxt.split(var) )
                rep[repstr] = var
                count=count+1
            for var in rep.keys():
                nxt = self.rules[rep[var]].join(nxt.split(var))

            self.system.append(nxt)

